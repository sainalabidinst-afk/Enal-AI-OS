"""
Cybersecurity Analyst Schemas
=============================

Typed contracts for the Cybersecurity Analyst capability pack.
Defines input (CybersecurityRequest) and output (CybersecurityReport)
contracts for threat modeling, vulnerability assessment, incident
detection, and compliance mapping.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class CybersecurityOperation(StrEnum):
    threat_model = "threat_model"
    vulnerability_assess = "vulnerability_assess"
    incident_detect = "incident_detect"
    compliance_map = "compliance_map"


class ThreatCategory(StrEnum):
    """STRIDE threat modeling categories."""

    spoofing = "spoofing"
    tampering = "tampering"
    repudiation = "repudiation"
    information_disclosure = "information_disclosure"
    denial_of_service = "denial_of_service"
    elevation_of_privilege = "elevation_of_privilege"


class Severity(StrEnum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    info = "info"


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=5, ge=1)


class CybersecurityInputs(BaseModel):
    operation: CybersecurityOperation
    # threat_model inputs
    system_description: str | None = None
    assets: list[str] = Field(default_factory=list)
    trust_boundaries: list[str] = Field(default_factory=list)
    data_flows: list[str] = Field(default_factory=list)
    # vulnerability_assess inputs
    vulnerabilities: list[dict[str, Any]] = Field(default_factory=list)
    # incident_detect inputs
    alerts: list[dict[str, Any]] = Field(default_factory=list)
    baseline_events: list[float] = Field(default_factory=list)
    current_event_count: float | None = None
    anomaly_threshold_pct: float = Field(default=50.0, ge=0, le=100)
    # compliance_map inputs
    framework: str | None = None
    requirements: list[dict[str, Any]] = Field(default_factory=list)
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    # common
    source_id: str | None = None
    checklist_version: str = "v1"


class CybersecurityRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: str = "threat_model"
    business_context: BusinessContext
    inputs: CybersecurityInputs
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


class ThreatFinding(BaseModel):
    id: str
    category: str
    title: str
    description: str
    affected_asset: str
    severity: str
    likelihood: str
    mitigation: str
    cvss_score: float | None = None


class ThreatModel(BaseModel):
    system_description: str
    assets: list[str]
    trust_boundaries: list[str]
    threat_findings: list[ThreatFinding]
    threat_count: int
    formula: str
    inputs_traced: list[str]


class VulnerabilityFinding(BaseModel):
    id: str
    cve: str | None = None
    title: str
    description: str
    severity: str
    cvss_score: float | None = None
    affected_component: str
    remediation: str


class VulnerabilityAssessment(BaseModel):
    vulnerabilities_found: list[VulnerabilityFinding]
    vulnerability_count: int
    severity_counts: dict[str, int] = Field(default_factory=dict)
    score_range: str
    formula: str
    inputs_traced: list[str]


class IncidentFinding(BaseModel):
    id: str
    alert_name: str
    severity: str
    description: str
    detected: bool
    confidence: float


class IncidentDetectionReport(BaseModel):
    alerts_analyzed: list[IncidentFinding]
    anomaly_detected: bool
    baseline_event_count: int
    current_event_count: float | None
    deviation_pct: float | None
    threshold_pct: float | None
    formula: str
    inputs_traced: list[str]


class ComplianceGap(BaseModel):
    requirement_id: str
    requirement_name: str
    status: str
    evidence_available: bool
    gap: str


class ComplianceMapping(BaseModel):
    framework: str
    gaps: list[ComplianceGap]
    total_requirements: int
    covered_requirements: int
    coverage_pct: float
    formula: str
    inputs_traced: list[str]


class CybersecurityReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    operation: CybersecurityOperation
    threat_model: ThreatModel | None = None
    vulnerability_assessment: VulnerabilityAssessment | None = None
    incident_report: IncidentDetectionReport | None = None
    compliance: ComplianceMapping | None = None
    findings: list[dict[str, Any]] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    source_reference_preserved: bool = False
    incident_detection_claim: bool = False
    root_cause_attribution: bool = False
    compliance_certification_claim: bool = False
    model_version: str = "2.4.0"
    quality_score: float = Field(default=0.90, ge=0, le=1)


class CybersecurityAnalystRecord(BaseModel):
    pack_id: str = "cybersecurity-analyst"
    version: str = "2.4.0"
    capabilities: list[str] = Field(default_factory=lambda: [
        "threat_model",
        "vulnerability_assess",
        "incident_detect",
        "compliance_map",
    ])


__all__ = [
    "BusinessContext",
    "ComplianceGap",
    "ComplianceMapping",
    "CybersecurityAnalystRecord",
    "CybersecurityInputs",
    "CybersecurityOperation",
    "CybersecurityReport",
    "CybersecurityRequest",
    "IncidentDetectionReport",
    "IncidentFinding",
    "Severity",
    "ThreatCategory",
    "ThreatFinding",
    "ThreatModel",
    "VulnerabilityAssessment",
    "VulnerabilityFinding",
]
