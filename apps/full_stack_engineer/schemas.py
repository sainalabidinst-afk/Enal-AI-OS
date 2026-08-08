"""
Full Stack Engineer — Public Contracts (Pydantic schemas).

Defines the input (FullStackRequest) and output (FullStackReport)
contracts for the Full Stack Engineer Capability Pack, plus all supporting types.

These schemas follow the RFC-0019 contract definitions exactly.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class OperationType(str, Enum):
    architecture_review = "architecture_review"
    code_review = "code_review"
    refactoring_plan = "refactoring_plan"
    test_engineering = "test_engineering"
    performance_analysis = "performance_analysis"
    release_review = "release_review"
    full_stack_review = "full_stack_review"


class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"
    info = "info"


class OutputFormat(str, Enum):
    json = "json"
    markdown = "markdown"
    html = "html"
    text = "text"


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ArchitectureStyle(str, Enum):
    clean_architecture = "clean_architecture"
    ddd = "ddd"
    microservices = "microservices"
    modular_monolith = "modular_monolith"
    layered = "layered"


class Grade(str, Enum):
    a = "A"
    b_plus = "B+"
    b = "B"
    c = "C"
    d = "D"
    f = "F"


class ArchitectureIssue(BaseModel):
    id: str = Field(default_factory=lambda: f"ARCH-{uuid.uuid4().hex[:8]}")
    severity: str = Field(default="medium")
    category: str = Field(default="layering", description="layering|dependency|modularity|tech_debt|circular_dep")
    description: str = Field(default="")
    location: str = Field(default="")
    recommendation: str = Field(default="")


class ArchitectureReviewResult(BaseModel):
    architecture_score: float = Field(default=0.0, ge=0.0, le=1.0)
    layering_grade: str = Field(default="B")
    dependency_grade: str = Field(default="B")
    modularity_grade: str = Field(default="B")
    tech_debt_grade: str = Field(default="B")
    issues: list[ArchitectureIssue] = Field(default_factory=list)


class CodeReviewFinding(BaseModel):
    severity: str = Field(default="medium")
    category: str = Field(default="maintainability", description="security|concurrency|reliability|maintainability|api")
    title: str = Field(default="")
    description: str = Field(default="")
    recommendation: str = Field(default="")
    evidence: str = Field(default="")
    line_number: int = Field(default=0)
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)
    cwe: str = Field(default="")


class CodeReviewSummary(BaseModel):
    total_findings: int = Field(default=0)
    by_severity: dict[str, int] = Field(default_factory=dict)
    by_category: dict[str, int] = Field(default_factory=dict)


class CodeReviewResult(BaseModel):
    findings: list[CodeReviewFinding] = Field(default_factory=list)
    summary: CodeReviewSummary = Field(default_factory=CodeReviewSummary)


class RefactoringStep(BaseModel):
    step_number: int = Field(default=1)
    description: str = Field(default="")
    files_affected: list[str] = Field(default_factory=list)
    effort: str = Field(default="medium", description="low|medium|high")


class RefactoringStepData(BaseModel):
    """A single migration step in a refactoring plan."""
    step: str = Field(default="")
    description: str = Field(default="")


class RefactoringPlanItem(BaseModel):
    id: str = Field(default_factory=lambda: f"REFACTOR-{uuid.uuid4().hex[:8]}")
    problem: str = Field(default="")
    cause: str = Field(default="")
    proposal: str = Field(default="")
    expected_benefit: str = Field(default="")
    risk: str = Field(default="medium")
    migration_steps: list[str | RefactoringStepData] = Field(default_factory=list)
    estimated_effort: str = Field(default="medium", description="low|medium|high")


class RefactoringPlanResult(BaseModel):
    plans: list[RefactoringPlanItem] = Field(default_factory=list)


class TestPlanItem(BaseModel):
    test_type: str = Field(default="unit", description="unit|integration|contract|performance|regression")
    description: str = Field(default="")
    suggested_tests: list[str] = Field(default_factory=list)
    priority: str = Field(default="medium")
    estimated_coverage: float = Field(default=0.0, ge=0.0, le=1.0)


class TestEngineeringResult(BaseModel):
    coverage_adequate: bool = Field(default=False)
    estimated_coverage: float = Field(default=0.0, ge=0.0, le=1.0)
    missing_tests: list[str] = Field(default_factory=list)
    plans: list[TestPlanItem] = Field(default_factory=list)


class PerformanceIssue(BaseModel):
    id: str = Field(default_factory=lambda: f"PERF-{uuid.uuid4().hex[:8]}")
    severity: str = Field(default="medium")
    category: str = Field(default="n_plus_1", description="n_plus_1|blocking_io|memory|algorithm|database")
    description: str = Field(default="")
    location: str = Field(default="")
    recommendation: str = Field(default="")
    estimated_improvement: str = Field(default="")


class PerformanceAnalysisResult(BaseModel):
    issues: list[PerformanceIssue] = Field(default_factory=list)
    summary: dict[str, Any] = Field(default_factory=dict)


class ReleaseCheckItem(BaseModel):
    check: str = Field(default="")
    passed: bool = Field(default=False)
    details: str = Field(default="")
    severity: str = Field(default="medium")


class ReleaseReadinessResult(BaseModel):
    ready: bool = Field(default=False)
    checks: list[ReleaseCheckItem] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)
    summary: dict[str, Any] = Field(default_factory=dict)


class FullStackRequest(BaseModel):
    """Input contract for a full stack engineering request."""

    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: OperationType = Field(..., description="Type of full stack engineering operation")
    inputs: dict[str, Any] = Field(default_factory=dict, description="Operation-specific inputs")
    context: dict[str, Any] = Field(default_factory=dict, description="Context like project_id, language, framework")
    quality_attributes: dict[str, Any] = Field(default_factory=dict)
    output_format: str = Field(default="json", description="json|markdown")


class FullStackReport(BaseModel):
    """Output contract for a full stack engineering report."""

    request_id: str = Field(..., description="Reference to the original request")
    operation: str = Field(..., description="The operation performed")
    architecture_review: ArchitectureReviewResult | None = Field(default=None)
    code_review: CodeReviewResult | None = Field(default=None)
    refactoring_plan: RefactoringPlanResult | None = Field(default=None)
    test_engineering: TestEngineeringResult | None = Field(default=None)
    performance_analysis: PerformanceAnalysisResult | None = Field(default=None)
    release_review: ReleaseReadinessResult | None = Field(default=None)
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0)
    explanation: str = Field(default="")
    raw: dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()


class FullStackRecord(BaseModel):
    """Persistent record for Experience Memory."""

    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str = Field(..., description="Reference to FullStackRequest")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    operation: str = Field(default="")
    repo_path: str = Field(default="")
    architecture_score: float = Field(default=0.0)
    findings_count: int = Field(default=0)
    release_ready: bool = Field(default=False)
    outcome: str = Field(default="pending", description="accepted|partially_accepted|rejected")
