"""
DevOps Worker
=============

Worker implementation for the DevOps domain.
Executes subtasks using DevOpsAssistantApp.

Exposes capabilities through the ECP pipeline:
- infrastructure design
- CI/CD pipeline
- monitoring setup
- deployment planning
"""

import logging
from typing import Any

from apps.devops_assistant import get_app

logger = logging.getLogger(__name__)


def _normalize_subtask(subtask: Any) -> dict[str, Any]:
    if isinstance(subtask, dict):
        return subtask
    if hasattr(subtask, "__dict__"):
        return subtask.__dict__
    return {}


class DevOpsWorker:
    """Worker that executes DevOps subtasks."""

    def __init__(self):
        self._app = get_app()

    async def execute(self, subtask: Any, context: dict[str, Any]) -> dict[str, Any]:
        subtask_data = _normalize_subtask(subtask)
        name = subtask_data.get("name", "")
        required_skills = subtask_data.get("required_skills", [])
        subtask_id = subtask_data.get("id", subtask_data.get("subtask_id", ""))

        lowered = name.lower()
        if "infrastructure" in lowered or "infra" in lowered:
            return await self._handle_infrastructure(subtask_data, context)
        if "ci/cd" in lowered or "pipeline" in lowered or "cicd" in lowered:
            return await self._handle_cicd(subtask_data, context)
        if "monitoring" in lowered or "observability" in lowered:
            return await self._handle_monitoring(subtask_data, context)
        if "deployment" in lowered or "deploy" in lowered:
            return await self._handle_deployment(subtask_data, context)
        return {
            "subtask_id": subtask_id,
            "status": "completed",
            "result": f"DevOps subtask executed: {name}",
            "required_skills": required_skills,
        }

    async def _handle_infrastructure(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        task_context = context.get("task", {})
        service = task_context.get("intent", task_context.get("name", "unknown-service"))
        try:
            result = await self._app.engine.design_infrastructure(service)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": result,
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_cicd(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        task_context = context.get("task", {})
        service = task_context.get("intent", task_context.get("name", "unknown-service"))
        try:
            result = await self._app.engine.generate_pipeline(service)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": result,
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_monitoring(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        return {
            "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
            "status": "completed",
            "result": {
                "monitoring": "enabled",
                "alerts": ["cpu", "memory", "latency"],
                "dashboard": "enabled",
            },
        }

    async def _handle_deployment(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        task_context = context.get("task", {})
        service = task_context.get("intent", task_context.get("name", "unknown-service"))
        try:
            result = await self._app.engine.plan_deployment(service)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": result,
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}


devops_worker = DevOpsWorker()
