"""
Full Stack Engineer — Domain Engine orchestrator.

Orchestrates the full full-stack engineering pipeline:
    1. Architecture Review (F1) - layer violations, dependency density, tech debt
    2. Code Review (F2) - AST analysis for security, concurrency, reliability
    3. Refactoring Planner (F3) - plans without automatic code modification
    4. Test Engineer (F4) - coverage estimation, test plan generation
    5. Performance Engineer (F5) - N+1 queries, blocking I/O, memory issues
    6. Release Engineer (F6) - changelog, versioning, migration, rollback

All business logic resides here (per ADR-004). The Worker is a thin
adapter (per ADR-003).
"""

from __future__ import annotations

import logging
import time
from typing import Any

from apps.full_stack_engineer.schemas import (
    FullStackRequest,
    FullStackReport,
    FullStackRecord,
    ArchitectureReviewResult,
    CodeReviewResult,
    RefactoringPlanResult,
    TestEngineeringResult,
    PerformanceAnalysisResult,
    ReleaseReadinessResult,
    OperationType,
)
from apps.full_stack_engineer.architecture_review import ArchitectureReviewEngine
from apps.full_stack_engineer.code_review import FullStackCodeReviewEngine
from apps.full_stack_engineer.refactoring_planner import RefactoringPlanner
from apps.full_stack_engineer.test_engineer import TestEngineer
from apps.full_stack_engineer.performance_engineer import PerformanceEngineer
from apps.full_stack_engineer.release_engineer import ReleaseEngineer

logger = logging.getLogger(__name__)


