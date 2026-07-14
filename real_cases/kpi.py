from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class KpiSnapshot:
    timestamp: datetime = field(default_factory=datetime.utcnow)
    total_cases: int = 0
    passed_cases: int = 0
    failed_cases: int = 0
    average_analysis_time_ms: float = 0.0
    evidence_coverage: float = 0.0
    explainability_coverage: float = 0.0
    compliance_coverage: float = 0.0
    cross_file_correlation_accuracy: float = 0.0
    recommendation_acceptance_rate: float = 0.0
    false_positive_rate: float = 0.0
    real_case_pass_rate: float = 0.0
    most_common_findings: list[str] = field(default_factory=list)
    top_vendors: list[str] = field(default_factory=list)


class KpiEngine:
    def __init__(self) -> None:
        self.snapshots: list[KpiSnapshot] = []

    def snapshot(self, cases: list[dict[str, Any]]) -> KpiSnapshot:
        total = len(cases)
        passed = sum(1 for case in cases if case.get("benchmark_passed") is True)
        failed = total - passed
        snap = KpiSnapshot(
            total_cases=total,
            passed_cases=passed,
            failed_cases=failed,
            evidence_coverage=self._compute_evidence_coverage(cases),
            explainability_coverage=self._compute_explainability_coverage(cases),
            compliance_coverage=self._compute_compliance_coverage(cases),
            real_case_pass_rate=round(passed / max(total, 1), 2),
            false_positive_rate=self._estimate_false_positive_rate(cases),
        )
        self.snapshots.append(snap)
        logger.info("KPI snapshot generated: total=%s pass_rate=%s", total, snap.real_case_pass_rate)
        return snap

    def _compute_evidence_coverage(self, cases: list[dict[str, Any]]) -> float:
        if not cases:
            return 0.0
        evidence_count = 0
        total_findings = 0
        for case in cases:
            result = case.get("result") or {}
            findings = (result.get("ast") or {}).get("findings", [])
            total_findings += len(findings)
            evidence_count += sum(1 for finding in findings if finding.get("evidence"))
        return round(evidence_count / max(total_findings, 1), 2)

    def _compute_explainability_coverage(self, cases: list[dict[str, Any]]) -> float:
        if not cases:
            return 0.0
        covered = sum(1 for case in cases if case.get("result") and case["result"].get("explainability"))
        return round(covered / len(cases), 2)

    def _compute_compliance_coverage(self, cases: list[dict[str, Any]]) -> float:
        if not cases:
            return 0.0
        scored = sum(1 for case in cases if case.get("result") and case["result"].get("compliance_score") is not None)
        return round(scored / len(cases), 2)

    def _estimate_false_positive_rate(self, cases: list[dict[str, Any]]) -> float:
        if not cases:
            return 0.0
        fp = sum(1 for case in cases if case.get("benchmark_passed") is False)
        return round(fp / len(cases), 2)

    def latest(self) -> KpiSnapshot | None:
        return self.snapshots[-1] if self.snapshots else None


kpi_engine = KpiEngine()
