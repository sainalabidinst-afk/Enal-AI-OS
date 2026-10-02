"""
Business Intelligence Engine.
"""

from __future__ import annotations

import logging

from apps.business_intelligence.bi_engine import BIAnalysisEngine
from apps.business_intelligence.schemas import (
    BusinessIntelligenceInputs,
    BusinessIntelligenceOperation,
    BusinessIntelligenceReport,
    BusinessIntelligenceRequest,
    DashboardConfig,
    KpiMetric,
    ScenarioAnalysis,
)

logger = logging.getLogger(__name__)


class BusinessIntelligenceEngine:
    """
    Orchestrates business intelligence pipeline:
        1. Input Validation
        2. KPI Tracking / Dashboard Generation / Scenario Planning / Metric Analysis
        3. Result Generation
    """

    def __init__(self) -> None:
        self.engine = BIAnalysisEngine()

    def analyze(self, request: BusinessIntelligenceRequest) -> BusinessIntelligenceReport:
        inputs: BusinessIntelligenceInputs = request.inputs
        validation = self.engine.check_input_validation(inputs)

        if not validation["valid"]:
            logger.warning("BI validation failed: %s", validation["errors"])
            return BusinessIntelligenceReport(
                request_id=request.request_id,
                kpis=[],
                dashboard_configs=[],
                scenarios=[],
                recommendations=validation["errors"],
                quality_score=0.0,
            )

        kpis: list[KpiMetric] = []
        dashboard_configs: list[DashboardConfig] = []
        scenarios: list[ScenarioAnalysis] = []
        recommendations: list[str] = []

        if inputs.operation == BusinessIntelligenceOperation.kpi_tracking:
            kpis = self.engine.track_kpis(inputs)
        elif inputs.operation == BusinessIntelligenceOperation.dashboard_generation:
            dashboard_configs.append(self.engine.generate_dashboard(inputs))
        elif inputs.operation == BusinessIntelligenceOperation.scenario_planning:
            scenarios = self.engine.plan_scenario(inputs)
        elif inputs.operation == BusinessIntelligenceOperation.metric_analysis:
            kpis = self.engine.analyze_metric(inputs)

        recommendations.extend(self.engine.safety_boundary_check())

        quality_score = self.engine.compute_quality_score(
            kpis=kpis,
            dashboard_configs=dashboard_configs,
            scenarios=scenarios,
        )

        return BusinessIntelligenceReport(
            request_id=request.request_id,
            kpis=kpis,
            dashboard_configs=dashboard_configs,
            scenarios=scenarios,
            recommendations=recommendations,
            quality_score=quality_score,
        )
