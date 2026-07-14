"""
Confidence Calibration
========================

Analyzes whether model confidence scores reflect actual accuracy.

Creates bins (e.g., 0.90-1.00, 0.80-0.89) and computes empirical accuracy
per bin. Useful for detecting overconfidence or underconfidence.

Usage:
    from benchmarks.calibration import ConfidenceCalibration
    from backend.app.core.benchmark.models import BenchmarkSuite

    calibration = ConfidenceCalibration(suite.results)
    report = calibration.report()
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class CalibrationBin:
    label: str
    confidence_min: float
    confidence_max: float
    count: int = 0
    correct: int = 0

    @property
    def accuracy(self) -> float:
        return round(self.correct / max(self.count, 1), 2)


@dataclass
class ConfidenceCalibration:
    results: list[Any]
    bins: list[CalibrationBin] = field(default_factory=lambda: [
        CalibrationBin("0.90-1.00", 0.90, 1.00),
        CalibrationBin("0.80-0.89", 0.80, 0.89),
        CalibrationBin("0.70-0.79", 0.70, 0.79),
        CalibrationBin("0.60-0.69", 0.60, 0.69),
        CalibrationBin("0.50-0.59", 0.50, 0.59),
        CalibrationBin("0.00-0.49", 0.00, 0.49),
    ])

    def __post_init__(self) -> None:
        self._build()

    def _build(self) -> None:
        for result in self.results:
            confidence = getattr(result, "confidence", 0.0) or 0.0
            passed = getattr(result, "passed", False)
            for bin in self.bins:
                if bin.confidence_min <= confidence <= bin.confidence_max:
                    bin.count += 1
                    if passed:
                        bin.correct += 1
                    break

    def report(self) -> dict[str, Any]:
        total = sum(bin.count for bin in self.bins)
        overall_accuracy = round(sum(bin.correct for bin in self.bins) / max(total, 1), 2)
        return {
            "total_calibrated": total,
            "overall_accuracy": overall_accuracy,
            "bins": [
                {
                    "label": b.label,
                    "count": b.count,
                    "correct": b.correct,
                    "accuracy": b.accuracy,
                }
                for b in self.bins
                if b.count > 0
            ],
            "overconfident_bins": self._overconfident_bins(),
            "underconfident_bins": self._underconfident_bins(),
        }

    def _overconfident_bins(self) -> list[dict[str, Any]]:
        return [
            {"label": b.label, "confidence": round((b.confidence_min + b.confidence_max) / 2, 2), "accuracy": b.accuracy}
            for b in self.bins
            if b.count > 0 and b.accuracy < (b.confidence_min + b.confidence_max) / 2 - 0.05
        ]

    def _underconfident_bins(self) -> list[dict[str, Any]]:
        return [
            {"label": b.label, "confidence": round((b.confidence_min + b.confidence_max) / 2, 2), "accuracy": b.accuracy}
            for b in self.bins
            if b.count > 0 and b.accuracy > (b.confidence_min + b.confidence_max) / 2 + 0.05
        ]
