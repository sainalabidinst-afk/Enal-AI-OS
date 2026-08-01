"""
QA Engineer Worker — thin adapter (per ADR-003).

Routes task requests to the QA Engineer Domain Engine.
Does not own business logic; delegates to QAEngineerEngine.
"""

from __future__ import annotations

from typing import Any

from apps.qa_engineer.engine import QAEngineerEngine
from apps.qa_engineer.schemas import QATestRequestModel, QATestOperation


class QAEngineerWorker:
    """
    Thin Worker adapter for the QA Engineer Capability Pack.

    Responsibilities:
        - Parse incoming task into QATestRequestModel
        - Delegate to QAEngineerEngine.review()
        - Return QATestReport as dict

    Usage::

        worker = QAEngineerWorker()
        report = await worker.execute(task)
    """

    def __init__(self, engine: QAEngineerEngine | None = None) -> None:
        self._engine = engine or QAEngineerEngine()

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a QA task.

        Expected task format::

            {
                "operation": "unit_test",
                "target": {"source_code": "...", "language": "python", "framework": "pytest"},
                "coverage_target": 0.8,
                "for_capability_pack": "code"
            }

        Returns:
            QATestReport as a JSON-serializable dict.
        """
        target = task.get("target", {})
        op_value = task.get("operation", "unit_test")

        try:
            operation = QATestOperation(op_value)
        except ValueError:
            operation = QATestOperation.unit_test

        request = QATestRequestModel(
            operation=operation,
            target=target,
            for_capability_pack=task.get("for_capability_pack"),
            coverage_target=task.get("coverage_target", 0.8),
            mutation_target=task.get("mutation_target", 0.8),
            performance_requirements=task.get("performance_requirements"),
            include_uncovered_code=task.get("include_uncovered_code", True),
        )

        report = self._engine.review(request)
        return report.to_dict()
