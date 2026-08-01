"""
System Architect — Layer Analyzer (Clean Architecture review).

Evaluates a project against Clean Architecture / layered architecture principles:
- Layer stratification (entities → use_cases → interface_adapters → frameworks → infrastructure)
- Dependency rule enforcement (inner layers must not import outer layers)
- Package boundary conformance
- Layer completeness and cohesion
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from apps.system_architect.dependency_graph import (
    DependencyGraphBuilder,
    DependencyGraphSnapshot,
    Layer,
    DependencyType,
    ModuleInfo,
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


class LayerAnalyzer:
    """
    Analyzes a project's layer structure for Clean Architecture conformance.

    Usage::
        analyzer = LayerAnalyzer(repo_path)
        findings, metrics, recs = await analyzer.analyze()
    """

    def __init__(self, repo_path: str | Path):
        self.repo_path = Path(repo_path)
        self.graph_builder = DependencyGraphBuilder(self.repo_path)

    async def analyze(self) -> tuple[list[Finding], ArchitectureMetrics, list[Recommendation]]:
        """Run full layer analysis and return findings + metrics + recommendations."""
        snapshot = await self.graph_builder.build()

        findings: list[Finding] = []
        recommendations: list[Recommendation] = []

        # 1. Layer violation detection
        findings.extend(self._find_layer_violations(snapshot))

        # 2. Package boundary analysis
        findings.extend(self._find_boundary_violations(snapshot))

        # 3. Circular dependency detection
        findings.extend(self._find_circular_deps(snapshot))

        # 4. Layer completeness analysis
        layer_findings = self._analyze_layer_completeness(snapshot)
        findings.extend(layer_findings)

        # 5. Compute metrics
        metrics = self._compute_metrics(snapshot, findings)

        # 6. Generate recommendations
        recommendations = self._generate_recommendations(findings, metrics)

        return findings, metrics, recommendations

    # ------------------------------------------------------------------
    # Analysis methods
    # ------------------------------------------------------------------

    def _find_layer_violations(self, snapshot: DependencyGraphSnapshot) -> list[Finding]:
        """Detect layer dependency rule violations (inner → outer)."""
        findings: list[Finding] = []
        for dep in snapshot.layer_violations:
            finding = Finding(
                category=FindingCategory.layer_violation,
                severity=self._severity_for_layer_violation(dep.source_layer, dep.target_layer),
                title=f"Layer violation: {dep.source_layer} → {dep.target_layer}",
                description=(
                    f"Module `{dep.source}` (layer: {dep.source_layer}) imports "
                    f"`{dep.target}` (layer: {dep.target_layer}). "
                    "Clean Architecture dependency rule states that inner layers "
                    "must not depend on outer layers."
                ),
                evidence={
                    "source_file": dep.source,
                    "target_module": dep.target,
                    "source_layer": dep.source_layer,
                    "target_layer": dep.target_layer,
                    "line_number": dep.line_number,
                },
                recommendation=(
                    f"Move the dependency or abstraction from {dep.source_layer} "
                    f"into {dep.target_layer} or introduce an interface at the "
                    "inner layer boundary."
                ),
                impact=Impact.maintainability,
                confidence=0.9,
            )
            findings.append(finding)
        return findings

    def _find_boundary_violations(self, snapshot: DependencyGraphSnapshot) -> list[Finding]:
        """Detect cross-package/package boundary violations."""
        findings: list[Finding] = []
        for dep in snapshot.boundary_violations:
            finding = Finding(
                category=FindingCategory.package_boundary,
                severity=Severity.high,
                title=f"Package boundary violation: {dep.target}",
                description=(
                    f"Module `{dep.source}` imports `{dep.target}`, which is "
                    "outside the allowed package boundary. "
                    "Cross-package communication should use shared contracts only."
                ),
                evidence={
                    "source_file": dep.source,
                    "target_module": dep.target,
                    "source_layer": dep.source_layer,
                    "line_number": dep.line_number,
                },
                recommendation=(
                    "Use shared contracts, interfaces, or dependency injection "
                    "to decouple cross-package communication."
                ),
                impact=Impact.modifiability,
                confidence=0.85,
            )
            findings.append(finding)
        return findings

    def _find_circular_deps(self, snapshot: DependencyGraphSnapshot) -> list[Finding]:
        """Detect circular dependencies from the snapshot."""
        findings: list[Finding] = []
        for cycle in snapshot.circular_dependencies:
            cycle_str = " → ".join(cycle)
            finding = Finding(
                category=FindingCategory.dependency_cycle,
                severity=Severity.high,
                title=f"Circular dependency detected ({len(cycle)} modules)",
                description=(
                    f"Circular dependency chain: {cycle_str}. "
                    "Circular dependencies create tight coupling, hinder testability, "
                    "and make the system harder to refactor."
                ),
                evidence={
                    "cycle": cycle,
                    "cycle_length": len(cycle),
                },
                recommendation=(
                    "Break the cycle by extracting shared interfaces, merging modules, "
                    "or applying dependency inversion."
                ),
                impact=Impact.testability,
                confidence=0.95,
            )
            findings.append(finding)
        return findings

    def _analyze_layer_completeness(self, snapshot: DependencyGraphSnapshot) -> list[Finding]:
        """Analyze whether all layers are present and reasonably separated."""
        findings: list[Finding] = []
        present_layers = set(snapshot.layer_counts.keys())

        # Check for missing core layers
        core_layers = [Layer.ENTITIES, Layer.USE_CASES, Layer.INTERFACE_ADAPTERS]
        for layer in core_layers:
            if layer not in present_layers:
                findings.append(
                    Finding(
                        category=FindingCategory.architecture_smell,
                        severity=Severity.medium,
                        title=f"Missing architectural layer: {layer}",
                        description=(
                            f"No modules found in the `{layer}` layer. "
                            "This may indicate an incomplete Clean Architecture "
                            "or a different architectural style."
                        ),
                        evidence={
                            "missing_layer": layer,
                            "present_layers": list(present_layers),
                        },
                        recommendation=(
                            f"Consider introducing a `{layer}` layer to separate concerns. "
                            "If using a different architectural style, document the decision."
                        ),
                        impact=Impact.maintainability,
                        confidence=0.7,
                    )
                )

        # Check for layer mixing (modules in wrong layers)
        for mod_path, mod_info in snapshot.modules.items():
            if mod_info.layer == Layer.UNKNOWN:
                # Check if this module has dependencies that suggest a layer
                layers_imported = set()
                for dep in mod_info.dependencies:
                    if dep.target_layer != Layer.UNKNOWN:
                        layers_imported.add(dep.target_layer)
                if layers_imported:
                    suggested = self._suggest_layer(layers_imported)
                    if suggested:
                        findings.append(
                            Finding(
                                category=FindingCategory.architecture_smell,
                                severity=Severity.low,
                                title=f"Unclassified module: {mod_path}",
                                description=(
                                    f"Module `{mod_path}` could not be classified into a layer. "
                                    f"It imports from layers: {', '.join(sorted(layers_imported))}. "
                                    f"Suggested layer: {suggested}."
                                ),
                                evidence={
                                    "module_path": mod_path,
                                    "imported_layers": list(layers_imported),
                                    "suggested_layer": suggested,
                                },
                                recommendation=(
                                    f"Move this module to `{suggested}` or add a package hint "
                                    "to clarify its architectural role."
                                ),
                                impact=Impact.maintainability,
                                confidence=0.6,
                            )
                        )
        return findings

    def _suggest_layer(self, imported_layers: set[str]) -> str | None:
        """Suggest a layer for a module based on its imported layers."""
        if Layer.USE_CASES in imported_layers:
            return Layer.INTERFACE_ADAPTERS
        if Layer.ENTITIES in imported_layers:
            return Layer.USE_CASES
        if Layer.INTERFACE_ADAPTERS in imported_layers:
            return Layer.FRAMEWORKS
        return None

    # ------------------------------------------------------------------
    # Metrics & Recommendations
    # ------------------------------------------------------------------

    def _compute_metrics(self, snapshot: DependencyGraphSnapshot, findings: list[Finding]) -> ArchitectureMetrics:
        """Compute quantitative architecture metrics from analysis."""
        layer_violations = sum(1 for f in findings if f.category == FindingCategory.layer_violation)
        dep_cycles = sum(1 for f in findings if f.category == FindingCategory.dependency_cycle)
        boundary_violations = sum(1 for f in findings if f.category == FindingCategory.package_boundary)

        total = snapshot.total_modules
        layer_violations_count = len(snapshot.layer_violations)
        cycles_count = len(snapshot.circular_dependencies)

        # Maintainability: inversely proportional to violations, cycles, and unclassified modules
        unknown_count = snapshot.layer_counts.get(Layer.UNKNOWN, 0)
        maintainability = max(0.0, 100.0 - (
            layer_violations_count * 5.0 + cycles_count * 10.0 + unknown_count * 3.0
        ))

        # Scalability: affected by circular deps and boundary violations
        scalability = max(0.0, 100.0 - (cycles_count * 8.0 + boundary_violations * 4.0))

        # Testability: affected by circular deps and layer violations
        testability = max(0.0, 100.0 - (cycles_count * 6.0 + layer_violations_count * 4.0))

        return ArchitectureMetrics(
            dependency_cycles=cycles_count,
            layer_violations=layer_violations_count,
            package_boundaries_crossed=boundary_violations,
            maintainability_score=round(maintainability, 1),
            scalability_score=round(scalability, 1),
            testability_score=round(testability, 1),
        )

    def _generate_recommendations(
        self,
        findings: list[Finding],
        metrics: ArchitectureMetrics,
    ) -> list[Recommendation]:
        """Generate remediation recommendations based on findings."""
        recs: list[Recommendation] = []

        if metrics.layer_violations > 0:
            recs.append(
                Recommendation(
                    priority=Priority.high,
                    problem=f"{metrics.layer_violations} layer violations detected",
                    solution=(
                        "Apply dependency inversion: introduce interfaces/abstractions at boundary "
                        "layers so inner layers depend on interfaces, not concrete implementations."
                    ),
                    effort=Effort.high,
                    impact="Restores Clean Architecture dependency rule",
                )
            )

        if metrics.dependency_cycles > 0:
            recs.append(
                Recommendation(
                    priority=Priority.high,
                    problem=f"{metrics.dependency_cycles} circular dependencies",
                    solution=(
                        "Break each cycle by extracting shared interfaces, merging modules, "
                        "or using dependency injection to invert the dependency direction."
                    ),
                    effort=Effort.medium,
                    impact="Improves testability, maintainability, and build times",
                )
            )

        if metrics.package_boundaries_crossed > 0:
            recs.append(
                Recommendation(
                    priority=Priority.medium,
                    problem=f"{metrics.package_boundaries_crossed} package boundary violations",
                    solution=(
                        "Define explicit API/interface contracts for each package. "
                        "Cross-package communication should use shared contracts only, "
                        "not direct imports."
                    ),
                    effort=Effort.medium,
                    impact="Enforces package encapsulation and reduces coupling",
                )
            )

        if metrics.maintainability_score < 70:
            recs.append(
                Recommendation(
                    priority=Priority.medium,
                    problem=f"Low maintainability score: {metrics.maintainability_score:.1f}/100",
                    solution=(
                        "Conduct a targeted refactoring sprint to reduce violations and cycles. "
                        "Focus on the modules with the highest impact scores."
                    ),
                    effort=Effort.high,
                    impact="Improves long-term maintainability and developer productivity",
                )
            )

        if not recs:
            recs.append(
                Recommendation(
                    priority=Priority.low,
                    problem="No critical architectural issues found",
                    solution="Continue monitoring architecture quality; consider periodic reviews.",
                    effort=Effort.low,
                    impact="Maintains current architecture quality",
                )
            )

        return recs

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _severity_for_layer_violation(self, source_layer: str, target_layer: str) -> Severity:
        """Determine severity based on how far the violation crosses layers."""
        if source_layer in Layer.INNER and target_layer in Layer.OUTER:
            return Severity.critical
        if source_layer == Layer.ENTITIES and target_layer == Layer.USE_CASES:
            return Severity.high
        return Severity.medium
