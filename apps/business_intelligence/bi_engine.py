"""
Business Intelligence — BI Analysis module.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.business_intelligence.schemas import (
    BIConfig,
    DashboardSpec,
    KpiStatus,
    KpiTarget,
    KpiTracking,
    MetricAnalysis,
    MetricDefinition,
    TrendAnalysis,
)

logger = logging.getLogger(__name__)


class BIAnalysisEngine:
    """
    Provides dashboard generation, KPI tracking, metric analysis, and trend
    analysis for business intelligence reporting.
    """

    TREND_THRESHOLDS = {
        "improving": 0.05,
        "declining": -0.05,
    }

    def generate_dashboard(self, config: BIConfig) -> list[DashboardSpec]:
        """Generate dashboard specifications from widget configurations."""
        dashboards = []
        if config.widgets:
            dashboards.append(DashboardSpec(
                dashboard_id=f"dashboard-{config.time_range}",
                title=f"Business Intelligence Dashboard ({config.time_range})",
                widgets=config.widgets,
                layout="grid",
                refresh_interval_seconds=300,
            ))
        return dashboards

    def track_kpis(self, config: BIConfig) -> list[KpiTracking]:
        """Track KPI progress against targets."""
        results = []
        for target in config.kpi_targets:
            metric = self._find_metric(config, target.metric_id)
            current = target.current_value
            target_val = target.target_value
            pct = round((current / target_val) * 100, 2) if target_val else 0.0
            status = self._classify_kpi_status(current, target_val, target)

            results.append(KpiTracking(
                metric_id=target.metric_id,
                metric_name=metric.name if metric else target.metric_id,
                target_value=target_val,
                current_value=current,
                percentage_to_target=pct,
                status=status,
                last_updated=config.time_range,
                trajectory=self._kpi_trajectory(current, target_val),
            ))
        return results

    def analyze_metrics(self, config: BIConfig) -> list[MetricAnalysis]:
        """Analyze individual metrics for variance, trend, and insights."""
        analyses = []
        for metric in config.metrics:
            current = self._get_current_value(config, metric.id)
            target = metric.target
            variance = round(current - target, 2) if target else 0.0
            trend = self._compute_trend(config, metric.id)
            status = self._classify_metric_status(current, target, variance, trend)
            insights = self._generate_insights(metric, current, target, trend)

            analyses.append(MetricAnalysis(
                metric_id=metric.id,
                metric_name=metric.name,
                current_value=current,
                target_value=target,
                variance=variance,
                trend=trend,
                status=status,
                insights=insights,
                confidence=90,
            ))
        return analyses

    def analyze_trends(self, config: BIConfig) -> list[TrendAnalysis]:
        """Analyze trends in historical data and forecast next period."""
        analyses = []
        for metric_id, data_points in config.historical_data.items():
            if len(data_points) < 2:
                continue
            trend = self._compute_numeric_trend(data_points)
            magnitude = self._compute_trend_magnitude(data_points)
            direction = "improving" if trend > 0 else "declining" if trend < 0 else "stable"
            significance = min(1.0, abs(magnitude))
            forecast = self._forecast_next(data_points)
            ci = self._confidence_interval(data_points)

            analyses.append(TrendAnalysis(
                metric_id=metric_id,
                direction=direction,
                magnitude=round(magnitude, 4),
                significance=round(significance, 4),
                forecast_next_period=round(forecast, 2),
                confidence_interval=(round(ci[0], 2), round(ci[1], 2)),
            ))
        return analyses

    def _find_metric(self, config: BIConfig, metric_id: str) -> MetricDefinition | None:
        """Find a metric definition by ID."""
        for metric in config.metrics:
            if metric.id == metric_id:
                return metric
        return None

    def _get_current_value(self, config: BIConfig, metric_id: str) -> float:
        """Get the most recent value for a metric from historical data."""
        points = config.historical_data.get(metric_id, [])
        if not points:
            # Fall back to KPI target current_value.
            for target in config.kpi_targets:
                if target.metric_id == metric_id:
                    return target.current_value
            return 0.0
        return points[-1].value

    def _compute_trend(self, config: BIConfig, metric_id: str) -> str:
        """Compute a categorical trend label for a metric."""
        points = config.historical_data.get(metric_id, [])
        if len(points) < 2:
            return "insufficient_data"
        values = [p.value for p in points]
        diffs = [values[i] - values[i - 1] for i in range(1, len(values))]
        avg_diff = sum(diffs) / len(diffs)
        if avg_diff > 0:
            return "up"
        if avg_diff < 0:
            return "down"
        return "flat"

    def _compute_numeric_trend(self, data_points: list[Any]) -> float:
        """Compute numeric trend slope."""
        values = [p.value for p in data_points]
        n = len(values)
        if n < 2:
            return 0.0
        x = list(range(n))
        x_mean = sum(x) / n
        y_mean = sum(values) / n
        numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((xi - x_mean) ** 2 for xi in x)
        return numerator / denominator if denominator else 0.0

    def _compute_trend_magnitude(self, data_points: list[Any]) -> float:
        """Compute trend magnitude as average absolute change."""
        values = [p.value for p in data_points]
        if len(values) < 2:
            return 0.0
        diffs = [abs(values[i] - values[i - 1]) for i in range(1, len(values))]
        return sum(diffs) / len(diffs)

    def _forecast_next(self, data_points: list[Any]) -> float:
        """Forecast the next period value using linear regression."""
        values = [p.value for p in data_points]
        n = len(values)
        if n < 2:
            return values[0] if values else 0.0
        x = list(range(n))
        x_mean = sum(x) / n
        y_mean = sum(values) / n
        numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((xi - x_mean) ** 2 for xi in x)
        slope = numerator / denominator if denominator else 0.0
        return round(values[-1] + slope, 2)

    def _confidence_interval(self, data_points: list[Any]) -> tuple[float, float]:
        """Compute a simple confidence interval for the forecast."""
        values = [p.value for p in data_points]
        if len(values) < 2:
            return (0.0, 0.0)
        mean = sum(values) / len(values)
        std = (sum((v - mean) ** 2 for v in values) / len(values)) ** 0.5
        margin = std * 1.96 / (len(values) ** 0.5)
        return (mean - margin, mean + margin)

    def _classify_kpi_status(
        self, current: float, target: float, kpi_target: KpiTarget
    ) -> KpiStatus:
        """Classify KPI status based on thresholds."""
        if target == 0:
            return KpiStatus.on_track
        pct = (current / target) * 100
        if pct >= 100:
            return KpiStatus.target_met
        if pct >= kpi_target.threshold_warning:
            return KpiStatus.on_track
        if pct >= kpi_target.threshold_critical:
            return KpiStatus.at_risk
        return KpiStatus.off_track

    def _kpi_trajectory(self, current: float, target: float) -> str:
        """Determine KPI trajectory direction."""
        if target == 0:
            return "unknown"
        if current >= target:
            return "exceeding"
        if current >= target * 0.8:
            return "approaching"
        return "falling_short"

    def _classify_metric_status(
        self, current: float, target: float, variance: float, trend: str
    ) -> KpiStatus:
        """Classify metric status based on variance and trend."""
        if target and current >= target:
            return KpiStatus.target_met
        if trend == "up" and variance >= 0:
            return KpiStatus.on_track
        if trend == "down" and variance < 0:
            return KpiStatus.at_risk
        return KpiStatus.off_track

    def _generate_insights(
        self, metric: MetricDefinition, current: float, target: float, trend: str
    ) -> list[str]:
        """Generate human-readable insights for a metric."""
        insights = []
        if target and current >= target:
            insights.append(f"{metric.name} has met or exceeded target of {target}")
        elif target:
            insights.append(
                f"{metric.name} is {abs(current - target):.2f} "
                f"below target of {target}"
            )
        if trend == "up":
            insights.append(f"{metric.name} is trending upward")
        elif trend == "down":
            insights.append(f"{metric.name} is trending downward")
        elif trend == "flat":
            insights.append(f"{metric.name} is stable")
        else:
            insights.append(f"{metric.name} has insufficient data for trend analysis")
        return insights

    def compute_overall_health(self, analyses: list[MetricAnalysis]) -> str:
        """Compute overall business health from metric analyses."""
        if not analyses:
            return "unknown"
        on_track = sum(
            1 for a in analyses
            if a.status in (KpiStatus.on_track, KpiStatus.target_met)
        )
        total = len(analyses)
        ratio = on_track / total
        if ratio >= 0.8:
            return "healthy"
        if ratio >= 0.6:
            return "moderate"
        return "at_risk"


__all__ = ["BIAnalysisEngine"]
