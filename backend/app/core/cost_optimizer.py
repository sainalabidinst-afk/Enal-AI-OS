import logging
from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class ModelPricing:
    MODELS = {
        "gpt-4o": {"input": 2.5, "output": 10.0, "reasoning": False},
        "gpt-4o-mini": {"input": 0.15, "output": 0.6, "reasoning": False},
        "claude-3-5-sonnet-20240620": {"input": 3.0, "output": 15.0, "reasoning": True},
        "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25, "reasoning": False},
        "gemini-1.5-pro": {"input": 1.25, "output": 5.0, "reasoning": True},
        "gemini-1.5-flash": {"input": 0.075, "output": 0.3, "reasoning": False},
        "ollama/llama3": {"input": 0.0, "output": 0.0, "reasoning": False},
    }

    @classmethod
    def estimate_cost(cls, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        pricing = cls.MODELS.get(model, {"input": 1.0, "output": 1.0})
        return (pricing["input"] * prompt_tokens + pricing["output"] * completion_tokens) / 1_000_000


class CostOptimizer:
    def __init__(self):
        self.pricing = ModelPricing()

    def select_model(self, task_type: str, complexity: str = "medium") -> str:
        task_lower = task_type.lower()
        if any(k in task_lower for k in ["translate", "summarize", "simple"]):
            return "gpt-4o-mini"
        if any(k in task_lower for k in ["code", "debug", "programming"]):
            return "claude-3-5-sonnet-20240620"
        if any(k in task_lower for k in ["reason", "analyze", "plan"]):
            return "claude-3-5-sonnet-20240620"
        if any(k in task_lower for k in ["chat", "simple", "fast"]):
            return "gpt-4o-mini"
        if complexity == "low":
            return "gpt-4o-mini"
        return settings.DEFAULT_MODEL

    def optimize_prompt(self, prompt: str) -> str:
        if len(prompt) > 4000:
            return prompt[:4000] + "... [truncated for cost optimization]"
        return prompt


cost_optimizer = CostOptimizer()
