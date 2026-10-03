"""
Compliance Officer — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.compliance_officer.engine import ComplianceOfficerEngine
from apps.compliance_officer.schemas import (
    AuditEvidence,
    BusinessContext,
    ComplianceConfig,
    ComplianceFramework,
    ComplianceOfficerRecord,
    ComplianceOfficerReport,
    ComplianceOfficerRequest,
    ComplianceOperation,
    ControlRequirement,
    RiskItem,
)
from apps.compliance_officer.worker import ComplianceOfficerWorker


class ComplianceOfficerApp(BaseReferenceApp):
    name = "compliance-officer"
    version = "1.0.0"
    description = "Compliance assessment, audit planning, risk management across ISO 27001, NIST, PCI-DSS, GDPR, SOC2"  # noqa: E501
    category = "security"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = ComplianceOfficerWorker()

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> ComplianceOfficerApp:
    return ComplianceOfficerApp()


__all__ = [
    "ComplianceOfficerApp",
    "get_app",
    "ComplianceOfficerEngine",
    "ComplianceOfficerWorker",
    "ComplianceOfficerRequest",
    "ComplianceOfficerReport",
    "ComplianceFramework",
    "ComplianceOperation",
    "ControlRequirement",
    "AuditEvidence",
    "RiskItem",
    "ComplianceConfig",
    "BusinessContext",
    "ComplianceOfficerRecord",
]
