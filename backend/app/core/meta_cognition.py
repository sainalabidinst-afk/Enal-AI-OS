import logging
from dataclasses import dataclass
from typing import Any
from backend.app.core.cognitive_budget import cognitive_budget, TaskComplexity
from backend.app.core.adaptive_runtime import PIPELINE_PRESETS
from backend.app.core.cost_optimizer import cost_optimizer

logger = logging.getLogger(__name__)


@dataclass
class CognitionTrace:
    task_description: str
    pipeline_used: list[str]
    model_used: str
    complexity: TaskComplexity
    success: bool
    quality_score: float
    latency_ms: float
    cost: float
    reasoning: str = ""


class MetaCognition:
    def __init__(self):
        self._traces: list[CognitionTrace] = []

    async def evaluate_and_optimize(self, task_description: str, result: dict[str, Any]) -> dict[str, Any]:
        trace = CognitionTrace(
            task_description=task_description,
            pipeline_used=result.get("pipeline", []),
            model_used=result.get("model", ""),
            complexity=TaskComplexity(result.get("complexity", TaskComplexity.MEDIUM.value)),
            success=result.get("verification", {}).get("passed", False),
            quality_score=result.get("reflection", {}).get("score", 0.0),
            latency_ms=result.get("latency_ms", 0.0),
            cost=result.get("cost", 0.0),
        )
        self._traces.append(trace)
        optimization = await self._optimize_pipeline(trace)
        return {
            "trace_id": len(self._traces),
            "current_pipeline": trace.pipeline_used,
            "optimization": optimization,
            "recommendation": optimization.get("recommendation", ""),
        }

    async def _optimize_pipeline(self, trace: CognitionTrace) -> dict[str, Any]:
        similar_traces = [t for t in self._traces if t.task_description == trace.task_description and t is not trace]
        if not similar_traces:
            return {"recommendation": "Continue current pipeline", "changes": []}
        avg_quality = sum(t.quality_score for t in similar_traces) / len(similar_traces)
        avg_cost = sum(t.cost for t in similar_traces) / len(similar_traces)
        if trace.quality_score < avg_quality - 1.0:
            return {"recommendation": "Add reasoning and verification steps", "changes": ["add_verification", "add_reasoning"]}
        if trace.cost > avg_cost * 1.5:
            return {"recommendation": "Simplify pipeline, use cheaper model", "changes": ["simplify_pipeline", "reduce_model"]}
        return {"recommendation": "Pipeline is optimal", "changes": []}

    async def choose_pipeline(self, task_description: str) -> dict[str, Any]:
        budget = cognitive_budget.estimate(task_description)
        preset = PIPELINE_PRESETS.get(budget.complexity, PIPELINE_PRESETS[TaskComplexity.MEDIUM])
        similar = [t for t in self._traces if t.task_description == task_description]
        if similar:
            best = max(similar, key=lambda t: t.quality_score)
            if best.quality_score >= 7.0:
                return {"pipeline": best.pipeline_used, "model": best.model_used, "reason": "Historical best"}
        model = cost_optimizer.select_model(task_description, budget.complexity.value)
        return {"pipeline": preset, "model": model, "complexity": budget.complexity.value, "reason": "Adaptive selection"}

    def get_metrics(self) -> dict[str, Any]:
        if not self._traces:
            return {"total_tasks": 0}
        return {
            "total_tasks": len(self._traces),
            "avg_quality": sum(t.quality_score for t in self._traces) / len(self._traces),
            "avg_cost": sum(t.cost for t in self._traces) / len(self._traces),
            "avg_latency_ms": sum(t.latency_ms for t in self._traces) / len(self._traces),
            "success_rate": sum(1 for t in self._traces if t.success) / len(self._traces),
        }


meta_cognition = MetaCognition()
