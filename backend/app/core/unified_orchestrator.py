"""
Unified Orchestrator
====================

Combines multi_agent + adaptive_runtime + organization into a single orchestrator
with dynamic team formation based on task complexity.
"""

import asyncio
import logging
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class OrchestrationMode(str, Enum):
    DIRECT = "direct"
    MULTI_AGENT = "multi_agent"
    WORKFLOW = "workflow"
    COGNITIVE = "cognitive"


@dataclass
class TeamFormation:
    team_id: str
    task: str
    agents: list[dict[str, Any]]
    strategy: str
    estimated_duration_ms: float
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class UnifiedOrchestrator:
    def __init__(self):
        self._teams: dict[str, TeamFormation] = {}

    def _get_kernel(self):
        from backend.app.core.cognitive_kernel import cognitive_kernel
        return cognitive_kernel

    def _get_runtime(self):
        from backend.app.core.adaptive_runtime import adaptive_runtime, PIPELINE_PRESETS, TaskComplexity
        return adaptive_runtime, PIPELINE_PRESETS, TaskComplexity

    def _get_planner(self):
        from apps.organization.ai_planner import ai_planner, PlanStatus
        return ai_planner, PlanStatus

    def _get_multi_agent(self):
        from apps.organization.multi_agent import multi_agent_orchestrator
        return multi_agent_orchestrator

    async def execute(
        self,
        task: str,
        project_id: str | None = None,
        mode: OrchestrationMode | str | None = None,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        context = context or {}
        mode = OrchestrationMode(mode) if isinstance(mode, str) else mode or OrchestrationMode.DIRECT

        if mode == OrchestrationMode.COGNITIVE:
            return await self._execute_cognitive(task, project_id, context)
        elif mode == OrchestrationMode.MULTI_AGENT:
            return await self._execute_multi_agent(task, project_id, context)
        elif mode == OrchestrationMode.WORKFLOW:
            return await self._execute_workflow(task, project_id, context)
        else:
            return await self._execute_direct(task, project_id, context)

    async def _execute_cognitive(self, task: str, project_id: str | None, context: dict) -> dict[str, Any]:
        kernel = self._get_kernel()
        runtime_obj, pipeline_presets, task_complexity = self._get_runtime()

        budget = runtime_obj.budget.estimate(task)
        pipeline = pipeline_presets.get(budget.complexity)
        if not pipeline:
            pipeline = pipeline_presets[task_complexity.MEDIUM]

        exec_context = {
            "input": task,
            "project_id": project_id,
            "budget": budget,
            **context,
        }
        result = await kernel.execute_pipeline(pipeline, exec_context)
        exec_context["pipeline"] = pipeline
        return exec_context

    async def _execute_direct(self, task: str, project_id: str | None, context: dict) -> dict[str, Any]:
        return await self._execute_cognitive(task, project_id, context)

    async def _execute_multi_agent(self, task: str, project_id: str | None, context: dict) -> dict[str, Any]:
        multi_agent = self._get_multi_agent()
        planner, PlanStatus = self._get_planner()

        team = await self._form_team(task, context)
        plan = planner.plan_from_goal(task, context)

        result = await multi_agent.execute_plan(plan)

        return {
            "team_id": team.team_id,
            "plan_id": plan.plan_id,
            "status": result.status.value if hasattr(result, 'status') else str(result.status),
            "aggregated_result": result.aggregated_result if hasattr(result, 'aggregated_result') else {},
        }

    async def _execute_workflow(self, task: str, project_id: str | None, context: dict) -> dict[str, Any]:
        multi_agent = self._get_multi_agent()

        plan = self._get_planner()[0].plan_from_goal(task, context)
        result = await multi_agent.execute_plan(plan)
        return {
            "plan_id": plan.plan_id,
            "status": result.status.value if hasattr(result, 'status') else str(result.status),
            "steps": len(plan.steps),
            "result": result.aggregated_result if hasattr(result, 'aggregated_result') else {},
        }

    async def _form_team(self, task: str, context: dict) -> TeamFormation:
        team_id = f"team-{uuid.uuid4().hex[:8]}"

        required_skills = self._extract_skills(task, context)
        agents = []

        from backend.app.core.organization import organization_tree
        for skill in required_skills[:4]:
            existing_agent = self._find_agent_by_skill(skill, organization_tree)
            if existing_agent:
                agents.append({
                    "agent_id": existing_agent.id,
                    "skill": skill,
                    "status": "assigned",
                })

        team = TeamFormation(
            team_id=team_id,
            task=task[:100],
            agents=agents,
            strategy="skill-based",
            estimated_duration_ms=float(len(agents) * 1000),
        )
        self._teams[team_id] = team
        return team

    def _extract_skills(self, task: str, context: dict) -> list[str]:
        skills = []
        task_lower = task.lower()
        # Check for direct keyword matches first, then skill prefixes
        if any(kw in task_lower for kw in ["network", "firewall", "router", "switch"]):
            skills.extend(["network", "security"])
        if any(kw in task_lower for kw in ["python", "coding", "programming", "function"]):
            skills.extend(["coding", "python", "testing"])
        if any(kw in task_lower for kw in ["research", "analyze", "investigate"]):
            skills.extend(["research", "analysis"])
        if any(kw in task_lower for kw in ["sql", "database", "query"]):
            skills.extend(["data-analysis", "sql"])
        if any(kw in task_lower for kw in ["write", "document", "manual"]):
            skills.extend(["writing", "documentation"])
        return skills

    def _find_agent_by_skill(self, skill: str, org_tree) -> Any:
        for node in org_tree._nodes.values():
            if skill in node.capabilities:
                return node
        return None

    def list_teams(self) -> list[dict[str, Any]]:
        return [
            {
                "team_id": t.team_id,
                "task": t.task,
                "agents": [a["agent_id"] for a in t.agents],
                "strategy": t.strategy,
            }
            for t in self._teams.values()
        ]


# Lazy singleton to avoid circular imports at module load
_unified_orchestrator = None


def get_unified_orchestrator() -> UnifiedOrchestrator:
    global _unified_orchestrator
    if _unified_orchestrator is None:
        _unified_orchestrator = UnifiedOrchestrator()
    return _unified_orchestrator
