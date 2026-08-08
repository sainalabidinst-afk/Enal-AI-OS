"""
Tests for Full Stack Engineer capability.

Covers F1-F6 operations through the domain engine, worker, and contract schemas.
"""

import asyncio
from pathlib import Path

import pytest

from apps.full_stack_engineer.architecture_review import ArchitectureReviewEngine
from apps.full_stack_engineer.engine import FullStackEngineerEngine
from apps.full_stack_engineer.schemas import (
    FullStackRequest,
    FullStackReport,
    OperationType,
    OutputFormat,
    Severity,
    RiskLevel,
    ArchitectureReviewResult,
    CodeReviewResult,
    RefactoringPlanResult,
    TestEngineeringResult,
    PerformanceAnalysisResult,
    ReleaseReadinessResult,
)
from apps.full_stack_engineer.worker import FullStackEngineerWorker


def test_capability_imports() -> None:
    """Verify that capability modules can be imported."""
    assert True


def test_capability_package() -> None:
    """Verify that capability package exists."""
    import importlib

    mod = importlib.import_module("apps.full_stack_engineer")
    assert mod is not None


def test_schemas_contract() -> None:
    """Verify the public contract schemas are well-formed."""
    req = FullStackRequest(
        operation=OperationType.architecture_review,
        inputs={"repo_path": "."},
        context={"project_id": "p1", "language": "python"},
    )
    assert req.request_id
    assert req.operation == OperationType.architecture_review
    assert req.output_format == "json"

    # Output model defaults
    report = FullStackReport(request_id="test", operation="architecture_review")
    assert report.quality_score == 0.0
    assert report.architecture_review is None
    assert report.to_dict()["operation"] == "architecture_review"


def test_enums() -> None:
    """Verify enum values align with the RFC-0019 contract."""
    ops = {op.value for op in OperationType}
    assert {
        "architecture_review",
        "code_review",
        "refactoring_plan",
        "test_engineering",
        "performance_analysis",
        "release_review",
        "full_stack_review",
    } == ops

    sev = {s.value for s in Severity}
    assert {"low", "medium", "high", "critical", "info"} == sev

    risk = {r.value for r in RiskLevel}
    assert {"low", "medium", "high"} == risk

    fmt = {f.value for f in OutputFormat}
    assert {"json", "markdown", "html", "text"} == fmt


@pytest.mark.asyncio
async def test_engine_architecture_review() -> None:
    """F1: Architecture review returns a report with score and issues."""
    engine = FullStackEngineerEngine()
    request = FullStackRequest(
        operation=OperationType.architecture_review,
        inputs={"repo_path": "."},
        context={"project_id": "audit-test", "language": "python"},
    )
    report = await engine.review(request)
    assert report.operation == "architecture_review"
    assert isinstance(report.architecture_review, ArchitectureReviewResult)
    assert 0.0 <= report.architecture_review.architecture_score <= 1.0
    assert report.raw["architecture_score"] >= 0.0


@pytest.mark.asyncio
async def test_engine_code_review() -> None:
    """F2: Code review returns findings and summary."""
    engine = FullStackEngineerEngine()
    request = FullStackRequest(
        operation=OperationType.code_review,
        inputs={
            "source_code": "def f():\n    open('/etc/passwd')\n    return 1\n",
            "filename": "sample.py",
        },
        context={"project_id": "code-review", "language": "python"},
    )
    report = await engine.review(request)
    assert isinstance(report.code_review, CodeReviewResult)
    assert report.code_review.summary.total_findings >= 0


@pytest.mark.asyncio
async def test_engine_refactoring_plan() -> None:
    """F3: Refactoring planner returns plans without executing changes."""
    engine = FullStackEngineerEngine()
    request = FullStackRequest(
        operation=OperationType.refactoring_plan,
        inputs={"source_code": "def a():\n    pass\n", "filename": "x.py"},
        context={"project_id": "refactor", "language": "python"},
    )
    report = await engine.review(request)
    assert isinstance(report.refactoring_plan, RefactoringPlanResult)
    assert report.refactoring_plan.plans


