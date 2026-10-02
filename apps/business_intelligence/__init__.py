"""
Business Intelligence Pack
=========================

Demonstrates ECP capabilities for business intelligence and data analytics.

Workflow:
    User Request
        ↓
    Intent Router
        ↓
    Capability Graph → business-intelligence-*
        ↓
    Task Planner
        ↓
    Subtasks:
    - Dashboard Generation
    - KPI Tracking
    - Metric Analysis
    - Trend Analysis
        ↓
    Execution Planner
        ↓
    Execution Runtime
        ↓
    BI Worker
        ↓
    BI Analysis Engine (full BI pipeline)
        ↓
    Result
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.business_intelligence.engine import BusinessIntelligenceEngine
from apps.business_intelligence.schemas import (
    BIConfig,
    BIReport,
    BIReportType,
    BIRequest,
    BusinessContext,
    BusinessIntelligencePackRecord,
    DashboardSpec,
    DashboardWidget,
    DataPoint,
    KpiStatus,
    KpiTarget,
    KpiTracking,
    MetricAnalysis,
    MetricDefinition,
    MetricType,
    TrendAnalysis,
    VisualizationType,
)
from apps.business_intelligence.worker import BusinessIntelligenceWorker


class BusinessIntelligenceApp(BaseReferenceApp):
    name = "business-intelligence"
    version = "1.0.0"
    description = "Business intelligence: dashboarding, KPI tracking, metric analysis, and trend forecasting"  # noqa: E501
    category = "business-intelligence"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = BusinessIntelligenceWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> BusinessIntelligenceApp:
    return BusinessIntelligenceApp()


__all__ = [
    "BusinessIntelligenceApp",
    "BusinessIntelligenceEngine",
    "BusinessIntelligenceWorker",
    "BIReportType",
    "VisualizationType",
    "MetricType",
    "KpiStatus",
    "DataPoint",
    "MetricDefinition",
    "KpiTarget",
    "DashboardWidget",
    "BusinessContext",
    "BIConfig",
    "BIRequest",
    "MetricAnalysis",
    "KpiTracking",
    "DashboardSpec",
    "TrendAnalysis",
    "BIReport",
    "BusinessIntelligencePackRecord",
]
