"""
Supply Chain Analyst Capability Schemas
==========================================

Typed contracts for the Supply Chain Analyst capability pack.
Defines input (SupplyChainRequest) and output (SupplyChainReport) contracts for
logistics optimization, route planning, inventory management, and demand forecasting.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class SupplyChainOperation(StrEnum):
    route_optimization = "route_optimization"
    inventory_optimization = "inventory_optimization"
    demand_forecasting = "demand_forecasting"
    supplier_risk_assessment = "supplier_risk_assessment"


class Location(BaseModel):
    name: str
    latitude: float
    longitude: float
    facility_type: str = "warehouse"


class Route(BaseModel):
    origin: str
    destination: str
    distance_km: float
    estimated_time_min: int
    cost: float


class Supplier(BaseModel):
    id: str
    name: str
    location: str
    reliability_score: float = Field(default=0.0, ge=0.0, le=1.0)
    capacity: int = 0
    lead_time_days: int = 0


class SKU(BaseModel):
    sku: str
    name: str
    unit_cost: float
    demand_rate: float = 0.0
    lead_time_days: int = 0


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=15, ge=1)


class SupplyChainConfig(BaseModel):
    operation: SupplyChainOperation
    locations: list[Location] = Field(default_factory=list)
    routes: list[Route] = Field(default_factory=list)
    suppliers: list[Supplier] = Field(default_factory=list)
    products: list[SKU] = Field(default_factory=list)
    constraints: dict[str, Any] = Field(default_factory=dict)


class SupplyChainRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: str = "route_optimization"
    business_context: BusinessContext
    inputs: SupplyChainConfig
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


class RouteRecommendation(BaseModel):
    route_id: str
    origin: str
    destination: str
    total_distance_km: float
    total_time_min: int
    total_cost: float
    stops: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class InventoryRecommendation(BaseModel):
    sku: str
    product_name: str
    economic_order_qty: float
    reorder_point: float
    safety_stock: float
    holding_cost: float
    recommendation: str


class DemandForecast(BaseModel):
    sku: str
    period: str
    forecasted_demand: float
    confidence_interval_lower: float
    confidence_interval_upper: float
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class SupplierRisk(BaseModel):
    supplier_id: str
    supplier_name: str
    risk_score: float = Field(default=0.0, ge=0.0, le=1.0)
    risk_level: str
    factors: list[str] = Field(default_factory=list)
    mitigation: str


class SupplyChainReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    operation: SupplyChainOperation
    route_recommendations: list[RouteRecommendation] = Field(default_factory=list)
    inventory_recommendations: list[InventoryRecommendation] = Field(default_factory=list)
    demand_forecasts: list[DemandForecast] = Field(default_factory=list)
    supplier_risks: list[SupplierRisk] = Field(default_factory=list)
    total_optimizations: int = 0
    cost_savings_estimate: float = 0.0
    model_version: str = "1.0.0"


class SupplyChainPackRecord(BaseModel):
    pack_id: str = "supply-chain-analyst"
    version: str = "1.0.0"
    capabilities: list[str] = Field(default_factory=lambda: [
        "route_optimization",
        "inventory_optimization",
        "demand_forecasting",
        "supplier_risk_assessment",
    ])


__all__ = [
    "BusinessContext",
    "DemandForecast",
    "InventoryRecommendation",
    "Location",
    "Route",
    "RouteRecommendation",
    "SKU",
    "Supplier",
    "SupplierRisk",
    "SupplyChainConfig",
    "SupplyChainOperation",
    "SupplyChainPackRecord",
    "SupplyChainReport",
    "SupplyChainRequest",
]
