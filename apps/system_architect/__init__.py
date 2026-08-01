"""
System Architect — architectural authority layer for ECP.

Provides architecture review, Clean Architecture/DDD guidance, event-driven
design, CQRS evaluation, microservices/monolith analysis, and ADR generation
for all ECP projects and Capability Packs — without modifying Core.

Pipeline:
    ArchitectureReviewRequest
        ↓
    DependencyGraph (import graph, circular deps, layer classification)
        ↓
    LayerAnalysis (Clean Architecture violations)
        ↓
    DDDAnalysis (bounded contexts, aggregates, anti-corruption)
        ↓
    EventAnalysis (event schema, saga patterns)
        ↓
    CQRSEvaluation (command/query separation)
        ↓
    MicroservicesReview (decomposition, migration)
        ↓
    BoundaryEnforcement (package boundary violations)
        ↓
    ADRGeneration (structured ADR drafts)
        ↓
    ArchitectureReviewReport
"""

from apps.system_architect.engine import SystemArchitectEngine
from apps.system_architect.worker import SystemArchitectWorker
from apps.system_architect.schemas import (
    ArchitectureReviewRequest,
    ArchitectureReviewReport,
    ArchitectureReviewRecord,
    ReviewType,
    ArchitectureStyle,
    Severity,
    FindingCategory,
    Impact,
    Priority,
    Effort,
    ADRStatus,
    ReviewOutcome,
    Finding,
    ADRDraft,
    BoundedContext,
    DDDAssessment,
    ArchitectureMetrics,
    Recommendation,
    ReviewSummary,
)

__all__ = [
    "SystemArchitectEngine",
    "SystemArchitectWorker",
    "ArchitectureReviewRequest",
    "ArchitectureReviewReport",
    "ArchitectureReviewRecord",
    "ReviewType",
    "ArchitectureStyle",
    "Severity",
    "FindingCategory",
    "Impact",
    "Priority",
    "Effort",
    "ADRStatus",
    "ReviewOutcome",
    "Finding",
    "ADRDraft",
    "BoundedContext",
    "DDDAssessment",
    "ArchitectureMetrics",
    "Recommendation",
    "ReviewSummary",
]

