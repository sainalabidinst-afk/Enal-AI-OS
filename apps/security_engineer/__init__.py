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

__all__ = [
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
