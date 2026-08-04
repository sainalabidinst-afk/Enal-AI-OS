"""
UI/UX Designer Worker — thin adapter (per ADR-003).

Routes task requests to the UI/UX Designer Domain Engine.
Does not own business logic; delegates to UIUXDesignerEngine.
"""

from __future__ import annotations

from typing import Any

from apps.ui_ux_designer.engine import UIUXDesignerEngine
from apps.ui_ux_designer.schemas import (
    UIUXDesignerRequest,
    OperationType,
    BusinessContext,
    StakeholderInput,
    Persona,
    QualityAttributes,
    OutputFormat,
)


class UIUXDesignerWorker:
    """
    Thin Worker adapter for the UI/UX Designer Capability Pack.

    Responsibilities:
        - Parse incoming task into UIUXDesignerRequest
        - Delegate to UIUXDesignerEngine.design()
        - Return UIUXDesignerReport as dict

    Usage::

        worker = UIUXDesignerWorker()
        report = await worker.execute(task)
    """

    def __init__(self, engine: UIUXDesignerEngine | None = None) -> None:
        self._engine = engine or UIUXDesignerEngine()

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a UI/UX design task.

        Expected task format::

            {
                "operation": "full_design",
                "business_context": {"domain": "e-commerce", "project_name": "Online Shop"},
                "inputs": {"product_requirements": ["Users must checkout in 3 steps"]},
                "personas": [{"name": "Alice", "role": "Customer", "goals": [...]}],
                "output_format": "json"
            }

        Returns:
            UIUXDesignerReport as a JSON-serializable dict.
        """
        ctx_data = task.get("business_context", {})
        context = BusinessContext(**ctx_data)

        inputs_data = task.get("inputs", {})
        inputs = StakeholderInput(**inputs_data)

        personas = [Persona(**p) for p in task.get("personas", [])]

        qa_data = task.get("quality_attributes", {})
        quality_attrs = QualityAttributes(**qa_data)

        op_value = task.get("operation", "full_design")
        try:
            operation = OperationType(op_value)
        except ValueError:
            operation = OperationType.full_design

        fmt_value = task.get("output_format", "json")
        try:
            output_format = OutputFormat(fmt_value)
        except ValueError:
            output_format = OutputFormat.json

        target_platforms = task.get("target_platforms", ["web"])

        request = UIUXDesignerRequest(
            operation=operation,
            business_context=context,
            inputs=inputs,
            personas=personas,
            quality_attributes=quality_attrs,
            output_format=output_format,
            target_platforms=target_platforms,
        )

        report = self._engine.design(request)
        return report.to_dict()
