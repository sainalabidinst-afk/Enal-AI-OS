import logging
from dataclasses import dataclass, field
from typing import Any
from enum import Enum

logger = logging.getLogger(__name__)


class TaskComplexity(str, Enum):
    TRIVIAL = "trivial"
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


@dataclass
class CognitiveBudget:
    task_description: str
    complexity: TaskComplexity = TaskComplexity.MEDIUM
    max_tokens: int = 4096
    temperature: float = 0.7
    model: str = "gpt-4o"
    require_reflection: bool = False
    require_review: bool = False
    max_iterations: int = 1
    estimated_cost: float = 0.0
    estimated_duration_seconds: int = 60
    metadata: dict[str, Any] = field(default_factory=dict)


class CognitiveBudgetManager:
    def __init__(self):
        self.complexity_model_map = {
            TaskComplexity.TRIVIAL: "gpt-4o-mini",
            TaskComplexity.SIMPLE: "gpt-4o-mini",
            TaskComplexity.MEDIUM: "gpt-4o",
            TaskComplexity.COMPLEX: "claude-3-5-sonnet-20240620",
            TaskComplexity.VERY_COMPLEX: "claude-3-5-sonnet-20240620",
        }
        self.token_budget_map = {
            TaskComplexity.TRIVIAL: 1024,
            TaskComplexity.SIMPLE: 2048,
            TaskComplexity.MEDIUM: 4096,
            TaskComplexity.COMPLEX: 8192,
            TaskComplexity.VERY_COMPLEX: 16384,
        }
        self.reflection_required_map = {
            TaskComplexity.TRIVIAL: False,
            TaskComplexity.SIMPLE: False,
            TaskComplexity.MEDIUM: True,
            TaskComplexity.COMPLEX: True,
            TaskComplexity.VERY_COMPLEX: True,
        }

    def estimate(self, task_description: str) -> CognitiveBudget:
        complexity = self._estimate_complexity(task_description)
        model = self.complexity_model_map.get(complexity, "gpt-4o")
        max_tokens = self.token_budget_map.get(complexity, 4096)
        require_reflection = self.reflection_required_map.get(complexity, False)
        duration_map = {
            TaskComplexity.TRIVIAL: 5,
            TaskComplexity.SIMPLE: 15,
            TaskComplexity.MEDIUM: 60,
            TaskComplexity.COMPLEX: 300,
            TaskComplexity.VERY_COMPLEX: 900,
        }
        return CognitiveBudget(
            task_description=task_description,
            complexity=complexity,
            model=model,
            max_tokens=max_tokens,
            temperature=0.3 if complexity in [TaskComplexity.COMPLEX, TaskComplexity.VERY_COMPLEX] else 0.7,
            require_reflection=require_reflection,
            require_review=complexity in [TaskComplexity.COMPLEX, TaskComplexity.VERY_COMPLEX],
            max_iterations=3 if complexity == TaskComplexity.VERY_COMPLEX else (2 if complexity == TaskComplexity.COMPLEX else 1),
            estimated_duration_seconds=duration_map.get(complexity, 60),
        )

    def _estimate_complexity(self, task_description: str) -> TaskComplexity:
        lower = task_description.lower()
        complex_keywords = ["build", "create", "design", "implement", "architecture", "system", "platform", "enterprise"]
        medium_keywords = ["analyze", "write", "generate", "configure", "setup"]
        simple_keywords = ["fix", "update", "rename", "delete", "list"]
        if any(k in lower for k in complex_keywords):
            return TaskComplexity.VERY_COMPLEX if len(task_description) > 500 else TaskComplexity.COMPLEX
        if any(k in lower for k in medium_keywords):
            return TaskComplexity.MEDIUM
        if any(k in lower for k in simple_keywords):
            return TaskComplexity.SIMPLE
        return TaskComplexity.TRIVIAL


cognitive_budget = CognitiveBudgetManager()
