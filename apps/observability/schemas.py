"""
Observability Capability Pack — Schemas
========================================

Typed contracts for the Observability capability pack.
Defines input (ObservabilityAnalystRequest) and output (ObservabilityReport)
contracts for metrics collection, distributed tracing, log analysis, and
anomaly detection.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class ObservabilityOperation(StrEnum):
    metrics_collect = "metrics_collect"
    trace_analyze = "trace_analyze"
    log_analyze = "log_analyze"
    anomaly_detect = "anomaly_detect"


class MetricType(StrEnum):
    gauge = "gauge"
    counter = "counter"
    histogram = "histogram"


class LogSeverity(StrEnum):
    critical = "critical"
    error = "error"
    warning = "warning"
    info = "info"
    debug = "debug"


class ThresholdDirection(StrEnum):
    above = "above"
    below = "below"


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=5, ge=1)


class MetricSample(BaseModel):
    name: str
    value: float
    unit: str = ""
    timestamp: str = ""


class TraceSpan(BaseModel):
    trace_id: str
    span_id: str
    service: str
    operation: str
    duration_ms: float
    status: str = "ok"


class LogEntry(BaseModel):
    timestamp: str
    level: str
    message: str
    service: str = ""
    trace_id: str | None = None


class ObservabilityInputs(BaseModel):
    operation: ObservabilityOperation
    # metrics_collect
    metric_name: str | None = None
    metric_type: str | None = None
    time_window: str | None = None
    aggregation: str | None = None
    threshold: float | None = None
    threshold_direction: str | None = None
    current_value: float | None = None
    historical_values: list[float] = Field(default_factory=list)
    metric_samples: list[MetricSample] = Field(default_factory=list)
    # trace_analyze
    service_name: str | None = None
    trace_id: str | None = None
    duration_ms: float | None = None
    span_count: int | None = None
    error_rate: float | None = None
    p95_latency_ms: float | None = None
    spans: list[TraceSpan] = Field(default_factory=list)
    # log_analyze
    log_level: str | None = None
    log_message: str | None = None
    log_source: str | None = None
    pattern: str | None = None
    log_entries: list[LogEntry] = Field(default_factory=list)
    # anomaly_detect
    data_points: list[float] = Field(default_factory=list)
    baseline: float | None = None
    window_size: int | None = None
    # common
    source_id: str | None = None
    checklist_version: str = "v1"
    evidence: list[dict[str, Any]] = Field(default_factory=list)


class ObservabilityAnalystRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: str = "metrics_collect"
    business_context: BusinessContext
    inputs: ObservabilityInputs
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


class MetricSummary(BaseModel):
    metric_name: str
    current_value: float | None
    average: float | None
    maximum: float | None
    minimum: float | None
    threshold: float | None
    threshold_direction: str | None
    breached: bool = False
    unit: str = ""
    formula: str = ""
    inputs_traced: list[str] = Field(default_factory=list)


class TraceSummary(BaseModel):
    service_name: str
    trace_id: str | None
    total_duration_ms: float | None
    span_count: int | None
    error_rate: float | None
    healthy: bool = True
    p95_latency_ms: float | None


class LogPattern(BaseModel):
    pattern: str
    level: str | None
    count: int
    services: list[str]
    severity: str = ""


class AnomalyFinding(BaseModel):
    metric: str
    value: float | None
    baseline: float | None
    threshold: float | None
    direction: str | None
    severity: str = ""
    explanation: str = ""


class AnomalyReport(BaseModel):
    metric_name: str
    baseline: float | None
    current_value: float | None
    threshold: float | None
    direction: str | None
    deviation_pct: float | None
    severity: str = "unknown"
    detected: bool = False
    explanation: str = ""
    formula: str = ""
    inputs_traced: list[str] = Field(default_factory=list)


class ObservabilityReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    operation: ObservabilityOperation
    metric_summary: MetricSummary | None = None
    trace_summary: TraceSummary | None = None
    log_patterns: list[LogPattern] = Field(default_factory=list)
    anomaly_report: AnomalyReport | None = None
    findings: list[AnomalyFinding] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    source_reference_preserved: bool = False
    anomaly_detection_claim: bool = False
    root_cause_attribution: bool = False
    model_version: str = "2.3.0"
    quality_score: float = Field(default=0.90, ge=0, le=1)


class ObservabilityRecord(BaseModel):
    pack_id: str = "observability"
    version: str = "2.3.0"
    capabilities: list[str] = Field(default_factory=lambda: [
        "metrics_collect",
        "trace_analyze",
        "log_analyze",
        "anomaly_detect",
    ])


__all__ = [
    "AnomalyFinding",
    "AnomalyReport",
    "BusinessContext",
    "LogPattern",
    "LogEntry",
    "LogSeverity",
    "MetricSample",
    "MetricSummary",
    "MetricType",
    "ObservabilityAnalystRequest",
    "ObservabilityInputs",
    "ObservabilityOperation",
    "ObservabilityRecord",
    "ObservabilityReport",
    "ThresholdDirection",
    "TraceSpan",
    "TraceSummary",
]
