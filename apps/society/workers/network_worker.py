"""
Network Worker
=============

Worker implementation for the Network domain.
Executes subtasks using NetworkEngineerApp.

Exposes capabilities through the ECP pipeline:
- parse config
- analyze config
- check compliance
- explain finding
- generate documentation
- design review
- troubleshooting
- migration planning
- network advisory
"""

import json
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
        if "design review" in name.lower() or "review_design" in name.lower() or "design" in name.lower():
            return await self._handle_design_review(subtask_data, context)
        if "troubleshoot" in name.lower() or "troubleshooting" in name.lower():
            return await self._handle_troubleshoot(subtask_data, context)
        if "migration" in name.lower() or "plan_migration" in name.lower():
            return await self._handle_migration(subtask_data, context)
        if "advise" in name.lower() or "advisory" in name.lower():
            return await self._handle_advise(subtask_data, context)
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
        task_context = context.get("task", {})
        config_content = task_context.get("intent", "")
        category = subtask_data.get("category", "")
        if not config_content or not category:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "completed", "result": "Missing config or category for explanation"}
        try:
            explanation = await self._app.explain_finding(config_content, category)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": {
                    "category": category,
                    "explanation": explanation or "No explanation available.",
                },
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_design_review(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        task_context = context.get("task", {})
        topology_json = task_context.get("topology") or subtask_data.get("topology") or {}
        if not topology_json:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "completed", "result": "No topology provided for design review"}
        try:
            review = await self._app.review_design(topology_json, context)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": {
                    "network_score": review.get("network_score"),
                    "availability_grade": review.get("availability_grade"),
                    "security_grade": review.get("security_grade"),
                    "scalability_grade": review.get("scalability_grade"),
                    "performance_grade": review.get("performance_grade"),
                    "total_issues": review.get("summary", {}).get("total_issues", 0),
                },
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_troubleshoot(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        task_context = context.get("task", {})
        symptom = task_context.get("intent") or subtask_data.get("symptom") or subtask_data.get("name", "")
        evidence = subtask_data.get("evidence", [])
        if not symptom:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "completed", "result": "No symptom provided for troubleshooting"}
        try:
            session = await self._app.troubleshoot(symptom, evidence)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": {
                    "session_id": session.get("session_id"),
                    "symptom": session.get("symptom"),
                    "hypotheses_count": len(session.get("hypotheses", [])),
                    "root_cause": session.get("root_cause"),
                    "status": session.get("status"),
                    "confidence": session.get("confidence"),
                },
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_migration(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        task_context = context.get("task", {})
        source_vendor = task_context.get("source_vendor") or subtask_data.get("source_vendor", "")
        target_vendor = task_context.get("target_vendor") or subtask_data.get("target_vendor", "")
        source_config = task_context.get("intent") or subtask_data.get("source_config", "")
        if not source_vendor or not target_vendor:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "completed", "result": "Missing source or target vendor for migration"}
        try:
            plan = await self._app.plan_migration(source_vendor, target_vendor, source_config)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": {
                    "source_vendor": plan.get("source_vendor"),
                    "target_vendor": plan.get("target_vendor"),
                    "overall_risk": plan.get("overall_risk"),
                    "estimated_downtime_minutes": plan.get("estimated_downtime_minutes"),
                    "phases_count": len(plan.get("phases", [])),
                    "warnings": plan.get("warnings", []),
                },
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}

    async def _handle_advise(self, subtask_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        task_context = context.get("task", {})
        query = task_context.get("intent") or subtask_data.get("query") or subtask_data.get("name", "")
        if not query:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "completed", "result": "No query provided for advisory"}
        try:
            advice = await self._app.advise(query, context)
            return {
                "subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")),
                "status": "completed",
                "result": {
                    "query": advice.get("query"),
                    "proposals_count": len(advice.get("proposals", [])),
                    "proposals": advice.get("proposals", []),
                },
            }
        except Exception as exc:
            return {"subtask_id": subtask_data.get("subtask_id", subtask_data.get("id", "")), "status": "failed", "error": str(exc)}


network_worker = NetworkWorker()
