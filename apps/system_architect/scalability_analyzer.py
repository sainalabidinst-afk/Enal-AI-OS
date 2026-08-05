"""
System Architect — Scalability Analyzer.

Assesses scalability of a system based on architecture patterns,
dependency graph, and workload characteristics.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from apps.system_architect.schemas import Finding, FindingCategory, Severity, Impact, Recommendation, Priority, Effort

logger = logging.getLogger(__name__)


@dataclass
class ScalabilityAssessment:
    """Scalability assessment result."""
    score: float = 0.0
    bottlenecks: list[str] = field(default_factory=list)
    recommendations: list[Recommendation] = field(default_factory=list)


class ScalabilityAnalyzer:
    """
    Analyzes system scalability based on architecture patterns.

    Usage::

        analyzer = ScalabilityAnalyzer()
        assessment = analyzer.assess(dependency_graph, architecture_metrics)
    """

    def assess(self, metrics: Any) -> ScalabilityAssessment:
        """Assess scalability of the system based on metrics."""
        assessment = ScalabilityAssessment()
        assessment.bottlenecks = self._detect_bottlenecks(metrics)
        assessment.score = self._compute_score(metrics, assessment.bottlenecks)
        assessment.recommendations = self._generate_recommendations(assessment.bottlenecks, assessment.score)
        return assessment

    def _detect_bottlenecks(self, metrics: Any) -> list[str]:
        bottlenecks: list[str] = []
        if hasattr(metrics, 'dependency_cycles') and metrics.dependency_cycles > 0:
            bottlenecks.append("Circular dependencies create tight coupling and hinder horizontal scaling")
        if hasattr(metrics, 'layer_violations') and metrics.layer_violations > 5:
            bottlenecks.append("High layer violation count indicates poor separation of concerns")
        if hasattr(metrics, 'package_boundaries_crossed') and metrics.package_boundaries_crossed > 3:
            bottlenecks.append("Frequent cross-package communication increases coupling")
        return bottlenecks

    def _compute_score(self, metrics: Any, bottlenecks: list[str]) -> float:
        base = 100.0
        if hasattr(metrics, 'dependency_cycles'):
            base -= metrics.dependency_cycles * 10.0
        if hasattr(metrics, 'layer_violations'):
            base -= metrics.layer_violations * 3.0
        if hasattr(metrics, 'package_boundaries_crossed'):
            base -= metrics.package_boundaries_crossed * 4.0
        return max(0.0, min(100.0, base))

    def _generate_recommendations(self, bottlenecks: list[str], score: float) -> list[Recommendation]:
        recs: list[Recommendation] = []
        if "Circular dependencies" in str(bottlenecks):
            recs.append(Recommendation(
                priority=Priority.high,
                problem="Circular dependencies limit scalability",
                solution="Break cycles using dependency inversion or event-driven communication",
                effort=Effort.medium,
                impact="Enables independent scaling of modules",
            ))
        if score < 70:
            recs.append(Recommendation(
                priority=Priority.high,
                problem=f"Low scalability score: {score:.1f}/100",
                solution="Refactor to reduce coupling and improve separation of concerns",
                effort=Effort.high,
                impact="Improves horizontal scalability and team autonomy",
            ))
        return recs

    def to_findings(self, assessment: ScalabilityAssessment) -> list[Finding]:
        """Convert assessment to findings."""
        findings: list[Finding] = []
        for bottleneck in assessment.bottlenecks:
            findings.append(Finding(
                category=FindingCategory.architecture_smell,
                severity=Severity.medium,
                title="Scalability bottleneck detected",
                description=bottleneck,
                recommendation="Refactor to improve scalability",
                impact=Impact.scalability,
                confidence=0.8,
            ))
        return findings
