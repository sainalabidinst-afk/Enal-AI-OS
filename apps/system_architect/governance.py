"""
System Architect — Architecture Governance.

Enforces architectural rules and constraints:
- Core change guard (no Core modification without ADR)
- Capability First Rule (no Core change for single pack)
- Architecture rule consistency checking
- ADR cross-reference validation
- Dependency constraint enforcement
"""

from __future__ import annotations

import ast
import logging
from pathlib import Path
from typing import Any

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


class ArchitectureGovernance:
    """
    Enforces ECP architectural rules and constraints.

    Usage::
        governance = ArchitectureGovernance(repo_path)
        findings, recs = await governance.check()
    """

    # Core directories that should remain frozen
    CORE_PATHS = [
        "backend/app/core",
        "backend/app/__init__.py",
        "backend/app/main.py",
    ]

    # Capability Pack directories (allowed to evolve freely)
    CAPABILITY_PACKS = [
        "apps/network_engineer",
        "apps/code_engineer",
        "apps/research_assistant",
        "apps/devops_assistant",
        "apps/trading_analyst",
        "apps/self_development",
        "apps/decision_intelligence",
        "apps/system_architect",
    ]

    # ADR directory
    ADR_DIR = "docs/adr"

    def __init__(self, repo_path: str | Path):
        self.repo_path = Path(repo_path)

    async def check(self) -> tuple[list[Finding], list[Recommendation]]:
        """Run governance rules check."""
        findings: list[Finding] = []
        recommendations: list[Recommendation] = []

        # 1. Core change guard
        findings.extend(self._check_core_changes())

        # 2. Capability First Rule check
        findings.extend(self._check_capability_first_rule())

        # 3. ADR presence check
        findings.extend(self._check_adr_presence())

        # 4. Capability Pack boundary check
        findings.extend(self._check_capability_boundaries())

        # 5. Architecture principle consistency
        findings.extend(self._check_principle_consistency())

        # Generate recommendations
        recommendations = self._generate_recommendations(findings)

        return findings, recommendations

    # ------------------------------------------------------------------
    # Governance checks
    # ------------------------------------------------------------------

    def _check_core_changes(self) -> list[Finding]:
        """Check if Core has been modified without ADR references."""
        findings: list[Finding] = []
        for core_path in self.CORE_PATHS:
            full_path = self.repo_path / core_path
            if full_path.exists():
                # Check for recent modifications (heuristic: check for ADR references)
                try:
                    content = full_path.read_text(encoding="utf-8")
                    if "ADR" not in content and "adr" not in content.lower():
                        findings.append(
                            Finding(
                                category=FindingCategory.architecture_smell,
                                severity=Severity.low,
                                title=f"Core module may lack ADR reference: {core_path}",
                                description=(
                                    f"Core module `{core_path}` exists but may not contain "
                                    "ADR references. Per Architecture Freeze Policy, all Core "
                                    "changes require an ADR."
                                ),
                                evidence={
                                    "core_path": core_path,
                                    "has_adr_reference": "ADR" in content,
                                },
                                recommendation=(
                                    "Ensure any Core changes are documented with an ADR. "
                                    "If no changes were made, add a reference to the "
                                    "freeze policy."
                                ),
                                impact=Impact.maintainability,
                                confidence=0.5,
                            )
                        )
                except (IOError, Exception):
                    continue
        return findings

    def _check_capability_first_rule(self) -> list[Finding]:
        """Check for Capability First Rule violations."""
        findings: list[Finding] = []
        # Check if any single-capability-specific code is in Core
        for py_file in self.repo_path.rglob("*.py"):
            relative = str(py_file.relative_to(self.repo_path))
            if not relative.startswith("backend/app/core"):
                continue
            try:
                content = py_file.read_text(encoding="utf-8")
                tree = ast.parse(content, filename=str(py_file))
            except (SyntaxError, Exception):
                continue

            # Look for references to specific Capability Pack names
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        for pack in self.CAPABILITY_PACKS:
                            pkg_name = pack.split("/")[-1]
                            if pkg_name in alias.name:
                                findings.append(
                                    Finding(
                                        category=FindingCategory.layer_violation,
                                        severity=Severity.critical,
                                        title=f"Capability First Rule violation: Core imports {pkg_name}",
                                        description=(
                                            f"Core module `{relative}` imports `{alias.name}` "
                                            f"from Capability Pack `{pkg_name}`. "
                                            "Core must not depend on any Capability Pack."
                                        ),
                                        evidence={
                                            "core_file": relative,
                                            "imported_pack": pkg_name,
                                            "line_number": node.lineno,
                                        },
                                        recommendation=(
                                            f"Move the dependency from Core to the Capability "
                                            f"Pack `{pkg_name}` or use shared contracts."
                                        ),
                                        impact=Impact.maintainability,
                                        confidence=0.95,
                                    )
                                )
                                break
        return findings

    def _check_adr_presence(self) -> list[Finding]:
        """Check if ADRs exist and are properly referenced."""
        findings: list[Finding] = []
        adr_dir = self.repo_path / self.ADR_DIR
        if not adr_dir.exists():
            findings.append(
                Finding(
                    category=FindingCategory.architecture_smell,
                    severity=Severity.medium,
                    title="ADR directory not found",
                    description=(
                        f"ADR directory `{self.ADR_DIR}` does not exist. "
                        "Architecture Decision Records are required for governance."
                    ),
                    evidence={"adr_dir": self.ADR_DIR, "exists": False},
                    recommendation=(
                        "Create the ADR directory and start documenting architecture "
                        "decisions following the ADR template."
                    ),
                    impact=Impact.maintainability,
                    confidence=0.9,
                )
            )
        else:
            adr_files = list(adr_dir.glob("*.md"))
            if len(adr_files) < 3:
                findings.append(
                    Finding(
                        category=FindingCategory.architecture_smell,
                        severity=Severity.low,
                        title=f"Only {len(adr_files)} ADR(s) found",
                        description=(
                            f"Only {len(adr_files)} ADR(s) exist. "
                            "For a project with multiple Capability Packs, "
                            "more ADRs are expected for cross-cutting decisions."
                        ),
                        evidence={
                            "adr_count": len(adr_files),
                            "adr_files": [f.name for f in adr_files],
                        },
                        recommendation=(
                            "Review cross-capability decisions and document them as ADRs."
                        ),
                        impact=Impact.modifiability,
                        confidence=0.6,
                    )
                )
        return findings

    def _check_capability_boundaries(self) -> list[Finding]:
        """Check if Capability Packs respect boundary rules."""
        findings: list[Finding] = []
        for pack in self.CAPABILITY_PACKS:
            pack_dir = self.repo_path / pack
            if not pack_dir.exists():
                continue
            for py_file in pack_dir.rglob("*.py"):
                try:
                    content = py_file.read_text(encoding="utf-8")
                    tree = ast.parse(content, filename=str(py_file))
                except (SyntaxError, Exception):
                    continue
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            for other_pack in self.CAPABILITY_PACKS:
                                other_name = other_pack.split("/")[-1]
                                if other_name in alias.name:
                                    if other_name != pack.split("/")[-1]:
                                        findings.append(
                                            Finding(
                                                category=FindingCategory.package_boundary,
                                                severity=Severity.high,
                                                title=f"Capability Pack imports other pack: {pack}",
                                                description=(
                                                    f"Capability Pack `{pack}` imports `{alias.name}` "
                                                    f"from `{other_name}`. "
                                                    "Per ADR-002, Capability Packs must not "
                                                    "import each other directly."
                                                ),
                                                evidence={
                                                    "source_pack": pack,
                                                    "target_pack": other_name,
                                                    "imported_module": alias.name,
                                                    "line_number": node.lineno,
                                                },
                                                recommendation=(
                                                    "Use Execution Runtime task routing and "
                                                    "shared contracts for cross-pack communication."
                                                ),
                                                impact=Impact.modifiability,
                                                confidence=0.95,
                                            )
                                        )
                                        break
        return findings

    def _check_principle_consistency(self) -> list[Finding]:
        """Check consistency with ECP architecture principles."""
        findings: list[Finding] = []
        # Check for principle violations in Capability Pack code
        for pack in self.CAPABILITY_PACKS:
            pack_dir = self.repo_path / pack
            if not pack_dir.exists():
                continue
            for py_file in pack_dir.rglob("*.py"):
                try:
                    content = py_file.read_text(encoding="utf-8")
                except (IOError, Exception):
                    continue
                # Check for hardcoded model references (violates Principle 6)
                if "gpt-4" in content.lower() or "claude-3" in content.lower():
                    findings.append(
                        Finding(
                            category=FindingCategory.architecture_smell,
                            severity=Severity.medium,
                            title=f"Hardcoded model reference in {pack}",
                            description=(
                                "Hardcoded model references violate the Runtime Authority "
                                "Over Models principle. Workers should specify capabilities, "
                                "not models."
                            ),
                            evidence={
                                "pack": pack,
                                "file": str(py_file.relative_to(self.repo_path)),
                            },
                            recommendation=(
                                "Replace hardcoded model references with capability-based "
                                "routing through the Model Router."
                            ),
                            impact=Impact.modifiability,
                            confidence=0.7,
                        )
                    )
        return findings

    def _generate_recommendations(self, findings: list[Finding]) -> list[Recommendation]:
        recs: list[Recommendation] = []
        if any(f.severity == Severity.critical for f in findings):
            recs.append(
                Recommendation(
                    priority=Priority.critical,
                    problem=f"{sum(1 for f in findings if f.severity == Severity.critical)} critical governance violation(s)",
                    solution=(
                        "Address critical violations immediately: remove Core dependencies "
                        "on Capability Packs, register ADRs for all Core changes, "
                        "and enforce the Capability First Rule."
                    ),
                    effort=Effort.high,
                    impact="Restores architecture governance integrity",
                )
            )
        if any(f.severity == Severity.high for f in findings):
            recs.append(
                Recommendation(
                    priority=Priority.high,
                    problem="Governance rule violations detected",
                    solution=(
                        "Review all governance findings and fix high-severity issues. "
                        "Add ADR references where missing."
                    ),
                    effort=Effort.medium,
                    impact="Improves architecture compliance",
                )
            )
        if not recs:
            recs.append(
                Recommendation(
                    priority=Priority.low,
                    problem="No governance violations detected",
                    solution="Maintain current governance posture; review periodically.",
                    effort=Effort.low,
                    impact="Preserves architecture governance",
                )
            )
        return recs
