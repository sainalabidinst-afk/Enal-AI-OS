"""
System Architect — Cost Optimizer.

Analyzes architecture for cost optimization opportunities:
- Resource utilization efficiency
- Redundant component identification
- Scalability cost trade-offs
- Infrastructure cost estimation
"""

from __future__ import annotations

import logging
from typing import Any

from apps.system_architect.schemas import (
    Finding,
    FindingCategory,
    Impact,
    Severity,
)

logger = logging.getLogger(__name__)


class CostOptimizer:
    """
    Analyzes architecture for cost optimization opportunities.

    Usage::

        optimizer = CostOptimizer()
        findings = optimizer.analyze(dependency_graph, metrics)
    """

    def analyze(self, snapshot: Any, metrics: Any) -> list[Finding]:
        """Analyze architecture for cost optimization based on dependency graph and metrics."""
        findings: list[Finding] = []
        findings.extend(self._check_redundancy(snapshot))
        findings.extend(self._check_resource_efficiency(metrics))
        findings.extend(self._check_scalability_cost(snapshot, metrics))
        return findings

    def _check_redundancy(self, snapshot: Any) -> list[Finding]:
        findings: list[Finding] = []
        modules = getattr(snapshot, "modules", {})
        if len(modules) > 50:
            findings.append(
                Finding(
                    category=FindingCategory.cost,
                    severity=Severity.low,
                    title="Large number of modules may indicate redundancy",
                    description=f"{len(modules)} modules detected; review for consolidation opportunities",  # noqa: E501
                    recommendation="Review modules for consolidation or shared library extraction",
                    impact=Impact.maintainability,
                    confidence=0.5,
                )
            )
        return findings

    def _check_resource_efficiency(self, metrics: Any) -> list[Finding]:
        findings: list[Finding] = []
        if hasattr(metrics, "maintainability_score") and metrics.maintainability_score < 60:
            findings.append(
                Finding(
                    category=FindingCategory.cost,
                    severity=Severity.medium,
                    title="Low maintainability increases operational cost",
                    description=f"Maintainability score {metrics.maintainability_score:.1f} indicates high technical debt",  # noqa: E501
                    recommendation="Invest in refactoring to reduce long-term maintenance costs",
                    impact=Impact.maintainability,
                    confidence=0.7,
                )
            )
        return findings

    def _check_scalability_cost(self, snapshot: Any, metrics: Any) -> list[Finding]:
        findings: list[Finding] = []
        cycles = len(getattr(snapshot, "circular_dependencies", []))
        if cycles > 3:
            findings.append(
                Finding(
                    category=FindingCategory.cost,
                    severity=Severity.medium,
                    title="Circular dependencies may increase scaling costs",
                    description=f"{cycles} circular dependencies detected; may require coordinated scaling",  # noqa: E501
                    recommendation="Break circular dependencies to enable independent scaling",
                    impact=Impact.scalability,
                    confidence=0.65,
                )
            )
        return findings
