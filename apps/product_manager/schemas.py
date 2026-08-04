"""
Product Manager — Public Contracts (Pydantic schemas).

Defines the input (ProductManagementRequest) and output (ProductManagementReport)
contracts for the Product Manager Capability Pack, plus all supporting types.

These schemas follow the RFC-0017 contract definitions exactly.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class OperationType(str, Enum):
    roadmap_management = "roadmap_management"
    backlog_management = "backlog_management"
    sprint_planning = "sprint_planning"
    okr_tracking = "okr_tracking"
    prioritization = "prioritization"
    release_coordination = "release_coordination"


class Priority(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class PrioritizationFramework(str, Enum):
    rice = "rice"
    moscow = "moscow"
    value_effort = "value_effort"
    custom = "custom"


class ProductContext(BaseModel):
    product_name: str = Field(default="", description="Product name")
    vision: str = Field(default="", description="Product vision")
    strategy: str = Field(default="", description="Product strategy")
    target_users: list[str] = Field(default_factory=list)


class BacklogItem(BaseModel):
    id: str = Field(default="")
    title: str = Field(default="")
    description: str = Field(default="")
    effort: str = Field(default="medium")
    value: str = Field(default="medium")
    dependencies: list[str] = Field(default_factory=list)


class BacklogInput(BaseModel):
    items: list[BacklogItem] = Field(default_factory=list)


class RoadmapItem(BaseModel):
    id: str = Field(default="")
    title: str = Field(default="")
    target_date: str = Field(default="")
    status: str = Field(default="planned")


class RoadmapInput(BaseModel):
    items: list[RoadmapItem] = Field(default_factory=list)


class KeyResult(BaseModel):
    description: str = Field(default="")
    target: str = Field(default="")
    current: str = Field(default="")


class Objective(BaseModel):
    id: str = Field(default="")
    objective: str = Field(default="")
    key_results: list[KeyResult] = Field(default_factory=list)


class OKRInput(BaseModel):
    objectives: list[Objective] = Field(default_factory=list)


class Constraints(BaseModel):
    team_capacity: str = Field(default="")
    budget: str = Field(default="")
    timeline: str = Field(default="")


class PrioritizationOptions(BaseModel):
    prioritization_framework: PrioritizationFramework = Field(default=PrioritizationFramework.rice)
    sprint_duration_weeks: int = Field(default=2)


class ProductManagementRequest(BaseModel):
    """Input contract for a product management request."""

    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: OperationType = Field(..., description="Type of product management operation")
    product_context: ProductContext = Field(default_factory=ProductContext)
    inputs: Any = Field(default=None, description="Dynamic inputs based on operation")
    constraints: Constraints = Field(default_factory=Constraints)
    options: PrioritizationOptions = Field(default_factory=PrioritizationOptions)


class ProductManagementReport(BaseModel):
    """Output contract for a product management report."""

    request_id: str = Field(..., description="Reference to the original request")
    operation: str = Field(..., description="The operation performed")
    roadmap: dict[str, Any] = Field(default_factory=dict)
    backlog: dict[str, Any] = Field(default_factory=dict)
    sprint_plan: dict[str, Any] = Field(default_factory=dict)
    okrs: dict[str, Any] = Field(default_factory=dict)
    prioritization: dict[str, Any] = Field(default_factory=dict)
    release_plan: dict[str, Any] = Field(default_factory=dict)
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0)
    explanation: str = Field(default="")
    raw: dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()


class ProductRecord(BaseModel):
    """Persistent record for Experience Memory."""

    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str = Field(..., description="Reference to ProductManagementRequest")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    operation: str = Field(default="")
    product_name: str = Field(default="")
    backlog_items_managed: int = Field(default=0)
    okrs_tracked: int = Field(default=0)
    sprints_planned: int = Field(default=0)
    releases_coordinated: int = Field(default=0)
    outcome: str = Field(default="pending", description="success|partial|failed|revised")
