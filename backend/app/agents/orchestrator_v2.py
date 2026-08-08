import logging
from typing import Any

from backend.app.core.perception_engine import PerceptionInput

logger = logging.getLogger(__name__)


class AIOrchestrator:
    def __init__(self):
        self._orchestrator = "ai-orchestrator"
        self._active_sessions: dict[str, dict[str, Any]] = {}

    async def orchestrate_goal(
        self,
        goal: str,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Full orchestration: goal → plan → execute with memory."""
        from apps.organization.ai_planner import ai_planner

        from backend.app.core.perception_engine import perception_engine

        context = context or {}

        perception_input = PerceptionInput(
            source="user",
            content=goal,
            content_type="text/plain",
            metadata=context,
        )
        perception_result = await perception_engine.process(perception_input)
        plan = ai_planner.plan_from_goal(goal, context)

        capabilities_needed = [
            s.capability_id for s in plan.steps if s.step_type.value == "capability"
        ]

        session_id = f"orch-{hash(goal) % 10000}"
        self._active_sessions[session_id] = {"goal": goal, "plan_id": plan.plan_id}

        return {
            "session_id": session_id,
            "plan_id": plan.plan_id,
            "goal": goal,
            "perception": {
                "entities": perception_result.entities,
                "intents": perception_result.intents,
            },
            "capabilities_needed": capabilities_needed,
            "steps": len(plan.steps),
            "cost_estimate": plan.metadata.get("cost_estimate"),
            "risk_assessment": plan.metadata.get("risk_assessment"),
        }


ai_orchestrator = AIOrchestrator()
