"""
QA Engineer — Domain Engine orchestrator.

Orchestrates the full QA pipeline:
    1. Unit Test Generation
    2. Integration Test Generation
    3. Regression Test Automation
    4. Mutation Testing
    5. Golden Test Generation
    6. Benchmark Test Generation
    7. Flaky Test Detection
    8. Coverage Analysis → Experience Memory
    9. Performance Validation

All business logic resides here (per ADR-004). The Worker is a thin
adapter (per ADR-003).
"""

from __future__ import annotations

import logging
import time
from typing import Any

from apps.qa_engineer.schemas import (
    QATestRequestModel,
    QATestReport,
    QATestSummary,
    CoverageReport,
    MutationReport,
    PerformanceValidation,
    TestQualityRecord,
)
from apps.qa_engineer.test_generator import TestGenerator
from apps.qa_engineer.mutation_tester import MutationTester
from apps.qa_engineer.flaky_detector import FlakyDetector
from apps.qa_engineer.coverage_analyzer import CoverageAnalyzer
from apps.qa_engineer.performance_validator import PerformanceValidator
from apps.qa_engineer.golden_test_gen import GoldenTestGenerator
from apps.qa_engineer.test_strategies import TestGenerationStrategies

logger = logging.getLogger(__name__)


class QAEngineerEngine:
    """
    Orchestrates the full QA pipeline.

    Public API::

        engine = QAEngineerEngine()
        report = engine.review(request)
    """

    def __init__(self) -> None:
        self.test_generator = TestGenerator()
        self.mutation_tester = MutationTester()
        self.flaky_detector = FlakyDetector()
        self.coverage_analyzer = CoverageAnalyzer()
        self.performance_validator = PerformanceValidator()
        self.golden_gen = GoldenTestGenerator()
        self.test_strategies = TestGenerationStrategies()

    def review(self, request: QATestRequestModel) -> QATestReport:
        """Run the QA pipeline based on the requested operation."""
        started = time.monotonic()
        op = request.operation

        test_artifacts: list[Any] = []
        coverage_report = CoverageReport()
        mutation_report = MutationReport()
        flaky_findings = []
        perf_validation = PerformanceValidation()
        regression_info: dict[str, Any] = {}
        findings: list[Any] = []
        recommendations: list[str] = []

        source_code = request.target.get("source_code", "")
        language = request.target.get("language", "python")
        framework = request.target.get("framework", "pytest")

        if op in ("unit_test", "integration_test"):
            test_artifacts = self.test_generator.generate(
                source_code=source_code,
                language=language,
                framework=framework,
                test_type="unit" if op == "unit_test" else "integration",
            )
            coverage_report = self.coverage_analyzer.analyze(source_code, test_artifacts)

        elif op == "regression_test":
            test_artifacts, regression_info = self.test_generator.generate_regression(
                source_code=source_code,
                language=language,
                framework=framework,
            )
            coverage_report = self.coverage_analyzer.analyze(source_code, test_artifacts)

        elif op == "mutation_test":
            test_artifacts = self.test_generator.generate(source_code, language, framework, "unit")
            mutation_report = self.mutation_tester.analyze(
                source_code=source_code,
                language=language,
                test_artifacts=test_artifacts,
            )

        elif op == "golden_test":
            target_pack = request.for_capability_pack or "code"
            test_artifacts = self.golden_gen.generate(
                target_pack=target_pack,
                source_code=source_code,
            )

        elif op == "benchmark_test":
            test_artifacts = self.test_generator.generate(
                source_code=source_code,
                language=language,
                framework=framework,
                test_type="benchmark",
            )

        elif op == "flaky_test":
            flaky_findings = self.flaky_detector.detect(
                test_results=request.target.get("test_results", []),
            )

        elif op == "coverage":
            coverage_report = self.coverage_analyzer.analyze(
                source_code=source_code,
                test_artifacts=request.target.get("test_suite", ""),
            )

        elif op == "performance_validation":
            perf_validation = self.performance_validator.validate(
                source_code=source_code,
                perf_reqs=request.performance_requirements or {},
            )

        # Deeper knowledge expansion
        strategy_findings = self.test_strategies.to_findings(
            op.value if hasattr(op, "value") else str(op),
            language,
        )
        findings.extend(strategy_findings)
        if strategy_findings:
            recommendations.extend([f.recommendation for f in strategy_findings])

        # Build summary.
        recommendations = self._build_recommendations(
            op, coverage_report, mutation_report, flaky_findings, perf_validation
        )

        # Record to Experience Memory.
        record = TestQualityRecord(
            request_id=request.request_id,
            target_capability_pack=request.for_capability_pack or "",
            tests_generated=len(test_artifacts),
            mutation_score=mutation_report.mutation_score,
            coverage_before=0.0,
            coverage_after=coverage_report.line_coverage,
            flaky_tests_found=len(flaky_findings),
            performance_validated=op == "performance_validation",
        )
        record_id = self._record(record)

        from apps.qa_engineer.schemas import QATestOperation as _OpsEnum
        # Use the string value for the report.
        op_str = op.value if hasattr(op, "value") else str(op)

        return QATestReport(
            request_id=request.request_id,
            operation=op_str,
            test_artifacts=test_artifacts,
            coverage_report=coverage_report,
            mutation_report=mutation_report,
            flaky_test_report={"flaky_tests": flaky_findings, "total_flaky": len(flaky_findings)},
            performance_validation=perf_validation,
            regression_report=regression_info,
            summary=QATestSummary(
                total_tests_generated=sum(len(a.content) for a in test_artifacts if hasattr(a, 'content')),
                coverage_improvement=coverage_report.line_coverage,
                mutation_score=mutation_report.mutation_score,
                overall_risk="low" if coverage_report.line_coverage >= 0.8 else "medium",
                recommendations=recommendations,
            ),
            raw={
                "latency_ms": round((time.monotonic() - started) * 1000.0, 2),
                "record_id": record_id,
            },
        )

    def _build_recommendations(
        self,
        op: Any,
        coverage: CoverageReport,
        mutation: MutationReport,
        flaky: list[Any],
        perf: PerformanceValidation,
    ) -> list[str]:
        recs: list[str] = []
        if coverage.line_coverage < 0.8:
            recs.append(f"Increase test coverage: current line coverage is {coverage.line_coverage:.0%}")
        if mutation.mutation_score < 0.8 and op and "mutation" in str(op).lower():
            recs.append(f"Improve mutation score: current score is {mutation.mutation_score:.0%}")
        if flaky:
            recs.append(f"Fix {len(flaky)} flaky test(s) identified in test history")
        if not perf.meets_latency_requirement and perf.latency_p95 > 0:
            recs.append(f"Optimize latency: P95 is {perf.latency_p95}ms")
        if not recs:
            recs.append("All quality checks passing. No immediate improvements needed.")
        return recs

    def _record(self, record: TestQualityRecord) -> str:
        """Record to in-memory store (Experience Memory interface)."""
        try:
            import json
            from pathlib import Path
            base = Path("artifacts/qa_test_history")
            base.mkdir(parents=True, exist_ok=True)
            path = base / f"{record.record_id}.json"
            path.write_text(json.dumps(record.model_dump(), indent=2, default=str), encoding="utf-8")
        except OSError:
            logger.warning("Failed to persist QA test record %s", record.record_id)
        return record.record_id
