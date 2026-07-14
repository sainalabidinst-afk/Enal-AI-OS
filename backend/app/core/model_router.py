import logging
from typing import Optional
from litellm import acompletion, completion
from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class ModelRouter:
    def __init__(self):
        self.default_model = settings.DEFAULT_MODEL
        self.reasoning_model = settings.DEFAULT_REASONING_MODEL
        self.embedding_model = settings.DEFAULT_EMBEDDING_MODEL

    def get_provider_config(self, model: str) -> dict:
        config = {"model": model}
        if model.startswith("gpt"):
            config["api_key"] = settings.OPENAI_API_KEY
        elif model.startswith("claude"):
            config["api_key"] = settings.ANTHROPIC_API_KEY
        elif model.startswith("gemini"):
            config["api_key"] = settings.GOOGLE_API_KEY
        elif model.startswith("ollama/"):
            config["api_base"] = settings.OLLAMA_BASE_URL
        return config

    def complete(
        self,
        messages: list[dict],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
        tools: Optional[list] = None,
    ):
        model = model or self.default_model
        config = self.get_provider_config(model)
        config.update({
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        })
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
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
        tools: Optional[list] = None,
    ):
        model = model or self.default_model
        config = self.get_provider_config(model)
        config.update({
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        })
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
