"""
AI Ethics & Governance Capability Schemas
============================================

Typed contracts for the AI Ethics & Governance capability pack.
Defines input (EthicsRequest) and output (EthicsReport) contracts for bias
detection, fairness auditing, and AI governance assessment.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class EthicsFramework(StrEnum):
    fairness = "fairness"
    accountability = "accountability"
    transparency = "transparency"
    privacy = "privacy"
    safety = "safety"
    sustainability = "sustainability"


class EthicsOperation(StrEnum):
    bias_detection = "bias_detection"
    fairness_audit = "fairness_audit"
    explanation_review = "explanation_review"
    impact_assessment = "impact_assessment"


class BiasMetric(StrEnum):
    demographic_parity = "demographic_parity"
    equalized_odds = "equalized_odds"
    statistical_parity = "statistical_parity"
    disparate_impact = "disparate_impact"
    calibration = "calibration"
    equal_opportunity = "equal_opportunity"


class Severity(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class ProtectedAttribute(BaseModel):
    name: str
    groups: list[str] = Field(default_factory=list)


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    ml_use_case: str = "general"
    team_size: int = Field(default=10, ge=1)
    protected_attributes: list[ProtectedAttribute] = Field(default_factory=list)


class EthicsConfig(BaseModel):
    operation: EthicsOperation
    frameworks: list[EthicsFramework] = Field(default_factory=list)
    bias_metrics: list[BiasMetric] = Field(default_factory=list)
    audit_targets: list[str] = Field(default_factory=list)
    risk_domains: list[str] = Field(default_factory=list)


class EthicsRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: str = "bias_detection"
    business_context: BusinessContext
    inputs: EthicsConfig
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


class BiasFinding(BaseModel):
    id: str
    metric: BiasMetric
    finding: str
    severity: Severity
    affected_groups: list[str] = Field(default_factory=list)
    recommendation: str
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class EthicsRisk(BaseModel):
    id: str
    description: str
    likelihood: float
    impact: float
    overall_risk: float
    mitigation: str


class FairnessViolation(BaseModel):
    metric: BiasMetric
    threshold: float
    observed_value: float
    delta: float
    status: str


class EthicsReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    operation: EthicsOperation
    frameworks: list[EthicsFramework]
    fairness_violations: list[FairnessViolation] = Field(default_factory=list)
    bias_findings: list[BiasFinding] = Field(default_factory=list)
    risks: list[EthicsRisk] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    fairness_score: float = Field(default=0.0, ge=0.0, le=1.0)
    model_version: str = "1.0.0"


class EthicsPackRecord(BaseModel):
    pack_id: str = "ai-ethics-governance"
    version: str = "1.0.0"
    capabilities: list[str] = Field(default_factory=lambda: [
        "bias_detection",
        "fairness_audit",
        "explanation_review",
        "impact_assessment",
    ])


__all__ = [
    "BiasFinding",
    "BiasMetric",
    "BusinessContext",
    "EthicsConfig",
    "EthicsFramework",
    "EthicsOperation",
    "EthicsPackRecord",
    "EthicsReport",
    "EthicsRequest",
    "EthicsRisk",
    "FairnessViolation",
    "ProtectedAttribute",
    "Severity",
]
