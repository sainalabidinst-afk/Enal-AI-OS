"""
Compliance Officer Worker.
"""

from __future__ import annotations

import json
from typing import Any

from apps.compliance_officer.engine import ComplianceOfficerEngine
from apps.compliance_officer.schemas import ComplianceOfficerRequest


class ComplianceOfficerWorker:
    """Thin adapter that exposes the Compliance Officer engine to agents."""

    def __init__(self) -> None:
        self.engine = ComplianceOfficerEngine()

    def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        request = ComplianceOfficerRequest(**task)
        report = self.engine.execute(request)
        return json.loads(report.model_dump_json())


__all__ = ["ComplianceOfficerWorker"]
