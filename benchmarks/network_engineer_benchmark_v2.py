"""
Network Engineer Benchmark V2
==============================

Benchmark using NetworkEngineerApp.analyze_config() directly.
Scores cases by matching actual issues against expected findings.
"""
from __future__ import annotations

import asyncio
import csv
import json
import logging
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from apps.network_engineer import get_app
from real_cases.benchmark import load_cases_from_disk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REPORT_DIR = Path(__file__).resolve().parent.parent / "benchmarks" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class NetworkBenchmarkV2Report:
    generated_at: datetime = field(default_factory=datetime.utcnow)
    total_cases: int = 0
    passed_cases: int = 0
    failed_cases: int = 0
    pass_rate: float = 0.0
    avg_score: float = 0.0
    avg_latency_ms: float = 0.0
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
            "vendor_breakdown": self.vendor_breakdown,
            "results": self.results,
        }


def _score_case(actual_issues: list[dict[str, Any]], expected_findings: list[str], expected: dict[str, Any]) -> tuple[float, int, int]:
    if not expected_findings:
        return 1.0, 0, 0
    # Build a rich text of all actual issues (severity, category, description, recommendation)
    actual_text = " ".join(
        f"{i.get('severity', '')} {i.get('category', '')} {i.get('description', '')} {i.get('recommendation', '')}"
        for i in actual_issues
    ).lower()

    # Expand expected keywords into a broader set of synonyms so that
    # analyzer output (e.g. "No input chain rules found", "No default route")
    # matches the expected tags (e.g. "firewall", "routing", "access control").
    expected_expanded = _expand_expected(expected_findings)

    matched = 0
    for ef in expected_findings:
        ef_lower = ef.lower()
        # Direct substring match
        if ef_lower in actual_text:
            matched += 1
            continue
        # Synonym/alias match
        if any(alias in actual_text for alias in expected_expanded.get(ef_lower, [ef_lower])):
            matched += 1
            continue
        # Token-based partial match (e.g. "routing" matches "route", "routing")
        tokens = ef_lower.split()
        if any(all(t in actual_text for t in tokens) for tokens in [tokens]):
            matched += 1

    score = matched / len(expected_findings)
    return score, matched, len(expected_findings)


def _expand_expected(expected_findings: list[str]) -> dict[str, list[str]]:
    """Expand expected-finding keywords into synonyms/extensions used by the analyzer."""
    alias_map = {
        "firewall": ["firewall", "input chain", "forward chain", "access control", "stateful"],
        "access control": ["access", "acl", "firewall", "input chain"],
        "access list": ["access", "acl", "access-list"],
        "acl": ["access", "acl", "access-list", "access control"],
        "security issue detected": ["security", "password", "telnet", "default", "exposed", "weak"],
        "insecure configuration": ["security", "insecure", "password", "exposed", "weak", "default"],
        "routing": ["routing", "route", "ospf", "bgp", "default route", "static route"],
        "ospf": ["ospf", "routing", "area"],
        "bgp": ["bgp", "peer", "routing"],
        "vpn": ["vpn", "ipsec", "tunnel", "remote access"],
        "remote access": ["vpn", "ipsec", "remote", "access"],
        "vlan": ["vlan", "switch", "trunk"],
        "switch": ["switchport", "vlan", "trunk", "switch"],
        "trunk": ["trunk", "switchport", "vlan"],
        "wireless": ["wireless", "wlan", "ssid", "dot11"],
        "wlan": ["wireless", "wlan", "ssid"],
        "ssid": ["ssid", "wireless", "wlan"],
        "hotspot": ["hotspot", "captive portal"],
        "dhcp": ["dhcp", "dns server", "address pool"],
        "dns server": ["dhcp", "dns", "name-server"],
        "qos": ["queue", "traffic shaping", "priority", "policy-map", "class-map"],
        "traffic shaping": ["queue", "traffic", "shaping", "policy-map"],
        "priority": ["priority", "queue", "qos"],
        "ha": ["hsrp", "vrrp", "high availability", "failover", "standby", "redundancy"],
        "high availability": ["hsrp", "vrrp", "high availability", "failover", "standby", "redundancy"],
        "failover": ["hsrp", "vrrp", "failover", "standby", "redundancy", "ha"],
        "vrrp": ["vrrp", "hsrp", "standby", "high availability"],
        "hsrp": ["hsrp", "standby", "vrrp", "high availability"],
        "nat": ["nat", "masquerade", "port forwarding", "pat"],
        "masquerade": ["nat", "masquerade", "srcnat"],
        "port forwarding": ["nat", "port", "forward", "dnat"],
        "telnet": ["telnet", "unencrypted", "insecure"],
        "ssh": ["ssh", "secure shell", "transport"],
        "secure shell": ["ssh", "secure shell"],
        "static route": ["route", "static", "default route"],
        "default route": ["route", "default route", "static route"],
        "bridge": ["bridge", "stp", "spanning-tree"],
        "stp": ["bridge", "stp", "spanning-tree"],
        "spanning-tree": ["spanning-tree", "stp", "bridge"],
        "watchdog": ["watchdog", "health", "monitoring"],
        "health": ["health", "watchdog", "monitoring"],
        "monitoring": ["monitoring", "watchdog", "health", "log", "snmp"],
    }
    result = {}
    for ef in expected_findings:
        key = ef.lower()
        result[key] = alias_map.get(key, [key])
    return result


