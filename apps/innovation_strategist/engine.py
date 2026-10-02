"""
Innovation Strategist Engine.
"""

from __future__ import annotations

import logging

from apps.innovation_strategist.schemas import (
    InnovationConfig,
    InnovationReport,
    InnovationRequest,
)
from apps.innovation_strategist.strategy_engine import StrategyAnalysisEngine

logger = logging.getLogger(__name__)


class InnovationStrategistEngine:
    """
    Orchestrates the innovation strategy pipeline:
        1. Trend Analysis
        2. Technology Forecast
        3. Competitive Intelligence
        4. Scenario Planning
        5. Opportunity Identification
    """

    def __init__(self) -> None:
        self.engine = StrategyAnalysisEngine()

    def execute(self, request: InnovationRequest) -> InnovationReport:
        config: InnovationConfig = request.inputs
        context = request.business_context

        trend_signals = self.engine.analyze_trends(config)
        forecasts = self.engine.forecast_technology(config, context)
        competitive_insights = self.engine.analyze_competition(config)
        scenarios = self.engine.plan_scenarios(config, trend_signals)
        opportunities = self.engine.identify_opportunities(config, trend_signals)
        narrative = self.engine.generate_narrative(
            trend_signals, forecasts, scenarios, opportunities
        )

        return InnovationReport(
            request_id=request.request_id,
            operation=config.operation,
            trend_signals=trend_signals,
            forecasts=forecasts,
            competitive_insights=competitive_insights,
            scenarios=scenarios,
            opportunities=opportunities,
            strategic_narrative=narrative,
        )


__all__ = ["InnovationStrategistEngine"]
