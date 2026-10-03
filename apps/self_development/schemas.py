"""
Self Development Schemas
=========================

Typed contracts for the Self Development capability pack.
"""

from __future__ import annotations  # noqa: I001

from dataclasses import dataclass, field
from enum import StrEnum, Enum  # noqa: F401
from typing import Any


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ProblemType(StrEnum):
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
    CAPABILITY_GAP = "capability_gap"
    PACK_OVERLAP = "pack_overlap"
    GOVERNANCE_VIOLATION = "governance_violation"
    DOCUMENTATION_GAP = "documentation_gap"


class ImprovementType(StrEnum):
    REFACTOR = "refactor"
    RESTRUCTURE = "restructure"
    OPTIMIZE = "optimize"
    SECURITY_HARDENING = "security_hardening"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    NEW_CAPABILITY = "new_capability"
    PACK_MERGE = "pack_merge"
    PACK_SPLIT = "pack_split"
    GOVERNANCE = "governance"


class CapabilityTier(StrEnum):
    TIER_A = "tier_a"
    TIER_B = "tier_b"
    TIER_C = "tier_c"
    PLATFORM = "platform"


class ProposalStatus(StrEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    IMPLEMENTED = "implemented"


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
    overall: float = 0.0

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


@dataclass
class ECPPlatformAnalysis:
    core_modules: int
    capability_packs: int
    total_files: int
    complexity: str
    hotspots: list[str] = field(default_factory=list)
    governance_issues: list[dict[str, Any]] = field(default_factory=list)
    pack_gaps: list[dict[str, Any]] = field(default_factory=list)
    cross_pack_patterns: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CapabilityProposal:
    id: str
    name: str
    domain: str
    description: str
    tier: str
    reuse_potential: int
    estimated_effort: str
    risk: str
    confidence: float
    rationale: str
    required_packs: list[str] = field(default_factory=list)
    status: str = ProposalStatus.DRAFT.value
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ImprovementProposal:
    id: str
    target_type: str
    target_id: str
    improvement_type: str
    description: str
    estimated_effort: str
    risk: str
    confidence: float
    expected_impact: str
    status: str = ProposalStatus.DRAFT.value
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CrossPackPattern:
    id: str
    pattern_type: str
    description: str
    source_packs: list[str]
    target_packs: list[str]
    reusability_score: float
    implementation_complexity: str
    metadata: dict[str, Any] = field(default_factory=dict)
