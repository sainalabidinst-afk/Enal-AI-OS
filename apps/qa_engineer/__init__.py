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

__all__ = [
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
