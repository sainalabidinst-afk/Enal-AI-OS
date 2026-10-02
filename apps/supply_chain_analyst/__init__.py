"""
Supply Chain Analyst Pack
=========================

Demonstrates ECP capabilities for supply chain logistics optimization.

Workflow:
    User Request
        ↓
    Intent Router
        ↓
    Capability Graph → supply-chain-analyst-*
        ↓
    Task Planner
        ↓
    Subtasks:
    - Route Optimization
    - Inventory Optimization
    - Demand Forecasting
    - Supplier Risk Assessment
        ↓
    Execution Planner
        ↓
    Execution Runtime
        ↓
    Supply Chain Worker
        ↓
    Logistics Optimization Engine (full supply chain pipeline)
        ↓
    Result
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.supply_chain_analyst.engine import SupplyChainAnalystEngine
from apps.supply_chain_analyst.schemas import (
    SKU,
    BusinessContext,
    DemandForecast,
    InventoryRecommendation,
    Location,
    Route,
    RouteRecommendation,
    Supplier,
    SupplierRisk,
    SupplyChainConfig,
    SupplyChainOperation,
    SupplyChainPackRecord,
    SupplyChainReport,
    SupplyChainRequest,
)
from apps.supply_chain_analyst.worker import SupplyChainAnalystWorker


class SupplyChainAnalystApp(BaseReferenceApp):
    name = "supply-chain-analyst"
    version = "1.0.0"
    description = "Supply chain logistics optimization: route planning, inventory management, demand forecasting, supplier risk assessment"  # noqa: E501
    category = "supply-chain"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = SupplyChainAnalystWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> SupplyChainAnalystApp:
    return SupplyChainAnalystApp()


__all__ = [
    "SupplyChainAnalystApp",
    "SupplyChainAnalystEngine",
    "SupplyChainAnalystWorker",
    "SupplyChainOperation",
    "Location",
    "Route",
    "RouteRecommendation",
    "Supplier",
    "SupplierRisk",
    "SKU",
    "BusinessContext",
    "SupplyChainConfig",
    "SupplyChainRequest",
    "InventoryRecommendation",
    "DemandForecast",
    "SupplyChainReport",
    "SupplyChainPackRecord",
]
