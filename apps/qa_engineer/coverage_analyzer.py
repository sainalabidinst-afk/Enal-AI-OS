"""
QA Engineer — Coverage Analyzer.

Analyzes test coverage across line, branch, and function dimensions.
Identifies uncovered code and coverage gaps.
"""

from __future__ import annotations

import ast
import logging
from dataclasses import dataclass, field
from typing import Any

from apps.qa_engineer.schemas import CoverageReport, QATestArtifact, CoverageMetric

logger = logging.getLogger(__name__)


@dataclass
class LineInfo:
    """Information about a single source line."""
    lineno: int
    code: str
    is_executable: bool
    is_covered: bool = False
    is_branch: bool = False
    branch_targets: list[int] = field(default_factory=list)


@dataclass
class FunctionInfo:
    """Information about a function for coverage analysis."""
    name: str
    lineno: int
    covered: bool = False
    lines: set[int] = field(default_factory=set)


class CoverageAnalyzer:
    """
    Analyzes code coverage from source code and test artifacts.

    In a real system, this would integrate with coverage.py, nyc, or
    similar tools to produce actual coverage data. Here we provide
    heuristic coverage estimation based on test artifact analysis.

    Usage::

        analyzer = CoverageAnalyzer()
        report = analyzer.analyze(source_code, test_artifacts)
    """

    def analyze(
        self,
        source_code: str,
        test_artifacts: list[QATestArtifact] | str | None = None,
    ) -> CoverageReport:
        """
        Analyze coverage for a source file given test artifacts.

        Args:
            source_code: Source code to analyze.
            test_artifacts: Either a list of QATestArtifact objects or
                           a string containing test code.

        Returns:
            CoverageReport with line, branch, function coverage and gaps.
        """
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return CoverageReport(
                line_coverage=0.0,
                branch_coverage=0.0,
                function_coverage=0.0,
                uncovered_lines=[],
                gaps=["Source has syntax errors — cannot analyze coverage"],
            )

        lines_info = self._build_line_info(source_code, tree)
        functions = self._extract_functions(tree)

        # Estimate coverage from test artifacts.
        covered_lines = self._estimate_covered_lines(test_artifacts, source_code, lines_info, functions)

        total_executable = sum(1 for l in lines_info if l.is_executable)
        covered_executable = sum(
            1 for l in lines_info
            if l.is_executable and l.lineno in covered_lines
        )

        line_cov = covered_executable / total_executable if total_executable > 0 else 1.0

        # Branch coverage: count branch points (if/elif/for/while) and check coverage.
        branch_points = [l for l in lines_info if l.is_branch]
        covered_branches = sum(1 for b in branch_points if b.lineno in covered_lines)
        branch_cov = covered_branches / len(branch_points) if branch_points else 1.0

        # Function coverage.
        covered_funcs = sum(1 for f in functions if f.covered)
        func_cov = covered_funcs / len(functions) if functions else 1.0

        # Identify gaps.
        uncovered = [
            f"line {l.lineno}: {l.code.strip()}"
            for l in lines_info
            if l.is_executable and l.lineno not in covered_lines
        ]
        gaps = self._identify_coverage_gaps(source_code, tree, line_cov)

        return CoverageReport(
            line_coverage=round(line_cov, 4),
            branch_coverage=round(branch_cov, 4),
            function_coverage=round(func_cov, 4),
            uncovered_lines=uncovered[:50],  # cap for readability
            gaps=gaps,
        )

    def _build_line_info(self, source_code: str, tree: ast.AST) -> list[LineInfo]:
        """Build line-by-line info from AST."""
        lines = source_code.splitlines()
        info: list[LineInfo] = []

        for i, line_text in enumerate(lines, 1):
            stripped = line_text.strip()
            entry = LineInfo(
                lineno=i,
                code=line_text,
                is_executable=False,
                is_branch=False,
            )

            if not stripped or stripped.startswith("#"):
                info.append(entry)
                continue

            # Check if this line contains a branch point.
            if re_match_branch(stripped):
                entry.is_branch = True

            # Check if executable (contains a call, assignment, return, etc.)
            if re_is_executable(stripped):
                entry.is_executable = True

            info.append(entry)

        return info

    def _extract_functions(self, tree: ast.AST) -> list[FunctionInfo]:
        """Extract function definitions from AST."""
        functions: list[FunctionInfo] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_lines = set()
                for child in ast.walk(node):
                    if isinstance(child, ast.stmt) and hasattr(child, 'lineno'):
                        func_lines.add(child.lineno)
                functions.append(FunctionInfo(
                    name=node.name,
                    lineno=node.lineno,
                    lines=func_lines,
                ))
        return functions

    def _estimate_covered_lines(
        self,
        test_artifacts: list[QATestArtifact] | str | None,
        source_code: str,
        lines_info: list[LineInfo],
        functions: list[FunctionInfo],
    ) -> set[int]:
        """Estimate which lines are covered by tests."""
        covered: set[int] = set()

        if test_artifacts is None:
            return covered

        if isinstance(test_artifacts, str):
            # String test code — count test functions as covering the module.
            test_code = test_artifacts
            func_count = test_code.count("def test_") + test_code.count("test(")
            if func_count == 0:
                return covered
            coverage_ratio = min(0.95, func_count / max(len(functions), 1) * 0.8)
            for func in functions:
                if random_check(coverage_ratio):
                    covered.update(func.lines)
            return covered

        # List of QATestArtifact objects.
        total_tests = sum(a.test_count for a in test_artifacts)
        total_funcs = len(functions)
        if total_tests == 0 or total_funcs == 0:
            return covered

        # Heuristic: distribute test coverage across functions.
        tests_per_func = total_tests / total_funcs
        for func in functions:
            # Each test has a chance of covering each function.
            coverage_prob = min(0.95, tests_per_func / max(len(func.lines), 1) * 0.6)
            for lineno in func.lines:
                if random_check(coverage_prob):
                    covered.add(lineno)

            # Always cover the function definition line if we're covering it.
            if coverage_prob > 0.3:
                covered.add(func.lineno)

        # Also cover lines that test artifacts reference by name.
        for artifact in test_artifacts:
            if artifact.content:
                for func in functions:
                    if func.name in artifact.content:
                        covered.add(func.lineno)
                        covered.update(func.lines)

        return covered

    def _identify_coverage_gaps(
        self, source_code: str, tree: ast.AST, line_cov: float
    ) -> list[str]:
        """Identify functional coverage gaps."""
        gaps: list[str] = []

        # Check for untested public functions.
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not node.name.startswith("_") and node.name not in ("main",):
                    gaps.append(f"Public function '{node.name}' may lack dedicated tests")

        # Check for missing edge cases.
        if line_cov < 0.8:
            gaps.append(f"Overall coverage is {line_cov:.0%} — below 80% threshold")
        if line_cov < 0.5:
            gaps.append("Significant test coverage gaps detected — consider adding more tests")

        return gaps[:10]


def re_match_branch(stripped: str) -> bool:
    """Check if a stripped line starts a branch (if/elif/for/while/try/except)."""
    branch_prefixes = ("if ", "elif ", "for ", "while ", "try:", "except", "else:", "match ")
    return any(stripped.startswith(p) for p in branch_prefixes)


def re_is_executable(stripped: str) -> bool:
    """Check if a line is executable code."""
    exec_prefixes = ("return", "yield", "raise", "=", "assert", "import", "from", "pass", "break", "continue")
    if any(stripped.startswith(p) for p in exec_prefixes):
        return True
    if "(" in stripped and "=" not in stripped[:stripped.index("(")]:
        return True
    if stripped.endswith("()") or stripped.endswith(")"):
        return True
    return False


def random_check(probability: float) -> bool:
    """Deterministic pseudo-random check for coverage simulation."""
    import hashlib
    h = int(hashlib.md5(str(probability).encode()).hexdigest(), 16)
    return (h % 1000) / 1000.0 < probability
