"""
Business Intelligence Capability Pack — BI Analysis Engine module.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.business_intelligence.schemas import (
    BusinessIntelligenceInputs,
    BusinessIntelligenceOperation,
    DashboardConfig,
    KpiMetric,
    ScenarioAnalysis,
)

logger = logging.getLogger(__name__)


class BIAnalysisEngine:
    """Provides KPI tracking, dashboard generation, and scenario planning."""

    def check_input_validation(self, inputs: BusinessIntelligenceInputs) -> dict[str, Any]:
        errors: list[str] = []
        valid = True

        if inputs.operation == BusinessIntelligenceOperation.kpi_tracking:
            if not inputs.metrics:
                errors.append("metrics is required for kpi_tracking")
                valid = False
        elif inputs.operation == BusinessIntelligenceOperation.dashboard_generation:
            if not inputs.departments:
                errors.append("departments is required for dashboard_generation")
                valid = False
        elif inputs.operation == BusinessIntelligenceOperation.scenario_planning:
            if not inputs.scenario_name:
                errors.append("scenario_name is required for scenario_planning")
                valid = False
        elif inputs.operation == BusinessIntelligenceOperation.metric_analysis:
            if not inputs.historical_data:
                errors.append("historical_data is required for metric_analysis")
                valid = False

        return {
            "valid": valid,
            "errors": errors,
            "missing_input_reported": True if errors else False,
            "fabricated_value": False,
        }

    def track_kpis(self, inputs: BusinessIntelligenceInputs) -> list[KpiMetric]:
        """Track KPIs against targets and compute variance."""
        kpis: list[KpiMetric] = []

        for metric_name in inputs.metrics:
            current = inputs.current_values.get(metric_name, 0)
            target = inputs.target_values.get(metric_name, current)
            variance = ((current - target) / target * 100) if target != 0 else 0

            if variance >= 10:
                status = "exceeding"
                trend = "up"
            elif variance >= -5:
                status = "on_target"
                trend = "stable"
            else:
                status = "below_target"
                trend = "down"

            kpis.append(KpiMetric(
                metric_name=metric_name,
                current_value=current,
                target_value=target,
                variance_pct=round(variance, 2),
                status=status,
                trend=trend,
                department=inputs.departments[0] if inputs.departments else "overall",
            ))

        return kpis

    def generate_dashboard(self, inputs: BusinessIntelligenceInputs) -> DashboardConfig:
        """Generate dashboard configuration from metrics and departments."""
        widgets = []
        for metric in inputs.metrics:
            widgets.append(f"kpi-card-{metric}")
            widgets.append(f"trend-chart-{metric}")

        for dept in inputs.departments:
            widgets.append(f"department-view-{dept}")

        return DashboardConfig(
            dashboard_name=f"{inputs.departments[0] if inputs.departments else 'Business'}_Dashboard",  # noqa: E501
            widgets=widgets[:12],
            layout="grid",
            refresh_interval_seconds=300,
            data_sources=["operational_db", "warehouse"],
        )

    def plan_scenario(self, inputs: BusinessIntelligenceInputs) -> list[ScenarioAnalysis]:
        """Run scenario analysis on specified variables."""
        scenarios: list[ScenarioAnalysis] = []

        if not inputs.historical_data:
            return scenarios

        baseline = sum(inputs.historical_data) / len(inputs.historical_data)

        for var in inputs.variables:
            for change in [-0.2, 0.0, 0.2]:
                projected = baseline * (1 + change)
                confidence = 0.85 if abs(change) < 0.1 else 0.75
                scenario_label = "negative" if change < 0 else "positive" if change > 0 else "baseline"  # noqa: E501
                scenarios.append(ScenarioAnalysis(
                    scenario_name=f"{inputs.scenario_name}_{var}_{scenario_label}",
                    variable_name=var,
                    change_pct=change * 100,
                    projected_outcome=round(projected, 2),
                    confidence=confidence,
                    assumptions=[f"Linear scaling assumed for {var}", "Historical correlation maintained"],  # noqa: E501
                ))

        return scenarios

    def analyze_metric(self, inputs: BusinessIntelligenceInputs) -> list[KpiMetric]:
        """Analyze historical metric data for trends."""
        kpis: list[KpiMetric] = []

        if not inputs.historical_data:
            return kpis

        avg = sum(inputs.historical_data) / len(inputs.historical_data)
        recent = inputs.historical_data[-3:] if len(inputs.historical_data) >= 3 else [avg]
        recent_avg = sum(recent) / len(recent)

        trend = "up" if recent_avg > avg else "down" if recent_avg < avg else "stable"

        for metric_name in inputs.metrics:
            target = inputs.target_values.get(metric_name, avg)
            variance = ((recent_avg - target) / target * 100) if target != 0 else 0

            kpis.append(KpiMetric(
                metric_name=metric_name,
                current_value=round(recent_avg, 2),
                target_value=target,
                variance_pct=round(variance, 2),
                status="on_target" if abs(variance) < 10 else "deviating",
                trend=trend,
            ))

        return kpis

    def safety_boundary_check(self) -> list[str]:
        return [
            "KPI targets are indicative and require business review",
            "Scenario projections are estimates based on historical patterns",
            "Dashboard recommendations are advisory, not prescriptive",
        ]

    def compute_quality_score(self, **kwargs) -> float:
        scores = []
        for key, value in kwargs.items():
            if isinstance(value, list) and len(value) > 0:
                scores.append(0.9)
        if not scores:
            return 0.5
        return round(sum(scores) / len(scores), 2)
