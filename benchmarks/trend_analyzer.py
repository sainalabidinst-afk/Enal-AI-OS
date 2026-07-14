"""
Trend Analyzer & Regression Detection
=========================================

Loads historical CCE results and computes:
- Per-vendor trend direction (up/down/stable)
- Regression detection against baseline
- Previous run comparison

Usage:
    from benchmarks.trend_analyzer import TrendAnalyzer

    analyzer = TrendAnalyzer()
    runs = analyzer.load_all_runs()
    trend = analyzer.compute_trend("mikrotik", current_score=92.0)
    regressions = analyzer.detect_regressions(current_results)
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

CCE_BASELINE_FILE = Path(__file__).resolve().parent / "cce_history" / "baseline.json"


@dataclass
class RegressionResult:
    vendor: str
    previous_score: float
    current_score: float
    delta: float
    threshold: float

    @property
    def is_regression(self) -> bool:
        return abs(self.delta) >= self.threshold and self.delta < 0


class TrendAnalyzer:
    def __init__(self, history_dir: Path = Path(__file__).resolve().parent / "cce_history") -> None:
        self.history_dir = history_dir

    def load_all_runs(self) -> list[dict[str, Any]]:
        runs: list[dict[str, Any]] = []
        if not self.history_dir.exists():
            return runs
        for path in sorted(self.history_dir.glob("*.json")):
            if path.name in ("baseline.json", "latest.json"):
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                data["_file"] = path.name
                runs.append(data)
            except Exception:
                continue
        runs.sort(key=lambda r: r.get("run_id", ""))
        return runs

    def load_previous_runs(self, limit: int = 5) -> list[dict[str, Any]]:
        return self.load_all_runs()[-limit:]

    def load_baseline(self) -> dict[str, Any] | None:
        if not CCE_BASELINE_FILE.exists():
            return None
        try:
            return json.loads(CCE_BASELINE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return None

    def save_baseline(self, summary: dict[str, Any]) -> None:
        try:
            CCE_BASELINE_FILE.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as exc:
            logger.warning("Failed to save baseline: %s", exc)

    def compute_trend(self, vendor: str, current_score: float) -> str:
        previous = self._latest_score_for_vendor(vendor)
        if previous is None:
            return "stable"
        delta = current_score - previous
        if delta > 0:
            return "up"
        if delta < 0:
            return "down"
        return "stable"

    def detect_regressions(self, current_summary: dict[str, Any], threshold: float = 5.0) -> list[RegressionResult]:
        baseline = self.load_baseline()
        if not baseline:
            return []
        regressions: list[RegressionResult] = []
        current_caps = current_summary.get("capabilities", {})
        baseline_caps = baseline.get("capabilities", {})
        for vendor, current in current_caps.items():
            previous = baseline_caps.get(vendor, {}).get("avg_capability_score")
            if previous is None:
                continue
            delta = current.get("avg_capability_score", previous) - previous
            if abs(delta) >= threshold and delta < 0:
                regressions.append(
                    RegressionResult(
                        vendor=vendor,
                        previous_score=previous,
                        current_score=current.get("avg_capability_score", previous),
                        delta=delta,
                        threshold=threshold,
                    )
                )
        return regressions

    def _latest_score_for_vendor(self, vendor: str) -> float | None:
        runs = self.load_previous_runs(limit=1)
        if not runs:
            return None
        caps = runs[-1].get("capabilities", {})
        vendor_data = caps.get(vendor)
        if not vendor_data:
            return None
        return vendor_data.get("avg_capability_score")
