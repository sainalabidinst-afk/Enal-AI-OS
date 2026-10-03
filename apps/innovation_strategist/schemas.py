"""
Innovation Strategist Schemas
===============================

Typed contracts for the Innovation Strategist capability pack.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class InnovationStrategistOperation(StrEnum):
    trend_analysis = "trend_analysis"
    portfolio_planning = "portfolio_planning"
    foresight_scenarios = "foresight_scenarios"
    competitive_intelligence = "competitive_intelligence"


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=5, ge=1)
    budget_monthly_usd: float = Field(default=10000, ge=0)


class InnovationStrategistInputs(BaseModel):
    operation: InnovationStrategistOperation
    domain: str = ""
    technologies: list[str] = Field(default_factory=list)
    competitors: list[str] = Field(default_factory=list)
    budget_allocated: float = Field(default=0, ge=0)
    timeframe_months: int = Field(default=24, ge=1)
    risk_tolerance: str = "medium"
    existing_portfolio: list[str] = Field(default_factory=list)
    research_areas: list[str] = Field(default_factory=list)


class TechTrend(BaseModel):
    technology: str
    maturity: str
    growth_rate_pct: float
    relevance_score: float
    adoption_timeline: str = ""
    risks: list[str] = Field(default_factory=list)


class PortfolioItem(BaseModel):
    initiative_name: str
    category: str
    estimated_cost: float
    expected_roi: float
    timeline_months: int
    priority: str = "medium"
    risk_level: str = "medium"
    strategic_alignment: float = 0.8


class ForesightScenario(BaseModel):
    scenario_name: str
    description: str
    probability: float
    timeline_years: float
    strategic_impact: str
    triggers: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)


class InnovationStrategistReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tech_trends: list[TechTrend] = Field(default_factory=list)
    portfolio_items: list[PortfolioItem] = Field(default_factory=list)
    foresight_scenarios: list[ForesightScenario] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    quality_score: float = Field(default=0.90, ge=0, le=1)
    model_version: str = "1.0.0"


class InnovationStrategistRecord(BaseModel):
    pack_id: str = "innovation-strategist"
    version: str = "2.9.0"
    capabilities: list[str] = Field(
        default_factory=lambda: [
            "trend_analysis",
            "portfolio_planning",
            "foresight_scenarios",
            "competitive_intelligence",
        ]
    )


class InnovationStrategistRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    business_context: BusinessContext
    inputs: InnovationStrategistInputs
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


__all__ = [
    "InnovationStrategistInputs",
    "InnovationStrategistOperation",
    "InnovationStrategistRequest",
    "InnovationStrategistReport",
    "InnovationStrategistRecord",
    "TechTrend",
    "PortfolioItem",
    "ForesightScenario",
    "BusinessContext",
]
