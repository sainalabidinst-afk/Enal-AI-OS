"""
Goal Aligner
============

Links self-development activities to long-term goals and validates whether
an activity is relevant to the learner's targets.

Goals come from two sources:
- Core Goal Management (``backend.app.core.goal_engine``) — imported lazily so
  the pack keeps working when the core engine is unavailable.
- Local growth goals stored in ``GrowthRepository`` (certification, portfolio,
  career milestone), which support explicit ``target_skills`` mapping.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from apps.self_development.growth_repository import GrowthRepository, growth_repository
from apps.self_development.learning_analytics import tokenize
from apps.self_development.schemas import (
    GoalAlignment,
    GoalVerdict,
    GrowthGoal,
    Habit,
    LearningActivity,
)

logger = logging.getLogger(__name__)

ALIGNED_THRESHOLD = 0.6
PARTIAL_THRESHOLD = 0.3


class GoalAligner:
    """Scores activities against development goals and accumulates progress."""

    def __init__(self, repository: GrowthRepository | None = None) -> None:
        self._repo = repository or growth_repository

    # ------------------------------------------------------------------
    # Goals
    # ------------------------------------------------------------------

    def create_goal(
        self,
        title: str,
        kind: str = "milestone",
        target_skills: list[str] | None = None,
        success_criteria: list[str] | None = None,
        target_date: str | None = None,
        core_goal_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> GrowthGoal:
        """Register a long-term development goal."""
        goal = GrowthGoal(
            id=f"gdev-{uuid.uuid4().hex[:8]}",
            title=title,
            kind=kind,
            target_skills=[s.strip() for s in (target_skills or []) if s and s.strip()],
            success_criteria=[c.strip() for c in (success_criteria or []) if c and c.strip()],
            target_date=target_date,
            source="core" if core_goal_id else "local",
            core_goal_id=core_goal_id,
            metadata=metadata or {},
        )
        return self._repo.add_goal(goal)

    def list_goals(self, include_core: bool = True) -> list[GrowthGoal]:
        """List local goals plus mirrored core Goal Management goals."""
        goals = list(self._repo.list_goals())
        if include_core:
            goals.extend(self._mirror_core_goals())
        return goals

    def resolve_goal(self, goal_id: str) -> GrowthGoal | None:
        """Find a goal by id in local storage or in the core goal engine."""
        goal = self._repo.get_goal(goal_id)
        if goal is not None:
            return goal
        for mirrored in self._mirror_core_goals():
            if mirrored.id == goal_id:
                return mirrored
        return None

    # ------------------------------------------------------------------
    # Alignment
    # ------------------------------------------------------------------

    def align(
        self,
        title: str,
        skills: list[str] | None = None,
        goal_id: str | None = None,
        duration_minutes: float = 0.0,
        kind: str = "project",
    ) -> GoalAlignment:
        """Score an activity against goals and return the best alignment."""
        if goal_id:
            goal = self.resolve_goal(goal_id)
            if goal is None:
                return GoalAlignment(
                    goal_id=goal_id,
                    goal_title=None,
                    score=0.0,
                    verdict=GoalVerdict.UNRELATED.value,
                    suggestions=[f"Goal {goal_id} tidak ditemukan"],
                )
            return self._score(goal, title, skills or [], duration_minutes)

        best = GoalAlignment(
            goal_id=None,
            goal_title=None,
            score=0.0,
            verdict=GoalVerdict.UNRELATED.value,
        )
        goals = self.list_goals()
        for goal in goals:
            candidate = self._score(goal, title, skills or [], duration_minutes)
            if candidate.score > best.score:
                best = candidate
        if best.score == 0.0 and not goals:
            best.suggestions = ["Belum ada goal terdaftar — daftarkan target jangka panjang dulu"]
        return best

    def record_activity_alignment(self, activity: LearningActivity) -> GoalAlignment:
        """Align a stored activity and persist the resulting alignment."""
        alignment = self.align(
            title=activity.title,
            skills=activity.skills,
            goal_id=activity.goal_id,
            duration_minutes=activity.duration_minutes,
            kind=activity.kind,
        )
        activity.goal_id = alignment.goal_id
        activity.goal_alignment = alignment.score
        activity.goal_verdict = alignment.verdict
        self._repo.update_activity(activity)
        if alignment.goal_id:
            alignment.contributing_minutes = sum(
                a.duration_minutes for a in self._repo.list_activities(goal_id=alignment.goal_id)
            )
            self._repo.record_alignment(alignment)
        return alignment

    def validate_relevance(
        self, title: str, skills: list[str] | None = None, goal_id: str | None = None
    ) -> dict[str, Any]:
        """Validate whether an activity is relevant to a goal."""
        alignment = self.align(title=title, skills=skills, goal_id=goal_id)
        return {
            "is_relevant": alignment.verdict != GoalVerdict.UNRELATED.value,
            "goal_id": alignment.goal_id,
            "goal_title": alignment.goal_title,
            "score": round(alignment.score, 2),
            "verdict": alignment.verdict,
            "matched_terms": alignment.matched_terms,
            "suggestions": alignment.suggestions,
        }

    def goal_progress(self, goal_id: str) -> dict[str, Any]:
        """Report accumulated minutes and skill coverage for a goal."""
        goal = self.resolve_goal(goal_id)
        if goal is None:
            return {"goal_id": goal_id, "found": False}
        activities = self._repo.list_activities(goal_id=goal_id)
        covered = {s.strip().lower() for a in activities for s in a.skills}
        target = {s.strip().lower() for s in goal.target_skills}
        coverage = (len(target & covered) / len(target)) if target else 0.0
        minutes = sum(a.duration_minutes for a in activities)
        return {
            "goal_id": goal.id,
            "goal_title": goal.title,
            "kind": goal.kind,
            "found": True,
            "target_date": goal.target_date,
            "activities": len(activities),
            "minutes_invested": round(minutes, 1),
            "hours_invested": round(minutes / 60.0, 2),
            "skill_coverage": round(coverage, 2),
            "target_skills": goal.target_skills,
            "covered_skills": sorted(target & covered),
            "missing_skills": sorted(target - covered),
            "progress": round(coverage * 100.0, 1) if target else 0.0,
        }

    def goals_progress(self) -> list[dict[str, Any]]:
        """Progress report for every known goal."""
        return [self.goal_progress(goal.id) for goal in self.list_goals()]

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _score(
        self,
        goal: GrowthGoal,
        title: str,
        skills: list[str],
        duration_minutes: float,
    ) -> GoalAlignment:
        goal_terms = set(tokenize(goal.title))
        for criterion in goal.success_criteria:
            goal_terms.update(tokenize(criterion))
        target_skills = {s.strip().lower() for s in goal.target_skills}
        skill_terms = {s.strip().lower() for s in skills if s.strip()}
        activity_terms = set(tokenize(title)) | skill_terms

        skill_hits = target_skills & skill_terms
        term_hits = goal_terms & activity_terms

        if target_skills:
            skill_score = len(skill_hits) / len(target_skills)
        elif goal_terms:
            skill_score = len(term_hits) / len(goal_terms)
        else:
            skill_score = 0.0

        term_score = (len(term_hits) / len(goal_terms)) if goal_terms else 0.0
        score = round(min(1.0, 0.65 * skill_score + 0.35 * term_score), 3)

        verdict = _verdict_for(score)
        suggestions: list[str] = []
        if verdict == GoalVerdict.UNRELATED.value:
            if goal.target_skills:
                missing = sorted(target_skills - skill_terms)[:3]
                suggestions.append(
                    "Tambahkan skill yang relevan: " + ", ".join(missing)
                    if missing
                    else f"Aktivitas ini belum menyentuh skill utama goal: {goal.title}"
                )
            elif goal_terms:
                keywords = ", ".join(sorted(goal_terms)[:3])
                suggestions.append(f"Judul aktivitas tidak memuat kata kunci goal: {keywords}")
            else:
                suggestions.append(
                    "Goal belum memiliki success criteria — lengkapi agar bisa divalidasi"
                )
        elif verdict == GoalVerdict.PARTIAL.value:
            suggestions.append(f"Tambahkan bobot waktu untuk mencapai target: {goal.title}")

        matched = sorted(skill_hits | term_hits)
        alignment = GoalAlignment(
            goal_id=goal.id,
            goal_title=goal.title,
            score=score,
            verdict=verdict,
            matched_terms=matched,
            suggestions=suggestions,
            contributing_minutes=duration_minutes,
        )
        return alignment

    def _mirror_core_goals(self) -> list[GrowthGoal]:
        """Reflect core Goal Management goals as growth goals."""
        try:
            from backend.app.core.goal_engine import goal_engine

            core_goals = goal_engine.list_goals()
        except Exception:
            logger.debug("Core goal engine unavailable", exc_info=True)
            return []

        mirrored: list[GrowthGoal] = []
        for core in core_goals:
            mirrored.append(
                GrowthGoal(
                    id=core.id,
                    title=getattr(core, "description", ""),
                    kind="milestone",
                    target_skills=list((getattr(core, "metadata", None) or {}).get("skills", [])),
                    success_criteria=list(getattr(core, "success_criteria", []) or []),
                    progress=float(getattr(core, "progress", 0.0) or 0.0),
                    source="core",
                    core_goal_id=core.id,
                    metadata={"status": getattr(core, "status", "active")},
                )
            )
        return mirrored

    def link_habits_to_goals(self) -> list[dict[str, Any]]:
        """Attribute open habits to the goals they support."""
        habits: list[Habit] = self._repo.list_habits()
        report = []
        for habit in habits:
            alignment = (
                self.align(title=habit.name, skills=[], goal_id=habit.goal_id)
                if habit.goal_id
                else GoalAlignment(None, None, 0.0, GoalVerdict.UNRELATED.value)
            )
            report.append(
                {
                    "habit_id": habit.id,
                    "habit": habit.name,
                    "goal_id": habit.goal_id,
                    "alignment": round(alignment.score, 2),
                    "verdict": alignment.verdict,
                }
            )
        return report


def _verdict_for(score: float) -> str:
    if score >= ALIGNED_THRESHOLD:
        return GoalVerdict.ALIGNED.value
    if score >= PARTIAL_THRESHOLD:
        return GoalVerdict.PARTIAL.value
    return GoalVerdict.UNRELATED.value


goal_aligner = GoalAligner()
