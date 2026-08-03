"""
DevOps Worker
=============

Execution adapter bridging the reference app and the upgraded engine.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.devops_assistant.engine import DevOpsEngine
from apps.devops_assistant.project_scanner import DevOpsProjectScanner
from apps.devops_assistant.schemas import ProjectAnalysis
from apps.devops_assistant.suggestion_generator import DevOpsSuggestionGenerator

logger = logging.getLogger(__name__)


class DevOpsWorker:
    """Execution adapter for DevOps Assistant."""

    def __init__(self) -> None:
        self.engine = DevOpsEngine()
        self.suggestion_generator = DevOpsSuggestionGenerator()
        self.project_scanner = DevOpsProjectScanner()

    async def execute(self, user_input: str, context: dict[str, Any]) -> dict[str, Any]:
        project_path = context.get("project_path", ".")
        artifacts = context.get("artifacts", [])

        pipeline = await self.engine.generate_pipeline(context.get("project_id", "default"))
        infra = await self.engine.design_infrastructure(context.get("project_id", "default"))
        deployment = await self.engine.plan_deployment(context.get("project_id", "default"))

        analysis: dict[str, Any] = {
            "pipeline": pipeline,
            "infrastructure": infra,
            "deployment": deployment,
        }

        if artifacts:
            analysis["artifact_analysis"] = []
            for artifact in artifacts:
                result = self.suggestion_generator.analyze(artifact)
                analysis["artifact_analysis"].append(result)

        if project_path:
            try:
                scan_result = self.project_scanner.scan(project_path)
                analysis["project_analysis"] = {
                    "project": scan_result.project,
                    "modules_count": scan_result.modules_count,
                    "files_count": scan_result.files_count,
                    "complexity": scan_result.complexity,
                    "language": scan_result.language,
                    "framework": scan_result.framework,
                    "metadata": scan_result.metadata,
                }
            except Exception as exc:
                logger.warning("Project scan failed: %s", exc)
                analysis["project_analysis"] = {"error": str(exc)}

        return {
            "app": "devops-assistant",
            "input": user_input,
            "result": analysis,
            "metadata": {
                "capabilities_used": [
                    "ci-cd",
                    "infrastructure-design",
                    "deployment",
                    "monitoring",
                    "security-hardening",
                ],
            },
        }
