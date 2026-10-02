"""
Supply Chain Analyst Engine.
"""

from __future__ import annotations

import logging

from apps.supply_chain_analyst.logistics_engine import LogisticsOptimizationEngine
from apps.supply_chain_analyst.schemas import (
    SupplyChainConfig,
    SupplyChainReport,
    SupplyChainRequest,
)

logger = logging.getLogger(__name__)


class SupplyChainAnalystEngine:
    """
    Orchestrates the supply chain analysis pipeline:
        1. Route Optimization
        2. Inventory Optimization
        3. Demand Forecasting
        4. Supplier Risk Assessment
    """

    def __init__(self) -> None:
        self.engine = LogisticsOptimizationEngine()

    def execute(self, request: SupplyChainRequest) -> SupplyChainReport:
        config: SupplyChainConfig = request.inputs

        route_recs = []
        inventory_recs = []
        forecasts = []
        supplier_risks = []

        if config.operation == "route_optimization":
            route_recs = self.engine.optimize_routes(config)
        elif config.operation == "inventory_optimization":
            inventory_recs = self.engine.optimize_inventory(config)
        elif config.operation == "demand_forecasting":
            forecasts = self.engine.forecast_demand(config)
        elif config.operation == "supplier_risk_assessment":
            supplier_risks = self.engine.assess_supplier_risks(config)
        else:
            # Run all sub-operations for comprehensive analysis.
            route_recs = self.engine.optimize_routes(config)
            inventory_recs = self.engine.optimize_inventory(config)
            forecasts = self.engine.forecast_demand(config)
            supplier_risks = self.engine.assess_supplier_risks(config)

        total_optimizations = (
            len(route_recs) + len(inventory_recs) + len(forecasts) + len(supplier_risks)
        )
        cost_savings = sum(r.total_cost for r in route_recs) * 0.15 + sum(
            i.holding_cost for i in inventory_recs
        ) * 0.10

        return SupplyChainReport(
            request_id=request.request_id,
            operation=config.operation,
            route_recommendations=route_recs,
            inventory_recommendations=inventory_recs,
            demand_forecasts=forecasts,
            supplier_risks=supplier_risks,
            total_optimizations=total_optimizations,
            cost_savings_estimate=round(cost_savings, 2),
        )


__all__ = ["SupplyChainAnalystEngine"]
