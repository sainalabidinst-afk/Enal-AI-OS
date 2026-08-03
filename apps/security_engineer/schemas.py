"""
Security Engineer — Public Contracts (Pydantic schemas).

Defines the input (SecurityAssessmentRequest) and output (SecurityAssessmentReport)
contracts for the Security Engineer Capability Pack, plus all supporting types.

These schemas follow the RFC-0008 contract definitions exactly.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AssessmentType(str, Enum):
    code = "code"
    config = "config"
    dependency = "dependency"
    architecture = "architecture"
    full_review = "full_review"


class Severity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class EvidenceType(str, Enum):
    static_analysis = "static_analysis"
    dependency_scan = "dependency_scan"
    config_review = "config_review"
    threat_model = "threat_model"
    manual = "manual"


class ThreatCategory(str, Enum):
    spoofing = "spoofing"
    tampering = "tampering"
    repudiation = "repudiation"
    info_disclosure = "info_disclosure"
    denial_service = "denial_service"
    elevation_privilege = "elevation_privilege"


class ComplianceStandard(str, Enum):
    soc2 = "soc2"
    iso27001 = "iso27001"
    hipaa = "hipaa"
    pci_dss = "pci_dss"
    nist_csf = "nist_csf"
    owasp_top10 = "owasp_top10"
    cis = "cis"


class SecretType(str, Enum):
    api_key = "api_key"
    password = "password"
    token = "token"
    certificate = "certificate"
    private_key = "private_key"
    other = "other"


class DependencySeverity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class AssessmentOutcome(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    revised = "revised"


class EvidenceSource(BaseModel):
    source_id: str = Field(..., description="Capability ID or external source identifier")
    evidence_type: EvidenceType = Field(..., description="Type of evidence")
    payload: dict[str, Any] = Field(default_factory=dict, description="Structured evidence payload")
    quality_score: float = Field(default=0.5, ge=0.0, le=1.0)
    weight: float = Field(default=1.0, ge=0.0, le=10.0)


class Finding(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    category: str = Field(..., description="OWASP category, STRIDE threat, or CIS benchmark")
    severity: Severity = Field(default=Severity.medium)
    title: str = Field(..., description="Short finding title")
    description: str = Field(..., description="Detailed description")
    evidence: dict[str, Any] = Field(default_factory=dict, description="File, line, code snippet")
    remediation: str = Field(default="", description="Fix guidance")
    owasp_mapping: str | None = Field(default=None, description="OWASP Top 10 category")
    compliance_mapping: list[str] = Field(default_factory=list, description="Compliance frameworks")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class SecretFinding(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: SecretType = Field(..., description="Type of secret")
    location: str = Field(..., description="File path or config section")
    severity: Severity = Field(default=Severity.high)
    remediation: str = Field(default="", description="Rotation guidance")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    evidence: dict[str, Any] = Field(default_factory=dict, description="Supporting evidence for the finding")


class DependencyFinding(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    package: str = Field(..., description="Package name")
    version: str = Field(default="", description="Installed version")
    severity: DependencySeverity = Field(default=DependencySeverity.medium)
    cve: str = Field(default="", description="CVE identifier")
    description: str = Field(default="")
    fix_version: str = Field(default="", description="Recommended upgrade version")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class ThreatModelEntry(BaseModel):
    threat_type: ThreatCategory = Field(..., description="STRIDE threat type")
    component: str = Field(..., description="Affected component or data flow")
    description: str = Field(..., description="Threat description")
    likelihood: float = Field(default=0.0, ge=0.0, le=1.0)
    impact: float = Field(default=0.0, ge=0.0, le=1.0)
    mitigation: str = Field(default="", description="Recommended mitigation")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class ThreatModelResult(BaseModel):
    attack_surface: str = Field(default="", description="Description of exposed surfaces")
    trust_boundaries: list[str] = Field(default_factory=list)
    data_flows: list[str] = Field(default_factory=list)
    threats: list[ThreatModelEntry] = Field(default_factory=list)
    risk_rating: Severity = Field(default=Severity.low)


class ComplianceReport(BaseModel):
    standards: list[str] = Field(default_factory=list)
    mapped_findings: int = Field(default=0)
    compliance_percentage: dict[str, float] = Field(default_factory=dict)
    gaps: list[str] = Field(default_factory=list)


class SecuritySummary(BaseModel):
    total_findings: int = Field(default=0)
    critical_count: int = Field(default=0)
    high_count: int = Field(default=0)
    medium_count: int = Field(default=0)
    low_count: int = Field(default=0)
    overall_risk: Severity = Field(default=Severity.low)
    compliance_score: float = Field(default=0.0, ge=0.0, le=1.0)
    recommendations_count: int = Field(default=0)


class SecurityAssessmentRequest(BaseModel):
    """Input contract for a security assessment request."""

    assessment_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    target_type: AssessmentType = Field(..., description="Type of artifact to assess")
    target: dict[str, Any] = Field(default_factory=dict, description="Source code, config files, dependencies")
    standards: list[str] = Field(default_factory=lambda: ["owasp_top10", "cis"], description="Security standards to check against")
    include_remediation: bool = Field(default=True)
    include_compliance_mapping: bool = Field(default=True)
    check_secrets: bool = Field(default=True)
    check_dependencies: bool = Field(default=True)
    scan_depth: str = Field(default="thorough", description="quick|thorough")


class SecurityAssessmentReport(BaseModel):
    """Output contract for a security assessment report."""

    assessment_id: str = Field(..., description="Reference to the original request")
    target_type: str = Field(..., description="Type of artifact assessed")
    findings: list[Finding] = Field(default_factory=list)
    secrets: list[SecretFinding] = Field(default_factory=list)
    dependency_findings: list[DependencyFinding] = Field(default_factory=list)
    threat_model: ThreatModelResult = Field(default_factory=ThreatModelResult)
    summary: SecuritySummary = Field(default_factory=SecuritySummary)
    compliance_report: ComplianceReport = Field(default_factory=ComplianceReport)
    raw: dict[str, Any] = Field(default_factory=dict, description="Raw diagnostic data")

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()


class SecurityAnalysisRecord(BaseModel):
    """Persistent record for Experience Memory."""

    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    assessment_id: str = Field(..., description="Reference to SecurityAssessmentRequest")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    target_type: str = Field(default="")
    total_findings: int = Field(default=0)
    critical_count: int = Field(default=0)
    high_count: int = Field(default=0)
    resolved: list[dict[str, Any]] = Field(default_factory=list)
    false_positives: list[dict[str, Any]] = Field(default_factory=list)
    fp_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    detection_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    outcome: AssessmentOutcome = Field(default=AssessmentOutcome.pending)
