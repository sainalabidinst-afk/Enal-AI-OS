"""
Business Intelligence Capability Schemas
==========================================

Typed contracts for the Business Intelligence capability pack.
Defines input (BIRequest) and output (BIReport) contracts for dashboard
generation, KPI tracking, metric analysis, and business insights.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class BIReportType(StrEnum):
    dashboard = "dashboard"
    kpi_report = "kpi_report"
    metric_analysis = "metric_analysis"
    drill_down = "drill_down"


class VisualizationType(StrEnum):
    line_chart = "line_chart"
    bar_chart = "bar_chart"
    pie_chart = "pie_chart"
    area_chart = "area_chart"
    table = "table"
    heatmap = "heatmap"
    kpi_card = "kpi_card"


class MetricType(StrEnum):
    revenue = "revenue"
    growth_rate = "growth_rate"
    conversion_rate = "conversion_rate"
    customer_acquisition_cost = "customer_acquisition_cost"
    lifetime_value = "lifetime_value"
    churn_rate = "churn_rate"
    engagement_score = "engagement_score"
    operational_efficiency = "operational_efficiency"


class KpiStatus(StrEnum):
    on_track = "on_track"
    at_risk = "at_risk"
    off_track = "off_track"
    target_met = "target_met"
    target_missed = "target_missed"


class DataPoint(BaseModel):
    timestamp: str
    value: float
    dimension: dict[str, Any] = Field(default_factory=dict)


class MetricDefinition(BaseModel):
    id: str
    name: str
    type: MetricType
    description: str
    target: float = 0.0
    unit: str = "count"
    aggregation: str = "sum"


class KpiTarget(BaseModel):
    metric_id: str
    target_value: float
    current_value: float
    threshold_warning: float = 0.0
    threshold_critical: float = 0.0


class DashboardWidget(BaseModel):
    id: str
    title: str
    visualization_type: VisualizationType
    metric_ids: list[str] = Field(default_factory=list)
    query: str = ""
    width: int = 4
    height: int = 3


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=10, ge=1)


class BIConfig(BaseModel):
    report_type: BIReportType
    metrics: list[MetricDefinition] = Field(default_factory=list)
    kpi_targets: list[KpiTarget] = Field(default_factory=list)
    widgets: list[DashboardWidget] = Field(default_factory=list)
    historical_data: dict[str, list[DataPoint]] = Field(default_factory=dict)
    filters: dict[str, Any] = Field(default_factory=dict)
    time_range: str = "last_30_days"


class BIRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    report_type: str = "dashboard"
    business_context: BusinessContext
    inputs: BIConfig
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


class MetricAnalysis(BaseModel):
    metric_id: str
    metric_name: str
    current_value: float
    target_value: float
    variance: float
    trend: str
    status: KpiStatus
    insights: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class KpiTracking(BaseModel):
    metric_id: str
    metric_name: str
    target_value: float
    current_value: float
    percentage_to_target: float
    status: KpiStatus
    last_updated: str
    trajectory: str


class DashboardSpec(BaseModel):
    dashboard_id: str
    title: str
    widgets: list[DashboardWidget]
    layout: str = "grid"
    refresh_interval_seconds: int = 300


class TrendAnalysis(BaseModel):
    metric_id: str
    direction: str
    magnitude: float
    significance: float
    forecast_next_period: float
    confidence_interval: tuple[float, float] = Field(default=(0.0, 0.0))


class BIReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    report_type: BIReportType
    dashboards: list[DashboardSpec] = Field(default_factory=list)
    kpi_tracking: list[KpiTracking] = Field(default_factory=list)
    metric_analyses: list[MetricAnalysis] = Field(default_factory=list)
    trend_analyses: list[TrendAnalysis] = Field(default_factory=list)
    overall_health: str = "unknown"
    summary: str = ""
    model_version: str = "1.0.0"


class BusinessIntelligencePackRecord(BaseModel):
    pack_id: str = "business-intelligence"
    version: str = "1.0.0"
    capabilities: list[str] = Field(default_factory=lambda: [
        "dashboard_generation",
        "kpi_tracking",
        "metric_analysis",
        "trend_analysis",
    ])


__all__ = [
    "BIConfig",
    "BIReport",
    "BIRequest",
    "BIReportType",
    "BusinessContext",
    "BusinessIntelligencePackRecord",
    "DashboardSpec",
    "DashboardWidget",
    "DataPoint",
    "KpiStatus",
    "KpiTarget",
    "KpiTracking",
    "MetricAnalysis",
    "MetricDefinition",
    "MetricType",
    "TrendAnalysis",
    "VisualizationType",
]