@pytest.mark.asyncio
async def test_engine_test_engineering() -> None:
    """F4: Test engineering estimates coverage and plans."""
    engine = FullStackEngineerEngine()
    request = FullStackRequest(
        operation=OperationType.test_engineering,
        inputs={"source_path": ".", "module_path": "apps.full_stack_engineer"},
        context={"project_id": "test-eng", "language": "python"},
    )
    report = await engine.review(request)
    assert isinstance(report.test_engineering, TestEngineeringResult)
    assert report.test_engineering.estimated_coverage >= 0.0


@pytest.mark.asyncio
async def test_engine_performance_analysis() -> None:
    """F5: Performance analysis detects issues in source code."""
    engine = FullStackEngineerEngine()
    request = FullStackRequest(
        operation=OperationType.performance_analysis,
        inputs={
            "source_code": (
                "for user in users:\n"
                "    for order in user.orders:\n"
                "        print(order)\n"
            ),
            "filename": "perf.py",
        },
        context={"project_id": "perf", "language": "python"},
    )
    report = await engine.review(request)
    assert isinstance(report.performance_analysis, PerformanceAnalysisResult)
    assert report.performance_analysis.issues


@pytest.mark.asyncio
async def test_engine_release_review() -> None:
    """F6: Release readiness validation returns checks."""
    engine = FullStackEngineerEngine()
    request = FullStackRequest(
        operation=OperationType.release_review,
        inputs={"changes": [{"type": "chore", "content": "bump", "filename": None}]},
        context={"project_id": "release", "language": "python"},
    )
    report = await engine.review(request)
    assert isinstance(report.release_review, ReleaseReadinessResult)
    assert isinstance(report.release_review.ready, bool)
    assert isinstance(report.release_review.checks, list)


@pytest.mark.asyncio
async def test_engine_full_stack_review() -> None:
    """Full stack review aggregates all six operations."""
    engine = FullStackEngineerEngine()
    request = FullStackRequest(
        operation=OperationType.full_stack_review,
        inputs={"repo_path": "."},
        context={"project_id": "full", "language": "python"},
    )
    report = await engine.review(request)
    assert report.operation == "full_stack_review"
    assert report.architecture_review is not None
    assert report.code_review is not None
    assert report.quality_score >= 0.0
    assert report.explanation


@pytest.mark.asyncio
async def test_worker_execute() -> None:
    """Worker adapter delegates to the domain engine and returns a dict."""
    worker = FullStackEngineerWorker()
    task = {
        "operation": "architecture_review",
        "inputs": {"repo_path": "."},
        "context": {"project_id": "worker-test", "language": "python"},
        "output_format": "json",
    }
    result = await worker.execute(task)
    assert isinstance(result, dict)
    assert result["operation"] == "architecture_review"
    assert "quality_score" in result


@pytest.mark.asyncio
async def test_worker_unknown_operation_falls_back() -> None:
    """Worker falls back to full_stack_review for unknown operations."""
    worker = FullStackEngineerWorker()
    result = await worker.execute({"operation": "unknown", "inputs": {"repo_path": "."}})
    assert result["operation"] == "full_stack_review"


def test_architecture_review_engine_scan(tmp_path: Path) -> None:
    """ArchitectureReviewEngine scans a repo and produces a report."""
    tmp_path.joinpath("mod_a.py").write_text(
        "import mod_b\n\n\ndef hello():\n    return mod_b.world()\n",
        encoding="utf-8",
    )
    tmp_path.joinpath("mod_b.py").write_text(
        "def world():\n    return 42\n",
        encoding="utf-8",
    )

    async def _run() -> dict:
        engine = ArchitectureReviewEngine()
        return await engine.review(str(tmp_path))

    report = asyncio.run(_run())
    assert report["total_modules"] >= 2
    assert report["total_lines"] > 0
    assert "architecture_score" in report
    assert "detected_style" in report
