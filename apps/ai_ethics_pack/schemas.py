"""
AI Ethics & Governance Schemas
================================

Typed contracts for the AI Ethics & Governance capability pack.
Defines input (AIEthicsGovernanceRequest) and output (AIEthicsGovernanceReport)
contracts for fairness auditing, bias detection, and compliance.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class AIEthicsOperation(StrEnum):
    fairness_audit = "fairness_audit"
    bias_detection = "bias_detection"
    explainability = "explainability"
    compliance_check = "compliance_check"


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=5, ge=1)
    budget_monthly_usd: float = Field(default=10000, ge=0)


class AIEthicsInputs(BaseModel):
    operation: AIEthicsOperation
    model_name: str = ""
    model_type: str = ""
    dataset_description: str = ""
    protected_attributes: list[str] = Field(default_factory=list)
    prediction_field: str = ""
    label_field: str = ""
    sample_size: int = Field(default=1000, ge=1)
    threshold: float = Field(default=0.8, ge=0, le=1)
    jurisdiction: str = ""
    standard: str = ""


class FairnessMetric(BaseModel):
    metric_name: str
    value: float
    threshold: float = 0.8
    passes: bool = True
    description: str = ""


class BiasFinding(BaseModel):
    attribute: str
    bias_type: str
    severity: str
    impact_score: float
    recommendation: str = ""


class EthicsAssessment(BaseModel):
    principle: str
    status: str
    score: float
    notes: str = ""


class ComplianceMapping(BaseModel):
    regulation: str
    requirement: str
    status: str
    evidence: str = ""


class AIEthicsGovernanceRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: str = "fairness_audit"
    business_context: BusinessContext
    inputs: AIEthicsInputs
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


class AIEthicsGovernanceReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    fairness_metrics: list[FairnessMetric] = Field(default_factory=list)
    bias_findings: list[BiasFinding] = Field(default_factory=list)
    ethics_assessments: list[EthicsAssessment] = Field(default_factory=list)
    compliance_mappings: list[ComplianceMapping] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    quality_score: float = Field(default=0.90, ge=0, le=1)
    model_version: str = "1.0.0"


class AIEthicsRecord(BaseModel):
    pack_id: str = "ai-ethics-governance"
    version: str = "2.5.0"
    capabilities: list[str] = Field(default_factory=lambda: [
        "fairness_auditing",
        "bias_detection",
        "explainability",
        "compliance_check",
    ])


__all__ = [
    "AIEthicsInputs",
    "AIEthicsOperation",
    "AIEthicsGovernanceRequest",
    "AIEthicsGovernanceReport",
    "AIEthicsRecord",
    "BiasFinding",
    "FairnessMetric",
    "EthicsAssessment",
    "ComplianceMapping",
    "BusinessContext",
]
