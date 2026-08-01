"""
System Architect — Boundary Enforcer.

Enforces package boundary rules and detects violations:
- Cross-package import detection
- Allowed dependency whitelist
- Layer boundary enforcement (combined with dependency_graph)
- Import cycle detection
- Unauthorized external dependency identification
"""

from __future__ import annotations

import ast
import logging
from pathlib import Path
from typing import Any

from apps.system_architect.dependency_graph import (
    DependencyGraphBuilder,
    DependencyGraphSnapshot,
    DependencyType,
)
from apps.system_architect.schemas import (
    Finding,
    FindingCategory,
    Severity,
    Impact,
    ArchitectureMetrics,
    Recommendation,
    Priority,
    Effort,
)

logger = logging.getLogger(__name__)


class BoundaryEnforcer:
    """
    Enforces package boundary rules and detects violations.

    Usage::
        enforcer = BoundaryEnforcer(repo_path, allowed_packages=["apps", "backend", "sdk"])
        findings, metrics, recs = await enforcer.enforce()
    """

    def __init__(
        self,
        repo_path: str | Path,
        allowed_packages: list[str] | None = None,
        forbidden_patterns: list[str] | None = None,
    ):
        self.repo_path = Path(repo_path)
        # Packages that are allowed to import each other (whitelist)
        self.allowed_packages = allowed_packages or ["backend", "apps", "sdk", "benchmarks"]

        # Patterns that should never be imported (e.g., test utilities in production code)
        self.forbidden_patterns = forbidden_patterns or [
            "test", "tests", "mock", "mocks", "fixture", "fixtures",
            "_test", "_smoke", "_diag",
        ]

        self.graph_builder = DependencyGraphBuilder(self.repo_path)

    async def enforce(self) -> tuple[list[Finding], ArchitectureMetrics, list[Recommendation]]:
        """Run boundary enforcement analysis."""
        snapshot = await self.graph_builder.build()

        findings: list[Finding] = []
        recommendations: list[Recommendation] = []

        # 1. Cross-package boundary violations
        findings.extend(self._find_cross_package_violations(snapshot))

        # 2. Forbidden dependency patterns
        findings.extend(self._find_forbidden_patterns(snapshot))

        # 3. Cycle analysis
        findings.extend(self._find_cycle_violations(snapshot))

        # 4. Compute metrics
        metrics = self._compute_metrics(snapshot, findings)

        # 5. Generate recommendations
        recommendations = self._generate_recommendations(findings, metrics)

        return findings, metrics, recommendations

    # ------------------------------------------------------------------
    # Analysis methods
    # ------------------------------------------------------------------

    def _get_package(self, module_path: str) -> str | None:
        """Extract the top-level package name from a module path."""
        parts = module_path.replace("\\", "/").split("/")
        return parts[0] if parts else None

    def _find_cross_package_violations(self, snapshot: DependencyGraphSnapshot) -> list[Finding]:
        """Detect unauthorized cross-package imports."""
        findings: list[Finding] = []
        package_imports: dict[str, set[str]] = {}

        for mod_path, mod_info in snapshot.modules.items():
            source_pkg = self._get_package(mod_path)
            if source_pkg is None or source_pkg not in self.allowed_packages:
                continue

            for dep in mod_info.dependencies:
                if dep.dependency_type != DependencyType.LOCAL:
                    continue
                target_pkg = self._get_package(dep.target)
                if target_pkg is None:
                    continue
                if target_pkg not in self.allowed_packages:
                    continue

                if target_pkg != source_pkg:
                    key = f"{source_pkg} -> {target_pkg}"
                    if key not in package_imports:
                        package_imports[key] = set()
                    package_imports[key].add(f"{mod_path} imports {dep.target}")

        # Check against allowed cross-package rules
        # Rules: packages that are allowed to import each other
        allowed_cross = {
            ("apps", "backend"): True,  # Apps can import backend
            ("backend", "apps"): False,  # Backend should not import apps
            ("sdk", "backend"): True,  # SDK can import backend
            ("backend", "sdk"): True,  # Backend can import SDK
            ("benchmarks", "apps"): True,  # Benchmarks can import apps
            ("benchmarks", "backend"): True,  # Benchmarks can import backend
            ("benchmarks", "sdk"): True,  # Benchmarks can import SDK
        }

        # Check if there are inter-package imports that are not allowed
        for (src_pkg, tgt_pkg), imports in package_imports.items():
            # Check if this cross-package import is allowed
            src, tgt = src_pkg, tgt_pkg
            is_allowed = allowed_cross.get((src, tgt), False)

            if not is_allowed:
                full_imports = list(imports)
                finding = Finding(
                    category=FindingCategory.package_boundary,
                    severity=Severity.high if not is_allowed else Severity.low,
                    title=f"Cross-package boundary violation: {src} → {tgt}",
                    description=(
                        f"Package `{src}` imports from `{tgt}`. "
                        f"Found {len(full_imports)} cross-package import(s). "
                        "Cross-package imports violate package encapsulation unless explicitly allowed."
                    ),
                    evidence={
                        "source_package": src,
                        "target_package": tgt,
                        "violations": full_imports[:10],
                        "total_violations": len(full_imports),
                    },
                    recommendation=(
                        f"Use shared contracts, not direct imports, to communicate "
                        f"between `{src}` and `{tgt}`. "
                        "If this dependency is necessary, submit an ADR."
                    ),
                    impact=Impact.modifiability,
                    confidence=0.85,
                )
                findings.append(finding)

        return findings

    def _find_forbidden_patterns(self, snapshot: DependencyGraphSnapshot) -> list[Finding]:
        """Detect forbidden dependency patterns (e.g., test code in production modules)."""
        findings: list[Finding] = []
        for mod_path, mod_info in snapshot.modules.items():
            for dep in mod_info.dependencies:
                if dep.dependency_type == DependencyType.LOCAL:
                    if any(pattern in dep.target.lower() for pattern in self.forbidden_patterns):
                        finding = Finding(
                            category=FindingCategory.package_boundary,
                            severity=Severity.medium,
                            title=f"Production code imports test/fixture: {mod_path}",
                            description=(
                                f"Module `{mod_path}` imports `{dep.target}`, which contains "
                                "test or fixture patterns. Production code should not depend "
                                "on test utilities."
                            ),
                            evidence={
                                "source_file": mod_path,
                                "target_module": dep.target,
                                "line_number": dep.line_number,
                            },
                            recommendation=(
                                "Move shared utilities to a `common` or `utils` package "
                                "that is not under `tests/`."
                            ),
                            impact=Impact.maintainability,
                            confidence=0.9,
                        )
                        findings.append(finding)
        return findings

    def _find_cycle_violations(self, snapshot: DependencyGraphSnapshot) -> list[Finding]:
        """Detect dependency cycles between packages."""
        findings: list[Finding] = []
        for cycle in snapshot.circular_dependencies:
            if len(cycle) >= 2:
                finding = Finding(
                    category=FindingCategory.dependency_cycle,
                    severity=Severity.high,
                    title=f"Package dependency cycle: {len(cycle)} modules involved",
                    description=(
                        f"Dependency cycle detected: {' → '.join(cycle)}. "
                        "Cycles between packages prevent independent testing and deployment."
                    ),
                    evidence={
                        "cycle": cycle,
                        "cycle_length": len(cycle),
                    },
                    recommendation=(
                        "Break the cycle by extracting shared interfaces or merging "
                        "the dependent modules."
                    ),
                    impact=Impact.testability,
                    confidence=0.95,
                )
                findings.append(finding)
        return findings

    def _compute_metrics(self, snapshot: DependencyGraphSnapshot, findings: list[Finding]) -> ArchitectureMetrics:
        """Compute boundary enforcement metrics."""
        boundary_violations = sum(1 for f in findings if f.category == FindingCategory.package_boundary)
        cycle_violations = sum(1 for f in findings if f.category == FindingCategory.dependency_cycle)
        layer_violations = len(snapshot.layer_violations)

        return ArchitectureMetrics(
            dependency_cycles=cycle_violations,
            layer_violations=layer_violations,
            package_boundaries_crossed=boundary_violations,
            maintainability_score=max(0.0, 100.0 - (layer_violations * 5.0 + cycle_violations * 10.0 + boundary_violations * 4.0)),
            scalability_score=max(0.0, 100.0 - (cycle_violations * 8.0 + boundary_violations * 3.0)),
            testability_score=max(0.0, 100.0 - (cycle_violations * 6.0 + layer_violations * 3.0)),
        )

    def _generate_recommendations(self, findings: list[Finding], metrics: ArchitectureMetrics) -> list[Recommendation]:
        recs: list[Recommendation] = []
        if metrics.package_boundaries_crossed > 0:
            recs.append(
                Recommendation(
                    priority=Priority.high,
                    problem=f"{metrics.package_boundaries_crossed} package boundary violations",
                    solution=(
                        "Define explicit API contracts for each package. "
                        "Cross-package communication must use shared contracts, "
                        "not direct imports."
                    ),
                    effort=Effort.medium,
                    impact="Enforces package encapsulation",
                )
            )
        if metrics.dependency_cycles > 0:
            recs.append(
                Recommendation(
                    priority=Priority.high,
                    problem=f"{metrics.dependency_cycles} dependency cycles",
                    solution="Break each cycle by extracting shared interfaces.",
                    effort=Effort.medium,
                    impact="Improves testability and build times",
                )
            )
        if not recs:
            recs.append(
                Recommendation(
                    priority=Priority.low,
                    problem="No boundary violations detected",
                    solution="Maintain current boundary rules; review as project grows.",
                    effort=Effort.low,
                    impact="Preserves architecture integrity",
                )
            )
        return recs
