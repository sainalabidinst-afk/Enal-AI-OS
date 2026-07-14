"""
Self Development Worker
=======================

Worker implementation for the Self Development domain.
Executes subtasks using SelfDevelopmentApp.

Exposes capabilities through the ECP pipeline:
- analyze project
- identify problems
- propose solution
- generate patch
- run tests
- await approval
- apply changes
"""

import logging
from typing import Any

from apps.self_development import get_app

logger = logging.getLogger(__name__)


def _normalize_subtask(subtask: Any) -> dict[str, Any]:
    if isinstance(subtask, dict):
        return subtask
    if hasattr(subtask, "__dict__"):
        return subtask.__dict__
    return {}


class SelfDevelopmentWorker:
    """Worker that executes self-development subtasks."""

    def __init__(self):
        self._app = get_app()

    async def execute(self, subtask: Any, context: dict[str, Any]) -> dict[str, Any]:
        subtask_data = _normalize_subtask(subtask)
        name = subtask_data.get("name", "")
        required_skills = subtask_data.get("required_skills", [])
        subtask_id = subtask_data.get("id", subtask_data.get("subtask_id", ""))

        lowered = name.lower()
        if "analyze" in lowered or "analysis" in lowered:
            return await self._handle_analyze_project(subtask_data, context)
        if "identify" in lowered or "problem" in lowered or "bottleneck" in lowered:
            return await self._handle_identify_problems(subtask_data, context)
        if "propose" in lowered or "solution" in lowered:
            return await self._handle_propose_solution(subtask_data, context)
        if "patch" in lowered or "generate" in lowered:
            return await self._handle_generate_patch(subtask_data, context)
        if "test" in lowered:
            return await self._handle_run_tests(subtask_data, context)
        if "approval" in lowered or "approve" in lowered:
            return await self._handle_approval(subtask_data, context)
        if "apply" in lowered or "change" in lowered or "commit" in lowered:
            return await self._handle_apply_changes(subtask_data, context)
        return {
            "subtask_id": subtask_id,
            "status": "completed",
            "result": f"Self-development subtask executed: {name}",
            "required_skills": required_skills,
        }

    async def _handle_analyze_project(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        try:
            result = await self._app.engine.analyze_project()
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": result,
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_identify_problems(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        try:
            result = await self._app.engine.identify_problems()
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": {
                    "problems_count": len(result),
                    "problems": result,
                },
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_propose_solution(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        problem_id = (context.get("task", {}) or {}).get("intent", "problem-1")
        try:
            result = await self._app.engine.propose_solution(problem_id)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": result,
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_generate_patch(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        problem_id = (context.get("task", {}) or {}).get("intent", "problem-1")
        try:
            result = await self._app.engine.generate_patch(problem_id)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": result,
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_run_tests(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        try:
            result = await self._app.engine.run_tests()
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": result,
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_approval(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        problem_id = (context.get("task", {}) or {}).get("intent", "problem-1")
        try:
            result = await self._app.engine.get_approval_status(problem_id)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": result,
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_apply_changes(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        problem_id = (context.get("task", {}) or {}).get("intent", "problem-1")
        try:
            approved = context.get("approved", False)
            result = await self._app.engine.apply_changes(problem_id, approved=approved)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": result,
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}


self_development_worker = SelfDevelopmentWorker()
