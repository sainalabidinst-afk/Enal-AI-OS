"""
QA Engineer — Performance Validator.

Validates performance requirements (latency, throughput, memory)
against specified targets and identifies bottlenecks.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any

from apps.qa_engineer.schemas import PerformanceValidation

logger = logging.getLogger(__name__)


@dataclass
class PerfMetric:
    """A single performance metric observation."""
    name: str
    value: float
    unit: str
    source: str


class PerformanceValidator:
    """
    Validates performance against requirements and identifies bottlenecks.

    Usage::

        validator = PerformanceValidator()
        result = validator.validate(source_code, perf_reqs={"latency_p95_ms": 200})
    """

    def validate(
        self,
        source_code: str,
        perf_reqs: dict[str, Any] | None = None,
    ) -> PerformanceValidation:
        """
        Validate performance requirements against observed/calculated metrics.

        Args:
            source_code: Source code to analyze for performance characteristics.
            perf_reqs: Performance requirements dict with:
                - latency_p95_ms: target P95 latency
                - throughput_rps: target throughput
                - max_memory_mb: max memory budget

        Returns:
            PerformanceValidation with pass/fail and bottleneck info.
        """
        if not perf_reqs:
            perf_reqs = {}

        bottlenecks: list[str] = []

        # Estimate metrics from source code analysis.
        metrics = self._estimate_metrics(source_code)

        target_latency = perf_reqs.get("latency_p95_ms", 200)
        target_throughput = perf_reqs.get("throughput_rps", 100)
        target_memory = perf_reqs.get("max_memory_mb", 512)

        observed_latency = metrics.get("latency_p95_ms", 50)
        observed_throughput = metrics.get("throughput_rps", 1000)
        observed_memory = metrics.get("memory_mb", 128)

        # Check bottlenecks from source analysis.
        bottlenecks.extend(self._detect_bottlenecks(source_code))

        meets_lat = observed_latency <= target_latency
        meets_thr = observed_throughput >= target_throughput
        meets_mem = observed_memory <= target_memory

        if not meets_lat:
            bottlenecks.append(f"Latency {observed_latency}ms exceeds target {target_latency}ms")
        if not meets_thr:
            bottlenecks.append(f"Throughput {observed_throughput:.1f} rps below target {target_throughput} rps")
        if not meets_mem:
            bottlenecks.append(f"Memory {observed_memory:.1f}MB exceeds budget {target_memory}MB")

        return PerformanceValidation(
            meets_latency_requirement=meets_lat,
            meets_throughput_requirement=meets_thr,
            meets_memory_requirement=meets_mem,
            latency_p95=int(observed_latency),
            throughput_rps=round(observed_throughput, 2),
            memory_mb=round(observed_memory, 2),
            bottlenecks=bottlenecks[:10],
        )

    def _estimate_metrics(self, source_code: str) -> dict[str, float]:
        """Estimate performance metrics from source code analysis."""
        metrics: dict[str, float] = {}

        # Count heavy operations that suggest performance characteristics.
        loop_count = len(re.findall(r'\bfor\b|\bwhile\b', source_code))
        io_ops = len(re.findall(r'\bopen\b|\bread\b|\bwrite\b|\brequest\.', source_code))
        db_ops = len(re.findall(r'\bexecute\b|\bquery\b|\bfind\b|\binsert\b|\bupdate\b', source_code))
        sleep_calls = len(re.findall(r'\bsleep\b|\bwait\b', source_code))

        # Heuristic metric estimation.
        metrics["latency_p95_ms"] = 50 + loop_count * 2 + io_ops * 10 + db_ops * 15 + sleep_calls * 100
        metrics["throughput_rps"] = max(1, 1000 - loop_count * 3 - io_ops * 5 - db_ops * 10)
        metrics["memory_mb"] = 64 + io_ops * 5 + db_ops * 10

        return metrics

    def _detect_bottlenecks(self, source_code: str) -> list[str]:
        """Detect likely performance bottlenecks in source code."""
        bottlenecks: list[str] = []

        if source_code.count("for") >= 5:
            bottlenecks.append("Nested loops detected — consider algorithmic optimization")

        if re.search(r'\bsleep\b|\btime\.sleep\b', source_code):
            bottlenecks.append("Sleep calls found — consider async/event-driven alternatives")

        if re.search(r'\bselect\b.*\*.*', source_code, re.IGNORECASE):
            bottlenecks.append("SELECT * detected — consider column-specific queries")

        if source_code.count("open(") > 5:
            bottlenecks.append("Frequent file I/O — consider batching or caching")

        return bottlenecks
