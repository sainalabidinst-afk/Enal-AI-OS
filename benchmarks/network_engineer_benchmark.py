"""
Network Engineer Benchmark
===========================

Runs benchmark against all real cases for network capability.
Exports results and computes accuracy/latency/coverage metrics.
"""

from __future__ import annotations

import csv
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from real_cases.benchmark import BenchmarkHarness, load_cases_from_disk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REPORT_DIR = Path(__file__).resolve().parent.parent / "benchmarks" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class NetworkBenchmarkReport:
    generated_at: datetime = field(default_factory=datetime.utcnow)
    total_cases: int = 0
    passed_cases: int = 0
    failed_cases: int = 0
    pass_rate: float = 0.0
    avg_score: float = 0.0
    avg_latency_ms: float = 0.0
    avg_capability_score: float = 0.0
    vendor_breakdown: dict[str, Any] = field(default_factory=dict)
    results: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at.isoformat(),
            "total_cases": self.total_cases,
            "passed_cases": self.passed_cases,
            "failed_cases": self.failed_cases,
            "pass_rate": self.pass_rate,
            "avg_score": self.avg_score,
            "avg_latency_ms": self.avg_latency_ms,
            "avg_capability_score": self.avg_capability_score,
            "vendor_breakdown": self.vendor_breakdown,
            "results": self.results,
        }


def run_network_benchmark() -> NetworkBenchmarkReport:
    logger.info("Loading network real cases...")
    cases = [case for case in load_cases_from_disk() if case.category in {"network", "mikrotik", "cisco", "fortinet"}]
    if not cases:
        logger.warning("No network real cases found. Run real_cases/collector.py to populate cases.")

    harness = BenchmarkHarness()
    report = NetworkBenchmarkReport(total_cases=len(cases))

    vendor_map: dict[str, list[dict[str, Any]]] = {}
    for case in cases:
        logger.info("Running benchmark for case: %s", case.id)
        result = harness.run(case)
        entry = {
            "case_id": case.id,
            "title": case.title,
            "vendor": case.vendor,
            "passed": result.passed,
            "score": result.score,
            "findings_matched": result.findings_matched,
            "expected_findings": result.expected_findings,
            "execution_time_ms": result.execution_time_ms,
            "capability_score": result.capability_score,
            "errors": result.errors,
        }
        report.results.append(entry)
        vendor_map.setdefault(case.vendor or "unknown", []).append(entry)

    passed = sum(1 for r in report.results if r["passed"])
    report.passed_cases = passed
    report.failed_cases = len(report.results) - passed
    report.pass_rate = round(passed / max(len(report.results), 1), 4)
    report.avg_score = round(sum(r["score"] for r in report.results) / max(len(report.results), 1), 4)
    report.avg_latency_ms = round(sum(r["execution_time_ms"] for r in report.results) / max(len(report.results), 1), 2)
    report.avg_capability_score = round(sum(r["capability_score"] for r in report.results) / max(len(report.results), 1), 4)

    for vendor, entries in vendor_map.items():
        v_passed = sum(1 for e in entries if e["passed"])
        report.vendor_breakdown[vendor] = {
            "total": len(entries),
            "passed": v_passed,
            "failed": len(entries) - v_passed,
            "pass_rate": round(v_passed / max(len(entries), 1), 4),
            "avg_score": round(sum(e["score"] for e in entries) / max(len(entries), 1), 4),
        }

    _write_report(report)
    return report


def _write_report(report: NetworkBenchmarkReport) -> None:
    json_path = REPORT_DIR / "network_benchmark.json"
    csv_path = REPORT_DIR / "network_benchmark.csv"

    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    logger.info("JSON report written: %s", json_path)

    if report.results:
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(report.results[0].keys()))
            writer.writeheader()
            writer.writerows(report.results)
        logger.info("CSV report written: %s", csv_path)


def print_summary(report: NetworkBenchmarkReport) -> None:
    print("\n" + "=" * 60)
    print("  Network Engineer Benchmark Report")
    print("=" * 60)
    print(f"  Generated : {report.generated_at.isoformat()}")
    print(f"  Total     : {report.total_cases}")
    print(f"  Passed    : {report.passed_cases}")
    print(f"  Failed    : {report.failed_cases}")
    print(f"  Pass Rate : {report.pass_rate:.0%}")
    print(f"  Avg Score : {report.avg_score:.0%}")
    print(f"  Avg Latency: {report.avg_latency_ms:.0f}ms")
    print(f"  Avg Capability: {report.avg_capability_score:.0%}")
    print("\n  Vendor Breakdown:")
    for vendor, stats in report.vendor_breakdown.items():
        print(f"    {vendor}: {stats['total']} cases, {stats['pass_rate']:.0%} pass rate")
    print("=" * 60 + "\n")

    if report.pass_rate >= 0.95 and report.avg_latency_ms < 2000:
        print("  ✅ Network Engineer benchmark PASSED")
    else:
        print("  ❌ Network Engineer benchmark FAILED — review results above")


def main() -> int:
    report = run_network_benchmark()
    print_summary(report)
    return 0 if report.pass_rate >= 0.95 and report.avg_latency_ms < 2000 else 1


if __name__ == "__main__":
    raise SystemExit(main())
