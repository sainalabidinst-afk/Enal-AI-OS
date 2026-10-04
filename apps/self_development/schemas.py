"""
Self Development Schemas
=========================

Typed contracts for the Self Development capability pack.
"""

from __future__ import annotations  # noqa: I001

from dataclasses import dataclass, field
from datetime import UTC, datetime
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


class ActivityKind(StrEnum):
    PROJECT = "project"
    STUDY = "study"
    HABIT = "habit"
    CERTIFICATION = "certification"
    MILESTONE = "milestone"
    CROSS_PACK = "cross_pack"
    RESEARCH = "research"


class SkillLevel(StrEnum):
    NOVICE = "novice"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class GoalVerdict(StrEnum):
    ALIGNED = "aligned"
    PARTIAL = "partial"
    UNRELATED = "unrelated"


class HabitCadence(StrEnum):
    DAILY = "daily"
    WEEKLY = "weekly"


class AlertSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class RecommendationKind(StrEnum):
    PROJECT = "project"
    SKILL = "skill"
    MILESTONE = "milestone"


class Granularity(StrEnum):
    WEEK = "week"
    MONTH = "month"


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


@dataclass
class GrowthGoal:
    """Long-term development target an activity can be aligned to."""

    id: str
    title: str
    kind: str = "milestone"
    target_skills: list[str] = field(default_factory=list)
    success_criteria: list[str] = field(default_factory=list)
    target_date: str | None = None
    progress: float = 0.0
    source: str = "local"
    core_goal_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.progress = max(0.0, min(100.0, self.progress))


@dataclass
class LearningActivity:
    """A single tracked self-development activity."""

    id: str
    title: str
    kind: str
    duration_minutes: float
    skills: list[str] = field(default_factory=list)
    goal_id: str | None = None
    goal_alignment: float = 0.0
    goal_verdict: str = GoalVerdict.UNRELATED.value
    source_pack: str | None = None
    completed_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    notes: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.duration_minutes = max(0.0, float(self.duration_minutes))
        self.goal_alignment = max(0.0, min(1.0, float(self.goal_alignment)))


@dataclass
class SkillProgress:
    """Aggregated progress for one skill."""

    skill: str
    activities: int = 0
    projects_completed: int = 0
    minutes_spent: float = 0.0
    level: str = SkillLevel.NOVICE.value
    last_practiced: datetime | None = None
    evidence: list[str] = field(default_factory=list)


@dataclass
class ProgressBucket:
    """Aggregated activity for one week or month."""

    period: str
    activities: int = 0
    projects_completed: int = 0
    minutes_spent: float = 0.0
    new_skills: list[str] = field(default_factory=list)


@dataclass
class ProgressSnapshot:
    """Point-in-time learning progress summary."""

    total_activities: int
    total_projects: int
    total_minutes: float
    active_skills: int
    current_streak_weeks: int
    buckets: list[ProgressBucket]
    skills: list[SkillProgress]
    aligned_activities: int
    unaligned_activities: int
    alignment_rate: float
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class Habit:
    """Recurring learning habit with check-in tracking."""

    id: str
    name: str
    cadence: str = HabitCadence.DAILY.value
    target_per_period: int = 1
    check_ins: list[str] = field(default_factory=list)
    goal_id: str | None = None
    reminder_hour: int = 9
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class HabitStatus:
    """Derived state of a habit at query time."""

    habit_id: str
    name: str
    cadence: str
    current_streak: int
    longest_streak: int
    period_check_ins: int
    target_per_period: int
    target_met: bool
    last_check_in: str | None
    next_due: str
    at_risk: bool
    goal_id: str | None = None


@dataclass
class GrowthAlert:
    """Reminder / nudge emitted by the habit and alignment monitors."""

    id: str
    alert_type: str
    severity: str
    subject: str
    message: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class GoalAlignment:
    """Result of validating an activity against development goals."""

    goal_id: str | None
    goal_title: str | None
    score: float
    verdict: str
    matched_terms: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    contributing_minutes: float = 0.0


@dataclass
class GrowthRecommendation:
    """Next project / skill recommended for the learner."""

    id: str
    kind: str
    title: str
    rationale: str
    skills_gained: list[str] = field(default_factory=list)
    difficulty: str = "medium"
    estimated_hours: float = 4.0
    confidence: float = 0.5
    source: str = "skill_ladder"
    source_pack: str | None = None
    goal_id: str | None = None
    project_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.confidence = max(0.0, min(1.0, float(self.confidence)))


@dataclass
class LearningProject:
    """Real project executed through another capability pack but counted as learning."""

    id: str
    title: str
    pack: str
    operation: str
    skills_gained: list[str] = field(default_factory=list)
    difficulty: str = "medium"
    estimated_hours: float = 4.0
    description: str = ""
    goal_hints: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
