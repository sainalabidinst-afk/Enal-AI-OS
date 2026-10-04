"""
GPU Inference Service — optional local LLM provider for the Model Router.

Design constraints (Architecture Freeze Policy + repo conventions):

- **No import-time heavy dependencies.** ``torch`` and ``transformers`` are
  imported inside :meth:`GPUInferenceService.initialize`. Importing them at
  module scope would add ~25s to every ``backend.app.runtime`` import because
  the Model Router imports this module eagerly. This mirrors the lazy-import
  convention already used by ``kafka_event_bus`` and ``storage``.
- **No hardcoded paths.** Model location comes from ``settings.GPU_MODEL_PATH``
  so the same build runs on developer machines and containers.
- **Never fatal.** If CUDA, bitsandbytes, the weights, or the packages are
  missing, the service reports itself unavailable and the Model Router falls
  back to ``settings.FALLBACK_MODEL`` instead of breaking the platform.

Selected with the ``gpu/`` model prefix, e.g. ``gpu/qwen2.5-3b``.
"""

from __future__ import annotations

import asyncio
import logging
import os
from threading import Lock
from typing import Any

from backend.app.core.config import settings

logger = logging.getLogger(__name__)

__all__ = [
    "GPUInferenceError",
    "GPUUnavailableError",
    "GPUInferenceService",
    "get_gpu_service",
    "reset_gpu_service",
]


class GPUInferenceError(RuntimeError):
    """Raised when GPU inference fails after the service was initialized."""


class GPUUnavailableError(GPUInferenceError):
    """Raised when no usable GPU runtime, weights, or dependency set exists."""


