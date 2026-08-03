"""
DevOps Assistant Schemas
========================

Typed contracts for the DevOps Assistant capability pack.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ProblemType(str, Enum):
    PIPELINE_BREAK = "pipeline_break"
    MISSING_HEALTH_CHECK = "missing_health_check"
    HARDCODED_SECRET = "hardcoded_secret"
    MISSING_ROLLBACK = "missing_rollback"
    MISSING_RESOURCE_LIMIT = "missing_resource_limit"
    INSECURE_CONFIG = "insecure_config"
    MISSING_BACKUP = "missing_backup"
    OUTDATED_IMAGE = "outdated_image"
    MISSING_MONITORING = "missing_monitoring"
    POLICY_VIOLATION = "policy_violation"


class ImprovementType(str, Enum):
    PIPELINE_FIX = "pipeline_fix"
    INFRASTRUCTURE = "infrastructure"
    MONITORING = "monitoring"
    DEPLOYMENT = "deployment"
    SECURITY_HARDENING = "security_hardening"
    POLICY_AS_CODE = "policy_as_code"
    CHAOS_ENGINEERING = "chaos_engineering"
    GITOPS = "gitops"


@dataclass
class Problem:
    id: str
    type: str
    severity: str
    location: str
    description: str
    impact: str
    confidence: float = 1.0
    evidence: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.confidence = max(0.0, min(1.0, self.confidence))


@dataclass
class Solution:
    problem_id: str
    solution_type: str
    description: str
    estimated_effort: str
    risk: str
    tests_required: bool = True
    confidence: float = 1.0

    def __post_init__(self) -> None:
        self.confidence = max(0.0, min(1.0, self.confidence))


@dataclass
class Patch:
    problem_id: str
    patch_type: str
    files_affected: list[str]
    diff: str
    tests_added: int = 0
    risk_score: float = 0.0


@dataclass
class RiskScore:
    probability: float
    impact: float
    reversibility: float
    overall: float

    def __post_init__(self) -> None:
        self.probability = max(0.0, min(1.0, self.probability))
        self.impact = max(0.0, min(1.0, self.impact))
        self.reversibility = max(0.0, min(1.0, self.reversibility))
        if self.overall <= 0:
            self.overall = (
                self.probability * 0.4 + self.impact * 0.4 + (1.0 - self.reversibility) * 0.2
            )
        self.overall = max(0.0, min(1.0, self.overall))


@dataclass
class ApprovalState:
    problem_id: str
    status: str
    requires_approval: bool = True
    approvers: list[str] = field(default_factory=lambda: ["user"])
    message: str = ""


@dataclass
class ProjectAnalysis:
    project: str
    modules_count: int
    files_count: int
    complexity: str
    language: str = "python"
    framework: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
