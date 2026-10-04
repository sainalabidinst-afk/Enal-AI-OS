"""
Learning Analytics
==================

Tracks personal learning progress for the Self Development capability pack:
projects completed, skills acquired, time invested, and alignment rate.

Progress is bucketed per week or per month and can be rendered as a console
chart so the observability view can show growth over time.
"""

from __future__ import annotations

import logging
import uuid
from collections import Counter
from datetime import UTC, datetime, timedelta
from typing import Any

from apps.self_development.growth_repository import GrowthRepository, growth_repository
from apps.self_development.schemas import (
    ActivityKind,
    GoalVerdict,
    Granularity,
    LearningActivity,
    ProgressBucket,
    ProgressSnapshot,
    SkillLevel,
    SkillProgress,
)

logger = logging.getLogger(__name__)

PROJECT_KINDS = {ActivityKind.PROJECT.value, ActivityKind.CROSS_PACK.value}

LEVEL_THRESHOLDS: tuple[tuple[int, str], ...] = (
    (20, SkillLevel.ADVANCED.value),
    (8, SkillLevel.INTERMEDIATE.value),
    (2, SkillLevel.BEGINNER.value),
)

_STOPWORDS = {
    "a",
    "an",
    "and",
    "the",
    "for",
    "with",
    "to",
    "of",
    "in",
    "on",
    "my",
    "project",
    "learn",
    "learning",
    "build",
    "create",
    "make",
    "saya",
    "untuk",
    "dan",
    "di",
    "yang",
}

CHART_GLYPHS = " .:-=+*#%@"


