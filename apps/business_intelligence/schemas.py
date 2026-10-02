"""
Business Intelligence Schemas
===============================

Typed contracts for the Business Intelligence capability pack.
Defines input/output contracts for KPI tracking, dashboarding, and scenario planning.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class BusinessIntelligenceOperation(StrEnum):
    kpi_tracking = "kpi_tracking"
    dashboard_generation = "dashboard_generation"
    scenario_planning = "scenario_planning"
    metric_analysis = "metric_analysis"


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=5, ge=1)
    budget_monthly_usd: float = Field(default=10000, ge=0)


class BusinessIntelligenceInputs(BaseModel):
    operation: BusinessIntelligenceOperation
    metrics: list[str] = Field(default_factory=list)
    target_values: dict[str, float] = Field(default_factory=dict)
    current_values: dict[str, float] = Field(default_factory=dict)
    historical_data: list[float] = Field(default_factory=list)
    departments: list[str] = Field(default_factory=list)
    timeframe: str = "monthly"
    scenario_name: str = ""
    variables: list[str] = Field(default_factory=list)


class KpiMetric(BaseModel):
    metric_name: str
    current_value: float
    target_value: float
    variance_pct: float
    status: str
    trend: str = "stable"
    department: str = ""


class DashboardConfig(BaseModel):
    dashboard_name: str
    widgets: list[str] = Field(default_factory=list)
    layout: str = "grid"
    refresh_interval_seconds: int = 300
    data_sources: list[str] = Field(default_factory=list)


class ScenarioAnalysis(BaseModel):
    scenario_name: str
    variable_name: str
    change_pct: float
    projected_outcome: float
    confidence: float
    assumptions: list[str] = Field(default_factory=list)


class BusinessIntelligenceReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    kpis: list[KpiMetric] = Field(default_factory=list)
    dashboard_configs: list[DashboardConfig] = Field(default_factory=list)
    scenarios: list[ScenarioAnalysis] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    quality_score: float = Field(default=0.90, ge=0, le=1)
    model_version: str = "1.0.0"


class BusinessIntelligenceRecord(BaseModel):
    pack_id: str = "business-intelligence"
    version: str = "2.8.0"
    capabilities: list[str] = Field(default_factory=lambda: [
        "kpi_tracking",
        "dashboard_generation",
        "scenario_planning",
        "metric_analysis",
    ])


class BusinessIntelligenceRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    business_context: BusinessContext
    inputs: BusinessIntelligenceInputs
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


__all__ = [
    "BusinessIntelligenceInputs",
    "BusinessIntelligenceOperation",
    "BusinessIntelligenceRequest",
    "BusinessIntelligenceReport",
    "BusinessIntelligenceRecord",
    "KpiMetric",
    "DashboardConfig",
    "ScenarioAnalysis",
    "BusinessContext",
]
