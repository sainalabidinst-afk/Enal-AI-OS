import logging
from typing import Any
from backend.app.core.cognitive_budget import cognitive_budget, TaskComplexity
from backend.app.core.cognitive_kernel import cognitive_kernel
from backend.app.core.model_router import model_router
from backend.app.core.cost_optimizer import cost_optimizer

logger = logging.getLogger(__name__)


PIPELINE_PRESETS = {
    TaskComplexity.TRIVIAL: ["perception", "memory", "decision", "action"],
    TaskComplexity.SIMPLE: ["perception", "memory", "reasoning", "decision", "action"],
    TaskComplexity.MEDIUM: ["perception", "memory", "planning", "reasoning", "decision", "reflection", "action"],
    TaskComplexity.COMPLEX: ["perception", "memory", "planning", "reasoning", "debate", "simulation", "decision", "verification", "reflection", "learning"],
    TaskComplexity.VERY_COMPLEX: ["perception", "memory", "planning", "reasoning", "debate", "simulation", "decision", "verification", "reflection", "learning"],
}

PIPELINE_DESCRIPTIONS = {
    TaskComplexity.TRIVIAL: "Quick perception → memory lookup → decision → action",
    TaskComplexity.SIMPLE: "Perception → memory → reasoning → decision → action",
    TaskComplexity.MEDIUM: "Perception → memory → planning → reasoning → decision → reflection → action",
    TaskComplexity.COMPLEX: "Full cognitive pipeline with debate, simulation, verification, and learning",
    TaskComplexity.VERY_COMPLEX: "Full cognitive pipeline with debate, simulation, verification, and learning",
}


class AdaptiveCognitiveRuntime:
    def __init__(self):
        self.kernel = cognitive_kernel
        self.budget = cognitive_budget
        self.model_router = model_router
        self.cost_optimizer = cost_optimizer

    async def execute(self, user_input: str, project_id: str | None = None, force_pipeline: list[str] | None = None) -> dict[str, Any]:
        budget = self.budget.estimate(user_input)
        context = {"input": user_input, "project_id": project_id, "budget": budget}
        if force_pipeline:
            pipeline = force_pipeline
        else:
            pipeline = PIPELINE_PRESETS.get(budget.complexity, PIPELINE_PRESETS[TaskComplexity.MEDIUM])
        model = budget.model
        context["selected_model"] = model
        result = await self.kernel.execute_pipeline(pipeline, context)
        result["pipeline"] = pipeline
        result["complexity"] = budget.complexity.value
        result["model"] = model
        result["budget"] = {
            "complexity": budget.complexity.value,
            "max_tokens": budget.max_tokens,
            "estimated_duration_seconds": budget.estimated_duration_seconds,
            "require_reflection": budget.require_reflection,
        }
        return result

    def get_pipeline_for_complexity(self, complexity: TaskComplexity) -> list[str]:
        return PIPELINE_PRESETS.get(complexity, PIPELINE_PRESETS[TaskComplexity.MEDIUM])

    def describe_pipeline(self, complexity: TaskComplexity) -> str:
        return PIPELINE_DESCRIPTIONS.get(complexity, "Standard cognitive pipeline")


adaptive_runtime = AdaptiveCognitiveRuntime()
