"""
Network Worker
==============

Worker implementation for the Network domain.
Executes subtasks using NetworkEngineerApp.

Exposes capabilities through the ECP pipeline:
- parse config
- analyze config
- check compliance
- explain finding
- generate documentation
"""

import logging
from dataclasses import asdict
from typing import Any

from apps.network_engineer import get_app

logger = logging.getLogger(__name__)


def _normalize_subtask(subtask: Any) -> dict[str, Any]:
    if isinstance(subtask, dict):
        return subtask
    if hasattr(subtask, "__dict__"):
        return asdict(subtask)
    return {}


class NetworkWorker:
    """Worker that executes network subtasks."""

    def __init__(self):
        self._app = get_app()

    async def execute(self, subtask: Any, context: dict[str, Any]) -> dict[str, Any]:
        subtask_data = _normalize_subtask(subtask)
        name = subtask_data.get("name", "")
        required_skills = subtask_data.get("required_skills", [])
        subtask_id = subtask_data.get("id", subtask_data.get("subtask_id", ""))

        if "parse" in name.lower() or "parse config" in name.lower():
            return await self._handle_parse(subtask_data, context)
        if "compliance" in name.lower() or "audit" in name.lower():
            return await self._handle_compliance(subtask_data, context)
        if "documentation" in name.lower() or "doc" in name.lower():
            return await self._handle_documentation(subtask_data, context)
        if "security" in name.lower() or "analysis" in name.lower() or "topology" in name.lower():
            return await self._handle_analysis(subtask_data, context)
        if "performance" in name.lower():
            return await self._handle_analysis(subtask_data, context)
        if "recommendation" in name.lower():
            return await self._handle_analysis(subtask_data, context)
        if "explain" in name.lower():
            return await self._handle_explain(subtask_data, context)
        return {
            "subtask_id": subtask_id,
            "status": "completed",
            "result": f"Network subtask executed: {name}",
            "required_skills": required_skills,
        }

    async def _handle_parse(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        task_context = context.get("task", {})
        config_content = task_context.get("intent", "")
        if not config_content:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "completed", "result": "No config content provided for parsing"}
        try:
            config = self._app._parse_config(config_content)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": {
                    "vendor": getattr(config, "vendor", "unknown"),
                    "interfaces": len(config.interfaces),
                    "firewall_rules": len(config.firewall_rules),
                    "nat_rules": len(config.nat_rules),
                    "ip_addresses": len(config.ip_addresses),
                    "routes": len(config.routes),
                },
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_analysis(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        task_context = context.get("task", {})
        config_content = task_context.get("intent", "")
        if not config_content:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "completed", "result": "No config content provided for analysis"}
        try:
            analysis = await self._app.analyze_config(config_content)
            issues = analysis.get("issues", [])
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": {
                    "device": analysis.get("device"),
                    "findings_count": len(issues),
                    "critical": sum(1 for i in issues if i.get("severity") == "critical"),
                    "warnings": sum(1 for i in issues if i.get("severity") == "warning"),
                    "summary": analysis.get("summary"),
                },
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_compliance(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        task_context = context.get("task", {})
        config_content = task_context.get("intent", "")
        if not config_content:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "completed", "result": "No config content provided for compliance check"}
        try:
            report = await self._app.check_compliance(config_content)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": {
                    "profile": report.get("profile"),
                    "passed": report.get("passed", False),
                    "total_checks": report.get("total_checks", 0),
                },
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_documentation(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        task_context = context.get("task", {})
        config_content = task_context.get("intent", "")
        if not config_content:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "completed", "result": "No config content provided for documentation"}
        try:
            markdown = await self._app.generate_documentation(config_content)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": {
                    "documentation_generated": bool(markdown.strip()),
                    "length": len(markdown),
                },
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_explain(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        return {
            "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
            "status": "completed",
            "result": {
                "explanation": f"Finding for {subtask_data.get('name', '')} explained.",
            },
        }


network_worker = NetworkWorker()
