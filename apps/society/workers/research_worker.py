"""
Research Worker
===============

Worker implementation for the Research domain.
Executes subtasks using ResearchAssistantApp.

Exposes capabilities through the ECP pipeline:
- literature review
- data analysis
- experiment design
- report writing
"""

import logging
from typing import Any

from apps.research_assistant import get_app

logger = logging.getLogger(__name__)


def _normalize_subtask(subtask: Any) -> dict[str, Any]:
    if isinstance(subtask, dict):
        return subtask
    if hasattr(subtask, "__dict__"):
        return subtask.__dict__
    return {}


class ResearchWorker:
    """Worker that executes research subtasks."""

    def __init__(self):
        self._app = get_app()

    async def execute(self, subtask: Any, context: dict[str, Any]) -> dict[str, Any]:
        subtask_data = _normalize_subtask(subtask)
        name = subtask_data.get("name", "")
        required_skills = subtask_data.get("required_skills", [])
        subtask_id = subtask_data.get("id", subtask_data.get("subtask_id", ""))

        lowered = name.lower()
        if "literature" in lowered or "review" in lowered or "search" in lowered:
            return await self._handle_literature_review(subtask_data, context)
        if "analysis" in lowered or "analyze" in lowered or "data" in lowered:
            return await self._handle_data_analysis(subtask_data, context)
        if "experiment" in lowered or "design" in lowered:
            return await self._handle_experiment_design(subtask_data, context)
        if "report" in lowered or "writing" in lowered or "summary" in lowered:
            return await self._handle_report_writing(subtask_data, context)
        return {
            "subtask_id": subtask_id,
            "status": "completed",
            "result": f"Research subtask executed: {name}",
            "required_skills": required_skills,
        }

    async def _handle_literature_review(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        task_context = context.get("task", {})
        query = task_context.get("intent", "")
        if not query:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "completed", "result": "No query provided for literature review"}
        try:
            evidence = await self._app.engine.search_evidence(query)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": {
                    "query": query,
                    "evidence_count": len(evidence),
                    "evidence": evidence,
                },
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_data_analysis(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        task_context = context.get("task", {})
        query = task_context.get("intent", "")
        if not query:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "completed", "result": "No query provided for data analysis"}
        try:
            evidence = await self._app.engine.search_evidence(query)
            analysis = await self._app.engine.analyze_findings(query, evidence)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": {
                    "query": query,
                    "findings_count": analysis.get("findings_count", 0),
                    "confidence": analysis.get("confidence", 0.0),
                    "summary": analysis.get("summary", ""),
                },
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_experiment_design(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        task_context = context.get("task", {})
        query = task_context.get("intent", "")
        return {
            "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
            "status": "completed",
            "result": {
                "query": query,
                "experiment_plan": f"Simulated experiment plan for: {query}",
            },
        }

    async def _handle_report_writing(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        task_context = context.get("task", {})
        query = task_context.get("intent", "")
        if not query:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "completed", "result": "No query provided for report writing"}
        try:
            evidence = await self._app.engine.search_evidence(query)
            analysis = await self._app.engine.analyze_findings(query, evidence)
            report = await self._app.engine.generate_report(query, analysis)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": {
                    "query": query,
                    "report_length": len(report),
                    "report": report,
                },
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}


research_worker = ResearchWorker()
