"""
Full Stack Worker
=================

Worker implementation for the Full Stack Engineer domain.
Executes subtasks using FullStackEngineerApp.

Exposes capabilities through the ECP pipeline:
- architecture review
- code review
- refactoring planning
- test engineering
- performance analysis
- release engineering
"""

import json
import logging
from typing import Any

from apps.full_stack_engineer import get_app

logger = logging.getLogger(__name__)


def _normalize_subtask(subtask: Any) -> dict[str, Any]:
    if isinstance(subtask, dict):
        return subtask
    if hasattr(subtask, "__dict__"):
        return subtask.__dict__
    return {}


class FullStackWorker:
    """Worker that executes full stack subtasks."""

    def __init__(self):
        self._app = get_app()

    async def execute(self, subtask: Any, context: dict[str, Any]) -> dict[str, Any]:
        subtask_data = _normalize_subtask(subtask)
        name = subtask_data.get("name", "")
        required_skills = subtask_data.get("required_skills", [])
        subtask_id = subtask_data.get("id", subtask_data.get("subtask_id", ""))

        lowered = name.lower()
        if "architecture" in lowered or "arch review" in lowered or "layering" in lowered:
            return await self._handle_architecture_review(subtask_data, context)
        if "code review" in lowered or "code-review" in lowered or "review" in lowered:
            return await self._handle_code_review(subtask_data, context)
        if "refactor" in lowered or "refactoring" in lowered:
            return await self._handle_refactoring(subtask_data, context)
        if "test" in lowered or "testing" in lowered:
            return await self._handle_test(subtask_data, context)
        if "performance" in lowered or "perf" in lowered:
            return await self._handle_performance(subtask_data, context)
        if "release" in lowered or "deployment" in lowered:
            return await self._handle_release(subtask_data, context)
        return {
            "subtask_id": subtask_id,
            "status": "completed",
            "result": f"Full stack subtask executed: {name}",
            "required_skills": required_skills,
        }

    async def _handle_architecture_review(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        repo_path = subtask_data.get("repo_path") or context.get("repo_path") or "."
        try:
            result = await self._app.review_architecture(repo_path, context)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": {
                    "architecture_score": result.get("architecture_score"),
                    "layering_grade": result.get("layering_grade"),
                    "dependency_grade": result.get("dependency_grade"),
                    "modularity_grade": result.get("modularity_grade"),
                    "tech_debt_grade": result.get("tech_debt_grade"),
                    "total_issues": result.get("summary", {}).get("total_issues", 0),
                },
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_code_review(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        code = subtask_data.get("code") or context.get("code") or ""
        filename = subtask_data.get("filename", "<unknown>")
        if not code:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "completed", "result": "No code provided for review"}
        try:
            result = await self._app.review_code(code, filename, context)
            findings = result.get("findings", [])
            summary = result.get("summary", {})
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": {
                    "filename": filename,
                    "findings_count": len(findings),
                    "critical": summary.get("critical", 0),
                    "high": summary.get("high", 0),
                    "medium": summary.get("medium", 0),
                    "low": summary.get("low", 0),
                    "info": summary.get("info", 0),
                },
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_refactoring(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        code = subtask_data.get("code") or context.get("code") or ""
        filename = subtask_data.get("filename", "<unknown>")
        if not code:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "completed", "result": "No code provided for refactoring plan"}
        try:
            result = await self._app.plan_refactoring(code, filename)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": {
                    "filename": result.get("filename"),
                    "total_plans": result.get("total_plans", 0),
                    "plans": result.get("plans", []),
                },
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_test(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        source_path = subtask_data.get("source_path") or context.get("source_path") or "."
        module_path = subtask_data.get("module_path") or context.get("module_path") or ""
        try:
            result = await self._app.engineer_tests(source_path, module_path)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": result,
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_performance(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        code = subtask_data.get("code") or context.get("code") or ""
        filename = subtask_data.get("filename", "<unknown>")
        if not code:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "completed", "result": "No code provided for performance analysis"}
        try:
            result = await self._app.analyze_performance(code, filename)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": {
                    "filename": filename,
                    "issues_count": len(result.get("issues", [])),
                    "summary": result.get("summary", {}),
                },
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_release(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        changes = subtask_data.get("changes") or context.get("changes") or []
        release_context = {k: v for k, v in subtask_data.items() if k not in {"id", "subtask_id", "name", "required_skills", "changes", "code", "filename", "repo_path", "source_path", "module_path"}}
        try:
            result = await self._app.review_release(changes, {**context, **release_context})
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": {
                    "ready": result.get("ready"),
                    "summary": result.get("summary", {}),
                },
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}


full_stack_worker = FullStackWorker()