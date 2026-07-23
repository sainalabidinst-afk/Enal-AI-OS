from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from real_cases.collector import save_case
from real_cases.schema import RealCase

logger = logging.getLogger(__name__)


@dataclass
class BenchmarkResult:
    case_id: str
    passed: bool = False
    score: float = 0.0
    findings_matched: int = 0
    expected_findings: int = 0
    risk_score_actual: float | None = None
    risk_score_expected: float | None = None
    compliance_score_actual: float | None = None
    compliance_score_expected: float | None = None
    execution_time_ms: int = 0
    errors: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    capability_score: float = 0.0
    capability_breakdown: dict[str, float] = field(default_factory=dict)


class BenchmarkHarness:
    def __init__(self) -> None:
        self.results: list[BenchmarkResult] = []

    def run(self, case: RealCase) -> BenchmarkResult:
        started = datetime.utcnow()
        result = BenchmarkResult(case_id=case.id)
        try:
            from backend.app.core.attachments.analyzer import analyze_attachment
            from backend.app.core.attachments.detector import detect_from_content

            for source in case.source_files:
                try:
                    text = Path(source).read_text(encoding="utf-8", errors="ignore")
                except Exception as exc:
                    result.errors.append(f"Failed to read {source}: {exc}")
                    continue
                meta = detect_from_content(Path(source).name, text)
                analysis = analyze_attachment(meta, text)
                result.risk_score_actual = analysis.risk_score
                result.compliance_score_actual = getattr(analysis, "compliance_score", None)
                ast_dict = analysis.ast.to_dict() if hasattr(analysis.ast, "to_dict") else analysis.ast
                actual_findings = [finding.get("title", "") for finding in ast_dict.get("findings", [])]
                matched = sum(
                    1
                    for expected in case.expected_findings
                    if any(expected.lower() in actual.lower() for actual in actual_findings)
                )
                result.findings_matched = matched
                result.expected_findings = len(case.expected_findings)
                result.score = matched / max(len(case.expected_findings), 1)
                result.passed = result.score >= 0.8

                breakdown = self._compute_capability_breakdown(analysis, ast_dict, actual_findings)
                result.capability_breakdown = breakdown
                result.capability_score = round(
                    sum(breakdown.values()) / max(len(breakdown), 1),
                    2,
                )

                case.metrics = {
                    "findings_matched": matched,
                    "expected_findings": len(case.expected_findings),
                    "score": result.score,
                    "risk_score_actual": analysis.risk_score,
                    "risk_score_expected": case.expected_risk_score,
                    "compliance_score_actual": result.compliance_score_actual,
                    "compliance_score_expected": case.expected_compliance_score,
                    "capability_score": result.capability_score,
                    "capability_breakdown": breakdown,
                }
                case.benchmark_passed = result.passed
                case.updated_at = datetime.utcnow()
                save_case(case)
                break
        except Exception as exc:
            result.errors.append(str(exc))
            result.passed = False
        finally:
            result.execution_time_ms = int((datetime.utcnow() - started).total_seconds() * 1000)
        self.results.append(result)
        logger.info("Benchmark executed for %s: passed=%s score=%s capability=%s", case.id, result.passed, result.score, result.capability_score)
        return result

    def _compute_capability_breakdown(self, analysis: Any, ast_dict: dict[str, Any], actual_findings: list[str]) -> dict[str, float]:
        findings_list = ast_dict.get("findings", [])
        breakdown: dict[str, float] = {
            "parser": 0.0,
            "reasoning": 0.0,
            "evidence": 0.0,
            "compliance": 0.0,
            "executive_report": 0.0,
        }

        breakdown["parser"] = self._score_parser(ast_dict)
        breakdown["reasoning"] = self._score_reasoning(findings_list)
        breakdown["evidence"] = self._score_evidence(findings_list)
        breakdown["compliance"] = self._score_compliance(ast_dict)
        breakdown["executive_report"] = self._score_executive_report(analysis)

        return {k: round(v, 2) for k, v in breakdown.items()}

    def _score_parser(self, ast_dict: dict[str, Any]) -> float:
        if not ast_dict:
            return 0.0
        has_vendor = 100.0 if ast_dict.get("vendor") else 0.0
        has_findings = 100.0 if ast_dict.get("findings") else 0.0
        has_structure = 100.0 if ast_dict.get("interfaces") or ast_dict.get("firewall") or ast_dict.get("routing") else 0.0
        return round((has_vendor + has_findings + has_structure) / 3, 2)

    def _score_reasoning(self, findings_list: list[dict[str, Any]]) -> float:
        if not findings_list:
            return 0.0
        with_recommendations = sum(1 for f in findings_list if f.get("recommendation"))
        with_confidence = sum(1 for f in findings_list if f.get("confidence") is not None)
        with_evidence_refs = sum(1 for f in findings_list if f.get("evidence"))
        scores = [
            min(100.0, (with_recommendations / max(len(findings_list), 1)) * 100),
            min(100.0, (with_confidence / max(len(findings_list), 1)) * 100),
            min(100.0, (with_evidence_refs / max(len(findings_list), 1)) * 100),
        ]
        return round(sum(scores) / len(scores), 2)

    def _score_evidence(self, findings_list: list[dict[str, Any]]) -> float:
        if not findings_list:
            return 0.0
        with_evidence = sum(1 for f in findings_list if f.get("evidence"))
        return round((with_evidence / len(findings_list)) * 100, 2)

    def _score_compliance(self, ast_dict: dict[str, Any]) -> float:
        compliance = ast_dict.get("compliance_score")
        if compliance is None:
            return 0.0
        return round(float(compliance) * 100, 2)

    def _score_executive_report(self, analysis: Any) -> float:
        if hasattr(analysis, "summary") and analysis.summary:
            return 100.0
        if hasattr(analysis, "reasoning_result") and analysis.reasoning_result:
            return 100.0
        return 0.0

    def summary(self) -> dict[str, Any]:
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        avg_score = round(sum(r.score for r in self.results) / max(total, 1), 2)
        avg_ms = round(sum(r.execution_time_ms for r in self.results) / max(total, 1), 2)
        avg_capability = round(sum(r.capability_score for r in self.results) / max(total, 1), 2)
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": round(passed / max(total, 1), 2),
            "average_score": avg_score,
            "average_execution_time_ms": avg_ms,
            "average_capability_score": avg_capability,
        }


