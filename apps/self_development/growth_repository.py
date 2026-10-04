"""
Growth Repository
=================

Persists personal growth state for the Self Development capability pack:
learning activities, development goals, and habits.

Storage: in-memory with optional JSON file persistence.
"""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.self_development.schemas import GoalAlignment, GrowthGoal, Habit, LearningActivity

logger = logging.getLogger(__name__)


class GrowthRepository:
    """In-memory repository for growth state with optional file persistence."""

    def __init__(self, storage_path: Path | None = None) -> None:
        self._activities: dict[str, LearningActivity] = {}
        self._goals: dict[str, GrowthGoal] = {}
        self._habits: dict[str, Habit] = {}
        self._alignments: list[GoalAlignment] = []
        self._storage_path = storage_path or Path("apps/self_development/growth.json")
        self._load()

    # ------------------------------------------------------------------
    # Activities
    # ------------------------------------------------------------------

    def add_activity(self, activity: LearningActivity) -> LearningActivity:
        self._activities[activity.id] = activity
        self._save()
        return activity

    def get_activity(self, activity_id: str) -> LearningActivity | None:
        return self._activities.get(activity_id)

    def list_activities(
        self,
        kind: str | None = None,
        skill: str | None = None,
        goal_id: str | None = None,
    ) -> list[LearningActivity]:
        activities = list(self._activities.values())
        if kind:
            activities = [a for a in activities if a.kind == kind]
        if skill:
            activities = [a for a in activities if skill.lower() in {s.lower() for s in a.skills}]
        if goal_id:
            activities = [a for a in activities if a.goal_id == goal_id]
        return sorted(activities, key=lambda a: a.completed_at)

    def update_activity(self, activity: LearningActivity) -> LearningActivity:
        self._activities[activity.id] = activity
        self._save()
        return activity

    # ------------------------------------------------------------------
    # Goals
    # ------------------------------------------------------------------

    def add_goal(self, goal: GrowthGoal) -> GrowthGoal:
        self._goals[goal.id] = goal
        self._save()
        return goal

    def get_goal(self, goal_id: str) -> GrowthGoal | None:
        return self._goals.get(goal_id)

    def list_goals(self, status: str | None = "active") -> list[GrowthGoal]:
        goals = list(self._goals.values())
        if status:
            goals = [g for g in goals if g.metadata.get("status", "active") == status]
        return goals

    def record_alignment(self, alignment: GoalAlignment) -> GoalAlignment:
        self._alignments = [a for a in self._alignments if a.goal_id != alignment.goal_id]
        self._alignments.append(alignment)
        self._save()
        return alignment

    def list_alignments(self) -> list[GoalAlignment]:
        return list(self._alignments)

    # ------------------------------------------------------------------
    # Habits
    # ------------------------------------------------------------------

    def add_habit(self, habit: Habit) -> Habit:
        self._habits[habit.id] = habit
        self._save()
        return habit

    def get_habit(self, habit_id: str) -> Habit | None:
        return self._habits.get(habit_id)

    def list_habits(self) -> list[Habit]:
        return sorted(self._habits.values(), key=lambda h: h.created_at)

    def delete_habit(self, habit_id: str) -> bool:
        removed = self._habits.pop(habit_id, None) is not None
        if removed:
            self._save()
        return removed

    def clear(self) -> None:
        self._activities.clear()
        self._goals.clear()
        self._habits.clear()
        self._alignments.clear()
        self._save()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _save(self) -> None:
        try:
            data = {
                "activities": [
                    {
                        "id": a.id,
                        "title": a.title,
                        "kind": a.kind,
                        "duration_minutes": a.duration_minutes,
                        "skills": a.skills,
                        "goal_id": a.goal_id,
                        "goal_alignment": a.goal_alignment,
                        "goal_verdict": a.goal_verdict,
                        "source_pack": a.source_pack,
                        "completed_at": a.completed_at.isoformat(),
                        "notes": a.notes,
                        "metadata": a.metadata,
                    }
                    for a in self._activities.values()
                ],
                "goals": [
                    {
                        "id": g.id,
                        "title": g.title,
                        "kind": g.kind,
                        "target_skills": g.target_skills,
                        "success_criteria": g.success_criteria,
                        "target_date": g.target_date,
                        "progress": g.progress,
                        "source": g.source,
                        "core_goal_id": g.core_goal_id,
                        "metadata": g.metadata,
                    }
                    for g in self._goals.values()
                ],
                "habits": [
                    {
                        "id": h.id,
                        "name": h.name,
                        "cadence": h.cadence,
                        "target_per_period": h.target_per_period,
                        "check_ins": h.check_ins,
                        "goal_id": h.goal_id,
                        "reminder_hour": h.reminder_hour,
                        "created_at": h.created_at.isoformat(),
                        "metadata": h.metadata,
                    }
                    for h in self._habits.values()
                ],
                "alignments": [
                    {
                        "goal_id": a.goal_id,
                        "goal_title": a.goal_title,
                        "score": a.score,
                        "verdict": a.verdict,
                        "matched_terms": a.matched_terms,
                        "suggestions": a.suggestions,
                        "contributing_minutes": a.contributing_minutes,
                    }
                    for a in self._alignments
                ],
            }
            self._storage_path.parent.mkdir(parents=True, exist_ok=True)
            self._storage_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception:
            logger.debug("Failed to save growth state", exc_info=True)

    def _load(self) -> None:
        if not self._storage_path.exists():
            return
        try:
            data = json.loads(self._storage_path.read_text(encoding="utf-8"))
        except Exception:
            logger.debug("Failed to load growth state", exc_info=True)
            return
        for item in data.get("activities", []):
            activity = LearningActivity(
                id=item["id"],
                title=item.get("title", ""),
                kind=item.get("kind", "project"),
                duration_minutes=item.get("duration_minutes", 0.0),
                skills=item.get("skills", []),
                goal_id=item.get("goal_id"),
                goal_alignment=item.get("goal_alignment", 0.0),
                goal_verdict=item.get("goal_verdict", "unrelated"),
                source_pack=item.get("source_pack"),
                completed_at=_parse_dt(item.get("completed_at")),
                notes=item.get("notes", ""),
                metadata=item.get("metadata", {}),
            )
            self._activities[activity.id] = activity
        for item in data.get("goals", []):
            goal = GrowthGoal(
                id=item["id"],
                title=item.get("title", ""),
                kind=item.get("kind", "milestone"),
                target_skills=item.get("target_skills", []),
                success_criteria=item.get("success_criteria", []),
                target_date=item.get("target_date"),
                progress=item.get("progress", 0.0),
                source=item.get("source", "local"),
                core_goal_id=item.get("core_goal_id"),
                metadata=item.get("metadata", {}),
            )
            self._goals[goal.id] = goal
        for item in data.get("habits", []):
            habit = Habit(
                id=item["id"],
                name=item.get("name", ""),
                cadence=item.get("cadence", "daily"),
                target_per_period=item.get("target_per_period", 1),
                check_ins=item.get("check_ins", []),
                goal_id=item.get("goal_id"),
                reminder_hour=item.get("reminder_hour", 9),
                created_at=_parse_dt(item.get("created_at")),
                metadata=item.get("metadata", {}),
            )
            self._habits[habit.id] = habit
        for item in data.get("alignments", []):
            self._alignments.append(
                GoalAlignment(
                    goal_id=item.get("goal_id"),
                    goal_title=item.get("goal_title"),
                    score=item.get("score", 0.0),
                    verdict=item.get("verdict", "unrelated"),
                    matched_terms=item.get("matched_terms", []),
                    suggestions=item.get("suggestions", []),
                    contributing_minutes=item.get("contributing_minutes", 0.0),
                )
            )


def _parse_dt(value: str | None) -> datetime:
    """Parse an ISO timestamp, falling back to now on malformed input."""
    if not value:
        return datetime.now(UTC)
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return datetime.now(UTC)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed


def activity_payload(activity: LearningActivity) -> dict[str, Any]:
    """Serialize an activity for API/engine responses."""
    return {
        "id": activity.id,
        "title": activity.title,
        "kind": activity.kind,
        "duration_minutes": activity.duration_minutes,
        "skills": activity.skills,
        "goal_id": activity.goal_id,
        "goal_alignment": round(activity.goal_alignment, 2),
        "goal_verdict": activity.goal_verdict,
        "source_pack": activity.source_pack,
        "completed_at": activity.completed_at.isoformat(),
        "notes": activity.notes,
    }


growth_repository = GrowthRepository()
