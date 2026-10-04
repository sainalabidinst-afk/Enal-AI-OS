"""
Anomaly Detector
================

Detects infrastructure, performance, and security anomalies from telemetry.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class Anomaly:
    anomaly_id: str
    category: str
    severity: str
    metric: str
    current_value: float
    baseline: float
    deviation_pct: float
    description: str
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class AnomalyDetector:
    """Detects anomalies from metric samples."""

    def detect(
        self,
        metric: str,
        current_value: float,
        baseline: float,
        threshold_pct: float = 20.0,
        category: str = "performance",
        severity: str = "medium",
        description: str = "",
    ) -> Anomaly | None:
        if baseline == 0:
            return None
        deviation = ((current_value - baseline) / baseline) * 100.0
        if abs(deviation) < threshold_pct:
            return None
        direction = "up" if deviation > 0 else "down"
        derived_severity = severity
        if abs(deviation) >= 100:
            derived_severity = "critical"
        elif abs(deviation) >= 50:
            derived_severity = "high"
        return Anomaly(
            anomaly_id=f"anomaly-{datetime.now(UTC).timestamp()}",
            category=category,
            severity=derived_severity,
            metric=metric,
            current_value=current_value,
            baseline=baseline,
            deviation_pct=round(deviation, 2),
            description=description or f"{metric} deviated {direction} by {abs(deviation):.2f}%",
        )

    def detect_batch(self, samples: list[dict[str, Any]]) -> list[Anomaly]:
        results: list[Anomaly] = []
        for sample in samples:
            anomaly = self.detect(
                metric=sample.get("metric", ""),
                current_value=float(sample.get("current_value", 0)),
                baseline=float(sample.get("baseline", 0)),
                threshold_pct=float(sample.get("threshold_pct", 20.0)),
                category=sample.get("category", "performance"),
                severity=sample.get("severity", "medium"),
                description=sample.get("description", ""),
            )
            if anomaly is not None:
                results.append(anomaly)
        return results


anomaly_detector = AnomalyDetector()