class GPUInferenceService:
    """Local Hugging Face causal-LM inference with 4-bit quantization."""

    def __init__(
        self,
        model_path: str | None = None,
        load_in_4bit: bool = True,
        max_context_tokens: int = 8192,
        max_new_tokens_reserve: int = 512,
    ) -> None:
        self.model_path = model_path or settings.GPU_MODEL_PATH
        self.load_in_4bit = load_in_4bit
        self.max_context_tokens = max_context_tokens
        self.max_new_tokens_reserve = max_new_tokens_reserve
        self._tokenizer: Any = None
        self._model: Any = None
        self._device: str = "cpu"
        self._init_lock = Lock()
        self._initialized = False

    @property
    def initialized(self) -> bool:
        """Whether weights are loaded and inference can run."""
        return self._initialized

    @property
    def device(self) -> str:
        """Resolved torch device string (``cuda``/``cuda:0``/``cpu``)."""
        return self._device

    def status(self) -> dict[str, Any]:
        """Health snapshot for the console observability panel."""
        return {
            "enabled": settings.GPU_INFERENCE_ENABLED,
            "model_path": self.model_path,
            "model_exists": os.path.isdir(self.model_path),
            "initialized": self._initialized,
            "device": self._device,
            "quantized": self.load_in_4bit,
            "max_context_tokens": self.max_context_tokens,
            "fallback_model": settings.FALLBACK_MODEL if settings.GPU_FALLBACK_ENABLED else None,
        }

    def initialize(self) -> None:
        """Load tokenizer and weights. Idempotent and thread-safe."""
        if self._initialized:
            return
        with self._init_lock:
            if self._initialized:
                return
            if not os.path.isdir(self.model_path):
                raise GPUUnavailableError(f"GPU model directory not found: {self.model_path}")

            torch = self._import_torch()
            auto_model, auto_tokenizer, bnb_config = self._import_transformers()

            self._device = self._resolve_device(torch)

            tokenizer = auto_tokenizer.from_pretrained(self.model_path)
            if tokenizer.pad_token_id is None and tokenizer.eos_token_id is not None:
                tokenizer.pad_token = tokenizer.eos_token

            quantization_config = None
            if self.load_in_4bit:
                quantization_config = self._build_quantization_config(torch, bnb_config)

            logger.info("Loading GPU model from %s on %s", self.model_path, self._device)
            model = self._load_model(
                auto_model,
                torch,
                quantization_config,
            )

            self._tokenizer = tokenizer
            self._model = model
            self._initialized = True
            logger.info("GPU model loaded successfully on %s", self._device)

    def _load_model(
        self,
        auto_model: Any,
        torch: Any,
        quantization_config: Any,
    ) -> Any:
        """Load weights, retrying unquantized when 4-bit kernels are unusable.

        bitsandbytes builds fail lazily at load time rather than at config
        construction, so the retry has to wrap ``from_pretrained`` itself.
        """
        dtype = torch.float16 if self._device != "cpu" else torch.float32
        try:
            model = auto_model.from_pretrained(
                self.model_path,
                torch_dtype=dtype,
                device_map="auto",
                quantization_config=quantization_config,
            )
        except Exception as exc:
            if quantization_config is None:
                raise
            logger.warning(
                "4-bit load failed (%s); retrying %s without quantization",
                exc,
                self.model_path,
            )
            self.load_in_4bit = False
            model = auto_model.from_pretrained(
                self.model_path,
                torch_dtype=dtype,
                device_map="auto",
            )

        model.eval()
        return model

    @staticmethod
    def _import_torch() -> Any:
        try:
            import torch
        except ImportError as exc:
            raise GPUUnavailableError("torch is not installed") from exc
        return torch

    @staticmethod
    def _import_transformers() -> tuple[Any, Any, Any]:
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise GPUUnavailableError("transformers is not installed") from exc

        bnb_config: Any = None
        try:
            from transformers import BitsAndBytesConfig

            bnb_config = BitsAndBytesConfig
        except ImportError:
            logger.info("BitsAndBytesConfig unavailable; loading weights unquantized")

        return AutoModelForCausalLM, AutoTokenizer, bnb_config

    def _resolve_device(self, torch: Any) -> str:
        if not torch.cuda.is_available():
            logger.warning("CUDA unavailable; GPU inference will run on CPU")
            return "cpu"
        return f"cuda:{torch.cuda.current_device()}"

    def _build_quantization_config(self, torch: Any, bnb_config: Any) -> Any:
        if self._device == "cpu" or bnb_config is None:
            return None
        try:
            return bnb_config(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
        except Exception as exc:  # pragma: no cover - depends on local bnb build
            logger.warning("4-bit quantization unavailable (%s); loading full precision", exc)
            return None

    def _format_messages(self, messages: list[dict]) -> str:
        """Render chat messages with the tokenizer's own chat template.

        Falls back to a plain role-prefixed transcript when the tokenizer has no
        template, which keeps non-chat-tuned base models usable.
        """
        if self._tokenizer is None:
            raise GPUInferenceError("GPU model not initialized")
        template = getattr(self._tokenizer, "chat_template", None)
        if template:
            return self._tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
        parts = [
            f"{message.get('role', 'user')}\n{message.get('content', '')}"
            for message in messages
        ]
        parts.append("assistant")
        return "\n".join(parts)

    def _truncate_to_context(self, prompt: str) -> str:
        """Drop oldest turns until the prompt fits the context window."""
        if self._tokenizer is None:
            return prompt
        tokens = self._tokenizer(prompt, add_special_tokens=False)["input_ids"]
        limit = self.max_context_tokens - self.max_new_tokens_reserve
        if len(tokens) <= limit:
            return prompt
        return self._tokenizer.decode(tokens[-limit:], skip_special_tokens=True)

    def _generate(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
        """Blocking generation. Callers inside a loop must use :meth:`agenerate`."""
        if self._model is None or self._tokenizer is None:
            raise GPUInferenceError("GPU model not initialized")

        torch = self._import_torch()
        prompt = self._truncate_to_context(prompt)
        inputs = self._tokenizer(prompt, return_tensors="pt").to(self._model.device)
        input_length = inputs["input_ids"].shape[-1]

        generate_kwargs: dict[str, Any] = {
            "max_new_tokens": max_tokens,
            "pad_token_id": self._tokenizer.pad_token_id,
        }
        if temperature > 0:
            generate_kwargs.update({"do_sample": True, "temperature": temperature})
        else:
            generate_kwargs["do_sample"] = False

        with torch.no_grad():
            outputs = self._model.generate(**inputs, **generate_kwargs)

        # Decode only the newly generated tokens, not the echoed prompt.
        return self._tokenizer.decode(
            outputs[0][input_length:],
            skip_special_tokens=True,
        ).strip()

    def generate(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
        """Synchronous generation entrypoint."""
        self.initialize()
        return self._generate(prompt, max_tokens=max_tokens, temperature=temperature)

    async def agenerate(
        self,
        prompt: str,
        max_tokens: int = 256,
        temperature: float = 0.7,
    ) -> str:
        """Async generation that keeps the event loop free during decoding."""
        return await asyncio.to_thread(self.generate, prompt, max_tokens, temperature)

    async def chat(
        self,
        messages: list[dict],
        max_tokens: int = 256,
        temperature: float = 0.7,
    ) -> str:
        """Async chat completion; offloads decoding to a worker thread."""
        await asyncio.to_thread(self.initialize)
        prompt = await asyncio.to_thread(self._format_messages, messages)
        return await self.agenerate(prompt, max_tokens=max_tokens, temperature=temperature)

    async def aclose(self) -> None:
        """Release GPU memory held by the loaded model."""
        if self._model is None:
            return
        with self._init_lock:
            self._model = None
            self._tokenizer = None
            self._initialized = False
        try:
            torch = self._import_torch()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except GPUUnavailableError:
            pass


_service: GPUInferenceService | None = None
_service_lock = Lock()


def get_gpu_service() -> GPUInferenceService | None:
    """Return the process-wide GPU service, or ``None`` when GPU mode is off.

    Returning ``None`` (rather than raising) keeps the Model Router's import of
    this module free of side effects and lets it degrade to the fallback model.
    """
    global _service
    if not settings.GPU_INFERENCE_ENABLED:
        return None
    if _service is not None:
        return _service
    with _service_lock:
        if _service is None:
            _service = GPUInferenceService(model_path=settings.GPU_MODEL_PATH)
        return _service


def reset_gpu_service() -> None:
    """Drop the cached singleton. Intended for tests and model hot-swap."""
    global _service
    with _service_lock:
        _service = None
