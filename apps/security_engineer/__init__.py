"""
Security Engineer — security analysis layer for ECP.

Provides OWASP Top 10 analysis, threat modeling, secret detection,
vulnerability analysis, dependency audit, configuration hardening,
and compliance mapping — without modifying Core.

Pipeline:
    SecurityAssessmentRequest
        ↓
    OWASP Analyzer (injection, XSS, broken auth, etc.)
        ↓
    Secret Detector (hardcoded credentials, API keys)
        ↓
    Dependency Auditor (CVE correlation, license check)
        ↓
    Threat Modeler (STRIDE analysis)
        ↓
    Vulnerability Scanner (known patterns)
        ↓
    Hardening Reviewer (CIS benchmarks)
        ↓
    Compliance Mapper (SOC 2, ISO 27001, HIPAA, PCI-DSS)
        ↓
    SecurityAssessmentReport
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.security_engineer.engine import SecurityEngineerEngine
from apps.security_engineer.worker import SecurityEngineerWorker
from apps.security_engineer.schemas import (
    SecurityAssessmentRequest,
    SecurityAssessmentReport,
    AssessmentType,
    Severity,
    EvidenceType,
    ThreatCategory,
    ComplianceStandard,
    SecretType,
    DependencySeverity,
    Finding,
    SecretFinding,
    DependencyFinding,
    ThreatModelEntry,
    ThreatModelResult,
    ComplianceReport,
    SecuritySummary,
    SecurityAnalysisRecord,
    AssessmentOutcome,
)


class SecurityEngineerApp(BaseReferenceApp):
    name = "security-engineer"
    version = "1.0.0"
    description = "Security analysis, hardening, and compliance assessment"
    category = "security"
    pipeline = ["perception", "analysis", "reasoning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = SecurityEngineerWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return await self.worker.execute(task)


def get_app() -> SecurityEngineerApp:
    return SecurityEngineerApp()

__all__ = [
    "SecurityEngineerApp",
    "get_app",
    "SecurityEngineerEngine",
    "SecurityEngineerWorker",
    "SecurityAssessmentRequest",
    "SecurityAssessmentReport",
    "AssessmentType",
    "Severity",
    "EvidenceType",
    "ThreatCategory",
    "ComplianceStandard",
    "SecretType",
    "DependencySeverity",
    "Finding",
    "SecretFinding",
    "DependencyFinding",
    "ThreatModelEntry",
    "ThreatModelResult",
    "ComplianceReport",
    "SecuritySummary",
    "SecurityAnalysisRecord",
    "AssessmentOutcome",
]
