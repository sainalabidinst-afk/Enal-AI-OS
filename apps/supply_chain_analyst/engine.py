"""
Supply Chain Analyst Engine.
"""

from __future__ import annotations

import logging

from apps.supply_chain_analyst.schemas import (
    CostBenefitAnalysis,
    DemandForecast,
    InventoryOptimization,
    RiskAssessment,
    SupplyChainInputs,
    SupplyChainOperation,
    SupplyChainReport,
    SupplyChainRequest,
)
from apps.supply_chain_analyst.supply_chain_engine import SupplyChainAnalysisEngine

logger = logging.getLogger(__name__)


class SupplyChainEngine:
    """
    Orchestrates supply chain analysis pipeline:
        1. Input Validation
        2. Demand Forecasting / Route Optimization / Inventory Analysis / Risk Assessment
        3. Cost-Benefit Analysis
        4. Recommendation Generation
    """

    def __init__(self) -> None:
        self.engine = SupplyChainAnalysisEngine()

    def analyze(self, request: SupplyChainRequest) -> SupplyChainReport:
        inputs: SupplyChainInputs = request.inputs
        validation = self.engine.check_input_validation(inputs)

        if not validation["valid"]:
            logger.warning("Supply Chain validation failed: %s", validation["errors"])
            return SupplyChainReport(
                request_id=request.request_id,
                forecasts=[],
                inventory_results=[],
                cost_benefit=[],
                risks=[],
                recommendations=validation["errors"],
                quality_score=0.0,
            )

        forecasts: list[DemandForecast] = []
        inventory_results: list[InventoryOptimization] = []
        cost_benefit: list[CostBenefitAnalysis] = []
        risks: list[RiskAssessment] = []
        recommendations: list[str] = []

        if inputs.operation == SupplyChainOperation.demand_forecast:
            forecasts = self.engine.forecast_demand(inputs)
        elif inputs.operation == SupplyChainOperation.route_optimization:
            recommendations = self.engine.optimize_routes(inputs)
        elif inputs.operation == SupplyChainOperation.inventory_analysis:
            inventory_results = self.engine.optimize_inventory(inputs)
        elif inputs.operation == SupplyChainOperation.risk_assessment:
            risks = self.engine.assess_risk(inputs)

        recommendations.extend(self.engine.safety_boundary_check())

        quality_score = self.engine.compute_quality_score(
            forecasts=forecasts,
            inventory_results=inventory_results,
            cost_benefit=cost_benefit,
            risks=risks,
        )

        return SupplyChainReport(
            request_id=request.request_id,
            forecasts=forecasts,
            inventory_results=inventory_results,
            cost_benefit=cost_benefit,
            risks=risks,
            recommendations=recommendations,
            quality_score=quality_score,
        )
