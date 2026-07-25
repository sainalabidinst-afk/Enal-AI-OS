"""
Regression Risk Analyzer
=========================

Analyzes test impact and regression risk for code changes.
Leverages the dependency graph and impact analysis to predict
which tests are affected by a given change.

Pipeline:
  Change Spec → Dependency Graph Lookup → Impact Propagation
  → Test Mapping → Risk Scoring → Prioritized Test List
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class TestImpact:
    """Impact assessment for a single test."""
    test_path: str
    test_name: str
    risk_score: float
    affected_by: list[str] = field(default_factory=list)
    is_direct: bool = False
    reason: str = ""

    @property
    def risk_label(self) -> str:
        if self.risk_score >= 0.8:
            return "critical"
        elif self.risk_score >= 0.5:
            return "high"
        elif self.risk_score >= 0.2:
            return "medium"
        return "low"


@dataclass
class RegressionReport:
    """Complete regression risk report for a set of changes."""
    changes: list[dict[str, Any]]
    total_tests: int = 0
    affected_tests: list[TestImpact] = field(default_factory=list)
    risk_distribution: dict[str, int] = field(default_factory=lambda: {
        "critical": 0, "high": 0, "medium": 0, "low": 0,
    })
    recommended_order: list[str] = field(default_factory=list)
    skip_recommended: list[str] = field(default_factory=list)
    coverage_gaps: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def overall_risk_score(self) -> float:
        if not self.affected_tests:
            return 0.0
        weighted = sum(t.risk_score for t in self.affected_tests)
        return weighted / len(self.affected_tests)

    @property
    def high_risk_count(self) -> int:
        return sum(1 for t in self.affected_tests if t.risk_score >= 0.5)

    def to_dict(self) -> dict[str, Any]:
        return {
            "changes_count": len(self.changes),
            "total_tests": self.total_tests,
            "affected_tests": len(self.affected_tests),
            "overall_risk_score": round(self.overall_risk_score, 2),
            "high_risk_count": self.high_risk_count,
            "risk_distribution": self.risk_distribution,
            "affected_tests": [
                {
                    "test_path": t.test_path,
                    "test_name": t.test_name,
                    "risk_score": round(t.risk_score, 2),
                    "risk_label": t.risk_label,
                    "affected_by": t.affected_by,
                    "is_direct": t.is_direct,
                    "reason": t.reason,
                }
                for t in self.affected_tests
            ],
            "recommended_order": self.recommended_order,
            "skip_recommended": self.skip_recommended,
            "coverage_gaps": self.coverage_gaps,
        }


class RegressionAnalyzer:
    """Analyzes regression risk for code changes."""

    def __init__(self):
        self._dependency_graph_builder_cls = None
        self._impact_analyzer_cls = None

    async def _ensure_components(self):
        """Lazy-load dependency graph and impact analyzer."""
        if self._dependency_graph_builder_cls is None:
            from apps.code_engineer.dependency_graph import DependencyGraphBuilder
            self._dependency_graph_builder_cls = DependencyGraphBuilder

        if self._impact_analyzer_cls is None:
            from apps.code_engineer.impact_analyzer import ImpactAnalyzer
            self._impact_analyzer_cls = ImpactAnalyzer

    async def analyze_changes(
        self,
        repo_path: str,
        changes: list[dict[str, Any]],
        test_patterns: Optional[list[str]] = None,
    ) -> RegressionReport:
        """
        Analyze regression risk for a set of changes.

        Args:
            repo_path: Path to the repository root.
            changes: List of change specs, each with:
                - file_path: Path to the changed file
                - change_type: "modified", "added", "deleted"
                - description: Optional description
            test_patterns: Optional list of test file patterns.
                Defaults to ["test_*.py", "*_test.py", "tests/"]

        Returns:
            RegressionReport with risk assessment.
        """
        await self._ensure_components()
        from pathlib import Path

        repo = Path(repo_path)
        test_patterns = test_patterns or ["test_*.py", "*_test.py", "tests/"]

        # Build dependency graph if not already built
        dep_graph = await self._dependency_graph.build_graph(str(repo))

        # Find all test files
        test_files = self._find_test_files(repo, test_patterns)

        # Map test files to the modules they test
        test_module_map = self._map_tests_to_modules(test_files, repo)

        report = RegressionReport(changes=changes)
        report.total_tests = len(test_files)
        report.metadata["repo_path"] = str(repo)
        report.metadata["test_files_found"] = len(test_files)

        for change in changes:
            file_path = change.get("file_path", "")
            change_type = change.get("change_type", "modified")

            if not file_path:
                continue

            # Get impacted modules from the dependency graph
            impacted = self._get_impacted_modules(dep_graph, file_path, change_type)

            # Find tests that cover impacted modules
            for test_path, test_name, covered_modules in test_module_map:
                matched_modules = [m for m in impacted if m in covered_modules]
                if not matched_modules:
                    continue

                is_direct = file_path in covered_modules
                risk_score = self._compute_risk_score(
                    change_type=change_type,
                    is_direct=is_direct,
                    distance=self._get_distance(dep_graph, file_path, covered_modules),
                    matched_count=len(matched_modules),
                    total_coverage=len(covered_modules),
                )

                report.affected_tests.append(TestImpact(
                    test_path=str(test_path),
                    test_name=test_name,
                    risk_score=risk_score,
                    affected_by=matched_modules,
                    is_direct=is_direct,
                    reason=self._generate_reason(change, matched_modules, is_direct),
                ))

        # Deduplicate tests (same test may be affected by multiple changes)
        seen: set[str] = set()
        unique_tests: list[TestImpact] = []
        for t in report.affected_tests:
            key = f"{t.test_path}::{t.test_name}"
            if key not in seen:
                seen.add(key)
                unique_tests.append(t)
            else:
                # Merge affected_by from duplicate
                for existing in unique_tests:
                    if f"{existing.test_path}::{existing.test_name}" == key:
                        existing.affected_by.extend(
                            m for m in t.affected_by if m not in existing.affected_by
                        )
                        existing.risk_score = max(existing.risk_score, t.risk_score)
                        break

        report.affected_tests = sorted(unique_tests, key=lambda t: t.risk_score, reverse=True)

        # Compute risk distribution
        for t in report.affected_tests:
            label = t.risk_label
            report.risk_distribution[label] = report.risk_distribution.get(label, 0) + 1

        # Generate recommended test order (high risk first)
        report.recommended_order = [
            f"{t.test_path}::{t.test_name}" for t in report.affected_tests
            if t.risk_score >= 0.3
        ]

        # Generate skip recommendations (very low risk, not directly affected)
        report.skip_recommended = [
            f"{t.test_path}::{t.test_name}" for t in report.affected_tests
            if t.risk_score < 0.2 and not t.is_direct
        ]

        # Detect coverage gaps (modules with changes but no tests)
        covered_modules = set()
        for _, _, modules in test_module_map:
            covered_modules.update(modules)

        for change in changes:
            file_path = change.get("file_path", "")
            impacted = self._get_impacted_modules(dep_graph, file_path, change.get("change_type", "modified"))
            uncovered = [m for m in impacted if m not in covered_modules]
            if uncovered:
                report.coverage_gaps.extend(uncovered)

        report.coverage_gaps = list(set(report.coverage_gaps))

        logger.info(
            f"Regression analysis: {len(report.affected_tests)} affected tests "
            f"out of {report.total_tests} total, "
            f"risk score: {report.overall_risk_score:.2f}"
        )
        return report

    def _find_test_files(self, repo_path: Path, patterns: list[str]) -> list[Path]:
        """Find test files matching the given patterns."""
        import fnmatch

        test_files = []
        for pattern in patterns:
            if pattern.endswith("/"):
                # Directory pattern
                test_dir = repo_path / pattern.rstrip("/")
                if test_dir.exists():
                    for f in test_dir.rglob("*.py"):
                        if f.name.startswith("test_") or f.name.endswith("_test.py"):
                            test_files.append(f)
            else:
                # Glob pattern
                for f in repo_path.rglob(pattern):
                    if f.is_file() and f.suffix == ".py":
                        test_files.append(f)

        return list(set(test_files))

    def _map_tests_to_modules(
        self, test_files: list[Path], repo_path: Path
    ) -> list[tuple[Path, str, list[str]]]:
        """
        Map test files to the modules they test.
        Tries to infer from test name conventions and imports.
        """
        import ast

        test_module_map: list[tuple[Path, str, list[str]]] = []

        for test_file in test_files:
            try:
                content = test_file.read_text(encoding="utf-8")
                tree = ast.parse(content, filename=str(test_file))
            except (SyntaxError, Exception):
                continue

            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)

            # Infer tested modules from filename
            rel_path = test_file.relative_to(repo_path)
            test_name = test_file.stem  # e.g., test_analyzer or analyzer_test

            # Remove test prefix/suffix to get module name
            module_name = test_name
            if module_name.startswith("test_"):
                module_name = module_name[5:]
            elif module_name.endswith("_test"):
                module_name = module_name[:-5]

            # Collect all covered modules
            covered = set(imports)
            if module_name:
                covered.add(module_name)

            # Add the parent package if it's a test within a package
            parts = list(rel_path.parts)
            if len(parts) > 1:
                # e.g., tests/test_analyzer.py → tests
                parent_pkg = parts[0]
                if parent_pkg != "tests":
                    covered.add(parent_pkg)

            test_module_map.append((test_file, test_name, list(covered)))

        return test_module_map

    def _get_impacted_modules(
        self, dep_graph: Any, file_path: str, change_type: str
    ) -> list[str]:
        """
        Get all modules impacted by a change to the given file.
        Uses dependency graph to find direct and transitive dependents.
        """
        impacted = set()

        # Normalize file path to module path
        module_path = file_path.replace("/", ".").replace("\\", ".")
        if module_path.endswith(".py"):
            module_path = module_path[:-3]
        if module_path.endswith(".__init__"):
            module_path = module_path[:-9]

        # Add the changed file itself
        impacted.add(module_path)

        # Find modules that depend on this file
        if hasattr(dep_graph, "get_dependents"):
            dependents = dep_graph.get_dependents(module_path)
            impacted.update(dependents)

        # Find modules that this file depends on (for "deleted" changes)
        if change_type == "deleted" and hasattr(dep_graph, "get_dependencies"):
            dependencies = dep_graph.get_dependencies(module_path)
            impacted.update(dependencies)

        # Find modules in the same package
        parts = module_path.split(".")
        if len(parts) > 1:
            parent = ".".join(parts[:-1])
            impacted.add(parent)

        return list(impacted)

    def _compute_risk_score(
        self,
        change_type: str,
        is_direct: bool,
        distance: int,
        matched_count: int,
        total_coverage: int,
    ) -> float:
        """
        Compute a risk score between 0.0 and 1.0.

        Factors:
        - Direct changes are higher risk
        - Deleted files are higher risk
        - Shorter dependency distance = higher risk
        - More matched coverage = higher confidence in risk
        """
        base_score = 0.3

        # Change type factor
        type_factors = {
            "deleted": 1.0,
            "modified": 0.8,
            "added": 0.4,
        }
        base_score *= type_factors.get(change_type, 0.5)

        # Direct vs indirect
        if is_direct:
            base_score += 0.3
        else:
            # Distance factor: closer = higher risk
            distance_factor = max(0.0, 1.0 - (distance * 0.1))
            base_score *= distance_factor

        # Coverage confidence
        if total_coverage > 0:
            coverage_ratio = matched_count / total_coverage
            base_score *= (0.5 + 0.5 * coverage_ratio)

        return min(1.0, max(0.0, base_score))

    def _get_distance(self, dep_graph: Any, file_path: str, covered_modules: list[str]) -> int:
        """
        Compute minimum dependency distance between file_path and covered modules.
        """
        if not hasattr(dep_graph, "get_distance"):
            return 1

        module_path = file_path.replace("/", ".").replace("\\", ".")
        if module_path.endswith(".py"):
            module_path = module_path[:-3]

        min_distance = float("inf")
        for module in covered_modules:
            try:
                dist = dep_graph.get_distance(module_path, module)
                if dist is not None and dist < min_distance:
                    min_distance = dist
            except Exception:
                continue

        return int(min_distance) if min_distance != float("inf") else 2

    def _generate_reason(
        self, change: dict[str, Any], matched_modules: list[str], is_direct: bool
    ) -> str:
        """Generate a human-readable reason for the test impact."""
        file_path = change.get("file_path", "unknown")
        change_type = change.get("change_type", "modified")

        if is_direct:
            return (
                f"Directly tests changed file '{file_path}' "
                f"({change_type})"
            )
        else:
            modules_str = ", ".join(matched_modules[:3])
            remaining = len(matched_modules) - 3
            if remaining > 0:
                modules_str += f" and {remaining} more"
            return (
                f"Depends on modules affected by change to "
                f"'{file_path}': {modules_str}"
            )


regression_analyzer = RegressionAnalyzer()
