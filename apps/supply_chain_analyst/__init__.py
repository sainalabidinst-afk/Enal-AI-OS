"""
Supply Chain Analyst Capability Pack — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.supply_chain_analyst.engine import SupplyChainEngine
from apps.supply_chain_analyst.schemas import (
    BusinessContext,
    CostBenefitAnalysis,
    DemandForecast,
    InventoryOptimization,
    RiskAssessment,
    SupplyChainInputs,
    SupplyChainOperation,
    SupplyChainRecord,
    SupplyChainReport,
    SupplyChainRequest,
)
from apps.supply_chain_analyst.worker import SupplyChainWorker


class SupplyChainAnalystApp(BaseReferenceApp):
    name = "supply-chain-analyst"
    version = "2.6.0"
    description = (
        "Logistics optimization, demand forecasting, inventory management, "
        "and supply chain risk analysis"
    )
    category = "business"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = SupplyChainWorker()

    async def run(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> SupplyChainAnalystApp:
    return SupplyChainAnalystApp()


__all__ = [
    "SupplyChainAnalystApp",
    "get_app",
    "SupplyChainEngine",
    "SupplyChainWorker",
    "SupplyChainRequest",
    "SupplyChainReport",
    "SupplyChainOperation",
    "SupplyChainInputs",
    "SupplyChainRecord",
    "DemandForecast",
    "InventoryOptimization",
    "CostBenefitAnalysis",
    "RiskAssessment",
    "BusinessContext",
]
