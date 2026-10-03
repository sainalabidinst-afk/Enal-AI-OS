"""
Finance Analyst Schemas
=======================

Typed contracts for the Finance Analyst capability pack.
Defines input (FinanceAnalystRequest) and output (FinanceAnalystReport)
contracts for financial analysis, scenario modeling, and control checks.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class FinanceOperation(StrEnum):
    financial_summary = "financial_summary"
    cash_flow = "cash_flow"
    scenario_analysis = "scenario_analysis"
    risk_model = "risk_model"
    control_check = "control_check"


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=5, ge=1)


class FinanceInputs(BaseModel):
    operation: FinanceOperation
    currency: str = "USD"
    period: str = "FY2025"
    revenue: float | None = None
    cost_of_goods_sold: float | None = None
    current_assets: float | None = None
    current_liabilities: float | None = None
    cash_balance: float | None = None
    monthly_net_burn: float | None = None
    baseline_revenue: float | None = None
    margin: float | None = None
    revenue_changes_pct: list[float] = Field(default_factory=list)
    baseline_cost: float | None = None
    downside_cost_increase_pct: float | None = None
    stress_pct: float | None = None
    source_id: str | None = None
    checklist_version: str = "v1"
    evidence: list[dict[str, str]] = Field(default_factory=list)


class FinanceAnalystRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: str = "financial_summary"
    business_context: BusinessContext
    inputs: FinanceInputs
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


class FinancialMetric(BaseModel):
    name: str
    value: float | None
    formula: str
    inputs_traced: list[str] = Field(default_factory=list)
    notes: str = ""


class SensitivityScenario(BaseModel):
    change_pct: float
    result: float | None
    labelled: bool = False


class RiskScenario(BaseModel):
    name: str
    baseline: float
    downside: float
    change_pct: float
    assumption_label: str


class EvidenceCheckResult(BaseModel):
    control_id: str
    status: str
    evidence_available: bool
    unsupported: bool = False


class FinanceAnalystReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    operation: FinanceOperation
    currency: str = "USD"
    period: str = ""
    metrics: list[FinancialMetric] = Field(default_factory=list)
    scenarios: list[SensitivityScenario] = Field(default_factory=list)
    risk_scenarios: list[RiskScenario] = Field(default_factory=list)
    evidence_check: list[EvidenceCheckResult] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    compliance_claim: bool = False
    investment_advice: bool = False
    quality_score: float = Field(default=0.90, ge=0, le=1)
    model_version: str = "1.0.0"


class FinanceAnalystRecord(BaseModel):
    pack_id: str = "finance-analyst"
    version: str = "1.0.0"
    capabilities: list[str] = Field(
        default_factory=lambda: [
            "financial_summary",
            "cash_flow",
            "scenario_analysis",
            "risk_model",
            "control_check",
        ]
    )


__all__ = [
    "BusinessContext",
    "EvidenceCheckResult",
    "FinanceAnalystRecord",
    "FinanceAnalystReport",
    "FinanceAnalystRequest",
    "FinanceInputs",
    "FinanceOperation",
    "FinancialMetric",
    "RiskScenario",
    "SensitivityScenario",
]
