"""
Self Development Worker
=======================

Thin execution adapter for Self Development.

Delegates all domain logic to SelfDevelopmentEngine.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from apps.self_development.engine import self_development_engine

logger = logging.getLogger(__name__)


class SelfDevelopmentWorker:
    """Adapter that routes requests to SelfDevelopmentEngine."""

    def __init__(self, engine: Any = None) -> None:
        self.engine = engine or self_development_engine

    async def analyze_project(self, project_path: str | None = None) -> dict[str, Any]:
        return await self.engine.analyze_project(project_path)

    async def identify_problems(self, project_path: str | None = None) -> list[dict[str, Any]]:
        return await self.engine.identify_problems(project_path)

    async def propose_solution(self, problem_id: str) -> dict[str, Any]:
        return await self.engine.propose_solution(problem_id)

    async def generate_patch(self, problem_id: str) -> dict[str, Any]:
        return await self.engine.generate_patch(problem_id)

    async def run_tests(self) -> dict[str, Any]:
        return await self.engine.run_tests()

    async def get_approval_status(self, problem_id: str) -> dict[str, Any]:
        return await self.engine.get_approval_status(problem_id)

    async def apply_changes(self, problem_id: str, approved: bool) -> dict[str, Any]:
        return await self.engine.apply_changes(problem_id, approved)

    async def analyze_ecp(self, ecp_root: str | None = None) -> dict[str, Any]:
        return await self.engine.analyze_ecp(ecp_root)

    async def propose_capabilities(self, ecp_root: str | None = None) -> list[dict[str, Any]]:
        return await self.engine.propose_capabilities(ecp_root)

    async def propose_improvements(self, ecp_root: str | None = None) -> list[dict[str, Any]]:
        return await self.engine.propose_improvements(ecp_root)

    async def detect_gap(self, user_query: str) -> dict[str, Any]:
        return await self.engine.detect_gap(user_query)

    async def synthesize_pack(self, proposal: Any | None = None) -> dict[str, Any]:
        return await self.engine.synthesize_pack(proposal)

    async def detect_anomalies(self, samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return await self.engine.detect_anomalies(samples)

    async def plan_remediation(self, anomaly: dict[str, Any]) -> dict[str, Any]:
        return await self.engine.plan_remediation(anomaly)

    async def publish_insight(
        self, source_node: str, insight_type: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        return await self.engine.publish_insight(source_node, insight_type, payload)

    async def list_insights(self) -> list[dict[str, Any]]:
        return await self.engine.list_insights()

    # ------------------------------------------------------------------
    # Growth engine adapters
    # ------------------------------------------------------------------

    async def record_activity(self, **kwargs: Any) -> dict[str, Any]:
        return await self.engine.record_activity(**kwargs)

    async def get_progress(self, granularity: str = "week", weeks: int = 12) -> dict[str, Any]:
        return await self.engine.get_progress(granularity, weeks)

    async def render_progress_chart(
        self, granularity: str = "week", weeks: int = 12, metric: str = "hours"
    ) -> dict[str, Any]:
        return await self.engine.render_progress_chart(granularity, weeks, metric)

    async def create_goal(self, **kwargs: Any) -> dict[str, Any]:
        return await self.engine.create_goal(**kwargs)

    async def list_goals(self) -> dict[str, Any]:
        return await self.engine.list_goals()

    async def align_goals(self) -> dict[str, Any]:
        return await self.engine.align_goals()

    async def validate_relevance(
        self, title: str, skills: list[str] | None = None, goal_id: str | None = None
    ) -> dict[str, Any]:
        return await self.engine.validate_relevance(title, skills, goal_id)

    async def recommend_next(self, limit: int = 5, goal_id: str | None = None) -> dict[str, Any]:
        return await self.engine.recommend_next(limit, goal_id)

    async def create_habit(self, **kwargs: Any) -> dict[str, Any]:
        return await self.engine.create_habit(**kwargs)

    async def check_in_habit(
        self, habit_id: str, note: str = "", completed_at: datetime | None = None
    ) -> dict[str, Any]:
        return await self.engine.check_in_habit(habit_id, note, completed_at)

    async def habit_statuses(self) -> dict[str, Any]:
        return await self.engine.habit_statuses()

    async def dispatch_growth_alerts(self) -> dict[str, Any]:
        return await self.engine.dispatch_growth_alerts()

    async def learning_projects(self, goal_id: str | None = None) -> dict[str, Any]:
        return await self.engine.learning_projects(goal_id)

    async def run_learning_project(
        self,
        project_id: str,
        params: dict[str, Any] | None = None,
        duration_minutes: float = 60.0,
        goal_id: str | None = None,
        notes: str = "",
    ) -> dict[str, Any]:
        return await self.engine.run_learning_project(
            project_id, params, duration_minutes, goal_id, notes
        )


self_development_worker = SelfDevelopmentWorker()
