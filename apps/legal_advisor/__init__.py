"""
Legal Advisor — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.legal_advisor.engine import LegalAdvisorEngine
from apps.legal_advisor.schemas import (
    BusinessContext,
    ClauseDeviation,
    ClauseExtraction,
    LegalAdvisorRecord,
    LegalAdvisorReport,
    LegalAdvisorRequest,
    LegalInputs,
    LegalOperation,
    ObligationRecord,
    SourceSummary,
)
from apps.legal_advisor.worker import LegalAdvisorWorker


class LegalAdvisorApp(BaseReferenceApp):
    name = "legal-advisor"
    version = "1.0.0"
    description = (
        "Legal document analysis, clause comparison, obligation tracking, and source grounding"  # noqa: E501
    )
    category = "legal"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = LegalAdvisorWorker()

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> LegalAdvisorApp:
    return LegalAdvisorApp()


__all__ = [
    "LegalAdvisorApp",
    "get_app",
    "LegalAdvisorEngine",
    "LegalAdvisorWorker",
    "LegalAdvisorRequest",
    "LegalAdvisorReport",
    "LegalOperation",
    "LegalInputs",
    "ClauseExtraction",
    "ClauseDeviation",
    "ObligationRecord",
    "SourceSummary",
    "BusinessContext",
    "LegalAdvisorRecord",
]
