import asyncio
import logging
from typing import Any

from litellm import acompletion, completion

from backend.app.core.config import settings
from backend.app.core.gpu_inference_service import (
    GPUInferenceError,
    GPUUnavailableError,
    get_gpu_service,
)

logger = logging.getLogger(__name__)


def _is_gpu_model(model: str) -> bool:
    if model.startswith("gpu/"):
        return True
    if model == "gpu":
        return True
    return False


def _format_messages(messages: list[dict]) -> str:
    parts = []
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        parts.append(f"{role}\n{content}")
    return "\n".join(parts)


def _run_async(coro):
    try:
        asyncio.get_running_loop()
        raise RuntimeError("Cannot run async GPU inference inside a running event loop")
    except RuntimeError:
        return asyncio.run(coro)


class ModelRouter:
    def __init__(self):
        self.default_model = settings.DEFAULT_MODEL
        self.reasoning_model = settings.DEFAULT_REASONING_MODEL
        self.embedding_model = settings.DEFAULT_EMBEDDING_MODEL

    def get_provider_config(self, model: str) -> dict:
        config: dict[str, Any] = {"model": model}
        if "/" in model:
            provider = model.split("/", 1)[0]
            config["model"] = model
            if provider == "openai":
                config["api_key"] = settings.OPENAI_API_KEY
            elif provider == "anthropic":
                config["api_key"] = settings.ANTHROPIC_API_KEY
            elif provider == "gemini":
                config["api_key"] = (
                    getattr(settings, "GEMINI_API_KEY", "") or settings.GOOGLE_API_KEY
                )
            elif provider == "ollama":
                config["api_base"] = settings.OLLAMA_BASE_URL
            elif provider == "gpu":
                config.pop("model", None)
            return config
        if model.startswith("gpt"):
            config["model"] = f"openai/{model}"
            config["api_key"] = settings.OPENAI_API_KEY
        elif model.startswith("claude"):
            config["model"] = f"anthropic/{model}"
            config["api_key"] = settings.ANTHROPIC_API_KEY
        elif model.startswith("gemini"):
            config["model"] = f"gemini/{model}"
            config["api_key"] = getattr(settings, "GEMINI_API_KEY", "") or settings.GOOGLE_API_KEY
        elif model.startswith("command"):
            config["model"] = model
        return config

    def _gpu_completion_sync(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> dict[str, Any]:
        service = get_gpu_service()
        if service is None:
            return self._fallback_completion_sync(
                messages, temperature=temperature, max_tokens=max_tokens
            )
        prompt = _format_messages(messages)
        try:
            text = service.generate(prompt, max_tokens=max_tokens, temperature=temperature)
        except GPUInferenceError as exc:
            if not settings.GPU_FALLBACK_ENABLED:
                raise
            logger.warning("GPU inference failed (%s); using %s", exc, settings.FALLBACK_MODEL)
            return self._fallback_completion_sync(
                messages, temperature=temperature, max_tokens=max_tokens
            )
        return {"choices": [{"message": {"content": text}}]}

    async def _gpu_completion_async(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> dict[str, Any]:
        service = get_gpu_service()
        if service is None:
            return await self._fallback_completion_async(
                messages, temperature=temperature, max_tokens=max_tokens
            )
        try:
            text = await service.chat(messages, max_tokens=max_tokens, temperature=temperature)
        except GPUInferenceError as exc:
            if not settings.GPU_FALLBACK_ENABLED:
                raise
            logger.warning("GPU inference failed (%s); using %s", exc, settings.FALLBACK_MODEL)
            return await self._fallback_completion_async(
                messages, temperature=temperature, max_tokens=max_tokens
            )
        return {"choices": [{"message": {"content": text}}]}

    def _fallback_completion_sync(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> dict[str, Any]:
        if not settings.GPU_FALLBACK_ENABLED:
            raise GPUUnavailableError(
                "GPU inference is unavailable and GPU_FALLBACK_ENABLED is disabled"
            )
        logger.warning("GPU inference unavailable; falling back to %s", settings.FALLBACK_MODEL)
        config = self.get_provider_config(settings.FALLBACK_MODEL)
        config.update(
            {
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False,
            }
        )
        return completion(**config)

    async def _fallback_completion_async(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> dict[str, Any]:
        if not settings.GPU_FALLBACK_ENABLED:
            raise GPUUnavailableError(
                "GPU inference is unavailable and GPU_FALLBACK_ENABLED is disabled"
            )
        logger.warning("GPU inference unavailable; falling back to %s", settings.FALLBACK_MODEL)
        config = self.get_provider_config(settings.FALLBACK_MODEL)
        config.update(
            {
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False,
            }
        )
        return await acompletion(**config)

    def complete(
        self,
        messages: list[dict],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
        tools: list | None = None,
    ):
        model = model or self.default_model
        if _is_gpu_model(model):
            if stream:
                raise RuntimeError("GPU provider does not support streaming in sync complete()")
            return self._gpu_completion_sync(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        config = self.get_provider_config(model)
        config.update(
            {
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": stream,
            }
        )
        if tools:
            config["tools"] = tools

        try:
            if stream:
                return completion(**config, stream=True)
            return completion(**config)
        except Exception as e:
            logger.error(f"Model completion failed for {model}: {e}")
            raise

    async def acomplete(
        self,
        messages: list[dict],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
        tools: list | None = None,
    ):
        model = model or self.default_model
        if _is_gpu_model(model):
            if stream:
                raise RuntimeError("GPU provider does not support streaming in acomplete()")
            return await self._gpu_completion_async(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        config = self.get_provider_config(model)
        config.update(
            {
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": stream,
            }
        )
        if tools:
            config["tools"] = tools

        try:
            if stream:
                return acompletion(**config, stream=True)
            return await acompletion(**config)
        except Exception as e:
            logger.error(f"Model completion failed for {model}: {e}")
            raise


model_router = ModelRouter()
