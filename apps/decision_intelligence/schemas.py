"""
Decision Intelligence — Public Contracts (Pydantic schemas).

Defines the input (DecisionRequest) and output (DecisionResult) contracts
for the Decision Intelligence Capability Pack, plus all supporting types.

These schemas follow the RFC-0007 contract definitions exactly.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class EvidenceSourceType(str, Enum):
    analysis = "analysis"
    recommendation = "recommendation"
    data = "data"
    benchmark = "benchmark"
    historical = "historical"


class ObjectiveGoal(str, Enum):
    maximize = "maximize"
    minimize = "minimize"


class RiskTolerance(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class DecisionOutcome(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    revised = "revised"


# ---------------------------------------------------------------------------
# Input models
# ---------------------------------------------------------------------------

class EvidenceSource(BaseModel):
    """A single evidence payload from a source Capability Pack."""

    source_id: str = Field(..., description="Capability ID or external source identifier")
    evidence_type: EvidenceSourceType = Field(..., description="Category of evidence")
    payload: dict[str, Any] = Field(default_factory=dict, description="Structured evidence payload")
    quality_score: float = Field(default=0.5, ge=0.0, le=1.0, description="Quality of this evidence (0-1)")
    weight: float = Field(default=1.0, ge=0.0, le=10.0, description="Relative importance weight")


class Objective(BaseModel):
    """A single objective for trade-off analysis."""

    name: str = Field(..., description="Objective name, e.g. Accuracy, Risk, Cost")
    weight: float = Field(default=0.25, ge=0.0, le=1.0, description="Relative weight (sum across objectives should be 1.0)")
    goal: ObjectiveGoal = Field(default=ObjectiveGoal.maximize, description="Whether to maximize or minimize")


class DecisionRequest(BaseModel):
    """Input contract for a decision intelligence request."""

    decision_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique decision identifier")
    context: str = Field(..., description="Natural language description of the decision to be made")
    evidence_sources: list[EvidenceSource] = Field(default_factory=list, description="Evidence from source Capability Packs")
    constraints: list[str] = Field(default_factory=list, description="Hard constraints that eliminate alternatives")
    objectives: list[Objective] = Field(default_factory=list, description="Weighted objectives for trade-off analysis")
    risk_tolerance: RiskTolerance = Field(default=RiskTolerance.medium, description="Risk tolerance level")
    max_alternatives: int = Field(default=5, ge=1, le=20, description="Maximum number of alternatives to generate")
    include_explanation: bool = Field(default=True, description="Whether to generate a full explanation chain")

    @field_validator("objectives")
    @classmethod
    def validate_objective_weights(cls, v: list[Objective]) -> list[Objective]:
        """Warn if objective weights do not sum to ~1.0."""
        if v:
            total = sum(o.weight for o in v)
            if abs(total - 1.0) > 0.01:
                raise ValueError(
                    f"Objective weights sum to {total:.2f}, expected ~1.0. "
                    f"Adjust weights so they sum to 1.0."
                )
        return v


# ---------------------------------------------------------------------------
# Output sub-models
# ---------------------------------------------------------------------------

class RiskProfile(BaseModel):
    """Risk assessment for a single alternative."""

    overall_risk: float = Field(default=0.0, ge=0.0, le=1.0, description="Composite risk score (0=low, 1=high)")
    probability: float = Field(default=0.0, ge=0.0, le=1.0, description="Probability of adverse outcome")
    impact: float = Field(default=0.0, ge=0.0, le=1.0, description="Impact if adverse outcome occurs")
    risk_factors: list[str] = Field(default_factory=list, description="Specific risk factors identified")


class TradeOff(BaseModel):
    """Trade-off scores for a single alternative."""

    accuracy: float = Field(default=0.0, ge=0.0, le=1.0)
    cost: float = Field(default=0.0, ge=0.0, le=1.0)
    latency: float = Field(default=0.0, ge=0.0, le=1.0)

    model_config = {"extra": "allow"}


class Alternative(BaseModel):
    """A single alternative considered in the decision."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Alternative identifier")
    description: str = Field(..., description="Description of this alternative")
    score: float = Field(default=0.0, ge=0.0, le=1.0, description="Composite decision score (0-1)")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence in this alternative's score")
    risk_profile: RiskProfile = Field(default_factory=RiskProfile, description="Risk assessment")
    trade_offs: TradeOff = Field(default_factory=TradeOff, description="Trade-off scores")


class ConfidenceScore(BaseModel):
    """Confidence estimation output."""

    score: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence score (0-1)")
    uncertainty_bound: float = Field(default=0.0, ge=0.0, le=1.0, description="Uncertainty margin")
    explanation: str = Field(default="", description="Why this confidence level was assigned")


class Explanation(BaseModel):
    """Full explainability chain."""

    evidence_summary: str = Field(default="", description="Summary of evidence collected")
    reasoning_chain: list[str] = Field(default_factory=list, description="Step-by-step reasoning")
    simulation_results: dict[str, Any] = Field(default_factory=dict, description="Simulation or scoring details")
    risk_assessment: str = Field(default="", description="Risk assessment summary")
    final_rationale: str = Field(default="", description="Final rationale for the recommended decision")


class DecisionRecord(BaseModel):
    """Persistent record of a decision for Experience Memory."""

    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Record identifier")
    decision_id: str = Field(..., description="Reference to the original decision")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat(), description="ISO 8601 timestamp")
    context: str = Field(default="", description="Decision context")
    chosen_alternative: str = Field(default="", description="The selected alternative description")
    alternatives_count: int = Field(default=0, description="Number of alternatives considered")
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    evidence_count: int = Field(default=0, description="Number of evidence items used")
    risk_score: float = Field(default=0.0, ge=0.0, le=1.0)
    explanation: str = Field(default="", description="Decision explanation summary")
    outcome: DecisionOutcome = Field(default=DecisionOutcome.pending, description="Current outcome status")
    user_feedback: str | None = Field(default=None, description="Optional user feedback")
    revision_history: list[dict[str, Any]] = Field(default_factory=list, description="Revision history entries")


# ---------------------------------------------------------------------------
# Output model
# ---------------------------------------------------------------------------

class DecisionResult(BaseModel):
    """Output contract for a decision intelligence result."""

    decision_id: str = Field(..., description="Reference to the original decision request")
    recommended_decision: str = Field(default="", description="The chosen alternative or action")
    alternatives: list[Alternative] = Field(default_factory=list, description="All alternatives considered")
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Overall confidence in the recommendation")
    confidence_explanation: str = Field(default="", description="Explanation of the confidence score")
    explanation: Explanation = Field(default_factory=Explanation, description="Full explainability chain")
    decision_history_ref: str = Field(default="", description="Reference to Experience Memory entry")
    raw: dict[str, Any] = Field(default_factory=dict, description="Raw diagnostic data for auditability")

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dict."""
        return self.model_dump()
