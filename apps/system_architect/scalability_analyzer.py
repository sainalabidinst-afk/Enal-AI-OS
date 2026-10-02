"""
System Architect — Scalability Analyzer.

Assesses scalability of a system based on architecture patterns,
dependency graph, and workload characteristics. Detects bottlenecks
categorized by resource type (CPU, memory, I/O, network, database)
and recommends horizontal vs vertical scaling strategies.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from apps.system_architect.schemas import (
    Effort,
    Finding,
    FindingCategory,
    Impact,
    Priority,
    Recommendation,
    Severity,
)

logger = logging.getLogger(__name__)


BOTTLENECK_CATEGORIES = {
    "cpu": "CPU",
    "memory": "Memory",
    "io": "I/O",
    "network": "Network",
    "database": "Database",
}


@dataclass
class Bottleneck:
    """A identified scalability bottleneck with category and impact."""
    category: str
    description: str
    priority: Priority
    horizontal_scaling: bool
    impact: str


@dataclass
class ScalabilityAssessment:
    """Scalability assessment result."""
    score: float = 0.0
    score_breakdown: dict[str, float] = field(default_factory=dict)
    bottlenecks: list[Bottleneck] = field(default_factory=list)
    recommendations: list[Recommendation] = field(default_factory=list)


class ScalabilityAnalyzer:
    """
    Analyzes system scalability based on architecture patterns,
    dependency graph, and workload metrics.

    Usage::

        analyzer = ScalabilityAnalyzer()
        assessment = analyzer.assess(dependency_graph, architecture_metrics)
        findings = analyzer.to_findings(assessment)
    """

    def assess(self, snapshot: Any, metrics: Any) -> ScalabilityAssessment:
        """Assess scalability of the system based on dependency graph and metrics."""
        assessment = ScalabilityAssessment()
        assessment.bottlenecks = self._detect_bottlenecks(snapshot, metrics)
        assessment.score_breakdown = self._compute_score_breakdown(metrics)
        assessment.score = self._compute_score(metrics, assessment.bottlenecks)
        assessment.recommendations = self._generate_recommendations(assessment.bottlenecks, assessment.score)  # noqa: E501
        return assessment

    def _detect_bottlenecks(self, snapshot: Any, metrics: Any) -> list[Bottleneck]:
        """Detect and categorize scalability bottlenecks."""
        bottlenecks: list[Bottleneck] = []

        cycles = len(getattr(snapshot, 'circular_dependencies', []))
        if cycles > 0:
            bottlenecks.append(Bottleneck(
                category="cpu",
                description=f"{cycles} circular dependencies create tight coupling, serializing computation and hindering horizontal scaling",  # noqa: E501
                priority=Priority.high,
                horizontal_scaling=False,
                impact="Tight coupling forces vertical scaling (more CPU/memory per instance) instead of horizontal",  # noqa: E501
            ))

        layer_violations = getattr(metrics, 'layer_violations', 0)
        if layer_violations > 5:
            bottlenecks.append(Bottleneck(
                category="io",
                description="High layer violation count indicates poor separation of concerns, increasing cross-layer I/O",  # noqa: E501
                priority=Priority.medium,
                horizontal_scaling=False,
                impact="Poor separation increases I/O contention under load",
            ))

        boundaries = getattr(metrics, 'package_boundaries_crossed', 0)
        if boundaries > 3:
            bottlenecks.append(Bottleneck(
                category="network",
                description=f"{boundaries} package boundary crossings increase network calls between services",  # noqa: E501
                priority=Priority.medium,
                horizontal_scaling=False,
                impact="Excessive inter-service network calls reduce horizontal scaling efficiency",  # noqa: E501
            ))

        db_connections = getattr(metrics, 'database_connections', 0)
        if db_connections > 50:
            bottlenecks.append(Bottleneck(
                category="database",
                description=f"Large database connection pool ({db_connections}) risks connection exhaustion at scale",  # noqa: E501
                priority=Priority.high,
                horizontal_scaling=False,
                impact="Database connection limits cap horizontal scaling capacity",
            ))

        p95_latency = getattr(metrics, 'p95_latency_ms', 0.0)
        if p95_latency > 1000:
            bottlenecks.append(Bottleneck(
                category="database",
                description=f"P95 latency ({p95_latency:.0f}ms) suggests database query or I/O bottleneck under load",  # noqa: E501
                priority=Priority.high,
                horizontal_scaling=True,
                impact="Database layer limits request throughput and horizontal scaling",
            ))

        memory_mb = getattr(metrics, 'memory_mb', 0.0)
        if memory_mb > 512:
            bottlenecks.append(Bottleneck(
                category="memory",
                description=f"High memory usage ({memory_mb:.0f}MB) per instance limits container density",  # noqa: E501
                priority=Priority.medium,
                horizontal_scaling=False,
                impact="Memory-heavy instances reduce horizontal pod density",
            ))

        max_concurrent = getattr(metrics, 'max_concurrent_requests', 0)
        if max_concurrent > 0 and max_concurrent < 100:
            bottlenecks.append(Bottleneck(
                category="io",
                description=f"Low concurrency capacity ({max_concurrent}) — synchronous I/O limits request throughput",  # noqa: E501
                priority=Priority.medium,
                horizontal_scaling=False,
                impact="Synchronous processing limits horizontal scaling efficiency",
            ))

        return bottlenecks

    def _compute_score_breakdown(self, metrics: Any) -> dict[str, float]:
        """Compute per-dimension scalability scores."""
        breakdown: dict[str, float] = {}

        breakdown["coupling"] = max(0.0, 100.0 - getattr(metrics, 'dependency_cycles', 0) * 20.0)
        breakdown["layer_separation"] = max(0.0, 100.0 - max(0, getattr(metrics, 'layer_violations', 0) - 5) * 5.0)  # noqa: E501
        breakdown["boundary_efficiency"] = max(0.0, 100.0 - max(0, getattr(metrics, 'package_boundaries_crossed', 0) - 3) * 3.0)  # noqa: E501

        return breakdown

    def _compute_score(self, metrics: Any, bottlenecks: list[Bottleneck]) -> float:
        """Compute overall scalability score."""
        base = 100.0
        base -= getattr(metrics, 'dependency_cycles', 0) * 10.0
        base -= max(0, getattr(metrics, 'layer_violations', 0) - 5) * 3.0
        base -= max(0, getattr(metrics, 'package_boundaries_crossed', 0) - 3) * 4.0
        base -= min(len(bottlenecks), 5) * 8.0
        return max(0.0, min(100.0, base))

    def _generate_recommendations(self, bottlenecks: list[Bottleneck], score: float) -> list[Recommendation]:  # noqa: E501
        """Generate horizontal vs vertical scaling recommendations."""
        recs: list[Recommendation] = []

        has_horizontal = any(b.horizontal_scaling for b in bottlenecks)
        if has_horizontal:
            recs.append(Recommendation(
                priority=Priority.high,
                problem="Database-layer bottleneck limits horizontal scaling",
                solution="Implement read replica, connection pooling, and query optimization for horizontal scaling",  # noqa: E501
                effort=Effort.high,
                impact="Enables horizontal scaling without database contention",
            ))

        if not bottlenecks or score >= 90:
            return recs

        if score < 70:
            recs.append(Recommendation(
                priority=Priority.high,
                problem=f"Low scalability score: {score:.0f}/100",
                solution="Refactor to reduce coupling through dependency inversion or event-driven patterns; consider horizontal scaling via stateless microservices",  # noqa: E501
                effort=Effort.high,
                impact="Improves horizontal scalability and team autonomy",
            ))

        cycles = sum(1 for b in bottlenecks if b.category == "cpu")
        if cycles > 0:
            recs.append(Recommendation(
                priority=Priority.high,
                problem="Circular dependencies limit scalability",
                solution="Break cycles using dependency inversion or event-driven communication; enables horizontal scaling of services",  # noqa: E501
                effort=Effort.medium,
                impact="Enables independent horizontal scaling of modules",
            ))

        db_bottleneck = any(b.category == "database" for b in bottlenecks)
        if db_bottleneck:
            recs.append(Recommendation(
                priority=Priority.high,
                problem="Database bottleneck restricts horizontal scaling",
                solution="Horizontal: implement read replicas and sharding. Vertical: increase instance resources temporarily",  # noqa: E501
                effort=Effort.high,
                impact="Horizontal scaling via database read replicas; vertical scaling as interim relief",  # noqa: E501
            ))

        return recs

    def to_findings(self, assessment: ScalabilityAssessment) -> list[Finding]:
        """Convert assessment to findings."""
        findings: list[Finding] = []
        for bottleneck in assessment.bottlenecks:
            findings.append(Finding(
                category=FindingCategory.scalability,
                severity=Severity.high if bottleneck.priority == Priority.high else Severity.medium,
                title=f"Scalability bottleneck: {BOTTLENECK_CATEGORIES.get(bottleneck.category, bottleneck.category)}",  # noqa: E501
                description=bottleneck.description,
                recommendation=f"Horizontal scaling: {bottleneck.horizontal_scaling}; Impact: {bottleneck.impact}",  # noqa: E501
                impact=Impact.scalability,
                confidence=0.8,
            ))
        return findings
