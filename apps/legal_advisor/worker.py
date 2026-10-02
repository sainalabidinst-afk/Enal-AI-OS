"""
Legal Advisor Worker.
"""

from __future__ import annotations

import json
from typing import Any

from apps.legal_advisor.engine import LegalAdvisorEngine
from apps.legal_advisor.schemas import LegalAdvisorRequest


class LegalAdvisorWorker:
    """Thin adapter that exposes the Legal Advisor engine to agents."""

    def __init__(self) -> None:
        self.engine = LegalAdvisorEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = LegalAdvisorRequest(**task)
        report = self.engine.execute(request)
        return json.loads(report.model_dump_json())


__all__ = ["LegalAdvisorWorker"]
