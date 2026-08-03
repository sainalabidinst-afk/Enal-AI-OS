"""
Business Analyst Worker — thin adapter (per ADR-003).

Routes task requests to the Business Analyst Domain Engine.
Does not own business logic; delegates to BusinessAnalystEngine.
"""

from __future__ import annotations

from typing import Any

from apps.business_analyst.engine import BusinessAnalystEngine
from apps.business_analyst.schemas import (
    BusinessAnalysisRequest,
    OperationType,
    BusinessContext,
    StakeholderInput,
    Persona,
    QualityAttributes,
    OutputFormat,
)


class BusinessAnalystWorker:
    """
    Thin Worker adapter for the Business Analyst Capability Pack.

    Responsibilities:
        - Parse incoming task into BusinessAnalysisRequest
        - Delegate to BusinessAnalystEngine.analyze()
        - Return BusinessAnalysisReport as dict

    Usage::

        worker = BusinessAnalystWorker()
        report = await worker.execute(task)
    """

    def __init__(self, engine: BusinessAnalystEngine | None = None) -> None:
        self._engine = engine or BusinessAnalystEngine()

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a business analysis task.

        Expected task format::

            {
                "operation": "requirement_gathering",
                "business_context": {"domain": "e-commerce", "project_name": "..."},
                "inputs": {"natural_language_requirements": [...]},
                "output_format": "markdown"
            }

        Returns:
            BusinessAnalysisReport as a JSON-serializable dict.
        """
        ctx_data = task.get("business_context", {})
        context = BusinessContext(**ctx_data)

        inputs_data = task.get("inputs", {})
        inputs = StakeholderInput(**inputs_data)

        personas = [Persona(**p) for p in task.get("personas", [])]

        qa_data = task.get("quality_attributes", {})
        quality_attrs = QualityAttributes(**qa_data)

        op_value = task.get("operation", "requirement_gathering")
        try:
            operation = OperationType(op_value)
        except ValueError:
            operation = OperationType.requirement_gathering

        fmt_value = task.get("output_format", "markdown")
        try:
            output_format = OutputFormat(fmt_value)
        except ValueError:
            output_format = OutputFormat.markdown

        request = BusinessAnalysisRequest(
            operation=operation,
            business_context=context,
            inputs=inputs,
            personas=personas,
            quality_attributes=quality_attrs,
            output_format=output_format,
        )

        report = self._engine.analyze(request)
        return report.to_dict()