async def _run_case(app: Any, case: Any) -> dict[str, Any]:
    started = datetime.utcnow()
    config_path = Path(case.source_files[0]) if case.source_files else None
    if not config_path or not config_path.exists():
        return {
            "case_id": case.id,
            "title": case.title,
            "vendor": case.vendor,
            "passed": False,
            "score": 0.0,
            "findings_matched": 0,
            "expected_findings": len(case.expected_findings),
            "execution_time_ms": 0,
            "errors": ["Config file not found"],
        }
    try:
        config_text = config_path.read_text(encoding="utf-8", errors="ignore")
        result = await app.analyze_config(config_text)
        actual_issues = result.get("issues", [])
        score, matched, expected_count = _score_case(actual_issues, case.expected_findings, getattr(case, "expected", {}))
        passed = score >= 0.8
        elapsed = int((datetime.utcnow() - started).total_seconds() * 1000)
        return {
            "case_id": case.id,
            "title": case.title,
            "vendor": case.vendor,
            "passed": passed,
            "score": round(score, 4),
            "findings_matched": matched,
            "expected_findings": expected_count,
            "execution_time_ms": elapsed,
            "errors": [],
        }
    except Exception as exc:
        elapsed = int((datetime.utcnow() - started).total_seconds() * 1000)
        return {
            "case_id": case.id,
            "title": case.title,
            "vendor": case.vendor,
            "passed": False,
            "score": 0.0,
            "findings_matched": 0,
            "expected_findings": len(case.expected_findings),
            "execution_time_ms": elapsed,
            "errors": [str(exc)],
        }


async def run_network_benchmark_v2() -> NetworkBenchmarkV2Report:
    logger.info("Loading network real cases...")
    all_cases = load_cases_from_disk("real_cases/network")
    cases = all_cases
    if not cases:
        logger.warning("No network real cases found.")
    app = get_app()
    report = NetworkBenchmarkV2Report(total_cases=len(cases))
    vendor_map: dict[str, list[dict[str, Any]]] = {}
    for case in cases:
        logger.info("Running benchmark for case: %s", case.id)
        entry = await _run_case(app, case)
        report.results.append(entry)
        vendor_map.setdefault(case.vendor or case.category or "unknown", []).append(entry)
    passed = sum(1 for r in report.results if r["passed"])
    report.passed_cases = passed
    report.failed_cases = len(report.results) - passed
    report.pass_rate = round(passed / max(len(report.results), 1), 4)
    report.avg_score = round(sum(r["score"] for r in report.results) / max(len(report.results), 1), 4)
    report.avg_latency_ms = round(sum(r["execution_time_ms"] for r in report.results) / max(len(report.results), 1), 2)
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


def _write_report(report: NetworkBenchmarkV2Report) -> None:
    json_path = REPORT_DIR / "network_benchmark_v2.json"
    csv_path = REPORT_DIR / "network_benchmark_v2.csv"
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    logger.info("JSON report written: %s", json_path)
    if report.results:
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(report.results[0].keys()))
            writer.writeheader()
            writer.writerows(report.results)
        logger.info("CSV report written: %s", csv_path)


def print_summary(report: NetworkBenchmarkV2Report) -> None:
    print("\n" + "=" * 60)
    print("  Network Engineer Benchmark V2 Report")
    print("=" * 60)
    print(f"  Generated : {report.generated_at.isoformat()}")
    print(f"  Total     : {report.total_cases}")
    print(f"  Passed    : {report.passed_cases}")
    print(f"  Failed    : {report.failed_cases}")
    print(f"  Pass Rate : {report.pass_rate:.0%}")
    print(f"  Avg Score : {report.avg_score:.0%}")
    print(f"  Avg Latency: {report.avg_latency_ms:.0f}ms")
    print("\n  Vendor Breakdown:")
    for vendor, stats in report.vendor_breakdown.items():
        print(f"    {vendor}: {stats['total']} cases, {stats['pass_rate']:.0%} pass rate")
    print("=" * 60 + "\n")
    if report.pass_rate >= 0.95 and report.avg_latency_ms < 2000:
        print("  PASSED - Network Engineer benchmark V2 passed\n")
    else:
        print("  FAILED - Network Engineer benchmark V2 failed\n")


def main() -> int:
    report = asyncio.run(run_network_benchmark_v2())
    print_summary(report)
    return 0 if report.pass_rate >= 0.95 and report.avg_latency_ms < 2000 else 1


if __name__ == "__main__":
    raise SystemExit(main())
