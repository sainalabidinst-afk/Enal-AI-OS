"""
System Architect — Performance Architecture.

Analyzes system architecture for performance characteristics:
- Latency profiling and P95/P99 analysis
- Memory utilization patterns
- Throughput capacity and bottlenecks
- Database connection pooling
- Caching layer effectiveness
- Concurrency model analysis
- Resource contention detection

Produces PerformanceAssessment with bottleneck categorized findings
and actionable scaling recommendations.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.system_architect.schemas import (
    Finding,
    FindingCategory,
    Impact,
    PerformanceAssessment,
    Recommendation,
    Severity,
)

logger = logging.getLogger(__name__)

BOTTLENECK_CATEGORIES = {
    "cpu": "CPU-bound: high computational load in single-threaded path",
    "memory": "Memory: insufficient RAM or memory leaks detected",
    "io": "I/O: blocking I/O operations serializing requests",
    "network": "Network: latency or bandwidth bottleneck in service-to-service calls",
    "database": "Database: query performance or connection pool exhaustion",
}


class PerformanceArchitect:
    """
    Analyzes architecture for performance concerns based on metrics
    and workload characteristics.

    Usage::

        architect = PerformanceArchitect()
        assessment = architect.assess(metrics)
        findings = architect.to_findings(assessment)
    """

    def assess(self, metrics: Any) -> PerformanceAssessment:
        """Assess performance architecture based on quantitative metrics."""
        assessment = PerformanceAssessment()
        assessment.latency_p95_ms = getattr(metrics, "p95_latency_ms", 0.0)
        assessment.memory_mb = getattr(metrics, "memory_mb", 0.0)
        assessment.max_concurrent_requests = getattr(metrics, "max_concurrent_requests", 0)
        assessment.database_connections = getattr(metrics, "database_connections", 0)

        assessment.bottlenecks = self._detect_bottlenecks(metrics)
        assessment.throughput_qps = self._estimate_throughput(metrics)
        assessment.recommendations = self._generate_recommendations(assessment.bottlenecks, assessment)
        return assessment

    def _detect_bottlenecks(self, metrics: Any) -> list[str]:
        """Detect performance bottlenecks based on quantitative metrics."""
        bottlenecks: list[str] = []

        latency = getattr(metrics, "p95_latency_ms", 0.0)
        if latency > 2000:
            bottlenecks.append("High P95 latency ({:.0f}ms) — request processing exceeds acceptable SLA".format(latency))
        elif latency > 500:
            bottlenecks.append("Elevated P95 latency ({:.0f}ms) — consider caching or async processing".format(latency))

        memory = getattr(metrics, "memory_mb", 0.0)
        if memory > 1024:
            bottlenecks.append("High memory usage ({:.0f}MB) — potential memory leak or inefficient data structures".format(memory))

        db_conn = getattr(metrics, "database_connections", 0)
        if db_conn > 50:
            bottlenecks.append("Large database connection pool ({}) — may cause connection contention".format(db_conn))

        max_req = getattr(metrics, "max_concurrent_requests", 0)
        if max_req > 0:
            if max_req < 100:
                bottlenecks.append("Low concurrency capacity ({}) — limits horizontal throughput".format(max_req))
        else:
            bottlenecks.append("No concurrency metrics available — capacity unknown")

        return bottlenecks

    def _estimate_throughput(self, metrics: Any) -> float:
        """Estimate baseline throughput in QPS from latency and concurrency."""
        latency = getattr(metrics, "p95_latency_ms", 0.0)
        max_req = getattr(metrics, "max_concurrent_requests", 0)
        if latency > 0 and max_req > 0:
            return round(max_req / (latency / 1000.0), 2)
        return 0.0

    def _generate_recommendations(self, bottlenecks: list[str], assessment: PerformanceAssessment) -> list[str]:
        """Generate performance improvement recommendations."""
        recs: list[str] = []
        for b in bottlenecks:
            if "latency" in b.lower() and "p95" in b.lower():
                if "high" in b.lower():
                    recs.append("Implement caching layer (Redis/Memcached) to reduce P95 latency by 50-70%")
                    recs.append("Add horizontal scaling with load balancer for stateless services")
                else:
                    recs.append("Offload heavy computations to background queues (Celery/RQ)")
            if "memory" in b.lower():
                recs.append("Profile memory usage; implement object pooling for high-allocation paths")
            if "database" in b.lower() or "connection" in b.lower():
                recs.append("Implement read replica for read-heavy workloads; use connection pooling")
            if "concurrency" in b.lower():
                recs.append("Evaluate event-driven or actor model for higher concurrency")
        return list(dict.fromkeys(recs))

    def to_findings(self, assessment: PerformanceAssessment) -> list[Finding]:
        """Convert performance assessment to structured findings."""
        findings: list[Finding] = []

        category_map: dict[str, tuple[FindingCategory, str, str]] = {
            "latency": (FindingCategory.performance, "Latency threshold exceeded", "P95 latency exceeds recommended SLA threshold"),
            "memory": (FindingCategory.performance, "Memory pressure detected", "Memory usage exceeds optimal threshold"),
            "database": (FindingCategory.performance, "Database connection bottleneck", "Large connection pool risks contention"),
            "concurrency": (FindingCategory.scalability, "Limited concurrency capacity", "Low max concurrent requests limits throughput"),
        }

        for bottleneck in assessment.bottlenecks:
            bn = bottleneck.lower()
            category, title, description = FindingCategory.performance, "Performance bottleneck", bottleneck

            for key, (cat, t, d) in category_map.items():
                if key in bn:
                    category, title, description = cat, t, d
                    break

            findings.append(Finding(
                category=category,
                severity=Severity.high if "high" in bn else Severity.medium,
                title=title,
                description=description,
                recommendation="Optimize for the identified bottleneck; see PerformanceAssessment recommendations",
                impact=Impact.scalability if "concurrency" in bn else Impact.maintainability,
                confidence=0.8 if bottleneck else 0.5,
            ))

        if not findings and assessment.latency_p95_ms > 0:
            findings.append(Finding(
                category=FindingCategory.performance,
                severity=Severity.low,
                title="Performance baseline established",
                description="No critical bottlenecks detected; system within acceptable performance envelope",
                recommendation="Continue monitoring P95 latency and memory usage",
                impact=Impact.maintainability,
                confidence=0.9,
            ))

        return findings

    def to_recommendations(self, assessment: PerformanceAssessment) -> list[Recommendation]:
        """Convert performance recommendations to architecture recommendations."""
        from apps.system_architect.schemas import Effort, Priority

        recs: list[Recommendation] = []
        for rec in assessment.recommendations:
            recs.append(Recommendation(
                priority=Priority.high,
                problem=rec,
                solution=rec,
                effort=Effort.medium,
                impact="Improves P95 latency and throughput capacity",
            ))
        return recs
