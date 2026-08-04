"""
Compliance Models
==================

Data models for the compliance profiles module.
"""

from dataclasses import dataclass, field
from typing import Any

from apps.network_engineer.nic.knowledge.ontology import UniversalConcept
from apps.network_engineer.vendor.models import NetworkAST


@dataclass
class ComplianceRule:
    id: str
    name: str
    description: str
    severity: str = "warning"
    vendor: str = "all"
    concept: UniversalConcept | None = None
    references: list[str] = field(default_factory=list)


@dataclass
class ComplianceCheck:
    rule_id: str
    rule_name: str
    status: str
    detail: str = ""
    evidence: str = ""
    concept: str | None = None
    references: list[str] = field(default_factory=list)


@dataclass
class ComplianceReport:
    device_id: str
    vendor: str
    profile: str
    checks: list[ComplianceCheck] = field(default_factory=list)
    score: float = 0.0
    passed: int = 0
    failed: int = 0
    warnings: int = 0
    skipped: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "device_id": self.device_id,
            "vendor": self.vendor,
            "profile": self.profile,
            "score": round(self.score, 2),
            "passed": self.passed,
            "failed": self.failed,
            "warnings": self.warnings,
            "skipped": self.skipped,
            "checks": [
                {
                    "rule_id": c.rule_id,
                    "rule_name": c.rule_name,
                    "status": c.status,
                    "detail": c.detail,
                    "evidence": c.evidence,
                    "concept": c.concept,
                    "references": c.references,
                }
                for c in self.checks
            ],
        }


class ComplianceProfile:
    """Base class for compliance profiles."""
    name: str = "base"
    description: str = "Base compliance profile"

    def get_rules(self) -> list[ComplianceRule]:
        raise NotImplementedError
