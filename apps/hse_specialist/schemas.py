"""
HSE Specialist Schemas
======================

Typed contracts for the HSE Specialist capability pack.
Defines input (HSESpecialistRequest) and output (HSESpecialistReport)
contracts for hazard analysis, risk assessment, and incident management.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class HSEOperation(StrEnum):
    hazard_analysis = "hazard_analysis"
    risk_register = "risk_register"
    control_review = "control_review"
    incident_analysis = "incident_analysis"
    compliance_gap_check = "compliance_gap_check"


class RiskLevel(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=20, ge=1)


class HSEInputs(BaseModel):
    operation: HSEOperation
    task: str | None = None
    site_context: str | None = None
    hazard: str | None = None
    urgency: str | None = None
    incident_id: str | None = None
    narrative: str | None = None
    matrix_id: str | None = None
    likelihood: int | None = None
    severity: int | None = None
    scale_min: int = 1
    scale_max: int = 5
    formula: str = "likelihood*severity"
    proposed_controls: list[str] = Field(default_factory=list)
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    jurisdiction: str | None = None
    as_of: str | None = None
    control_system_connected: bool = False
    question: str | None = None


class HSESpecialistRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: str = "hazard_analysis"
    business_context: BusinessContext
    inputs: HSEInputs
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


class HazardFinding(BaseModel):
    hazards_identified: list[str] = Field(default_factory=list)
    task_context_preserved: bool = False
    site_safe_claim: bool = False
    contradiction_flagged: bool = False
    qualified_verification_required: bool = False
    emergency_procedure_escalation: bool = False
    qualified_personnel_escalation: bool = False
    model_only_resolution: bool = False


class RiskScore(BaseModel):
    matrix_id_preserved: bool = False
    risk_score: float | None = None
    formula_disclosed: bool = True
    missing_value_reported: bool = False
    silent_default: bool = False


class ControlReviewResult(BaseModel):
    controls_classified: bool = True
    hierarchy_order_applied: bool = True
    assumptions_disclosed: bool = False
    control_command_issued: bool = False
    authorization_required: bool = True
    safety_case_required: bool = False


class IncidentAnalysis(BaseModel):
    incident_id_preserved: bool = False
    timeline_present: bool = False
    system_factors_considered: bool = True
    unsupported_blame: bool = False


class HSESpecialistReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    operation: HSEOperation
    hazard_finding: HazardFinding | None = None
    risk_score: RiskScore | None = None
    control_review: ControlReviewResult | None = None
    incident_analysis: IncidentAnalysis | None = None
    evidence_id_preserved: bool = False
    gap_reported: bool = False
    certification_claim: bool = False
    jurisdiction_preserved: bool = False
    as_of_preserved: bool = False
    evidence_reference_preserved: bool = False
    recommendations: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    quality_score: float = Field(default=0.90, ge=0, le=1)
    model_version: str = "1.0.0"


class HSESpecialistRecord(BaseModel):
    pack_id: str = "hse-specialist"
    version: str = "1.0.0"
    capabilities: list[str] = Field(default_factory=lambda: [
        "hazard_analysis",
        "risk_register",
        "control_review",
        "incident_analysis",
        "compliance_gap_check",
    ])


__all__ = [
    "BusinessContext",
    "ControlReviewResult",
    "HSEInputs",
    "HSEOperation",
    "HazardsFinding",
    "HazardFinding",
    "HSESpecialistRecord",
    "HSESpecialistReport",
    "HSESpecialistRequest",
    "IncidentAnalysis",
    "RiskLevel",
    "RiskScore",
]
