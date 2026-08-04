"""
F4 — Test Engineer
===================

Creates test plans for:
- Unit Test
- Integration Test
- Contract Test
- Performance Test
- Regression Test

Also checks test coverage adequacy.
"""

import ast
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from apps.code_engineer.test_generator import TestGenerator

logger = logging.getLogger(__name__)


@dataclass
class TestPlan:
    test_type: str
    description: str
    suggested_tests: list[str]
    priority: str = "medium"
    estimated_coverage: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "test_type": self.test_type,
            "description": self.description,
            "suggested_tests": self.suggested_tests,
            "priority": self.priority,
            "estimated_coverage": self.estimated_coverage,
        }


@dataclass
class TestEngineerReport:
    coverage_adequate: bool = False
    missing_tests: list[str] = field(default_factory=list)
    plans: list[TestPlan] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "coverage_adequate": self.coverage_adequate,
            "missing_tests": self.missing_tests,
            "plans": [p.to_dict() for p in self.plans],
            "summary": self.summary,
        }


class TestEngineer:
    """Engineers comprehensive test suites."""

    async def engineer(self, source_path: str, module_path: str) -> dict[str, Any]:
        report = TestEngineerReport()
        self._analyze_source(source_path, module_path, report)
        self._generate_plans(report)
        return report.to_dict()

    def _analyze_source(self, source_path: str, module_path: str, report: TestEngineerReport):
        source = Path(source_path)
        if not source.exists():
            report.missing_tests.append(f"Source path not found: {source_path}")
            return

        py_files = list(source.rglob("*.py"))
        if not py_files:
            report.missing_tests.append("No Python files found for test generation.")
            return

        has_tests = any("test" in p.name.lower() for p in py_files)
        if not has_tests:
            report.missing_tests.append("No test files found.")

        total_functions = 0
        tested_functions = 0
        for py_file in py_files:
            try:
                tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
                funcs = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")]
                total_functions += len(funcs)
            except SyntaxError:
                continue

        test_files = [p for p in py_files if "test" in p.name.lower()]
        for test_file in test_files:
            try:
                tree = ast.parse(test_file.read_text(encoding="utf-8"), filename=str(test_file))
                funcs = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]
                tested_functions += len(funcs)
            except SyntaxError:
                continue

        if total_functions > 0:
            coverage = tested_functions / total_functions
            report.coverage_adequate = coverage >= 0.7
            report.summary = {
                "total_functions": total_functions,
                "tested_functions": tested_functions,
                "estimated_coverage": round(coverage, 2),
            }

    def _generate_plans(self, report: TestEngineerReport):
        if report.missing_tests:
            report.plans.append(TestPlan(
                test_type="Unit Test",
                description="Create unit tests for core functions.",
                suggested_tests=["test_<module>_<function>_returns_expected", "test_<module>_<function>_handles_error"],
                priority="high",
                estimated_coverage=0.7,
            ))
            report.plans.append(TestPlan(
                test_type="Integration Test",
                description="Test module interactions and API contracts.",
                suggested_tests=["test_api_<endpoint>_returns_200", "test_service_<name>_calls_repository"],
                priority="medium",
                estimated_coverage=0.5,
            ))
            report.plans.append(TestPlan(
                test_type="Regression Test",
                description="Run full test suite after changes.",
                suggested_tests=["test_full_suite_passes", "test_no_breaking_changes"],
                priority="medium",
                estimated_coverage=0.3,
            ))
        report.plans.append(TestPlan(
            test_type="Performance Test",
            description="Benchmark critical paths.",
            suggested_tests=["benchmark_<critical_path>", "profile_memory_usage"],
            priority="low",
            estimated_coverage=0.2,
        ))


test_engineer = TestEngineer()
