"""
Cloud Architect Schemas
=======================

Typed contracts for the Cloud Architect capability pack.
Defines input (CloudArchitectRequest) and output (CloudArchitectReport)
contracts for cloud architecture design and evaluation.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class CloudProvider(StrEnum):
    aws = "aws"
    azure = "azure"
    gcp = "gcp"
    hybrid = "hybrid"


class ArchitecturePattern(StrEnum):
    microservices = "microservices"
    serverless = "serverless"
    containerized = "containerized"
    vm_based = "vm_based"


class CostOptimizationStrategy(StrEnum):
    reserved_instances = "reserved_instances"
    spot_instances = "spot_instances"
    autoscaling = "autoscaling"
    rightsizing = "rightsizing"


class RegionStrategy(StrEnum):
    single_region = "single_region"
    multi_region = "multi_region"
    active_passive = "active_passive"
    active_active = "active_active"


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=5, ge=1)
    budget_monthly_usd: float = Field(default=10000, ge=0)


class LandingZoneSpec(BaseModel):
    provider: CloudProvider
    regions: list[str] = Field(default_factory=list)
    architecture_pattern: ArchitecturePattern
    region_strategy: RegionStrategy
    cost_strategy: list[CostOptimizationStrategy] = Field(default_factory=list)


class CloudArchitectRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: str = "cloud_design"
    business_context: BusinessContext
    inputs: LandingZoneSpec
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


class CloudComponent(BaseModel):
    name: str
    service_type: str
    provider: CloudProvider
    region: str
    estimated_monthly_cost: float
    sla: str = "99.9%"


class DRRecoveryPoint:
    pass


class CloudArchitectReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    provider: CloudProvider
    architecture_pattern: ArchitecturePattern
    landing_zone: dict[str, Any] = Field(default_factory=dict)
    multi_region_strategy: dict[str, Any] = Field(default_factory=dict)
    cost_optimization: dict[str, Any] = Field(default_factory=dict)
    disaster_recovery: dict[str, Any] = Field(default_factory=dict)
    recommendations: list[str] = Field(default_factory=list)
    architecture_diagram: str = ""
    quality_score: float = Field(default=0.90, ge=0, le=1)
    model_version: str = "1.0.0"

    class Config:
        arbitrary_types_allowed = True


class CloudArchitectRecord(BaseModel):
    pack_id: str = "cloud-architect"
    version: str = "1.0.0"
    capabilities: list[str] = Field(default_factory=lambda: [
        "landing_zone_design",
        "multi_region_strategy",
        "cost_optimization",
        "disaster_recovery",
    ])


__all__ = [
    "BusinessContext",
    "CloudArchitectReport",
    "CloudArchitectRequest",
    "CloudArchitectRecord",
    "CloudComponent",
    "CloudProvider",
    "CostOptimizationStrategy",
    "ArchitecturePattern",
    "LandingZoneSpec",
    "RegionStrategy",
]
