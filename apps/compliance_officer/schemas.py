"""
Compliance Officer Schemas
==========================

Typed contracts for the Compliance Officer capability pack.
Defines input (ComplianceOfficerRequest) and output (ComplianceOfficerReport)
contracts for compliance assessment, audit evidence, and risk management.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class ComplianceFramework(StrEnum):
    iso27001 = "iso27001"
    nist = "nist"
    pci_dss = "pci_dss"
    gdpr = "gdpr"
    soc2 = "soc2"


class ComplianceOperation(StrEnum):
    compliance_assessment = "compliance_assessment"
    audit_planning = "audit_planning"
    risk_assessment = "risk_assessment"
    remediation_plan = "remediation_plan"


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=20, ge=1)


class ComplianceConfig(BaseModel):
    operation: ComplianceOperation
    frameworks: list[ComplianceFramework] = Field(default_factory=list)
    scope: list[str] = Field(default_factory=list)
    environment: str = "production"


class ComplianceOfficerRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: str = "compliance_assessment"
    business_context: BusinessContext
    inputs: ComplianceConfig
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


class ControlRequirement(BaseModel):
    id: str
    name: str
    framework: ComplianceFramework
    description: str
    severity: str
    status: str
    evidence_needed: list[str] = Field(default_factory=list)


class AuditEvidence(BaseModel):
    control_id: str
    evidence_type: str
    collected: bool
    description: str


class RiskItem(BaseModel):
    id: str
    description: str
    likelihood: float
    impact: float
    overall_risk: float
    mitigation: str


class ComplianceOfficerReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    operation: ComplianceOperation
    frameworks: list[ComplianceFramework]
    requirements: list[ControlRequirement] = Field(default_factory=list)
    audit_evidence: list[AuditEvidence] = Field(default_factory=list)
    risks: list[RiskItem] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    compliance_score: float = Field(default=0.0, ge=0, le=1)
    model_version: str = "1.0.0"


class ComplianceOfficerRecord(BaseModel):
    pack_id: str = "compliance-officer"
    version: str = "1.0.0"
    capabilities: list[str] = Field(
        default_factory=lambda: [
            "compliance_assessment",
            "audit_planning",
            "risk_assessment",
            "remediation_plan",
        ]
    )


__all__ = [
    "AuditEvidence",
    "BusinessContext",
    "ComplianceConfig",
    "ComplianceFramework",
    "ComplianceOfficerRecord",
    "ComplianceOfficerReport",
    "ComplianceOfficerRequest",
    "ControlRequirement",
    "RiskItem",
    "ComplianceOperation",
]
