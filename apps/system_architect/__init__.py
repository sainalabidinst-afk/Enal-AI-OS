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

from typing import Any

from apps.base import BaseReferenceApp
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


class SystemArchitectApp(BaseReferenceApp):
    name = "system-architect"
    version = "1.0.0"
    description = "Architecture review, governance, and design guidance"
    category = "architecture"
    pipeline = ["perception", "analysis", "reasoning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = SystemArchitectWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return await self.worker.execute(task)


def get_app() -> SystemArchitectApp:
    return SystemArchitectApp()

__all__ = [
    "SystemArchitectApp",
    "get_app",
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

