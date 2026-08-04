"""
Infrastructure Engineer Worker — thin adapter (per ADR-003).

Routes task requests to the Infrastructure Engineer Domain Engine.
Does not own business logic; delegates to InfrastructureEngineerEngine.
"""

from __future__ import annotations

from typing import Any

from apps.infrastructure_engineer.engine import InfrastructureEngineerEngine
from apps.infrastructure_engineer.schemas import (
    InfrastructureEngineerRequest,
    OperationType,
    BusinessContext,
    QualityAttributes,
    InfrastructureType,
    OutputFormat,
)


class InfrastructureEngineerWorker:
    """
    Thin Worker adapter for the Infrastructure Engineer Capability Pack.

    Responsibilities:
        - Parse incoming task into InfrastructureEngineerRequest
        - Delegate to InfrastructureEngineerEngine.design()
        - Return InfrastructureEngineerReport as dict

    Usage::

        worker = InfrastructureEngineerWorker()
        report = await worker.execute(task)
    """

    def __init__(self, engine: InfrastructureEngineerEngine | None = None) -> None:
        self._engine = engine or InfrastructureEngineerEngine()

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute an infrastructure engineering task.

        Expected task format::

            {
                "operation": "kubernetes_design",
                "business_context": {"domain": "e-commerce", "project_name": "..."},
                "inputs": {"service_specs": [...]},
                "quality_attributes": {"availability_target": "99.9%"},
                "output_format": "yaml"
            }

        Returns:
            InfrastructureEngineerReport as a JSON-serializable dict.
        """
        ctx_data = task.get("business_context", {})
        context = BusinessContext(**ctx_data)

        qa_data = task.get("quality_attributes", {})
        quality_attrs = QualityAttributes(**qa_data)

        op_value = task.get("operation", "kubernetes_design")
        try:
            operation = OperationType(op_value)
        except ValueError:
            operation = OperationType.kubernetes_design

        infra_type_value = task.get("infrastructure_type", "kubernetes")
        try:
            infra_type = InfrastructureType(infra_type_value)
        except ValueError:
            infra_type = InfrastructureType.kubernetes

        fmt_value = task.get("output_format", "yaml")
        try:
            output_format = OutputFormat(fmt_value)
        except ValueError:
            output_format = OutputFormat.yaml

        request = InfrastructureEngineerRequest(
            operation=operation,
            business_context=context,
            quality_attributes=quality_attrs,
            infrastructure_type=infra_type,
            output_format=output_format,
            inputs=task.get("inputs", {}),
        )

        report = self._engine.design(request)
        return report.to_dict()
