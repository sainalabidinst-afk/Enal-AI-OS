import json
import logging
import uuid
from dataclasses import dataclass, field
from typing import Any

from backend.app.core.evaluation import evaluation_framework
from backend.app.core.experience import experience_learning
from backend.app.core.model_router import model_router

logger = logging.getLogger(__name__)


@dataclass
class HumanFeedback:
    rating: float  # 0.0 - 5.0
    feedback_text: str
    source: str  # human or system
    timestamp: str = field(default_factory=lambda: str(uuid.uuid4().time))


@dataclass
class RLAction:
    action_id: str
    context: dict[str, Any]
    reward: float
    next_context: dict[str, Any] | None = None


@dataclass
class LearningCycle:
    id: str
    benchmark_id: str
    failures: list[dict[str, Any]]
    improvements: list[str]
    applied: bool = False
    human_feedback: list[HumanFeedback] = field(default_factory=list)
    rl_actions: list[RLAction] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class ContinuousLearning:
    def __init__(self):
        self._cycles: dict[str, LearningCycle] = {}
        self._feedback_queue: list[HumanFeedback] = []

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
        response = await model_router.acomplete([{"role": "user", "content": prompt}], temperature=0.5, max_tokens=512)
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

    def record_human_feedback(self, cycle_id: str, rating: float, feedback_text: str, source: str = "human") -> None:
        feedback = HumanFeedback(rating=rating, feedback_text=feedback_text, source=source)
        cycle = self._cycles.get(cycle_id)
        if cycle:
            cycle.human_feedback.append(feedback)
        else:
            self._feedback_queue.append(feedback)
        logger.info(f"Human feedback recorded for cycle {cycle_id}: rating={rating}")

    def record_rl_action(self, cycle_id: str, action: RLAction) -> None:
        cycle = self._cycles.get(cycle_id)
        if cycle:
            cycle.rl_actions.append(action)
        logger.debug(f"RL action recorded for cycle {cycle_id}")

    def compute_policy_gradient(self, cycle_id: str) -> dict[str, float]:
        cycle = self._cycles.get(cycle_id)
        if not cycle or not cycle.rl_actions:
            return {}
        rewards = [a.reward for a in cycle.rl_actions]
        return {
            "avg_reward": sum(rewards) / len(rewards),
            "total_reward": sum(rewards),
            "action_count": len(cycle.rl_actions),
        }


continuous_learning = ContinuousLearning()
