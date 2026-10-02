"""
Finance Analyst — __init__.py
"""

from typing import Any

from apps.finance_analyst.engine import FinanceAnalystEngine
from apps.finance_analyst.schemas import (
    BusinessContext,
    EvidenceCheckResult,
    FinanceAnalystRecord,
    FinanceAnalystReport,
    FinanceAnalystRequest,
    FinanceInputs,
    FinanceOperation,
    FinancialMetric,
    RiskScenario,
    SensitivityScenario,
)
from apps.finance_analyst.worker import FinanceAnalystWorker
from apps.base import BaseReferenceApp


class FinanceAnalystApp(BaseReferenceApp):
    name = "finance-analyst"
    version = "1.0.0"
    description = "Financial analysis, scenario modeling, risk assessment, and control compliance checking"
    category = "finance"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = FinanceAnalystWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> FinanceAnalystApp:
    return FinanceAnalystApp()


__all__ = [
    "FinanceAnalystApp",
    "get_app",
    "FinanceAnalystEngine",
    "FinanceAnalystWorker",
    "FinanceAnalystRequest",
    "FinanceAnalystReport",
    "FinanceOperation",
    "FinanceInputs",
    "FinancialMetric",
    "SensitivityScenario",
    "RiskScenario",
    "EvidenceCheckResult",
    "BusinessContext",
    "FinanceAnalystRecord",
]
