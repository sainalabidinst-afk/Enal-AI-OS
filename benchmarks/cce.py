"""
Continuous Capability Evaluation (CCE)
=========================================

Automated quality gate for Enal AI OS capabilities.

Runs on every commit/PR and produces:
- Capability scores per vendor
- Regression detection against baseline
- Trend analysis across runs
- HTML report
- GitHub Badge data

Usage:
    from benchmarks.cce import CCERunner

    runner = CCERunner(base_url="http://localhost:8000")
    result = await runner.run()
    print(result.summary)
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from benchmarks.trend_analyzer import TrendAnalyzer, RegressionResult
from benchmarks.report_generator import generate_html_report
from benchmarks.calibration import ConfidenceCalibration
from backend.app.core.benchmark.runner import BenchmarkRunner
from backend.app.core.benchmark.models import BenchmarkSuite

logger = logging.getLogger(__name__)

CCE_HISTORY_DIR = Path(__file__).resolve().parent / "cce_history"
CCE_HISTORY_DIR.mkdir(parents=True, exist_ok=True)
CCE_BASELINE_FILE = CCE_HISTORY_DIR / "baseline.json"


@dataclass
class CCECapabilityResult:
    vendor: str
    cases: int = 0
    passed: int = 0
    failed: int = 0
    avg_score: float = 0.0
    avg_capability_score: float = 0.0
    parser: float = 0.0
    reasoning: float = 0.0
    evidence: float = 0.0
    compliance: float = 0.0
    executive_report: float = 0.0
    regression: bool = False
    trend: str = "stable"
    previous_score: float | None = None


@dataclass
class CCEResult:
    run_id: str
    timestamp: str
    total_cases: int = 0
    passed_cases: int = 0
    failed_cases: int = 0
    avg_score: float = 0.0
    avg_capability_score: float = 0.0
    duration_ms: int = 0
    regressions: list[RegressionResult] = field(default_factory=list)
    capabilities: dict[str, CCECapabilityResult] = field(default_factory=dict)
    calibration: dict[str, Any] = field(default_factory=dict)
    details: dict[str, Any] = field(default_factory=dict)

    @property
    def summary(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "total_cases": self.total_cases,
            "passed_cases": self.passed_cases,
            "failed_cases": self.failed_cases,
            "pass_rate": round(self.passed_cases / max(self.total_cases, 1), 2),
            "avg_score": round(self.avg_score, 2),
            "avg_capability_score": round(self.avg_capability_score, 2),
            "regression_count": len(self.regressions),
            "regressions": [
                {
                    "vendor": r.vendor,
                    "previous": round(r.previous_score, 2),
                    "current": round(r.current_score, 2),
                    "delta": round(r.delta, 2),
                }
                for r in self.regressions
            ],
            "capabilities": {
                vendor: {
                    "vendor": cap.vendor,
                    "cases": cap.cases,
                    "passed": cap.passed,
                    "failed": cap.failed,
                    "avg_score": round(cap.avg_score, 2),
                    "avg_capability_score": round(cap.avg_capability_score, 2),
                    "parser": round(cap.parser, 2),
                    "reasoning": round(cap.reasoning, 2),
                    "evidence": round(cap.evidence, 2),
                    "compliance": round(cap.compliance, 2),
                    "executive_report": round(cap.executive_report, 2),
                    "regression": cap.regression,
                    "trend": cap.trend,
                    "previous_score": round(cap.previous_score, 2) if cap.previous_score is not None else None,
                }
                for vendor, cap in sorted(self.capabilities.items())
            },
        }


class CCERunner:
    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        concurrency: int = 5,
        regression_threshold: float = 5.0,
        history_dir: Path = CCE_HISTORY_DIR,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.concurrency = concurrency
        self.regression_threshold = regression_threshold
        self.history_dir = history_dir
        self.runner = BenchmarkRunner(base_url=base_url, concurrency=concurrency)
        self.trend_analyzer = TrendAnalyzer(history_dir=history_dir)

    async def run(self, suite: BenchmarkSuite | None = None) -> CCEResult:
        run_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        started = time.perf_counter()
        result = CCEResult(run_id=run_id, timestamp=datetime.now(timezone.utc).isoformat())

        if suite is None:
            from backend.app.api.benchmark import _load_suite_from_disk
            suite = _load_suite_from_disk()

        if not suite.cases:
            result.details = {"warning": "No benchmark cases found"}
            return result

        suite = await self.runner.run_suite(suite)
        result.total_cases = len(suite.results)
        result.passed_cases = sum(1 for r in suite.results if r.passed)
        result.failed_cases = result.total_cases - result.passed_cases
        result.avg_score = sum(r.score for r in suite.results) / max(result.total_cases, 1)
        result.avg_capability_score = sum(r.capability_score for r in suite.results) / max(result.total_cases, 1)
        result.duration_ms = int((time.perf_counter() - started) * 1000)

        capability_data: dict[str, dict[str, Any]] = {}
        for r in suite.results:
            vendor = r.case_id.split(":")[0]
            if vendor not in capability_data:
                capability_data[vendor] = {
                    "scores": [],
                    "capability_scores": [],
                    "parser": [],
                    "reasoning": [],
                    "evidence": [],
                    "compliance": [],
                    "executive_report": [],
                    "passed": 0,
                    "failed": 0,
                }
            cd = capability_data[vendor]
            cd["scores"].append(r.score)
            cd["capability_scores"].append(r.capability_score)
            cd["passed" if r.passed else "failed"] += 1
            if r.capability_breakdown:
                cd["parser"].append(r.capability_breakdown.parser)
                cd["reasoning"].append(r.capability_breakdown.reasoning)
                cd["evidence"].append(r.capability_breakdown.evidence)
                cd["compliance"].append(r.capability_breakdown.compliance)
                cd["executive_report"].append(r.capability_breakdown.executive_report)

        previous_runs = self.trend_analyzer.load_previous_runs(limit=1)
        previous_scores: dict[str, float] = {}
        if previous_runs:
            for vendor, cap in previous_runs[-1].get("capabilities", {}).items():
                previous_scores[vendor] = cap.get("avg_capability_score", 0.0)

        for vendor, cd in capability_data.items():
            cap = CCECapabilityResult(
                vendor=vendor,
                cases=len(cd["scores"]),
                passed=cd["passed"],
                failed=cd["failed"],
                avg_score=sum(cd["scores"]) / max(len(cd["scores"]), 1),
                avg_capability_score=sum(cd["capability_scores"]) / max(len(cd["capability_scores"]), 1),
                parser=sum(cd["parser"]) / max(len(cd["parser"]), 1),
                reasoning=sum(cd["reasoning"]) / max(len(cd["reasoning"]), 1),
                evidence=sum(cd["evidence"]) / max(len(cd["evidence"]), 1),
                compliance=sum(cd["compliance"]) / max(len(cd["compliance"]), 1),
                executive_report=sum(cd["executive_report"]) / max(len(cd["executive_report"]), 1),
            )
            prev = previous_scores.get(vendor)
            if prev is not None:
                cap.previous_score = prev
                cap.trend = self.trend_analyzer.compute_trend(vendor, cap.avg_capability_score)
                if abs(cap.avg_capability_score - prev) >= self.regression_threshold and cap.avg_capability_score < prev:
                    cap.regression = True
                    result.regressions.append(
                        RegressionResult(
                            vendor=vendor,
                            previous_score=prev,
                            current_score=cap.avg_capability_score,
                            delta=cap.avg_capability_score - prev,
                            threshold=self.regression_threshold,
                        )
                    )
            result.capabilities[vendor] = cap

        calibration = ConfidenceCalibration(suite.results)
        result.calibration = calibration.report()

        self.history_dir.mkdir(parents=True, exist_ok=True)
        (self.history_dir / "latest.json").write_text(
            json.dumps(result.summary, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        history_file = self.history_dir / f"{run_id}.json"
        history_file.write_text(json.dumps(result.summary, indent=2, ensure_ascii=False), encoding="utf-8")

        logger.info(
            "CCE complete: run_id=%s total=%s passed=%s regressions=%s",
            run_id,
            result.total_cases,
            result.passed_cases,
            len(result.regressions),
        )
        return result

    def generate_report(self, result: CCEResult, output_path: Path | None = None) -> Path:
        if output_path is None:
            output_path = self.history_dir / f"report-{result.run_id}.html"
        generate_html_report(result, output_path)
        logger.info("CCE HTML report generated: %s", output_path)
        return output_path

    def has_regression(self, result: CCEResult) -> bool:
        return any(cap.regression for cap in result.capabilities.values())
