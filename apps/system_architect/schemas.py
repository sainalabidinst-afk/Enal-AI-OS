"""
System Architect — Public Contracts (Pydantic schemas).

Defines the input (ArchitectureReviewRequest) and output (ArchitectureReviewReport)
contracts for the System Architect Capability Pack, plus all supporting types.

These schemas follow the RFC-0011 contract definitions exactly.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ReviewType(str, Enum):
    full_review = "full_review"
    clean_architecture = "clean_architecture"
    ddd = "ddd"
    event_driven = "event_driven"
    cqrs = "cqrs"
    microservices = "microservices"
    package_boundary = "package_boundary"
    adr_generation = "adr_generation"


class ArchitectureStyle(str, Enum):
    clean_architecture = "clean_architecture"
    layered = "layered"
    hexagonal = "hexagonal"
    ddd = "ddd"
    microservices = "microservices"
    monolith = "monolith"
    event_driven = "event_driven"


class Severity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class FindingCategory(str, Enum):
    layer_violation = "layer_violation"
    dependency_cycle = "dependency_cycle"
    package_boundary = "package_boundary"
    ddd_violation = "ddd_violation"
    event_design = "event_design"
    cqrs_mismatch = "cqrs_mismatch"
    monolith_anti_pattern = "monolith_anti_pattern"
    architecture_smell = "architecture_smell"


class Impact(str, Enum):
    scalability = "scalability"
    maintainability = "maintainability"
    testability = "testability"
    deployability = "deployability"
    modifiability = "modifiability"


class Priority(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class Effort(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ADRStatus(str, Enum):
    proposed = "proposed"
    accepted = "accepted"
    rejected = "rejected"


class ReviewOutcome(str, Enum):
    accepted = "accepted"
    partially_accepted = "partially_accepted"
    rejected = "rejected"
    revised = "revised"


# ---------------------------------------------------------------------------
# Input model
# ---------------------------------------------------------------------------

class ArchitectureReviewRequest(BaseModel):
    """Input contract for an architecture review request."""

    review_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique review identifier")
    review_type: ReviewType = Field(default=ReviewType.full_review, description="Type of architectural review")
    workspace_path: str = Field(..., description="Path to project or workspace to review")
    architecture_style: ArchitectureStyle = Field(
        default=ArchitectureStyle.clean_architecture,
        description="Expected architecture style of the project",
    )
    existing_adrs: list[str] = Field(default_factory=list, description="ADR IDs already in effect")
    constraints: list[str] = Field(default_factory=list, description="Architectural constraints")
    focus_areas: list[Impact] = Field(default_factory=list, description="Architectural qualities to focus on")
    include_recommendations: bool = Field(default=True, description="Whether to include remediation recommendations")


# ---------------------------------------------------------------------------
# Output sub-models
# ---------------------------------------------------------------------------

class Finding(BaseModel):
    """A single architectural finding."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Finding identifier")
    category: FindingCategory = Field(..., description="Finding category")
    severity: Severity = Field(..., description="Finding severity")
    title: str = Field(..., description="Short title")
    description: str = Field(default="", description="Detailed description")
    evidence: dict[str, Any] = Field(default_factory=dict, description="File path, line, code snippet")
    recommendation: str = Field(default="", description="Suggested remediation")
    impact: Impact = Field(default=Impact.maintainability, description="Affected architectural quality")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence score (0-1)")


class ADRDraft(BaseModel):
    """Generated Architecture Decision Record draft."""

    title: str = Field(default="", description="ADR title")
    status: ADRStatus = Field(default=ADRStatus.proposed, description="ADR status")
    context: str = Field(default="", description="Decision context")
    decision: str = Field(default="", description="The decision made")
    consequences: list[str] = Field(default_factory=list, description="Consequences of the decision")


class BoundedContext(BaseModel):
    """A DDD bounded context."""

    name: str = Field(default="", description="Context name")
    entities: list[str] = Field(default_factory=list, description="Entities in this context")
    value_objects: list[str] = Field(default_factory=list, description="Value objects")
    aggregates: list[str] = Field(default_factory=list, description="Aggregates")
    repositories: list[str] = Field(default_factory=list, description="Repositories")


class DDDAssessment(BaseModel):
    """DDD pattern assessment output."""

    bounded_contexts: list[BoundedContext] = Field(default_factory=list, description="Detected bounded contexts")
    anti_corruption_layers: list[str] = Field(default_factory=list, description="Anti-corruption layers found")
    domain_events: list[str] = Field(default_factory=list, description="Domain events detected")


class ArchitectureMetrics(BaseModel):
    """Quantitative architecture metrics."""

    dependency_cycles: int = Field(default=0, description="Number of circular dependencies")
    layer_violations: int = Field(default=0, description="Number of layer violations")
    package_boundaries_crossed: int = Field(default=0, description="Unauthorized cross-package imports")
    maintainability_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Maintainability score (0-100)")
    scalability_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Scalability score (0-100)")
    testability_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Testability score (0-100)")


class Recommendation(BaseModel):
    """A remediation recommendation."""

    priority: Priority = Field(..., description="Recommendation priority")
    problem: str = Field(..., description="Problem being addressed")
    solution: str = Field(default="", description="Proposed solution")
    effort: Effort = Field(default=Effort.medium, description="Estimated effort")
    impact: str = Field(default="", description="Expected impact")


class ReviewSummary(BaseModel):
    """Summary statistics for the review report."""

    total_findings: int = Field(default=0)
    critical_count: int = Field(default=0)
    high_count: int = Field(default=0)
    medium_count: int = Field(default=0)
    low_count: int = Field(default=0)
    overall_risk: Severity = Field(default=Severity.low, description="Overall project risk level")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Overall review confidence")


# ---------------------------------------------------------------------------
# Output model
# ---------------------------------------------------------------------------

class ArchitectureReviewReport(BaseModel):
    """Output contract for an architecture review report."""

    review_id: str = Field(..., description="Reference to the original review request")
    review_type: ReviewType = Field(default=ReviewType.full_review, description="Type of review performed")
    findings: list[Finding] = Field(default_factory=list, description="All architectural findings")
    adr_draft: ADRDraft = Field(default_factory=ADRDraft, description="Generated ADR draft")
    ddd_assessment: DDDAssessment = Field(default_factory=DDDAssessment, description="DDD analysis output")
    architecture_metrics: ArchitectureMetrics = Field(default_factory=ArchitectureMetrics, description="Quantitative metrics")
    recommendations: list[Recommendation] = Field(default_factory=list, description="Remediation recommendations")
    summary: ReviewSummary = Field(default_factory=ReviewSummary, description="Summary statistics")

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dict."""
        return self.model_dump()


# ---------------------------------------------------------------------------
# Architecture Review Record (Experience Memory)
# ---------------------------------------------------------------------------

class ArchitectureReviewRecord(BaseModel):
    """Persistent record of an architecture review for Experience Memory."""

    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Record identifier")
    review_id: str = Field(..., description="Reference to the review")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat(), description="ISO 8601 timestamp")
    review_type: ReviewType = Field(default=ReviewType.full_review, description="Type of review")
    total_findings: int = Field(default=0)
    violations_detected: int = Field(default=0)
    adr_generated: bool = Field(default=False)
    recommendations_count: int = Field(default=0)
    outcome: ReviewOutcome = Field(default=ReviewOutcome.accepted, description="Review outcome")
    adr_status: ADRStatus = Field(default=ADRStatus.proposed, description="ADR status")
    revisions: list[dict[str, Any]] = Field(default_factory=list, description="Revision history")

