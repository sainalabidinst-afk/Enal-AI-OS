"""
Supply Chain Analyst Schemas
==============================

Typed contracts for the Supply Chain Analyst capability pack.
Defines input (SupplyChainRequest) and output (SupplyChainReport)
contracts for demand forecasting, inventory optimization, and risk analysis.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class SupplyChainOperation(StrEnum):
    demand_forecast = "demand_forecast"
    route_optimization = "route_optimization"
    inventory_analysis = "inventory_analysis"
    risk_assessment = "risk_assessment"


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=5, ge=1)
    budget_monthly_usd: float = Field(default=10000, ge=0)


class SupplyChainInputs(BaseModel):
    operation: SupplyChainOperation
    product_id: str = ""
    historical_demand: list[float] = Field(default_factory=list)
    lead_time_days: int = Field(default=7, ge=1)
    holding_cost_rate: float = Field(default=0.2, ge=0)
    ordering_cost: float = Field(default=100, ge=0)
    current_inventory: float = Field(default=0, ge=0)
    service_level: float = Field(default=0.95, ge=0, le=1)
    suppliers: list[str] = Field(default_factory=list)
    routes: list[str] = Field(default_factory=list)
    seasonality: str = "monthly"
    forecast_horizon_days: int = Field(default=30, ge=1)


class DemandForecast(BaseModel):
    period: str
    predicted_demand: float
    confidence_interval_lower: float
    confidence_interval_upper: float
    method: str
    assumptions: list[str] = Field(default_factory=list)


class InventoryOptimization(BaseModel):
    product_id: str
    eoq: float
    reorder_point: float
    safety_stock: float
    current_stock: float
    status: str
    recommendation: str = ""


class CostBenefitAnalysis(BaseModel):
    option_name: str
    total_cost: float
    total_benefit: float
    net_benefit: float
    roi: float
    payback_period_months: float


class RiskAssessment(BaseModel):
    risk_id: str
    risk_type: str
    description: str
    likelihood: float
    impact: float
    risk_score: float
    mitigation: str = ""


class SupplyChainReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    forecasts: list[DemandForecast] = Field(default_factory=list)
    inventory_results: list[InventoryOptimization] = Field(default_factory=list)
    cost_benefit: list[CostBenefitAnalysis] = Field(default_factory=list)
    risks: list[RiskAssessment] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    quality_score: float = Field(default=0.90, ge=0, le=1)
    model_version: str = "1.0.0"


class SupplyChainRecord(BaseModel):
    pack_id: str = "supply-chain-analyst"
    version: str = "2.6.0"
    capabilities: list[str] = Field(
        default_factory=lambda: [
            "demand_forecasting",
            "route_optimization",
            "inventory_analysis",
            "risk_assessment",
        ]
    )


class SupplyChainRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    business_context: BusinessContext
    inputs: SupplyChainInputs
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


__all__ = [
    "SupplyChainInputs",
    "SupplyChainOperation",
    "SupplyChainRequest",
    "SupplyChainReport",
    "SupplyChainRecord",
    "DemandForecast",
    "InventoryOptimization",
    "CostBenefitAnalysis",
    "RiskAssessment",
    "BusinessContext",
]
