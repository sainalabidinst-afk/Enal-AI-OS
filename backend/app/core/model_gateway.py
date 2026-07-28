import asyncio
from typing import Any


class ModelGateway:
    def __init__(self) -> None:
        self._providers: dict[str, dict[str, Any]] = {
            "openai": {"models": ["gpt-4o", "gpt-4o-mini"], "available": True},
            "anthropic": {"models": ["claude-opus-4", "claude-sonnet-4"], "available": True},
            "gemini": {"models": ["gemini-2.5-pro", "gemini-2.5-flash"], "available": True},
            "qwen": {"models": ["qwen-2.5-72b", "qwen-2.5-coder"], "available": True},
            "deepseek": {"models": ["deepseek-r1", "deepseek-v3"], "available": True},
            "llama": {"models": ["llama-3.1-70b", "llama-3.1-8b"], "available": True},
            "ollama": {"models": ["local-*"], "available": True},
        }
        self._health: dict[str, dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    async def health_check(self, provider: str) -> dict[str, Any]:
        async with self._lock:
            if provider not in self._providers:
                return {"provider": provider, "status": "unknown", "latency_ms": None}
            p = self._providers[provider]
            health = {
                "provider": provider,
                "status": "healthy" if p.get("available", False) else "unhealthy",
                "models": p.get("models", []),
                "latency_ms": None,
            }
            self._health[provider] = health
            return health

    async def route(self, task_type: str, capability: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        routing = {
            "coding": "qwen",
            "reasoning": "deepseek",
            "research": "gemini",
            "network": "anthropic",
            "trading": "deepseek",
            "default": "openai",
        }
        provider = routing.get(capability, routing["default"])
        model = self._providers.get(provider, {}).get("models", [None])[0]
        return {"provider": provider, "model": model, "task_type": task_type, "capability": capability}

    async def get_status(self) -> dict[str, Any]:
        return {"providers": self._providers, "health": self._health}


model_gateway = ModelGateway()
