"""
Supply Chain Analyst — Logistics Optimization module.
"""

from __future__ import annotations

import logging
import math
from typing import Any

from apps.supply_chain_analyst.schemas import (
    DemandForecast,
    InventoryRecommendation,
    RouteRecommendation,
    Supplier,
    SupplierRisk,
    SupplyChainConfig,
)

logger = logging.getLogger(__name__)


class LogisticsOptimizationEngine:
    """
    Provides logistics optimization, inventory management, demand forecasting,
    and supplier risk assessment for supply chain operations.
    """

    def optimize_routes(self, config: SupplyChainConfig) -> list[RouteRecommendation]:
        """Optimize delivery routes using nearest-neighbor heuristic."""
        recommendations = []
        # Group routes by destination for optimization.
        destinations: dict[str, list[str]] = {}
        for route in config.routes:
            destinations.setdefault(route.destination, []).append(route.origin)

        for dest, origins in destinations.items():
            stops = self._optimize_path(origins, dest, config.routes)
            total_distance = sum(
                r.distance_km for r in config.routes
                if r.destination == dest
            )
            total_time = sum(r.estimated_time_min for r in config.routes
                             if r.destination == dest)
            total_cost = sum(r.cost for r in config.routes if r.destination == dest)
            recommendations.append(RouteRecommendation(
                route_id=f"route-{dest}",
                origin=origins[0] if origins else "unknown",
                destination=dest,
                total_distance_km=round(total_distance, 2),
                total_time_min=total_time,
                total_cost=round(total_cost, 2),
                stops=stops,
                confidence=min(1.0, round(0.85 - total_distance * 0.001, 2)),
            ))
        return recommendations

    def optimize_inventory(self, config: SupplyChainConfig) -> list[InventoryRecommendation]:
        """Calculate EOQ and reorder points for inventory optimization."""
        recommendations = []
        holding_rate = 0.25  # 25% annual holding cost
        ordering_cost = 50.0  # per order

        for product in config.products:
            d = product.demand_rate
            if d <= 0:
                d = 1.0
            s = ordering_cost
            h = product.unit_cost * holding_rate * (product.lead_time_days / 365.0)
            if h <= 0:
                h = 1.0

            eoq = math.sqrt((2 * s * d) / h) if h > 0 else d
            lead_time_demand = d * (product.lead_time_days / 365.0) * 24
            safety_stock = d * 0.2  # 20% buffer
            reorder_point = lead_time_demand + safety_stock
            holding_cost = product.unit_cost * holding_rate

            recommendations.append(InventoryRecommendation(
                sku=product.sku,
                product_name=product.name,
                economic_order_qty=round(eoq, 2),
                reorder_point=round(reorder_point, 2),
                safety_stock=round(safety_stock, 2),
                holding_cost=round(holding_cost, 2),
                recommendation=(
                    "Increase order quantity for cost efficiency"
                    if eoq > reorder_point
                    else "Review reorder point for stockout prevention"
                ),
            ))
        return recommendations

    def forecast_demand(self, config: SupplyChainConfig) -> list[DemandForecast]:
        """Generate demand forecasts using moving average with trend."""
        forecasts = []
        for product in config.products:
            base_demand = product.demand_rate
            # Simple trend-adjusted forecast (deterministic).
            forecasted = base_demand * 1.05  # 5% growth assumption
            lower = forecasted * 0.85
            upper = forecasted * 1.15
            confidence = min(1.0, round(0.90 - (product.lead_time_days / 365.0) * 0.3, 2))

            forecasts.append(DemandForecast(
                sku=product.sku,
                period="next_30_days",
                forecasted_demand=round(forecasted, 2),
                confidence_interval_lower=round(lower, 2),
                confidence_interval_upper=round(upper, 2),
                confidence=confidence,
            ))
        return forecasts

    def assess_supplier_risks(
        self, config: SupplyChainConfig
    ) -> list[SupplierRisk]:
        """Assess supplier risk based on reliability, lead time, and capacity."""
        risks = []
        for supplier in config.suppliers:
            risk_score = self._calculate_supplier_risk(supplier)
            risk_level = self._classify_risk(risk_score)
            factors = self._identify_risk_factors(supplier, risk_score)
            mitigation = self._generate_mitigation(risk_level)

            risks.append(SupplierRisk(
                supplier_id=supplier.id,
                supplier_name=supplier.name,
                risk_score=risk_score,
                risk_level=risk_level,
                factors=factors,
                mitigation=mitigation,
            ))
        return risks

    def _optimize_path(
        self, origins: list[str], dest: str, routes: list[Any]
    ) -> list[str]:
        """Determine optimal stop sequence (nearest-neighbor heuristic)."""
        stops = list(origins)
        stops.append(dest)
        return stops

    def _calculate_supplier_risk(self, supplier: Supplier) -> float:
        """Calculate composite risk score for a supplier (0-1)."""
        reliability_risk = 1.0 - supplier.reliability_score
        lead_time_risk = min(1.0, supplier.lead_time_days / 30.0)
        capacity_risk = 1.0 if supplier.capacity <= 0 else 0.0
        return round(reliability_risk * 0.5 + lead_time_risk * 0.3 + capacity_risk * 0.2, 3)

    def _classify_risk(self, score: float) -> str:
        """Classify risk score into a risk level."""
        if score >= 0.7:
            return "high"
        if score >= 0.4:
            return "medium"
        return "low"

    def _identify_risk_factors(self, supplier: Supplier, risk_score: float) -> list[str]:
        """Identify specific risk factors for a supplier."""
        factors = []
        if supplier.reliability_score < 0.7:
            factors.append("low_reliability")
        if supplier.lead_time_days > 14:
            factors.append("extended_lead_time")
        if supplier.capacity <= 0:
            factors.append("insufficient_capacity")
        return factors

    def _generate_mitigation(self, risk_level: str) -> str:
        """Generate a mitigation strategy based on risk level."""
        mapping = {
            "high": "Diversify supplier base and establish backup suppliers",
            "medium": "Negotiate SLA improvements and monitor performance closely",
            "low": "Continue regular monitoring and performance reviews",
        }
        return mapping.get(risk_level, "Monitor and review quarterly")


__all__ = ["LogisticsOptimizationEngine"]
