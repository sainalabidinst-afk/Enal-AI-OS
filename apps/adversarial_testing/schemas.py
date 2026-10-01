"""
Adversarial Testing — Public Contracts (Pydantic schemas).

Defines the input (AdversarialTestRequest) and output (AdversarialTestResult)
contracts for the Adversarial Testing Capability Pack ("Devil's Advocate").
"""

from __future__ import annotations  # noqa: I001

import uuid
from dataclasses import dataclass, field
from enum import StrEnum, Enum  # noqa: F401
from typing import Any

from pydantic import BaseModel, Field


class SubjectType(StrEnum):
    """Type of subject being tested."""

    PLAN = "plan"
    RECOMMENDATION = "recommendation"
    ARCHITECTURE = "architecture"
    CODE_PATCH = "code_patch"
    STRATEGY = "strategy"
    DECISION = "decision"


class AttackCategory(StrEnum):
    """Categories of adversarial attacks."""

    EXTERNAL_SHOCK = "external_shock"
    DEPENDENCY_FAILURE = "dependency_failure"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    COMPETITIVE_RESPONSE = "competitive_response"
    REGULATORY_CHANGE = "regulatory_change"
    DATA_CORRUPTION = "data_corruption"
    INFORMATION_WARFARE = "information_warfare"
    OPERATIONAL_DISRUPTION = "operational_disruption"


class Severity(StrEnum):
    """Severity of a vulnerability or attack."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Priority(StrEnum):
    """Priority of a hardening recommendation."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class GateResult(StrEnum):
    """Result of the adversarial pass/fail gate."""

    PASS = "pass"
    FAIL = "fail"
    REVIEW_REQUIRED = "review_required"


# ---------------------------------------------------------------------------
# Input models
# ---------------------------------------------------------------------------


class AttackRequest(BaseModel):
    """A single attack to generate/test."""

    category: AttackCategory = Field(..., description="Category of attack")
    description: str | None = None
    severity: Severity = Field(default=Severity.MEDIUM, description="Expected severity of this attack")  # noqa: E501
    assumptions: list[str] = Field(default_factory=list, description="Worst-case assumptions")


class AdversarialTestRequest(BaseModel):
    """Input contract for an adversarial testing request."""

    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique request identifier")  # noqa: E501
    subject: str = Field(..., description="The plan/strategy/recommendation to attack")
    subject_type: SubjectType = Field(..., description="Type of subject")
    context: str | None = Field(default=None, description="Additional context")
    evidence: dict[str, Any] = Field(default_factory=dict, description="Supporting evidence")
    constraints: list[str] = Field(default_factory=list, description="What should NOT be violated")
    attack_budget: int = Field(default=10, ge=1, le=50, description="Number of attacks to generate")
    attack_categories: list[AttackCategory] = Field(
        default_factory=lambda: list(AttackCategory),
        description="Categories of attacks to generate",
    )
    existing_hardening: list[str] = Field(default_factory=list, description="Already-applied mitigations")  # noqa: E501


# ---------------------------------------------------------------------------
# Output models
# ---------------------------------------------------------------------------


@dataclass
class AttackVector:
    """A generated adversarial attack scenario."""

    id: str
    category: AttackCategory
    description: str
    severity: Severity
    assumptions: list[str]
    worst_case_impact: str


@dataclass
class Vulnerability:
    """A vulnerability found by attacking the subject."""

    id: str
    attack_id: str
    vulnerability: str
    impact: str
    severity: Severity
    exploit_path: str
    exploitable: bool
    confidence: float


@dataclass
class HardeningAction:
    """A recommendation to harden against a vulnerability."""

    id: str
    attack_id: str
    recommendation: str
    priority: Priority
    estimated_effort: str
    applies_to_constraint: str | None = None


@dataclass
class AdversarialTestResult:
    """Output contract for an adversarial testing result."""

    request_id: str
    subject: str
    subject_type: SubjectType
    attack_vectors: list[dict[str, Any]]
    vulnerabilities_found: list[dict[str, Any]]
    hardening_recommendations: list[dict[str, Any]]
    gate_result: GateResult
    pass_score: float
    confidence: float
    explanation_chain: dict[str, Any]
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "subject": self.subject,
            "subject_type": self.subject_type.value,
            "attack_vectors": self.attack_vectors,
            "vulnerabilities_found": self.vulnerabilities_found,
            "hardening_recommendations": self.hardening_recommendations,
            "gate_result": self.gate_result.value,
            "pass_score": self.pass_score,
            "confidence": self.confidence,
            "explanation_chain": self.explanation_chain,
            "raw": self.raw,
        }
