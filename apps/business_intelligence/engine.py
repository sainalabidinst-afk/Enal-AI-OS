"""
Business Intelligence Engine.
"""

from __future__ import annotations

import logging

from apps.business_intelligence.bi_engine import BIAnalysisEngine
from apps.business_intelligence.schemas import (
    BIConfig,
    BIReport,
    BIRequest,
)

logger = logging.getLogger(__name__)


class BusinessIntelligenceEngine:
    """
    Orchestrates the business intelligence pipeline:
        1. Dashboard Generation
        2. KPI Tracking
        3. Metric Analysis
        4. Trend Analysis
    """

    def __init__(self) -> None:
        self.engine = BIAnalysisEngine()

    def execute(self, request: BIRequest) -> BIReport:
        config: BIConfig = request.inputs

        dashboards = self.engine.generate_dashboard(config)
        kpi_tracking = self.engine.track_kpis(config)
        metric_analyses = self.engine.analyze_metrics(config)
        trend_analyses = self.engine.analyze_trends(config)
        overall_health = self.engine.compute_overall_health(metric_analyses)

        summary = self._generate_summary(
            dashboards, kpi_tracking, metric_analyses, trend_analyses, overall_health
        )

        return BIReport(
            request_id=request.request_id,
            report_type=config.report_type,
            dashboards=dashboards,
            kpi_tracking=kpi_tracking,
            metric_analyses=metric_analyses,
            trend_analyses=trend_analyses,
            overall_health=overall_health,
            summary=summary,
        )

    def _generate_summary(
        self,
        dashboards: list,
        kpi_tracking: list,
        metric_analyses: list,
        trend_analyses: list,
        overall_health: str,
    ) -> str:
        """Generate a human-readable summary of the BI report."""
        parts = [f"Overall health: {overall_health}."]
        if kpi_tracking:
            parts.append(f"Tracked {len(kpi_tracking)} KPIs.")
        if metric_analyses:
            parts.append(f"Analyzed {len(metric_analyses)} metrics.")
        if trend_analyses:
            parts.append(f"Identified {len(trend_analyses)} trends.")
        if dashboards:
            parts.append(f"Generated {len(dashboards)} dashboard(s).")
        return " ".join(parts)


__all__ = ["BusinessIntelligenceEngine"]
