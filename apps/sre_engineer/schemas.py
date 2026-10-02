"""
SRE Engineer Schemas
====================

Typed contracts for the SRE Engineer capability pack.
Defines input (SREEngineerRequest) and output (SREEngineerReport)
contracts for site reliability engineering, observability, and incident management.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class SREOperation(StrEnum):
    observability_setup = "observability_setup"
    slo_design = "slo_design"
    incident_response = "incident_response"
    capacity_planning = "capacity_planning"


class MonitoringStack(StrEnum):
    prometheus = "prometheus"
    grafana = "grafana"
    opentelemetry = "opentelemetry"
    datadog = "datadog"
    newrelic = "newrelic"


class ServiceLevelIndicator(StrEnum):
    latency = "latency"
    availability = "availability"
    error_rate = "error_rate"
    throughput = "throughput"


class IncidentSeverity(StrEnum):
    sev1 = "sev1"
    sev2 = "sev2"
    sev3 = "sev3"


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=10, ge=1)


class SREConfig(BaseModel):
    operation: SREOperation
    monitoring_stack: list[MonitoringStack] = Field(default_factory=list)
    slis: list[ServiceLevelIndicator] = Field(default_factory=list)
    services: list[str] = Field(default_factory=list)
    environment: str = "production"


class SREEngineerRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: str = "observability_setup"
    business_context: BusinessContext
    inputs: SREConfig
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


class SLOSpec(BaseModel):
    service: str
    indicator: str
    target: float
    window: str
    alert_threshold: float


class DashboardSpec(BaseModel):
    name: str
    metrics: list[str]
    panels: int = Field(default=1, ge=1)


class RunbookSpec(BaseModel):
    incident_type: str
    severity: IncidentSeverity
    steps: list[str] = Field(default_factory=list)
    runbook_url: str = ""


class SREEngineerReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    operation: SREOperation
    slos: list[SLOSpec] = Field(default_factory=list)
    dashboards: list[DashboardSpec] = Field(default_factory=list)
    runbooks: list[RunbookSpec] = Field(default_factory=list)
    alerts: list[dict[str, Any]] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    capacity_plan: dict[str, Any] = Field(default_factory=dict)
    quality_score: float = Field(default=0.90, ge=0, le=1)
    model_version: str = "1.0.0"


class SREEngineerRecord(BaseModel):
    pack_id: str = "sre-engineer"
    version: str = "1.0.0"
    capabilities: list[str] = Field(default_factory=lambda: [
        "observability_setup",
        "slo_design",
        "incident_response",
        "capacity_planning",
    ])


__all__ = [
    "BusinessContext",
    "DashboardSpec",
    "IncidentSeverity",
    "MonitoringStack",
    "RunbookSpec",
    "SREConfig",
    "SREEngineerRecord",
    "SREEngineerReport",
    "SREEngineerRequest",
    "SREOperation",
    "SLOSpec",
    "ServiceLevelIndicator",
]
