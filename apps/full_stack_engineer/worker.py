"""
Full Stack Engineer Worker — thin adapter (per ADR-003).

Routes task requests to the Full Stack Engineer Domain Engine.
Does not own business logic; delegates to FullStackEngineerEngine.
"""

from __future__ import annotations

from typing import Any

from apps.full_stack_engineer.engine import FullStackEngineerEngine
from apps.full_stack_engineer.schemas import (
    FullStackRequest,
    OperationType,
    OutputFormat,
)


class FullStackEngineerWorker:
    """
    Thin Worker adapter for the Full Stack Engineer Capability Pack.

    Responsibilities:
        - Parse incoming task into FullStackRequest
        - Delegate to FullStackEngineerEngine.review()
        - Return FullStackReport as dict

    Usage::

        worker = FullStackEngineerWorker()
        report = await worker.execute(task)
    """

    def __init__(self, engine: FullStackEngineerEngine | None = None) -> None:
        self._engine = engine or FullStackEngineerEngine()

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a full stack engineering task.

        Expected task format::

            {
                "operation": "full_stack_review",
                "inputs": {"repo_path": "/path/to/repo"},
                "context": {"project_id": "my-project", "language": "python"},
                "output_format": "json"
            }

        Returns:
            FullStackReport as a JSON-serializable dict.
        """
        op_value = task.get("operation", "full_stack_review")
        try:
            operation = OperationType(op_value)
        except ValueError:
            operation = OperationType.full_stack_review

        fmt_value = task.get("output_format", "json")
        output_format = fmt_value if fmt_value in ("json", "markdown") else "json"

        request = FullStackRequest(
            operation=operation,
            inputs=task.get("inputs", {}),
            context=task.get("context", {}),
            quality_attributes=task.get("quality_attributes", {}),
            output_format=output_format,
        )

        report = await self._engine.review(request)
        return report.to_dict()
