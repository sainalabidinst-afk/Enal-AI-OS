"""
Research Assistant — Public Contracts (Pydantic schemas).

Defines the input (ResearchRequest) and output (ResearchReport) contracts
for the Research Assistant Capability Pack, plus all supporting types.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ResearchOperation(str, Enum):
    literature_review = "literature_review"
    evidence_gathering = "evidence_gathering"
    contradiction_analysis = "contradiction_analysis"
    citation_assessment = "citation_assessment"
    confidence_estimation = "confidence_estimation"
    synthesis = "synthesis"
    report_generation = "report_generation"


class SourceType(str, Enum):
    journal = "journal"
    conference = "conference"
    book = "book"
    preprint = "preprint"
    thesis = "thesis"
    report = "report"
    website = "website"
    dataset = "dataset"


class SourceQuality(str, Enum):
    peer_reviewed = "peer_reviewed"
    expert_review = "expert_review"
    editorial = "editorial"
    unverified = "unverified"


class CitationStyle(str, Enum):
    apa = "apa"
    mla = "mla"
    chicago = "chicago"
    ieee = "ieee"
    harvard = "harvard"


class ConfidenceLevel(str, Enum):
    very_high = "very_high"
    high = "high"
    moderate = "moderate"
    low = "low"
    very_low = "very_low"


class FindingSeverity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    informational = "informational"


class ContradictionType(str, Enum):
    methodological = "methodological"
    results = "results"
    interpretation = "interpretation"
    sample = "sample"
    theoretical = "theoretical"


class Evidence(BaseModel):
    """A piece of evidence from a research source."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., description="Title of the source")
    authors: list[str] = Field(default_factory=list, description="List of authors")
    year: int = Field(default=0, description="Publication year")
    source_type: SourceType = Field(..., description="Type of source")
    source_quality: SourceQuality = Field(..., description="Quality assessment of source")
    content: str = Field(..., description="Content or abstract of the evidence")
    url: str | None = Field(default=None, description="URL or DOI if available")
    citation: str = Field(default="", description="Formatted citation")
    recency_score: float = Field(default=0.0, ge=0.0, le=1.0, description="How recent the source is (0-1)")
    methodology_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Quality of methodology (0-1)")
    relevance_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Relevance to query (0-1)")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence in this evidence (0-1)")
    keywords: list[str] = Field(default_factory=list, description="Keywords extracted from source")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class Citation(BaseModel):
    """A formatted citation with quality assessment."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    evidence_id: str = Field(..., description="Reference to the evidence")
    style: CitationStyle = Field(..., description="Citation style used")
    text: str = Field(..., description="Formatted citation text")
    completeness: float = Field(default=0.0, ge=0.0, le=1.0, description="Completeness score (0-1)")
    format_accuracy: float = Field(default=0.0, ge=0.0, le=1.0, description="Format accuracy (0-1)")
    provenance_traceability: float = Field(default=0.0, ge=0.0, le=1.0, description="Provenance traceability (0-1)")
    overall_quality: float = Field(default=0.0, ge=0.0, le=1.0, description="Overall citation quality (0-1)")
    issues: list[str] = Field(default_factory=list, description="Issues found with citation")


class Contradiction(BaseModel):
    """A detected contradiction between sources."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: ContradictionType = Field(..., description="Type of contradiction")
    evidence_a: str = Field(..., description="First evidence ID")
    evidence_b: str = Field(..., description="Second evidence ID")
    description: str = Field(..., description="Description of the contradiction")
    severity: FindingSeverity = Field(..., description="Severity of contradiction")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence in this contradiction (0-1)")
    resolution_suggestion: str = Field(default="", description="Suggested resolution or further investigation")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class Finding(BaseModel):
    """A research finding with quality assessment."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., description="Title of the finding")
    description: str = Field(..., description="Detailed description")
    evidence_ids: list[str] = Field(default_factory=list, description="Supporting evidence IDs")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence in finding (0-1)")
    uncertainty_factors: list[str] = Field(default_factory=list, description="Factors contributing to uncertainty")
    severity: FindingSeverity = Field(..., description="Severity/importance of finding")
    category: str = Field(default="general", description="Category of finding")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class Synthesis(BaseModel):
    """Synthesis of multiple sources into coherent narrative."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query: str = Field(..., description="Original research query")
    narrative: str = Field(..., description="Synthesized narrative text")
    supporting_evidence: list[str] = Field(default_factory=list, description="Evidence IDs supporting synthesis")
    contradicted_evidence: list[str] = Field(default_factory=list, description="Evidence IDs contradicted by synthesis")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence in synthesis (0-1)")
    gaps_identified: list[str] = Field(default_factory=list, description="Research gaps identified")
    future_work: list[str] = Field(default_factory=list, description="Suggested future work")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ResearchRequest(BaseModel):
    """Input contract for a research request."""

    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query: str = Field(..., description="Research question or topic")
    operation: ResearchOperation = Field(..., description="Type of research operation")
    sources: list[Evidence] = Field(default_factory=list, description="Pre-provided sources (optional)")
    citation_style: CitationStyle = Field(default=CitationStyle.apa, description="Preferred citation style")
    max_sources: int = Field(default=20, description="Maximum number of sources to retrieve")
    min_confidence: float = Field(default=0.5, ge=0.0, le=1.0, description="Minimum confidence threshold")
    include_contradictions: bool = Field(default=True, description="Whether to detect contradictions")
    include_citations: bool = Field(default=True, description="Whether to generate citations")
    context: dict[str, Any] = Field(default_factory=dict, description="Additional context")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ResearchReport(BaseModel):
    """Output contract for a research report."""

    request_id: str = Field(..., description="Reference to the original request")
    query: str = Field(..., description="Original research query")
    operation: str = Field(..., description="Operation performed")
    evidence: list[Evidence] = Field(default_factory=list, description="Gathered evidence")
    findings: list[Finding] = Field(default_factory=list, description="Research findings")
    contradictions: list[Contradiction] = Field(default_factory=list, description="Detected contradictions")
    citations: list[Citation] = Field(default_factory=list, description="Generated citations")
    synthesis: Synthesis | None = Field(default=None, description="Synthesized narrative")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Overall confidence (0-1)")
    uncertainty_factors: list[str] = Field(default_factory=list, description="Factors affecting uncertainty")
    report_markdown: str = Field(default="", description="Generated report in Markdown")
    raw: dict[str, Any] = Field(default_factory=dict, description="Raw analysis data")

    def to_dict(self) -> dict[str, Any]:
        return _serialize(self.model_dump())


class ResearchQualityRecord(BaseModel):
    """Record of research quality metrics for benchmarking."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str = Field(..., description="Reference to research request")
    operation: str = Field(..., description="Operation performed")
    evidence_count: int = Field(default=0, description="Number of evidence items")
    finding_count: int = Field(default=0, description="Number of findings")
    contradiction_count: int = Field(default=0, description="Number of contradictions detected")
    citation_accuracy: float = Field(default=0.0, ge=0.0, le=1.0, description="Citation accuracy score")
    evidence_quality_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Average evidence quality")
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Overall confidence score")
    completeness: float = Field(default=0.0, ge=0.0, le=1.0, description="Completeness of research")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


def _serialize(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return value.to_dict()
    if isinstance(value, list):
        return [_serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: _serialize(val) for key, val in value.items()}
    return value
