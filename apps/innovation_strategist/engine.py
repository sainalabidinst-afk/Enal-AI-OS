"""
Innovation Strategist Engine.
"""

from __future__ import annotations

import logging

from apps.innovation_strategist.schemas import (
    ForesightScenario,
    InnovationStrategistInputs,
    InnovationStrategistOperation,
    InnovationStrategistReport,
    InnovationStrategistRequest,
    PortfolioItem,
    TechTrend,
)
from apps.innovation_strategist.strategy_engine import InnovationStrategyEngine

logger = logging.getLogger(__name__)


class InnovationStrategistEngine:
    """
    Orchestrates innovation strategy pipeline:
        1. Input Validation
        2. Trend Analysis / Portfolio Planning / Foresight Scenarios / Competitive Intel
        3. Result Generation
    """

    def __init__(self) -> None:
        self.engine = InnovationStrategyEngine()

    def analyze(self, request: InnovationStrategistRequest) -> InnovationStrategistReport:
        inputs: InnovationStrategistInputs = request.inputs
        validation = self.engine.check_input_validation(inputs)

        if not validation["valid"]:
            logger.warning("Innovation Strategist validation failed: %s", validation["errors"])
            return InnovationStrategistReport(
                request_id=request.request_id,
                tech_trends=[],
                portfolio_items=[],
                foresight_scenarios=[],
                recommendations=validation["errors"],
                quality_score=0.0,
            )

        tech_trends: list[TechTrend] = []
        portfolio_items: list[PortfolioItem] = []
        foresight_scenarios: list[ForesightScenario] = []
        recommendations: list[str] = []

        if inputs.operation == InnovationStrategistOperation.trend_analysis:
            tech_trends = self.engine.analyze_trends(inputs)
        elif inputs.operation == InnovationStrategistOperation.portfolio_planning:
            portfolio_items = self.engine.plan_portfolio(inputs)
        elif inputs.operation == InnovationStrategistOperation.foresight_scenarios:
            foresight_scenarios = self.engine.generate_scenarios(inputs)
        elif inputs.operation == InnovationStrategistOperation.competitive_intelligence:
            tech_trends = self.engine.analyze_trends(inputs)
            foresight_scenarios = self.engine.generate_scenarios(inputs)

        recommendations.extend(self.engine.safety_boundary_check())

        quality_score = self.engine.compute_quality_score(
            tech_trends=tech_trends,
            portfolio_items=portfolio_items,
            foresight_scenarios=foresight_scenarios,
        )

        return InnovationStrategistReport(
            request_id=request.request_id,
            tech_trends=tech_trends,
            portfolio_items=portfolio_items,
            foresight_scenarios=foresight_scenarios,
            recommendations=recommendations,
            quality_score=quality_score,
        )
