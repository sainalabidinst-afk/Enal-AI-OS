"""
QA Engineer — Public Contracts (Pydantic schemas).

Defines the input (QATestRequest) and output (QATestReport) contracts
for the QA Engineer Capability Pack, plus all supporting types.

These schemas follow the RFC-0012 contract definitions exactly.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class QATestOperation(str, Enum):
    unit_test = "unit_test"
    integration_test = "integration_test"
    regression_test = "regression_test"
    mutation_test = "mutation_test"
    golden_test = "golden_test"
    benchmark_test = "benchmark_test"
    flaky_test = "flaky_test"
    coverage = "coverage"
    performance_validation = "performance_validation"


class TestType(str, Enum):
    unit = "unit"
    integration = "integration"
    regression = "regression"
    golden = "golden"
    benchmark = "benchmark"


class FindingSeverity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class CoverageMetric(str, Enum):
    line = "line"
    branch = "branch"
    function = "function"


class MutantStatus(str, Enum):
    killed = "killed"
    survived = "survived"
    timeout = "timeout"
    no_coverage = "no_coverage"


class FlakyClassification(str, Enum):
    network = "network"
    timing = "timing"
    shared_state = "shared_state"
    order_dependent = "order_dependent"
    unknown = "unknown"


class QATestArtifact(BaseModel):
    file_path: str = Field(..., description="Path where the test file would be written")
    test_type: TestType = Field(..., description="Type of test generated")
    test_count: int = Field(default=0, description="Number of test cases generated")
    expected_pass: int = Field(default=0, description="Expected passing tests")
    content: str = Field(default="", description="Generated test content")


class CoverageReport(BaseModel):
    line_coverage: float = Field(default=0.0, ge=0.0, le=1.0)
    branch_coverage: float = Field(default=0.0, ge=0.0, le=1.0)
    function_coverage: float = Field(default=0.0, ge=0.0, le=1.0)
    uncovered_lines: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)


class MutantResult(BaseModel):
    mutant_id: str = Field(..., description="Unique mutant identifier")
    status: MutantStatus = Field(..., description="Killed, survived, timeout, or no coverage")
    location: str = Field(default="", description="File and line of mutation")
    mutation_type: str = Field(default="", description="Type of mutation applied")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class MutationReport(BaseModel):
    mutation_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Mutants killed / total mutants")
    total_mutants: int = Field(default=0)
    killed: int = Field(default=0)
    survived: int = Field(default=0)
    timeout: int = Field(default=0)
    no_coverage: int = Field(default=0)
    weakest_areas: list[str] = Field(default_factory=list)


class FlakyTestFinding(BaseModel):
    test_name: str = Field(..., description="Name of the flaky test")
    failure_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    classification: FlakyClassification = Field(default=FlakyClassification.unknown)
    severity: FindingSeverity = Field(default=FindingSeverity.medium)
    evidence: list[str] = Field(default_factory=list, description="Sample failure messages")


class PerformanceValidation(BaseModel):
    meets_latency_requirement: bool = Field(default=False)
    meets_throughput_requirement: bool = Field(default=False)
    meets_memory_requirement: bool = Field(default=False)
    latency_p95: int = Field(default=0, description="P95 latency in milliseconds")
    throughput_rps: float = Field(default=0.0, description="Requests per second")
    memory_mb: float = Field(default=0.0, description="Peak memory usage in MB")
    bottlenecks: list[str] = Field(default_factory=list)


class RegressionFinding(BaseModel):
    risk: float = Field(default=0.0, ge=0.0, le=1.0, description="Risk score from 0-1")
    explanation: str = Field(default="", description="Why this change is risky for regression")


class QATestSummary(BaseModel):
    total_tests_generated: int = Field(default=0)
    tests_passing: int = Field(default=0)
    coverage_improvement: float = Field(default=0.0, ge=0.0, le=1.0)
    mutation_score: float = Field(default=0.0, ge=0.0, le=1.0)
    overall_risk: str = Field(default="low", description="critical|high|medium|low")
    recommendations: list[str] = Field(default_factory=list)


QATestRequest = BaseModel


class QATestRequestModel(BaseModel):
    """Input contract for a QA test generation request."""

    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: QATestOperation = Field(..., description="Type of QA operation")
    target: dict[str, Any] = Field(default_factory=dict, description="Source code, test suite, language, framework")
    for_capability_pack: str | None = Field(default=None, description="Target pack for golden test generation")
    coverage_target: float = Field(default=0.8, ge=0.0, le=1.0)
    mutation_target: float = Field(default=0.8, ge=0.0, le=1.0)
    performance_requirements: dict[str, Any] | None = Field(default=None)
    include_uncovered_code: bool = Field(default=True)


class QATestReport(BaseModel):
    """Output contract for a QA test report."""

    request_id: str = Field(..., description="Reference to the original request")
    operation: str = Field(..., description="The QA operation performed")
    test_artifacts: list[QATestArtifact] = Field(default_factory=list)
    coverage_report: CoverageReport = Field(default_factory=CoverageReport)
    mutation_report: MutationReport = Field(default_factory=MutationReport)
    regression_report: dict[str, Any] = Field(default_factory=dict)
    flaky_test_report: dict[str, Any] = Field(default_factory=dict)
    performance_validation: PerformanceValidation = Field(default_factory=PerformanceValidation)
    summary: QATestSummary = Field(default_factory=QATestSummary)
    raw: dict[str, Any] = Field(default_factory=dict, description="Raw diagnostic data")

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()


class TestQualityRecord(BaseModel):
    """Persistent record for Experience Memory."""

    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str = Field(..., description="Reference to QATestRequest")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    target_capability_pack: str = Field(default="", description="For golden test generation")
    tests_generated: int = Field(default=0)
    mutation_score: float = Field(default=0.0, ge=0.0, le=1.0)
    coverage_before: float = Field(default=0.0, ge=0.0, le=1.0)
    coverage_after: float = Field(default=0.0, ge=0.0, le=1.0)
    flaky_tests_found: int = Field(default=0)
    performance_validated: bool = Field(default=False)
    outcome: str = Field(default="pending", description="passed|partial|failed|revised")


class Finding(BaseModel):
    """A single QA finding."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    category: str = Field(..., description="unit_test|integration_test|regression|mutation|flaky|coverage|performance")
    severity: FindingSeverity = Field(default=FindingSeverity.medium)
    title: str = Field(..., description="Short title")
    description: str = Field(..., description="Detailed description")
    evidence: dict[str, Any] = Field(default_factory=dict)
    recommendation: str = Field(default="", description="Remediation guidance")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