class LearningAnalytics:
    """Aggregates learning activities into progress metrics and charts."""

    def __init__(self, repository: GrowthRepository | None = None) -> None:
        self._repo = repository or growth_repository

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    def record_activity(
        self,
        title: str,
        kind: str = ActivityKind.PROJECT.value,
        duration_minutes: float = 0.0,
        skills: list[str] | None = None,
        goal_id: str | None = None,
        goal_alignment: float = 0.0,
        goal_verdict: str = GoalVerdict.UNRELATED.value,
        source_pack: str | None = None,
        completed_at: datetime | None = None,
        notes: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> LearningActivity:
        """Record one learning activity and return the stored entity."""
        activity = LearningActivity(
            id=f"act-{uuid.uuid4().hex[:8]}",
            title=title,
            kind=kind,
            duration_minutes=duration_minutes,
            skills=[s.strip() for s in (skills or []) if s and s.strip()],
            goal_id=goal_id,
            goal_alignment=goal_alignment,
            goal_verdict=goal_verdict,
            source_pack=source_pack,
            completed_at=completed_at or datetime.now(UTC),
            notes=notes,
            metadata=metadata or {},
        )
        return self._repo.add_activity(activity)

    # ------------------------------------------------------------------
    # Aggregation
    # ------------------------------------------------------------------

    def list_activities(
        self,
        kind: str | None = None,
        skill: str | None = None,
        goal_id: str | None = None,
    ) -> list[LearningActivity]:
        """Return stored activities, optionally filtered."""
        return self._repo.list_activities(kind=kind, skill=skill, goal_id=goal_id)

    def bucket(self, granularity: str = Granularity.WEEK.value) -> list[ProgressBucket]:
        """Aggregate activities into consecutive week or month buckets."""
        if granularity not in (Granularity.WEEK.value, Granularity.MONTH.value):
            raise ValueError(f"Unsupported granularity: {granularity}")

        activities = self._repo.list_activities()
        if not activities:
            return []

        key_fn = _week_key if granularity == Granularity.WEEK.value else _month_key
        sort_fn = _week_sort_key if granularity == Granularity.WEEK.value else _month_sort_key

        buckets: dict[str, ProgressBucket] = {}
        seen_skills: dict[str, set[str]] = {}
        for activity in activities:
            key = key_fn(activity.completed_at)
            bucket = buckets.get(key)
            if bucket is None:
                bucket = ProgressBucket(period=key)
                buckets[key] = bucket
                seen_skills[key] = set()
            bucket.activities += 1
            bucket.minutes_spent += activity.duration_minutes
            if activity.kind in PROJECT_KINDS:
                bucket.projects_completed += 1
            for skill in activity.skills:
                normalized = skill.strip()
                if not normalized:
                    continue
                key_lower = normalized.lower()
                if key_lower not in seen_skills[key]:
                    seen_skills[key].add(key_lower)
                    bucket.new_skills.append(normalized)

        ordered = sorted(buckets.values(), key=lambda b: sort_fn(b.period))
        if granularity == Granularity.WEEK.value:
            return _fill_week_gaps(ordered)
        return ordered

    def skill_progress(self) -> list[SkillProgress]:
        """Aggregate per-skill activity counts, time, and derived level."""
        progress: dict[str, SkillProgress] = {}
        for activity in self._repo.list_activities():
            for skill in activity.skills:
                normalized = skill.strip()
                if not normalized:
                    continue
                entry = progress.get(normalized)
                if entry is None:
                    entry = SkillProgress(skill=normalized)
                    progress[normalized] = entry
                entry.activities += 1
                entry.minutes_spent += activity.duration_minutes
                if activity.kind in PROJECT_KINDS:
                    entry.projects_completed += 1
                if entry.last_practiced is None or activity.completed_at > entry.last_practiced:
                    entry.last_practiced = activity.completed_at
                if len(entry.evidence) < 10:
                    entry.evidence.append(activity.id)
        for entry in progress.values():
            entry.level = _derive_level(entry)
        return sorted(progress.values(), key=lambda s: (s.minutes_spent, s.skill), reverse=True)

    def snapshot(
        self, granularity: str = Granularity.WEEK.value, weeks: int = 12
    ) -> ProgressSnapshot:
        """Build a full progress snapshot including recent buckets."""
        activities = self._repo.list_activities()
        buckets = self.bucket(granularity)
        if weeks > 0:
            buckets = buckets[-weeks:]
        aligned = sum(1 for a in activities if a.goal_verdict == GoalVerdict.ALIGNED.value)
        unaligned = sum(1 for a in activities if a.goal_verdict == GoalVerdict.UNRELATED.value)
        mean_alignment = (
            sum(a.goal_alignment for a in activities) / len(activities) if activities else 0.0
        )
        skills = self.skill_progress()
        return ProgressSnapshot(
            total_activities=len(activities),
            total_projects=sum(1 for a in activities if a.kind in PROJECT_KINDS),
            total_minutes=sum(a.duration_minutes for a in activities),
            active_skills=len(skills),
            current_streak_weeks=self.current_streak_weeks(),
            buckets=buckets,
            skills=skills,
            aligned_activities=aligned,
            unaligned_activities=unaligned,
            alignment_rate=mean_alignment,
        )

    def current_streak_weeks(self) -> int:
        """Count consecutive weeks (ending this week) with at least one activity."""
        active = {b.period for b in self.bucket(Granularity.WEEK.value) if b.activities > 0}
        if not active:
            return 0
        streak = 0
        cursor = _week_start(datetime.now(UTC))
        while _week_key(cursor) in active:
            streak += 1
            cursor -= timedelta(days=7)
        return streak

    def weekly_hours(self, weeks: int = 12) -> list[float]:
        """Return invested hours per week, oldest first."""
        buckets = self.bucket(Granularity.WEEK.value)[-weeks:]
        return [round(b.minutes_spent / 60.0, 2) for b in buckets]

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render_chart(
        self,
        granularity: str = Granularity.WEEK.value,
        weeks: int = 12,
        metric: str = "hours",
        width: int = 40,
    ) -> str:
        """Render an ASCII progress chart for the console observability view."""
        buckets = self.bucket(granularity)
        if weeks > 0:
            buckets = buckets[-weeks:]
        if not buckets:
            return "No learning activity recorded yet."

        if metric == "projects":
            values = [float(b.projects_completed) for b in buckets]
            unit = "projects"
        elif metric == "skills":
            values = [float(len(b.new_skills)) for b in buckets]
            unit = "new skills"
        else:
            values = [round(b.minutes_spent / 60.0, 2) for b in buckets]
            unit = "hours"

        title = f"Learning progress per {granularity} ({unit})"
        body = _render_bars(buckets, values, width=width)
        peak = max(values)
        footer = f"peak {peak:g} {unit} | total {sum(values):g} {unit}"
        return f"{title}\n{body}\n{footer}"

    def render_sparkline(self, weeks: int = 12) -> str:
        """Render a compact one-line sparkline of weekly invested hours."""
        values = self.weekly_hours(weeks)
        if not values:
            return ""
        return _sparkline(values)

    # ------------------------------------------------------------------
    # Series (for observability / frontend charts)
    # ------------------------------------------------------------------

    def series(
        self, granularity: str = Granularity.WEEK.value, periods: int = 12
    ) -> dict[str, Any]:
        """Return a JSON-friendly chart series."""
        buckets = self.bucket(granularity)
        if periods > 0:
            buckets = buckets[-periods:]
        return {
            "granularity": granularity,
            "labels": [b.period for b in buckets],
            "hours": [round(b.minutes_spent / 60.0, 2) for b in buckets],
            "projects": [b.projects_completed for b in buckets],
            "activities": [b.activities for b in buckets],
            "new_skills": [len(b.new_skills) for b in buckets],
        }


# ----------------------------------------------------------------------
# Module helpers
# ----------------------------------------------------------------------


def _week_start(moment: datetime) -> datetime:
    moment = _as_utc(moment)
    start = moment - timedelta(days=moment.weekday())
    return start.replace(hour=0, minute=0, second=0, microsecond=0)


def _month_start(moment: datetime) -> datetime:
    moment = _as_utc(moment)
    return moment.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def _week_key(moment: datetime) -> str:
    iso_year, iso_week, _ = _as_utc(moment).isocalendar()
    return f"{iso_year}-W{iso_week:02d}"


def _month_key(moment: datetime) -> str:
    return _as_utc(moment).strftime("%Y-%m")


def _as_utc(moment: datetime) -> datetime:
    return moment if moment.tzinfo else moment.replace(tzinfo=UTC)


def _week_start_from_key(key: str) -> datetime:
    year, week = key.split("-W")
    return datetime.fromisocalendar(int(year), int(week), 1).replace(tzinfo=UTC)


def _week_sort_key(period: str) -> datetime:
    return _week_start_from_key(period)


def _month_sort_key(period: str) -> datetime:
    return datetime.strptime(period, "%Y-%m").replace(tzinfo=UTC)


def _fill_week_gaps(buckets: list[ProgressBucket]) -> list[ProgressBucket]:
    """Insert empty buckets so the chart has no holes in the timeline."""
    if len(buckets) < 2:
        return buckets
    filled: list[ProgressBucket] = []
    for current, following in zip(buckets, buckets[1:], strict=False):
        filled.append(current)
        cursor = _week_start_from_key(current.period) + timedelta(days=7)
        while cursor < _week_start_from_key(following.period):
            filled.append(ProgressBucket(period=_week_key(cursor)))
            cursor += timedelta(days=7)
    filled.append(buckets[-1])
    return filled


def _derive_level(progress: SkillProgress) -> str:
    score = progress.projects_completed * 2 + progress.activities
    for threshold, level in LEVEL_THRESHOLDS:
        if score >= threshold:
            return level
    return SkillLevel.NOVICE.value


def _render_bars(buckets: list[ProgressBucket], values: list[float], width: int = 40) -> str:
    label_width = max(len(b.period) for b in buckets)
    label_width = max(label_width, len("period"))
    bar_width = max(width - label_width - 8, 10)
    lines = []
    for bucket, value in zip(buckets, values, strict=False):
        filled = int(round((value / max(values)) * bar_width)) if max(values) > 0 else 0
        bar = "#" * filled
        lines.append(f"{bucket.period:<{label_width}} | {bar:<{bar_width}} {value:g}")
    return "\n".join(lines)


def _sparkline(values: list[float]) -> str:
    peak = max(values)
    if peak <= 0:
        return CHART_GLYPHS[0] * len(values)
    step = (len(CHART_GLYPHS) - 1) / peak
    return "".join(CHART_GLYPHS[min(len(CHART_GLYPHS) - 1, int(v * step))] for v in values)


def tokenize(text: str) -> list[str]:
    """Lowercase alphanumeric tokens with stopwords removed."""
    cleaned = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
    return [t for t in cleaned.split() if t and t not in _STOPWORDS]


def skill_frequency(activities: list[LearningActivity]) -> Counter[str]:
    """Count skill mentions across activities (lowercased)."""
    counter: Counter[str] = Counter()
    for activity in activities:
        counter.update(s.strip().lower() for s in activity.skills if s.strip())
    return counter


learning_analytics = LearningAnalytics()
