"""
QA Engineer — testing and quality assurance layer for ECP.

Provides unit/integration test generation, regression test automation,
mutation testing, golden test generation for other packs, benchmark
test generation, flaky test detection, coverage analysis, and
performance validation — without modifying Core.

Pipeline:
    QATestRequest
        ↓
    TestGenerator (unit/integration/regression/benchmark/golden)
        ↓
    MutationTester (mutation score)
        ↓
    FlakyDetector (intermittent failure detection)
        ↓
    CoverageAnalyzer (line/branch/function coverage)
        ↓
    PerformanceValidator (latency/throughput/memory)
        ↓
    QATestReport
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.qa_engineer.engine import QAEngineerEngine
from apps.qa_engineer.worker import QAEngineerWorker
from apps.qa_engineer.schemas import (
    QATestRequestModel,
    QATestReport,
    QATestOperation,
    TestType,
    CoverageReport,
    MutationReport,
    MutantStatus,
    FlakyClassification,
    PerformanceValidation,
    TestQualityRecord,
    Finding,
    FindingSeverity,
    CoverageMetric,
    QATestArtifact,
)


class QAEngineerApp(BaseReferenceApp):
    name = "qa-engineer"
    version = "1.0.0"
    description = "Test generation, quality analysis, and validation"
    category = "quality"
    pipeline = ["perception", "analysis", "reasoning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = QAEngineerWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return await self.worker.execute(task)


def get_app() -> QAEngineerApp:
    return QAEngineerApp()

__all__ = [
    "QAEngineerApp",
    "get_app",
    "QAEngineerEngine",
    "QAEngineerWorker",
    "QATestRequestModel",
    "QATestReport",
    "QATestOperation",
    "TestType",
    "CoverageReport",
    "MutationReport",
    "MutantStatus",
    "FlakyClassification",
    "PerformanceValidation",
    "TestQualityRecord",
    "Finding",
    "FindingSeverity",
    "CoverageMetric",
    "QATestArtifact",
]
