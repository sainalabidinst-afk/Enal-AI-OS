"""
Self Development Schemas
=========================

Typed contracts for the Self Development capability pack.
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
    BOTTLENECK = "bottleneck"
    DEAD_CODE = "dead_code"
    DUPLICATION = "duplication"
    ARCHITECTURE_SMELL = "architecture_smell"
    SECURITY_HOLE = "security_hole"
    PERFORMANCE_ISSUE = "performance_issue"
    TEST_COVERAGE_GAP = "test_coverage_gap"
    DEPENDENCY_CYCLE = "dependency_cycle"
    LAYER_VIOLATION = "layer_violation"
    API_CONTRACT_BREAKING = "api_contract_breaking"


class ImprovementType(str, Enum):
    REFACTOR = "refactor"
    RESTRUCTURE = "restructure"
    OPTIMIZE = "optimize"
    SECURITY_HARDENING = "security_hardening"
    TESTING = "testing"
    DOCUMENTATION = "documentation"


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
