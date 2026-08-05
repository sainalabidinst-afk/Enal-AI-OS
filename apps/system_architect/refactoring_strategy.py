"""
System Architect — Refactoring Strategy.

Recommends refactoring strategies based on architecture analysis:
- Code smells and anti-patterns
- Dependency restructuring
- Layer reorganization
- Module consolidation
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from apps.system_architect.schemas import Finding, FindingCategory, Severity, Impact, Recommendation, Priority, Effort

logger = logging.getLogger(__name__)


class RefactoringStrategy:
    """
    Recommends refactoring strategies based on architecture analysis.

    Usage::

        strategy = RefactoringStrategy()
        recs = strategy.recommend(findings, metrics)
    """

    def recommend(self, findings: list[Finding], metrics: Any) -> list[Recommendation]:
        """Generate refactoring recommendations."""
        recs: list[Recommendation] = []
        layer_violations = sum(1 for f in findings if f.category == FindingCategory.layer_violation)
        cycles = sum(1 for f in findings if f.category == FindingCategory.dependency_cycle)
        boundaries = sum(1 for f in findings if f.category == FindingCategory.package_boundary)

        if layer_violations > 0:
            recs.append(Recommendation(
                priority=Priority.high,
                problem=f"{layer_violations} layer violations detected",
                solution="Apply dependency inversion and move dependencies to correct layers",
                effort=Effort.high,
                impact="Restores Clean Architecture dependency rule",
            ))

        if cycles > 0:
            recs.append(Recommendation(
                priority=Priority.high,
                problem=f"{cycles} circular dependencies detected",
                solution="Break cycles by extracting shared interfaces or merging modules",
                effort=Effort.medium,
                impact="Improves testability and reduces coupling",
            ))

        if boundaries > 0:
            recs.append(Recommendation(
                priority=Priority.medium,
                problem=f"{boundaries} package boundary violations detected",
                solution="Define explicit API contracts and use dependency injection",
                effort=Effort.medium,
                impact="Reduces coupling between packages",
            ))

        return recs
