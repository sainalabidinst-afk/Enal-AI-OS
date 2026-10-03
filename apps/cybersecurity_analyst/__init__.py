"""
Cybersecurity Analyst — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.cybersecurity_analyst.engine import CybersecurityAnalystEngine
from apps.cybersecurity_analyst.schemas import (
    BusinessContext,
    ComplianceGap,
    ComplianceMapping,
    CybersecurityAnalystRecord,
    CybersecurityInputs,
    CybersecurityOperation,
    CybersecurityReport,
    CybersecurityRequest,
    IncidentDetectionReport,
    IncidentFinding,
    Severity,
    ThreatCategory,
    ThreatFinding,
    ThreatModel,
    VulnerabilityAssessment,
    VulnerabilityFinding,
)
from apps.cybersecurity_analyst.worker import CybersecurityAnalystWorker


class CybersecurityAnalystApp(BaseReferenceApp):
    name = "cybersecurity-analyst"
    version = "2.4.0"
    description = "Threat modeling (STRIDE), vulnerability assessment, incident detection, and compliance mapping"  # noqa: E501
    category = "security"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = CybersecurityAnalystWorker()

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> CybersecurityAnalystApp:
    return CybersecurityAnalystApp()


__all__ = [
    "CybersecurityAnalystApp",
    "get_app",
    "CybersecurityAnalystEngine",
    "CybersecurityAnalystWorker",
    "CybersecurityRequest",
    "CybersecurityReport",
    "CybersecurityInputs",
    "CybersecurityOperation",
    "BusinessContext",
    "ThreatModel",
    "ThreatFinding",
    "ThreatCategory",
    "VulnerabilityAssessment",
    "VulnerabilityFinding",
    "Severity",
    "IncidentDetectionReport",
    "IncidentFinding",
    "ComplianceMapping",
    "ComplianceGap",
    "CybersecurityAnalystRecord",
]
