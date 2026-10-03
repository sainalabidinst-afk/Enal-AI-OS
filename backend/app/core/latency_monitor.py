"""
Latency monitor for voice agents.

Tracks TTFS, P50/P90/P99 latencies for voice pipeline stages.
"""

from __future__ import annotations

import logging
from collections import deque
from typing import Any

logger = logging.getLogger(__name__)


class LatencyMonitor:
    """Track voice agent latency metrics."""

    def __init__(self, max_samples: int = 1000) -> None:
        self.max_samples = max_samples
        self._samples: deque[float] = deque(maxlen=max_samples)
        self._stage_samples: dict[str, deque[float]] = {}

    def record(self, latency_ms: float, stage: str = "total") -> None:
        self._samples.append(latency_ms)
        if stage not in self._stage_samples:
            self._stage_samples[stage] = deque(maxlen=self.max_samples)
        self._stage_samples[stage].append(latency_ms)

    def percentile(self, p: float) -> float | None:
        if not self._samples:
            return None
        sorted_samples = sorted(self._samples)
        index = int(len(sorted_samples) * p / 100)
        return sorted_samples[min(index, len(sorted_samples) - 1)]

    def stats(self) -> dict[str, Any]:
        if not self._samples:
            return {}
        sorted_samples = sorted(self._samples)
        return {
            "count": len(sorted_samples),
            "min": sorted_samples[0],
            "max": sorted_samples[-1],
            "p50": self.percentile(50),
            "p90": self.percentile(90),
            "p99": self.percentile(99),
            "mean": sum(sorted_samples) / len(sorted_samples),
        }

    def stage_stats(self, stage: str) -> dict[str, Any]:
        samples = self._stage_samples.get(stage)
        if not samples:
            return {}
        sorted_samples = sorted(samples)
        return {
            "stage": stage,
            "count": len(sorted_samples),
            "min": sorted_samples[0],
            "max": sorted_samples[-1],
            "p50": self.percentile(50),
            "p90": self.percentile(90),
            "p99": self.percentile(99),
        }


latency_monitor = LatencyMonitor()
