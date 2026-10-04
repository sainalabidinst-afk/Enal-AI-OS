"""
Recommendation Engine
=====================

Recommends the next project or skill for the learner by combining:

1. Skill ladder — deterministic progression rules based on how many projects
   have already been completed per skill.
2. Goal gaps — skills required by active goals but not yet practised.
3. Knowledge signals — success/failure patterns and recommendations from the
   core Knowledge ``LearningEngine`` when a bridge is available.
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from typing import Any

from apps.self_development.goal_aligner import GoalAligner, goal_aligner
from apps.self_development.growth_repository import GrowthRepository, growth_repository
from apps.self_development.schemas import (
    GrowthRecommendation,
    RecommendationKind,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LadderStep:
    """Progression rule: after N projects on a skill, move to the next one."""

    skill: str
    min_projects: int
    title: str
    description: str
    skills_gained: tuple[str, ...]
    difficulty: str
    estimated_hours: float
    next_skill: str | None = None
    source_pack: str | None = None
    project_id: str | None = None


SKILL_LADDER: tuple[LadderStep, ...] = (
    LadderStep(
        skill="python",
        min_projects=3,
        title="Data Engineering mini-project: batch ETL pipeline",
        description=(
            "Bangun pipeline ETL end-to-end (extract, transform, load) dengan checkpoint, "
            "retry, dan data quality check sebagai peralihan dari Python murni ke jalur "
            "data engineering."
        ),
        skills_gained=("data-engineering", "etl", "data-quality"),
        difficulty="medium",
        estimated_hours=8.0,
        next_skill="data-engineering",
        source_pack="data-engineer",
        project_id="data-pipeline-etl",
    ),
    LadderStep(
        skill="sql",
        min_projects=2,
        title="Query optimisation study: window functions on 1M rows",
        description=(
            "Bandingkan window function, CTE, dan index strategy pada dataset besar "
            "lalu dokumentasikan hasil EXPLAIN sebagai portofolio."
        ),
        skills_gained=("sql", "performance-tuning", "data-analysis"),
        difficulty="medium",
        estimated_hours=5.0,
        next_skill="data-analysis",
        source_pack="data_engineer",
        project_id=None,
    ),
    LadderStep(
        skill="fastapi",
        min_projects=2,
        title="Service contract hardening: OpenAPI + contract tests",
        description=(
            "Kunci kontrak API dengan schema validation, contract test, dan versioned "
            "migration plan sebelum service masuk produksi."
        ),
        skills_gained=("api-design", "contract-testing", "distributed-systems"),
        difficulty="medium",
        estimated_hours=6.0,
        next_skill="distributed-systems",
        source_pack="code_engineer",
        project_id="architecture-review",
    ),
    LadderStep(
        skill="docker",
        min_projects=2,
        title="Containerise the platform stack and measure cold start",
        description=(
            "Dockerfile multi-stage untuk service utama, lalu ukur cold start dan image size "
            "sebagai baseline sebelum masuk orkestrasi."
        ),
        skills_gained=("docker", "container-observability"),
        difficulty="easy",
        estimated_hours=4.0,
        next_skill="kubernetes",
        source_pack="devops_assistant",
        project_id=None,
    ),
    LadderStep(
        skill="statistics",
        min_projects=3,
        title="Mini backtest engine with walk-forward validation",
        description=(
            "Implementasi backtest engine sendiri (entry/exit, position sizing, max drawdown, "
            "Sharpe) lalu validasi dengan walk-forward validation."
        ),
        skills_gained=("quantitative-finance", "backtesting", "risk-management"),
        difficulty="hard",
        estimated_hours=10.0,
        next_skill="quantitative-finance",
        source_pack="trading-analyst",
        project_id="trading-backtest",
    ),
    LadderStep(
        skill="machine-learning",
        min_projects=2,
        title="MLOps loop: training, evaluation, dan drift monitoring",
        description=(
            "Bangun loop ML lengkap: dataset version, training run, evaluation metrics, "
            "serta drift monitoring sebelum deployment."
        ),
        skills_gained=("mlops", "model-evaluation", "observability"),
        difficulty="hard",
        estimated_hours=12.0,
        next_skill="mlops",
        source_pack="data_scientist",
        project_id=None,
    ),
    LadderStep(
        skill="clean-architecture",
        min_projects=2,
        title="Architecture review dan refactor bounded context",
        description=(
            "Jalankan architecture review pada satu capability pack, lalu pecah atau rapikan "
            "bounded context berdasarkan temuan."
        ),
        skills_gained=("ddd", "architecture-review", "refactoring"),
        difficulty="medium",
        estimated_hours=8.0,
        next_skill="ddd",
        source_pack="system-architect",
        project_id="architecture-review",
    ),
    LadderStep(
        skill="javascript",
        min_projects=3,
        title="Full-stack vertical slice dengan contract test",
        description=(
            "Bangun satu fitur end-to-end (frontend + API + contract test) untuk menutup "
            "gap full-stack dan menambah pengalaman pengujian kontrak."
        ),
        skills_gained=("full-stack", "testing"),
        difficulty="medium",
        estimated_hours=8.0,
        next_skill="full-stack",
        source_pack="full_stack_engineer",
        project_id=None,
    ),
)


class RecommendationEngine:
    """Generates ranked next-step recommendations for the learner."""

    def __init__(
        self,
        repository: GrowthRepository | None = None,
        aligner: GoalAligner | None = None,
        learning_engine: Any = None,
    ) -> None:
        self._repo = repository or growth_repository
        self._aligner = aligner or goal_aligner
        self._learning_engine = learning_engine

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def recommend(self, limit: int = 5, goal_id: str | None = None) -> list[GrowthRecommendation]:
        """Return ranked recommendations combining ladder, goal gaps, and knowledge."""
        candidates = self._ladder_candidates(goal_id)
        candidates.extend(self._goal_gap_candidates(goal_id))
        candidates.extend(self._knowledge_candidates(goal_id))
        deduped: dict[str, GrowthRecommendation] = {}
        for candidate in candidates:
            key = candidate.title.strip().lower()
            existing = deduped.get(key)
            if existing is None:
                deduped[key] = candidate
            else:
                existing.confidence = min(1.0, existing.confidence + 0.1)
                existing.rationale = f"{existing.rationale} | {candidate.rationale}"
                for skill in candidate.skills_gained:
                    if skill not in existing.skills_gained:
                        existing.skills_gained.append(skill)
                existing.project_id = existing.project_id or candidate.project_id
                existing.source_pack = existing.source_pack or candidate.source_pack
        ranked = sorted(
            deduped.values(),
            key=lambda r: (r.confidence, r.estimated_hours),
            reverse=True,
        )
        return ranked[:limit] if limit > 0 else ranked

    def explain(self) -> dict[str, Any]:
        """Return the ladder state driving the recommendations."""
        activities = self._repo.list_activities()
        counts: dict[str, int] = {}
        for activity in activities:
            for skill in activity.skills:
                counts[skill.strip().lower()] = counts.get(skill.strip().lower(), 0) + 1
        project_counts: dict[str, int] = {}
        for activity in activities:
            if activity.kind in {"project", "cross_pack"}:
                for skill in activity.skills:
                    key = skill.strip().lower()
                    project_counts[key] = project_counts.get(key, 0) + 1
        return {
            "activities_tracked": len(activities),
            "skill_activity_counts": dict(sorted(counts.items())),
            "skill_project_counts": dict(sorted(project_counts.items())),
            "ladder": [
                {
                    "skill": step.skill,
                    "min_projects": step.min_projects,
                    "next_skill": step.next_skill,
                    "title": step.title,
                    "unlocked": project_counts.get(step.skill, 0) >= step.min_projects,
                    "current_projects": project_counts.get(step.skill, 0),
                }
                for step in SKILL_LADDER
            ],
        }

    def set_learning_engine(self, learning_engine: Any) -> None:
        """Inject a core Knowledge ``LearningEngine`` or knowledge bridge."""
        self._learning_engine = learning_engine

    # ------------------------------------------------------------------
    # Signal sources
    # ------------------------------------------------------------------

    def _ladder_candidates(self, goal_id: str | None) -> list[GrowthRecommendation]:
        analytics_counts: dict[str, int] = {}
        for activity in self._repo.list_activities():
            if activity.kind not in {"project", "cross_pack"}:
                continue
            for skill in activity.skills:
                key = skill.strip().lower()
                analytics_counts[key] = analytics_counts.get(key, 0) + 1

        out: list[GrowthRecommendation] = []
        for step in SKILL_LADDER:
            completed = analytics_counts.get(step.skill, 0)
            if completed < step.min_projects:
                continue
            ratio = completed / max(step.min_projects, 1)
            confidence = min(1.0, 0.5 + 0.1 * ratio)
            if step.next_skill:
                rationale = (
                    f"Kamu sudah menyelesaikan {completed} project {step.skill} "
                    f"(threshold {step.min_projects}). Langkah berikutnya: {step.next_skill}."
                )
            else:
                rationale = (
                    f"Kamu sudah menyelesaikan {completed} project {step.skill} "
                    f"(threshold {step.min_projects}); projeksi level lanjutan."
                )
            if goal_id:
                rationale = f"{rationale} (diprioritaskan untuk goal {goal_id})"
            out.append(
                GrowthRecommendation(
                    id=f"rec-ladder-{uuid.uuid4().hex[:8]}",
                    kind=RecommendationKind.PROJECT.value,
                    title=step.title,
                    rationale=rationale,
                    skills_gained=list(step.skills_gained),
                    difficulty=step.difficulty,
                    estimated_hours=step.estimated_hours,
                    confidence=confidence,
                    source="skill_ladder",
                    source_pack=step.source_pack,
                    goal_id=goal_id,
                    project_id=step.project_id,
                    metadata={"ladder_skill": step.skill, "projects_completed": completed},
                )
            )
        return out

    def _goal_gap_candidates(self, goal_id: str | None) -> list[GrowthRecommendation]:
        goals = self._aligner.list_goals()
        if goal_id:
            resolved = self._aligner.resolve_goal(goal_id)
            goals = [resolved] if resolved is not None else []
        practised: set[str] = set()
        for activity in self._repo.list_activities():
            practised.update(s.strip().lower() for s in activity.skills)

        out: list[GrowthRecommendation] = []
        for goal in goals:
            missing = [s for s in goal.target_skills if s.strip().lower() not in practised]
            if not missing:
                continue
            missing_skills = ", ".join(missing[:4])
            out.append(
                GrowthRecommendation(
                    id=f"rec-goal-{uuid.uuid4().hex[:8]}",
                    kind=RecommendationKind.SKILL.value,
                    title=f"Pelajari skill yang dibutuhkan goal '{goal.title}'",
                    rationale=(
                        f"Goal '{goal.title}' masih membutuhkan skill: {missing_skills}. "
                        f"Target skills belum pernah dipractice pada aktivitas tercatat."
                    ),
                    skills_gained=list(missing[:4]),
                    difficulty="medium",
                    estimated_hours=2.0 * len(missing[:4]),
                    confidence=0.7 if goal_id else 0.55,
                    source="goal_gap",
                    goal_id=goal.id,
                    metadata={"missing_skills": missing, "goal_kind": goal.kind},
                )
            )
        return out

    def _knowledge_candidates(self, goal_id: str | None) -> list[GrowthRecommendation]:
        if self._learning_engine is None:
            return []
        out: list[GrowthRecommendation] = []
        try:
            recommendation = self._learning_engine.recommend(
                domain="self-development", context={"goal_id": goal_id}
            )
        except Exception:
            logger.debug("Knowledge recommendation unavailable", exc_info=True)
            return []
        if recommendation is None:
            return []
        out.append(
            GrowthRecommendation(
                id=f"rec-knowledge-{uuid.uuid4().hex[:8]}",
                kind=RecommendationKind.SKILL.value,
                title=f"Insight dari Knowledge: {recommendation.suggestion}",
                rationale=recommendation.rationale,
                confidence=float(recommendation.confidence or 0.4),
                source="knowledge",
                goal_id=goal_id,
                metadata={"based_on_patterns": list(recommendation.based_on_patterns)},
            )
        )
        return out


recommendation_engine = RecommendationEngine()
