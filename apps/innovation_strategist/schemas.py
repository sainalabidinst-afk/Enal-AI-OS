"""
Innovation Strategist Capability Schemas
==========================================

Typed contracts for the Innovation Strategist capability pack.
Defines input (InnovationRequest) and output (InnovationReport) contracts for
trend analysis, technology foresight, competitive intelligence, and scenario planning.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class InnovationOperation(StrEnum):
    trend_analysis = "trend_analysis"
    technology_forecast = "technology_forecast"
    competitive_intelligence = "competitive_intelligence"
    scenario_planning = "scenario_planning"


class TrendCategory(StrEnum):
    emerging_technology = "emerging_technology"
    market_dynamics = "market_dynamics"
    regulatory_change = "regulatory_change"
    consumer_behavior = "consumer_behavior"
    sustainability = "sustainability"


class TrendImpact(StrEnum):
    transformative = "transformative"
    high = "high"
    medium = "medium"
    low = "low"


class TrendTimeframe(StrEnum):
    short_term = "short_term"
    medium_term = "medium_term"
    long_term = "long_term"


class ScenarioLikelihood(StrEnum):
    unlikely = "unlikely"
    possible = "possible"
    likely = "likely"
    certain = "certain"


class TechnologyDomain(BaseModel):
    name: str
    description: str
    maturity_level: str = "emerging"


class TrendDataPoint(BaseModel):
    timestamp: str
    value: float
    source: str = ""


class Competitor(BaseModel):
    name: str
    market_share: float = 0.0
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=6, ge=1)


class InnovationConfig(BaseModel):
    operation: InnovationOperation
    trend_categories: list[TrendCategory] = Field(default_factory=list)
    technology_domains: list[TechnologyDomain] = Field(default_factory=list)
    competitors: list[Competitor] = Field(default_factory=list)
    historical_trends: dict[str, list[TrendDataPoint]] = Field(default_factory=dict)
    time_horizon: TrendTimeframe = TrendTimeframe.medium_term
    confidence_level: float = Field(default=0.8, ge=0.0, le=1.0)
    constraints: dict[str, Any] = Field(default_factory=dict)


class InnovationRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: str = "trend_analysis"
    business_context: BusinessContext
    inputs: InnovationConfig
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


class TrendSignal(BaseModel):
    id: str
    name: str
    category: TrendCategory
    description: str
    impact: TrendImpact
    timeframe: TrendTimeframe
    current_adoption: float = Field(default=0.0, ge=0.0, le=1.0)
    growth_rate: float = 0.0
    evidence: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class TechnologyForecast(BaseModel):
    technology: str
    domain: str
    adoption_curve: dict[str, float] = Field(default_factory=dict)
    peak_year: int = 0
    mainstream_year: int = 0
    plateau_year: int = 0
    risk_factors: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class CompetitiveInsight(BaseModel):
    competitor: str
    strength: str
    weakness: str
    market_position: str
    threat_level: TrendImpact
    opportunity: str


class Scenario(BaseModel):
    name: str
    description: str
    likelihood: ScenarioLikelihood
    impact: TrendImpact
    probability_score: float = Field(default=0.0, ge=0.0, le=1.0)
    key_drivers: list[str] = Field(default_factory=list)
    implications: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)


class InnovationOpportunity(BaseModel):
    title: str
    description: str
    trend_ids: list[str] = Field(default_factory=list)
    potential_value: float = 0.0
    implementation_effort: TrendImpact
    time_to_market: TrendTimeframe
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class InnovationReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    operation: InnovationOperation
    trend_signals: list[TrendSignal] = Field(default_factory=list)
    forecasts: list[TechnologyForecast] = Field(default_factory=list)
    competitive_insights: list[CompetitiveInsight] = Field(default_factory=list)
    scenarios: list[Scenario] = Field(default_factory=list)
    opportunities: list[InnovationOpportunity] = Field(default_factory=list)
    strategic_narrative: str = ""
    model_version: str = "1.0.0"


class InnovationStrategistPackRecord(BaseModel):
    pack_id: str = "innovation-strategist"
    version: str = "1.0.0"
    capabilities: list[str] = Field(default_factory=lambda: [
        "trend_analysis",
        "technology_forecast",
        "competitive_intelligence",
        "scenario_planning",
    ])


__all__ = [
    "BusinessContext",
    "CompetitiveInsight",
    "Competitor",
    "InnovationConfig",
    "InnovationOperation",
    "InnovationOpportunity",
    "InnovationReport",
    "InnovationRequest",
    "InnovationStrategistPackRecord",
    "Scenario",
    "ScenarioLikelihood",
    "TechnologyDomain",
    "TechnologyForecast",
    "TrendCategory",
    "TrendDataPoint",
    "TrendImpact",
    "TrendSignal",
    "TrendTimeframe",
]
