from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class RealCaseEvidence:
    source_file: str
    vendor: str = ""
    device_role: str = ""
    finding: str = ""
    evidence: list[str] = field(default_factory=list)
    line_references: list[str] = field(default_factory=list)


@dataclass
class RealCase:
    id: str
    title: str
    category: str
    subcategory: str = ""
    vendor: str = ""
    os_version: str = ""
    difficulty: str = "medium"
    device_role: str = ""
    source_files: list[str] = field(default_factory=list)
    context: str = ""
    expected_findings: list[str] = field(default_factory=list)
    expected_risk_score: float | None = None
    expected_compliance_score: float | None = None
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    result: dict[str, Any] | None = None
    lesson_learned: str = ""
    capability_gap: str = ""
    future_recommendation: str = ""
    benchmark_passed: bool | None = None
    metrics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "subcategory": self.subcategory,
            "vendor": self.vendor,
            "device_role": self.device_role,
            "source_files": self.source_files,
            "context": self.context,
            "expected_findings": self.expected_findings,
            "expected_risk_score": self.expected_risk_score,
            "expected_compliance_score": self.expected_compliance_score,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "result": self.result,
            "lesson_learned": self.lesson_learned,
            "capability_gap": self.capability_gap,
            "future_recommendation": self.future_recommendation,
            "benchmark_passed": self.benchmark_passed,
            "metrics": self.metrics,
        }
