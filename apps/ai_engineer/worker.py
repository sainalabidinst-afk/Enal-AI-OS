"""
AI Engineer Worker — thin adapter (per ADR-003).

Routes task requests to the AI Engineer Domain Engine.
Does not own business logic; delegates to AIEngineerEngine.
"""

from __future__ import annotations

from typing import Any

from apps.ai_engineer.engine import AIEngineerEngine
from apps.ai_engineer.schemas import (
    AIEngineerRequest,
    OperationType,
    BusinessContext,
    QualityAttributes,
    OutputFormat,
)


class AIEngineerWorker:
    """
    Thin Worker adapter for the AI Engineer Capability Pack.

    Responsibilities:
        - Parse incoming task into AIEngineerRequest
        - Delegate to AIEngineerEngine.design()
        - Return AIEngineerReport as dict

    Usage::

        worker = AIEngineerWorker()
        report = await worker.execute(task)
    """

    def __init__(self, engine: AIEngineerEngine | None = None) -> None:
        self._engine = engine or AIEngineerEngine()

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute an AI engineering task.

        Expected task format::

            {
                "operation": "agent_design",
                "business_context": {"domain": "trading", "project_name": "..."},
                "quality_attributes": {"accuracy_target": "95%"},
                "output_format": "json"
            }

        Returns:
            AIEngineerReport as a JSON-serializable dict.
        """
        ctx_data = task.get("business_context", {})
        context = BusinessContext(**ctx_data)

        qa_data = task.get("quality_attributes", {})
        quality_attrs = QualityAttributes(**qa_data)

        op_value = task.get("operation", "agent_design")
        try:
            operation = OperationType(op_value)
        except ValueError:
            operation = OperationType.agent_design

        fmt_value = task.get("output_format", "json")
        try:
            output_format = OutputFormat(fmt_value)
        except ValueError:
            output_format = OutputFormat.json

        request = AIEngineerRequest(
            operation=operation,
            business_context=context,
            quality_attributes=quality_attrs,
            output_format=output_format,
            inputs=task.get("inputs", {}),
        )

        report = self._engine.design(request)
        return report.to_dict()
