"""
Pydantic schemas for the REA Capability Pack.

Defines evidence-based reverse engineering result models:
    * REAEvidence — atomic observation/inference unit with ID
    * REAAnalysisResult — full analysis result for a target
    * REAArtifactInspection — per-file/type inspection entry
    * REARequest — task request submitted to the pack
    * REAResponse — pack response returned to the caller
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class REATargetType(StrEnum):
    """Types of targets REA can analyse."""

    NATIVE = "native"
    ELECTRON_JS = "electron_js"
    DOTNET = "dotnet"
    WEB = "web"
    UNKNOWN = "unknown"


class REAEvidence(BaseModel):
    """Atomic evidence entry produced by REA analysis.

    Every conclusion in ECP must trace back to one or more evidence IDs so
    that AI reasoning stays evidence-based rather than speculative.
    """

    evidence_id: str = Field(
        default_factory=lambda: f"EVID-{uuid4().hex[:8]}",
        description="Unique evidence identifier",
    )
    target_type: REATargetType = Field(
        default=REATargetType.UNKNOWN,
        description="Type of reverse-engineering target",
    )
    target_path: str = Field(..., description="Path/URL of the analysed target")
    summary: str = Field(..., description="Human-readable summary of findings")
    observations: list[str] = Field(
        default_factory=list,
        description="Direct observations (what was seen)",
    )
    inferences: list[str] = Field(
        default_factory=list,
        description="Logical inferences drawn from observations",
    )
    unknowns: list[str] = Field(
        default_factory=list,
        description="Items that could not be determined",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Raw REA/engine-specific metadata",
    )


class REAArtifactInspection(BaseModel):
    """Inspection result for a single artifact (file, function, IPC channel)."""

    artifact_id: str = Field(..., description="Unique artifact identifier")
    artifact_type: str = Field(..., description="Kind of artifact (function, class, IPC, etc.)")
    path: str = Field(..., description="File path or location within target")
    evidence_refs: list[str] = Field(
        default_factory=list,
        description="Evidence IDs supporting this inspection",
    )
    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence score for this inspection",
    )
    details: dict[str, Any] = Field(
        default_factory=dict,
        description="Raw inspection details",
    )


class REAAnalysisResult(BaseModel):
    """Complete reverse-engineering analysis result for a target."""

    analysis_id: str = Field(
        default_factory=lambda: f"ANA-{uuid4().hex[:8]}",
        description="Unique analysis identifier",
    )
    target_path: str = Field(..., description="Analysed target path")
    target_type: REATargetType = Field(
        default=REATargetType.UNKNOWN,
        description="Type of target analysed",
    )
    summary: str = Field(..., description="Overall analysis summary")
    evidence: list[REAEvidence] = Field(
        default_factory=list,
        description="All evidence collected during analysis",
    )
    artifacts: list[REAArtifactInspection] = Field(
        default_factory=list,
        description="Individual artifact inspections",
    )
    findings: list[str] = Field(
        default_factory=list,
        description="High-level findings suitable for display",
    )
    recommendations: list[str] = Field(
        default_factory=list,
        description="Recommended follow-up actions",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Raw REA engine output",
    )


class REARequest(BaseModel):
    """Task request submitted to the REA Capability Pack."""

    query: str = Field(..., description="Natural-language analysis request")
    target_path: str | None = Field(
        default=None,
        description="Path to the target binary/app to analyse",
    )
    target_type: REATargetType | None = Field(
        default=None,
        description="Hint about target type (auto-detected if omitted)",
    )
    deep_analysis: bool = Field(
        default=False,
        description="Request deeper/heuristic REA analysis",
    )


class REAResponse(BaseModel):
    """Pack response returned to the caller."""

    status: str = Field(..., description="success | info | error")
    pack: str = Field(default="reverse-engineer", description="Capability pack name")
    version: str = Field(default="1.0.0", description="Pack version")
    result: REAAnalysisResult | None = Field(
        default=None,
        description="Full analysis result when available",
    )
    message: str | None = Field(
        default=None,
        description="Human-readable status/informational message",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata",
    )