class FullStackEngineerEngine:
    """
    Orchestrates the full full-stack engineering pipeline.

    Public API::

        engine = FullStackEngineerEngine()
        report = engine.review(request)
    """

    def __init__(self) -> None:
        self.arch_review_engine = ArchitectureReviewEngine()
        self.code_review_engine = FullStackCodeReviewEngine()
        self.refactoring_planner = RefactoringPlanner()
        self.test_engineer = TestEngineer()
        self.performance_engineer = PerformanceEngineer()
        self.release_engineer = ReleaseEngineer()

    def review(self, request: FullStackRequest) -> FullStackReport:
        """
        Run the full-stack engineering pipeline based on operation.

        Args:
            request: FullStackRequest with inputs, context, options.

        Returns:
            FullStackReport with architecture review, code review, etc.
        """
        started = time.monotonic()
        op = request.operation.value if hasattr(request.operation, 'value') else str(request.operation)

        inputs = request.inputs
        context = request.context

        architecture_review: ArchitectureReviewResult | None = None
        code_review: CodeReviewResult | None = None
        refactoring_plan: RefactoringPlanResult | None = None
        test_engineering: TestEngineeringResult | None = None
        performance_analysis: PerformanceAnalysisResult | None = None
        release_review: ReleaseReadinessResult | None = None

        if op in ("architecture_review", "full_stack_review"):
            repo_path = inputs.get("repo_path", ".")
            architecture_review = self.arch_review_engine.review(repo_path)

        if op in ("code_review", "full_stack_review"):
            source_code = inputs.get("source_code", "")
            filename = inputs.get("filename", "<unknown>")
            code_review = self.code_review_engine.review(source_code, filename)

        if op in ("refactoring_plan", "full_stack_review"):
            source_code = inputs.get("source_code", "")
            filename = inputs.get("filename", "<unknown>")
            refactoring_plan = self.refactoring_planner.plan(source_code, filename)

        if op in ("test_engineering", "full_stack_review"):
            source_path = inputs.get("source_path", ".")
            module_path = inputs.get("module_path", "")
            test_engineering = self.test_engineer.engineer(source_path, module_path)

        if op in ("performance_analysis", "full_stack_review"):
            source_code = inputs.get("source_code", "")
            filename = inputs.get("filename", "<unknown>")
            performance_analysis = self.performance_engineer.analyze(source_code, filename)

        if op in ("release_review", "full_stack_review"):
            changes = inputs.get("changes", [])
            release_review = self.release_engineer.review(changes, context)

        quality_score = self._compute_quality_score(
            architecture_review, code_review, refactoring_plan,
            test_engineering, performance_analysis, release_review
        )

        explanation = self._build_explanation(
            op, architecture_review, code_review, refactoring_plan,
            test_engineering, performance_analysis, release_review
        )

        report = FullStackReport(
            request_id=request.request_id,
            operation=op,
            architecture_review=architecture_review,
            code_review=code_review,
            refactoring_plan=refactoring_plan,
            test_engineering=test_engineering,
            performance_analysis=performance_analysis,
            release_review=release_review,
            quality_score=quality_score,
            explanation=explanation,
            raw={
                "latency_ms": round((time.monotonic() - started) * 1000.0, 2),
                "architecture_score": architecture_review.architecture_score if architecture_review else 0.0,
                "findings_count": len(code_review.findings) if code_review else 0,
                "refactoring_plans": len(refactoring_plan.plans) if refactoring_plan else 0,
                "performance_issues": len(performance_analysis.issues) if performance_analysis else 0,
                "release_ready": release_review.ready if release_review else False,
            },
        )

        record = FullStackRecord(
            request_id=request.request_id,
            operation=op,
            repo_path=inputs.get("repo_path", ""),
            architecture_score=architecture_review.architecture_score if architecture_review else 0.0,
            findings_count=len(code_review.findings) if code_review else 0,
            release_ready=release_review.ready if release_review else False,
            outcome="accepted" if quality_score >= 0.7 else "partially_accepted",
        )
        self._record(record)

        return report

    def _compute_quality_score(
        self,
        arch: ArchitectureReviewResult | None,
        code: CodeReviewResult | None,
        refactor: RefactoringPlanResult | None,
        test: TestEngineeringResult | None,
        perf: PerformanceAnalysisResult | None,
        release: ReleaseReadinessResult | None,
    ) -> float:
        """Compute overall quality score."""
        score = 0.5

        if arch:
            score += min(0.1, arch.architecture_score * 0.1)

        if code:
            score += 0.1

        if refactor:
            score += 0.05

        if test:
            score += 0.05
            if test.estimated_coverage > 0:
                score += min(0.1, test.estimated_coverage * 0.1)

        if perf:
            critical_issues = sum(1 for i in perf.issues if i.severity == "critical")
            if critical_issues == 0:
                score += 0.1

        if release:
            if release.ready:
                score += 0.1

        return max(0.0, min(1.0, round(score, 4)))

    def _build_explanation(
        self,
        op: str,
        arch: ArchitectureReviewResult | None,
        code: CodeReviewResult | None,
        refactor: RefactoringPlanResult | None,
        test: TestEngineeringResult | None,
        perf: PerformanceAnalysisResult | None,
        release: ReleaseReadinessResult | None,
    ) -> str:
        """Build human-readable explanation."""
        parts = [f"Performed {op} full-stack engineering review."]
        if arch:
            parts.append(
                f"Architecture score: {arch.architecture_score:.0%}, "
                f"{len(arch.issues)} issues found."
            )
        if code:
            parts.append(
                f"Code review: {len(code.findings)} findings, "
                f"precision {code.summary.by_severity}."
            )
        if refactor:
            parts.append(
                f"Refactoring: {len(refactor.plans)} plans generated."
            )
        if test:
            parts.append(
                f"Test engineering: coverage {test.estimated_coverage:.0%}, "
                f"{len(test.plans)} test plans."
            )
        if perf:
            parts.append(
                f"Performance: {len(perf.issues)} issues found."
            )
        if release:
            parts.append(
                f"Release readiness: {'Ready' if release.ready else 'Not ready'}, "
                f"{len(release.checks)} checks performed."
            )
        return " ".join(parts)

    def _record(self, record: FullStackRecord) -> str:
        """Record to in-memory store (Experience Memory interface)."""
        try:
            import json
            from pathlib import Path
            base = Path("artifacts/full_stack_history")
            base.mkdir(parents=True, exist_ok=True)
            path = base / f"{record.record_id}.json"
            path.write_text(
                json.dumps(record.model_dump(), indent=2, default=str),
                encoding="utf-8",
            )
        except OSError:
            logger.warning("Failed to persist full stack record %s", record.record_id)
        return record.record_id
