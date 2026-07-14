import logging
import json
import uuid
from typing import Any
from dataclasses import dataclass, field
from backend.app.core.model_router import model_router
from backend.app.core.evaluation import evaluation_framework
from backend.app.core.experience import experience_learning

logger = logging.getLogger(__name__)


@dataclass
class LearningCycle:
    id: str
    benchmark_id: str
    failures: list[dict[str, Any]]
    improvements: list[str]
    applied: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


class ContinuousLearning:
    def __init__(self):
        self._cycles: dict[str, LearningCycle] = {}

    async def run_benchmark_and_learn(self, benchmark_id: str, run_fn) -> dict[str, Any]:
        result = await evaluation_framework.run_benchmark(benchmark_id, run_fn)
        if result.passed / result.total >= 0.9:
            return {"status": "passed", "pass_rate": result.passed / result.total}
        cycle = await self._analyze_failures(benchmark_id, result)
        improvements = await self._generate_improvements(cycle)
        cycle.improvements = improvements
        return {
            "status": "needs_improvement",
            "pass_rate": result.passed / result.total,
            "failures": result.failed,
            "improvements": improvements,
            "cycle_id": cycle.id,
        }

    async def _analyze_failures(self, benchmark_id: str, result) -> LearningCycle:
        cycle_id = f"cycle-{uuid.uuid4().hex[:8]}"
        failures = [r for r in result.results if not r.get("passed", False)]
        return LearningCycle(id=cycle_id, benchmark_id=benchmark_id, failures=failures, improvements=[])

    async def _generate_improvements(self, cycle: LearningCycle) -> list[str]:
        if not cycle.failures:
            return []
        prompt = (
            "Analyze the following benchmark failures and suggest improvements to prompts, workflows, or skills.\n\n"
            "Failures:\n"
        )
        for failure in cycle.failures[:5]:
            prompt += f"- {json.dumps(failure)}\n"
        prompt += "\nOutput JSON array of improvement strings."
        response = model_router.complete([{"role": "user", "content": prompt}], temperature=0.5, max_tokens=512)
        try:
            return json.loads(response.choices[0].message.content)
        except (json.JSONDecodeError, AttributeError):
            return ["Review and improve prompt templates"]

    async def apply_improvements(self, cycle_id: str) -> bool:
        cycle = self._cycles.get(cycle_id)
        if not cycle:
            return False
        for improvement in cycle.improvements:
            await experience_learning.record(
                project_id="system",
                category="improvement",
                situation=f"Benchmark {cycle.benchmark_id} failures",
                action_taken=improvement,
                outcome="Applied",
                quality_score=0.0,
            )
        cycle.applied = True
        return True


continuous_learning = ContinuousLearning()
