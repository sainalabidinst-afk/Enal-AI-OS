import logging
import os
from typing import Any

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

logger = logging.getLogger(__name__)

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
)


class GPUInferenceService:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self._tokenizer = None
        self._model = None

    async def initialize(self):
        if self._model is not None:
            return
        logger.info("Loading GPU model from %s", self.model_path)
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            torch_dtype=torch.float16,
            device_map="auto",
            quantization_config=quantization_config,
        )
        logger.info("GPU model loaded successfully")

    def _format_messages(self, messages: list[dict]) -> str:
        parts = []
        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            parts.append(f"{role}\n{content}")
        return "\n".join(parts)

    def _generate(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
        if self._model is None or self._tokenizer is None:
            raise RuntimeError("GPU model not initialized")

        inputs = self._tokenizer(prompt, return_tensors="pt").to("cuda")
        with torch.no_grad():
            outputs = self._model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
            )
        return self._tokenizer.decode(outputs[0], skip_special_tokens=True)

    async def chat(self, messages: list[dict], max_tokens: int = 256, temperature: float = 0.7) -> str:
        prompt = self._format_messages(messages)
        return self._generate(prompt, max_tokens=max_tokens, temperature=temperature)


def get_gpu_service() -> GPUInferenceService | None:
    model_path = os.environ.get("GPU_MODEL_PATH", "E:/Enal-AI-OS/models/qwen2.5-3b")
    if not os.path.exists(model_path):
        return None
    return GPUInferenceService(model_path=model_path)
