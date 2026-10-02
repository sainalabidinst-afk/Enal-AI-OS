"""
Finance Analyst Worker.
"""

from __future__ import annotations

import json
from typing import Any

from apps.finance_analyst.engine import FinanceAnalystEngine
from apps.finance_analyst.schemas import FinanceAnalystRequest


class FinanceAnalystWorker:
    """Thin adapter that exposes the Finance Analyst engine to agents."""

    def __init__(self) -> None:
        self.engine = FinanceAnalystEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = FinanceAnalystRequest(**task)
        report = self.engine.execute(request)
        return json.loads(report.model_dump_json())


__all__ = ["FinanceAnalystWorker"]
