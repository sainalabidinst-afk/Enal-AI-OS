from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CapabilityScore:
    vendor: str
    parser: float = 0.0
    reasoning: float = 0.0
    evidence: float = 0.0
    compliance: float = 0.0
    executive_report: float = 0.0
    total: float = 0.0

    def compute_total(self) -> float:
        self.total = round(
            (
                self.parser
                + self.reasoning
                + self.evidence
                + self.compliance
                + self.executive_report
            )
            / 5,
            2,
        )
        return self.total


@dataclass
class ExpectedResult:
    vendor: str = ""
    device_type: str = ""
    findings_min: int = 0
    risk_max: float = 1.0
    confidence_min: float = 0.0
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0
    compliance_score_min: float | None = None
    expected_keywords: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ExpectedResult:
        expected = data.get("expected", data)
        return cls(
            vendor=data.get("vendor", ""),
            device_type=data.get("device_type", ""),
            findings_min=int(expected.get("findings_min", data.get("findings_min", 0))),
            risk_max=float(expected.get("risk_max", data.get("risk_max", 1.0))),
            confidence_min=float(expected.get("confidence_min", data.get("confidence_min", 0.0))),
            critical=int(expected.get("critical", 0)),
            high=int(expected.get("high", 0)),
            medium=int(expected.get("medium", 0)),
            low=int(expected.get("low", 0)),
            compliance_score_min=float(expected["compliance_score_min"])
            if expected.get("compliance_score_min") is not None
            else None,
            expected_keywords=list(expected.get("expected_keywords", []) or []),
            metadata=dict(data.get("metadata", {}) or {}),
        )


@dataclass
class BenchmarkCase:
    case_id: str
    vendor: str
    device_type: str
    category: str
    filename: str
    expected_findings_min: int = 0
    expected_risk_max: float = 1.0
    expected_confidence_min: float = 0.0
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    expected: ExpectedResult | None = None


@dataclass
class BenchmarkResult:
    case_id: str
    passed: bool
    score: float
    findings: int
    risk_score: float
    confidence: float
    analysis_time_ms: float
    details: dict[str, Any] = field(default_factory=dict)
    expected: ExpectedResult | None = None
    capability_score: float = 0.0
    capability_breakdown: CapabilityScore | None = None
    regression: bool = False


@dataclass
class BenchmarkSuite:
    suite_id: str
    name: str
    cases: list[BenchmarkCase] = field(default_factory=list)
    results: list[BenchmarkResult] = field(default_factory=list)
