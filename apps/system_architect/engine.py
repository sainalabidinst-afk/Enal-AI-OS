"""
System Architect Engine — domain engine orchestrator.

Orchestrates the full architecture review pipeline:
    1. Dependency Graph (import graph, circular deps, layer classification)
    2. Layer Analysis (Clean Architecture violations)
    3. DDD Analysis (bounded contexts, aggregates, anti-corruption)
    4. Event Analysis (event schema, saga patterns)
    5. CQRS Evaluation (command/query separation)
    6. Microservices Review (decomposition, migration)
    7. Boundary Enforcement (package boundary violations)
    8. Governance (architecture rules, Core change guard)
    9. ADR Generation (structured ADR drafts)

All business logic resides here (per ADR-004). The Worker is a thin
adapter (per ADR-003).
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any

from apps.system_architect.schemas import (
    ArchitectureReviewRequest,
    ArchitectureReviewReport,
    ArchitectureReviewRecord,
    ReviewType,
    ReviewOutcome,
    ADRStatus,
    Severity,
    Finding,
    ADRDraft,
    ArchitectureMetrics,
    Recommendation,
    ReviewSummary,
)
from apps.system_architect.dependency_graph import DependencyGraphBuilder
from apps.system_architect.layer_analyzer import LayerAnalyzer
from apps.system_architect.ddd_analyzer import DDDAnalyzer
from apps.system_architect.event_analyzer import EventAnalyzer
from apps.system_architect.cqrs_evaluator import CQRSEvaluator
from apps.system_architect.microservices_analyzer import MicroservicesAnalyzer
from apps.system_architect.boundary_enforcer import BoundaryEnforcer
from apps.system_architect.governance import ArchitectureGovernance
from apps.system_architect.adr_generator import ADRGenerator
from apps.system_architect.scalability_analyzer import ScalabilityAnalyzer
from apps.system_architect.security_architect import SecurityArchitect
from apps.system_architect.cost_optimizer import CostOptimizer
from apps.system_architect.refactoring_strategy import RefactoringStrategy

logger = logging.getLogger(__name__)


class SystemArchitectEngine:
    """
    Orchestrates the full architecture review pipeline.

    Public API::
        engine = SystemArchitectEngine()
        report = await engine.review(request)
    """

    def __init__(self, adr_dir: str | Path | None = None) -> None:
        self.adr_dir = Path(adr_dir) if adr_dir else None
        self._layer_analyzer: LayerAnalyzer | None = None
        self._ddd_analyzer: DDDAnalyzer | None = None
        self._event_analyzer: EventAnalyzer | None = None
        self._cqrs_evaluator: CQRSEvaluator | None = None
        self._microservices_analyzer: MicroservicesAnalyzer | None = None
        self._boundary_enforcer: BoundaryEnforcer | None = None
        self._governance: ArchitectureGovernance | None = None
        self._scalability_analyzer: ScalabilityAnalyzer | None = None
        self._security_architect: SecurityArchitect | None = None
        self._cost_optimizer: CostOptimizer | None = None
        self._refactoring_strategy: RefactoringStrategy | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def review(self, request: ArchitectureReviewRequest) -> ArchitectureReviewReport:
        """
        Run the full architecture review pipeline.

        Args:
            request: ArchitectureReviewRequest with workspace path and review type.

        Returns:
            ArchitectureReviewReport with findings, metrics, ADR draft.
        """
        started = time.monotonic()
        workspace_path = Path(request.workspace_path)
        if not workspace_path.exists():
            raise FileNotFoundError(f"Workspace path not found: {request.workspace_path}")

        # Initialize analyzers for this workspace
        findings: list[Finding] = []
        metrics = ArchitectureMetrics()
        recommendations: list[Recommendation] = []
        ddd_assessment = None
        adr_draft: ADRDraft | None = None

        # 1. Complete review or selected review type
        review_types = self._resolve_review_types(request.review_type)

        if ReviewType.clean_architecture in review_types or ReviewType.full_review in review_types:
            layer_findings, layer_metrics, layer_recs = await self._get_layer_analyzer(workspace_path).analyze()
            findings.extend(layer_findings)
            metrics = self._merge_metrics(metrics, layer_metrics)
            recommendations.extend(layer_recs)

        if ReviewType.ddd in review_types or ReviewType.full_review in review_types:
            ddd_findings, assessment, ddd_recs = await self._get_ddd_analyzer(workspace_path).analyze()
            findings.extend(ddd_findings)
            ddd_assessment = assessment
            recommendations.extend(ddd_recs)

        if ReviewType.event_driven in review_types or ReviewType.full_review in review_types:
            event_findings, event_recs = await self._get_event_analyzer(workspace_path).analyze()
            findings.extend(event_findings)
            recommendations.extend(event_recs)

        if ReviewType.cqrs in review_types or ReviewType.full_review in review_types:
            cqrs_findings, cqrs_recs = await self._get_cqrs_evaluator(workspace_path).analyze()
            findings.extend(cqrs_findings)
            recommendations.extend(cqrs_recs)

        if ReviewType.microservices in review_types or ReviewType.full_review in review_types:
            ms_findings, ms_recs = await self._get_microservices_analyzer(workspace_path).analyze()
            findings.extend(ms_findings)
            recommendations.extend(ms_recs)

        if ReviewType.package_boundary in review_types or ReviewType.full_review in review_types:
            boundary_findings, boundary_metrics, boundary_recs = await self._get_boundary_enforcer(workspace_path).enforce()
            findings.extend(boundary_findings)
            metrics = self._merge_metrics(metrics, boundary_metrics)
            recommendations.extend(boundary_recs)

        # Governance always runs for full review
        if ReviewType.full_review in review_types:
            gov_findings, gov_recs = await self._get_governance(workspace_path).check()
            findings.extend(gov_findings)
            recommendations.extend(gov_recs)

        # Deeper knowledge expansion
        if ReviewType.full_review in review_types:
            scalability = self._get_scalability_analyzer().assess(metrics)
            findings.extend(self._get_scalability_analyzer().to_findings(scalability))

            security_findings = self._get_security_architect().review(metrics)
            findings.extend(security_findings)

            cost_findings = self._get_cost_optimizer().analyze(metrics)
            findings.extend(cost_findings)

            refactor_recs = self._get_refactoring_strategy().recommend(findings, metrics)
            recommendations.extend(refactor_recs)

        # 2. Compute consolidated metrics if not already set
        metrics = self._finalize_metrics(metrics, findings)

        # 3. Filter findings by focus areas
        if request.focus_areas:
            findings = [f for f in findings if f.impact in request.focus_areas] or findings

        # 4. Generate ADR draft
        adr_generator = ADRGenerator(existing_adrs=request.existing_adrs, adr_dir=self.adr_dir)
        adr_draft = adr_generator.generate(
            title=self._derive_adr_title(request),
            context=self._derive_adr_context(request),
            findings=findings,
        )

        # 5. Build summary
        summary = self._build_summary(findings)

        # 6. Filter recommendations if disabled
        if not request.include_recommendations:
            recommendations = []

        # Ensure ddd_assessment is never None
        from apps.system_architect.schemas import DDDAssessment as DDAssess
        safe_ddd = ddd_assessment if ddd_assessment is not None else DDAssess()

        report = ArchitectureReviewReport(
            review_id=request.review_id,
            review_type=request.review_type,
            findings=findings,
            adr_draft=adr_draft,
            ddd_assessment=safe_ddd,
            architecture_metrics=metrics,
            recommendations=recommendations,
            summary=summary,
        )
        return report

    # ------------------------------------------------------------------
    # Analyzer helpers
    # ------------------------------------------------------------------

    def _resolve_review_types(self, review_type: ReviewType) -> list[ReviewType]:
        """Resolve a review type into the analyzers to run."""
        if review_type == ReviewType.full_review:
            return [
                ReviewType.clean_architecture,
                ReviewType.ddd,
                ReviewType.event_driven,
                ReviewType.cqrs,
                ReviewType.microservices,
                ReviewType.package_boundary,
            ]
        return [review_type]

    def _get_layer_analyzer(self, workspace_path: Path) -> LayerAnalyzer:
        self._layer_analyzer = self._layer_analyzer or LayerAnalyzer(workspace_path)
        self._layer_analyzer.repo_path = workspace_path
        return self._layer_analyzer

    def _get_ddd_analyzer(self, workspace_path: Path) -> DDDAnalyzer:
        self._ddd_analyzer = self._ddd_analyzer or DDDAnalyzer(workspace_path)
        self._ddd_analyzer.repo_path = workspace_path
        return self._ddd_analyzer

    def _get_event_analyzer(self, workspace_path: Path) -> EventAnalyzer:
        self._event_analyzer = self._event_analyzer or EventAnalyzer(workspace_path)
        self._event_analyzer.repo_path = workspace_path
        return self._event_analyzer

    def _get_cqrs_evaluator(self, workspace_path: Path) -> CQRSEvaluator:
        self._cqrs_evaluator = self._cqrs_evaluator or CQRSEvaluator(workspace_path)
        self._cqrs_evaluator.repo_path = workspace_path
        return self._cqrs_evaluator

    def _get_microservices_analyzer(self, workspace_path: Path) -> MicroservicesAnalyzer:
        self._microservices_analyzer = self._microservices_analyzer or MicroservicesAnalyzer(workspace_path)
        self._microservices_analyzer.repo_path = workspace_path
        return self._microservices_analyzer

    def _get_boundary_enforcer(self, workspace_path: Path) -> BoundaryEnforcer:
        self._boundary_enforcer = self._boundary_enforcer or BoundaryEnforcer(workspace_path)
        self._boundary_enforcer.repo_path = workspace_path
        return self._boundary_enforcer

    def _get_governance(self, workspace_path: Path) -> ArchitectureGovernance:
        self._governance = self._governance or ArchitectureGovernance(workspace_path)
        self._governance.repo_path = workspace_path
        return self._governance

    def _get_scalability_analyzer(self) -> ScalabilityAnalyzer:
        self._scalability_analyzer = self._scalability_analyzer or ScalabilityAnalyzer()
        return self._scalability_analyzer

    def _get_security_architect(self) -> SecurityArchitect:
        self._security_architect = self._security_architect or SecurityArchitect()
        return self._security_architect

    def _get_cost_optimizer(self) -> CostOptimizer:
        self._cost_optimizer = self._cost_optimizer or CostOptimizer()
        return self._cost_optimizer

    def _get_refactoring_strategy(self) -> RefactoringStrategy:
        self._refactoring_strategy = self._refactoring_strategy or RefactoringStrategy()
        return self._refactoring_strategy

    # ------------------------------------------------------------------
    # Consolidation helpers
    # ------------------------------------------------------------------

    def _merge_metrics(self, base: ArchitectureMetrics, add: ArchitectureMetrics) -> ArchitectureMetrics:
        """Merge metrics from multiple analyzers (taking worst-case / max)."""
        return ArchitectureMetrics(
            dependency_cycles=base.dependency_cycles + add.dependency_cycles,
            layer_violations=base.layer_violations + add.layer_violations,
            package_boundaries_crossed=base.package_boundaries_crossed + add.package_boundaries_crossed,
            maintainability_score=min(base.maintainability_score, add.maintainability_score) if base.maintainability_score and add.maintainability_score else max(base.maintainability_score, add.maintainability_score),
            scalability_score=min(base.scalability_score, add.scalability_score) if base.scalability_score and add.scalability_score else max(base.scalability_score, add.scalability_score),
            testability_score=min(base.testability_score, add.testability_score) if base.testability_score and add.testability_score else max(base.testability_score, add.testability_score),
        )

    def _finalize_metrics(self, metrics: ArchitectureMetrics, findings: list[Finding]) -> ArchitectureMetrics:
        """Ensure metrics reflect all findings."""
        layer_count = sum(1 for f in findings if f.category.value == "layer_violation")
        cycle_count = sum(1 for f in findings if f.category.value == "dependency_cycle")
        boundary_count = sum(1 for f in findings if f.category.value == "package_boundary")

        # Take the max of detected counts
        metrics.dependency_cycles = max(metrics.dependency_cycles + cycle_count, cycle_count)
        metrics.layer_violations = max(metrics.layer_violations, layer_count)
        metrics.package_boundaries_crossed = max(metrics.package_boundaries_crossed, boundary_count)
        return metrics

    def _derive_adr_title(self, request: ArchitectureReviewRequest) -> str:
        """Derive an ADR title from the review request."""
        style = request.architecture_style.value.replace("_", " ").title()
        rtype = request.review_type.value.replace("_", " ").title()
        return f"Architecture Review ({rtype}) of {style} System"

    def _derive_adr_context(self, request: ArchitectureReviewRequest) -> str:
        """Derive ADR context from the review request."""
        return (
            f"Architecture review request {request.review_id} for workspace "
            f"{request.workspace_path}. Style: {request.architecture_style.value}. "
            f"Focus: {', '.join(a.value for a in request.focus_areas) or 'all'.strip(', ')}. "
            f"Constraints: {', '.join(request.constraints) or 'none'}."
        )

    def _build_summary(self, findings: list[Finding]) -> ReviewSummary:
        """Build summary statistics from findings."""
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for f in findings:
            key = f.severity.value
            if key in counts:
                counts[key] += 1
        total = len(findings)

        if counts["critical"] > 0:
            risk = Severity.critical
        elif counts["high"] > 0:
            risk = Severity.high
        elif counts["medium"] > 0:
            risk = Severity.medium
        else:
            risk = Severity.low

        # Confidence decreases with more findings (less certainty about completeness)
        confidence = max(0.0, min(1.0, 0.95 - total * 0.01))

        return ReviewSummary(
            total_findings=total,
            critical_count=counts["critical"],
            high_count=counts["high"],
            medium_count=counts["medium"],
            low_count=counts["low"],
            overall_risk=risk,
            confidence=round(confidence, 2),
        )

    def create_record(
        self,
        report: ArchitectureReviewReport,
        outcome: ReviewOutcome = ReviewOutcome.accepted,
    ) -> ArchitectureReviewRecord:
        """Create a persistent review record for Experience Memory."""
        return ArchitectureReviewRecord(
            review_id=report.review_id,
            review_type=report.review_type,
            total_findings=report.summary.total_findings,
            violations_detected=(
                report.summary.critical_count + report.summary.high_count
            ),
            adr_generated=bool(report.adr_draft.title),
            recommendations_count=len(report.recommendations),
            outcome=outcome,
            adr_status=ADRStatus.proposed,
        )

