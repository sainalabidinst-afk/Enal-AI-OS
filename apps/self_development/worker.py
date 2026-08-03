"""
Self Development Worker
=======================

Thin execution adapter for Self Development.

Delegates all domain logic to SelfDevelopmentEngine.
"""

from __future__ import annotations

import logging
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


self_development_worker = SelfDevelopmentWorker()