def _derive_expected_findings(expected_inner: dict[str, Any], tags: list[str]) -> list[str]:
    findings: list[str] = []
    tag_to_finding = {
        "security": ["security issue detected", "insecure configuration"],
        "telnet": ["telnet enabled", "insecure management"],
        "ssh": ["ssh", "secure shell"],
        "vpn": ["vpn", "remote access"],
        "firewall": ["firewall", "access control"],
        "acl": ["access list", "acl"],
        "nat": ["nat", "masquerade", "port forwarding"],
        "routing": ["routing", "ospf", "bgp", "static route"],
        "vlan": ["vlan", "switch", "trunk"],
        "bridge": ["bridge", "stp"],
        "wireless": ["wireless", "wlan", "ssid"],
        "hotspot": ["hotspot", "captive portal"],
        "dhcp": ["dhcp", "dns server"],
        "qos": ["queue", "traffic shaping", "priority"],
        "ha": ["vrrp", "hsrp", "high availability", "failover"],
        "high_availability": ["vrrp", "hsrp", "high availability", "failover", "watchdog"],
        "bgp": ["bgp", "routing", "peer"],
        "ospf": ["ospf", "routing", "area"],
        "watchdog": ["watchdog", "health monitoring"],
        "health": ["health", "watchdog"],
    }
    for tag in tags:
        if tag.lower() in tag_to_finding:
            findings.extend(tag_to_finding[tag.lower()])
    critical = expected_inner.get("critical", 0)
    high = expected_inner.get("high", 0)
    medium = expected_inner.get("medium", 0)
    low = expected_inner.get("low", 0)
    total_expected = critical + high + medium + low
    if total_expected > 0 and not findings:
        findings = [f"finding_{i}" for i in range(total_expected)]
    return findings


def load_cases_from_disk(base_dir: str = "real_cases") -> list[RealCase]:
    cases: list[RealCase] = []
    if not Path(base_dir).exists():
        return cases
    for vendor_dir in sorted(Path(base_dir).iterdir()):
        if not vendor_dir.is_dir():
            continue
        for case_dir in sorted(vendor_dir.iterdir()):
            if not case_dir.is_dir():
                continue
            config_file = None
            for f in ("config.rsc", "config.txt", "sample_hotspot.txt"):
                if (case_dir / f).exists():
                    config_file = f
                    break
            if not config_file:
                continue
            expected_path = case_dir / "expected.json"
            expected: dict[str, Any] = {}
            if expected_path.exists():
                try:
                    expected = json.loads(expected_path.read_text(encoding="utf-8"))
                except Exception:
                    pass
            expected_inner = expected.get("expected", expected)
            expected_findings = _derive_expected_findings(expected_inner, expected.get("metadata", {}).get("tags", []))
            case = RealCase(
                id=f"{vendor_dir.name}:{case_dir.name}",
                title=expected.get("title", case_dir.name),
                category=vendor_dir.name,
                vendor=vendor_dir.name,
                source_files=[str(case_dir / config_file)],
                context=expected.get("metadata", {}).get("description", ""),
                expected_findings=expected_findings,
                expected_risk_score=expected_inner.get("risk_max"),
                expected_compliance_score=expected_inner.get("compliance_score_min"),
                tags=expected.get("metadata", {}).get("tags", [vendor_dir.name]),
            )
            cases.append(case)
    return cases


def run_benchmark_for_category(category: str) -> dict[str, Any]:
    all_cases = load_cases_from_disk()
    category_cases = [case for case in all_cases if case.category == category]
    if not category_cases:
        return {"category": category, "total": 0, "passed": 0, "failed": 0, "pass_rate": 0.0}
    harness = BenchmarkHarness()
    results = [harness.run(case) for case in category_cases]
    passed = sum(1 for r in results if r.passed)
    return {
        "category": category,
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "pass_rate": round(passed / max(len(results), 1), 2),
        "summary": harness.summary(),
    }
