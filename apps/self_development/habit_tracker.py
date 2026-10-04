"""
Habit Tracker
=============

Simple habit formation for learning routines: daily/weekly check-ins, streak
counters, reminders, and alert emission.

The alert surface mirrors the anomaly → remediation flow already used by the
pack: conditions are evaluated, ``GrowthAlert`` records are produced, and the
dispatcher publishes them on the stable event bus so any subscriber (console,
notification service, pipeline stage) can react.
"""

from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from apps.self_development.growth_repository import GrowthRepository, growth_repository
from apps.self_development.schemas import (
    AlertSeverity,
    GoalVerdict,
    GrowthAlert,
    Habit,
    HabitCadence,
    HabitStatus,
)

logger = logging.getLogger(__name__)

HABIT_REMINDER_EVENT = "self_development.habit.reminder"
HABIT_STREAK_EVENT = "self_development.habit.streak"
GOAL_DRIFT_EVENT = "self_development.goal.drift"


class HabitTracker:
    """Tracks learning habits, streaks, and reminder alerts."""

    def __init__(self, repository: GrowthRepository | None = None) -> None:
        self._repo = repository or growth_repository
        self._alerts: list[GrowthAlert] = []

    # ------------------------------------------------------------------
    # Habit lifecycle
    # ------------------------------------------------------------------

    def create_habit(
        self,
        name: str,
        cadence: str = HabitCadence.DAILY.value,
        target_per_period: int = 1,
        goal_id: str | None = None,
        reminder_hour: int = 9,
        metadata: dict[str, Any] | None = None,
    ) -> Habit:
        """Register a recurring learning habit."""
        if cadence not in (HabitCadence.DAILY.value, HabitCadence.WEEKLY.value):
            raise ValueError(f"Unsupported cadence: {cadence}")
        if target_per_period < 1:
            raise ValueError("target_per_period must be >= 1")
        habit = Habit(
            id=f"habit-{uuid.uuid4().hex[:8]}",
            name=name,
            cadence=cadence,
            target_per_period=target_per_period,
            goal_id=goal_id,
            reminder_hour=max(0, min(23, reminder_hour)),
            metadata=metadata or {},
        )
        return self._repo.add_habit(habit)

    def list_habits(self) -> list[Habit]:
        return self._repo.list_habits()

    def delete_habit(self, habit_id: str) -> bool:
        return self._repo.delete_habit(habit_id)

    # ------------------------------------------------------------------
    # Check-ins
    # ------------------------------------------------------------------

    def check_in(
        self,
        habit_id: str,
        checked_at: datetime | None = None,
        note: str = "",
    ) -> dict[str, Any]:
        """Record a check-in and return the updated habit status."""
        habit = self._repo.get_habit(habit_id)
        if habit is None:
            raise KeyError(f"Unknown habit_id: {habit_id}")
        moment = _as_utc(checked_at or datetime.now(UTC))
        period_key = _period_key(moment, habit.cadence)
        if period_key not in habit.check_ins:
            habit.check_ins.append(period_key)
            habit.check_ins.sort()
        if note:
            habit.metadata.setdefault("notes", {})[period_key] = note
        self._repo.add_habit(habit)

        status = self.status(habit_id, now=moment)
        payload = _status_payload(status)
        if status.current_streak > 1:
            self._emit(
                HABIT_STREAK_EVENT,
                AlertSeverity.INFO,
                subject=habit.name,
                message=f"Streak {status.current_streak} periode untuk {habit.name}",
                metadata={"habit_id": habit.id, "streak": status.current_streak},
            )
        return payload

    def status(self, habit_id: str, now: datetime | None = None) -> HabitStatus:
        """Derive current streak, period progress, and risk for a habit."""
        habit = self._repo.get_habit(habit_id)
        if habit is None:
            raise KeyError(f"Unknown habit_id: {habit_id}")
        return self._derive_status(habit, _as_utc(now or datetime.now(UTC)))

    def all_statuses(self, now: datetime | None = None) -> list[dict[str, Any]]:
        """Status payload for every registered habit."""
        moment = _as_utc(now or datetime.now(UTC))
        return [_status_payload(self._derive_status(h, moment)) for h in self._repo.list_habits()]

    # ------------------------------------------------------------------
    # Reminders and alerts
    # ------------------------------------------------------------------

    def due_reminders(self, now: datetime | None = None) -> list[GrowthAlert]:
        """Return reminders for habits whose current period is not satisfied."""
        moment = _as_utc(now or datetime.now(UTC))
        alerts: list[GrowthAlert] = []
        for habit in self._repo.list_habits():
            status = self._derive_status(habit, moment)
            if status.target_met:
                continue
            severity = (
                AlertSeverity.CRITICAL
                if habit.cadence == HabitCadence.DAILY.value
                else AlertSeverity.WARNING
            )
            alerts.append(
                GrowthAlert(
                    id=f"alert-{uuid.uuid4().hex[:8]}",
                    alert_type="habit_reminder",
                    severity=severity.value,
                    subject=habit.name,
                    message=(
                        f"{habit.name}: {status.period_check_ins}/{habit.target_per_period} "
                        f"check-in untuk periode {status.next_due}. "
                        f"Streak saat ini {status.current_streak}."
                    ),
                    metadata={
                        "habit_id": habit.id,
                        "cadence": habit.cadence,
                        "goal_id": habit.goal_id,
                        "next_due": status.next_due,
                    },
                )
            )
        return alerts

    def goal_drift_alerts(self, min_alignment: float = 0.3, limit: int = 50) -> list[GrowthAlert]:
        """Raise alerts for recent activities unrelated to any development goal."""
        alerts: list[GrowthAlert] = []
        for activity in self._repo.list_activities():
            if len(alerts) >= limit:
                break
            if activity.goal_verdict != GoalVerdict.UNRELATED.value:
                continue
            alerts.append(
                GrowthAlert(
                    id=f"alert-{uuid.uuid4().hex[:8]}",
                    alert_type="goal_drift",
                    severity=AlertSeverity.WARNING.value,
                    subject=activity.title,
                    message=(
                        f"Aktivitas '{activity.title}' tidak selaras dengan goal mana pun "
                        f"(alignment {activity.goal_alignment:.2f} < {min_alignment:.2f})."
                    ),
                    metadata={
                        "activity_id": activity.id,
                        "kind": activity.kind,
                        "skills": activity.skills,
                    },
                )
            )
        return alerts

    def evaluate_alerts(self, now: datetime | None = None) -> list[GrowthAlert]:
        """Evaluate every alert rule and cache the result."""
        alerts = self.due_reminders(now) + self.goal_drift_alerts()
        self._alerts = alerts
        return alerts

    def list_alerts(self) -> list[GrowthAlert]:
        return list(self._alerts)

    async def dispatch_alerts(self, now: datetime | None = None) -> list[dict[str, Any]]:
        """Evaluate alerts and publish them on the stable event bus."""
        alerts = self.evaluate_alerts(now)
        published: list[dict[str, Any]] = []
        for alert in alerts:
            event_type = (
                GOAL_DRIFT_EVENT if alert.alert_type == "goal_drift" else HABIT_REMINDER_EVENT
            )
            delivered = await self._publish(
                event_type,
                alert.subject,
                alert.message,
                {
                    "alert_id": alert.id,
                    "alert_type": alert.alert_type,
                    "severity": alert.severity,
                    **alert.metadata,
                },
            )
            _record_growth_alert(alert, delivered)
            published.append(
                {
                    "alert_id": alert.id,
                    "alert_type": alert.alert_type,
                    "event_type": event_type,
                    "severity": alert.severity,
                    "published": delivered,
                }
            )
        _record_growth_metrics(alerts)
        return published

    def clear_alerts(self) -> None:
        self._alerts.clear()

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _derive_status(self, habit: Habit, now: datetime) -> HabitStatus:
        period_key = _period_key(now, habit.cadence)
        period_check_ins = sum(1 for key in habit.check_ins if key == period_key)
        check_in_keys = sorted(habit.check_ins)

        streak = _consecutive_period_streak(check_in_keys, period_key, habit.cadence)
        longest = _longest_period_streak(check_in_keys, habit.cadence)
        target_met = period_check_ins >= habit.target_per_period
        next_due = _next_period(period_key, habit.cadence)

        at_risk = False
        if check_in_keys:
            last = check_in_keys[-1]
            gap = _period_distance(last, period_key, habit.cadence)
            at_risk = gap >= 2 or (target_met is False and gap >= 1)

        return HabitStatus(
            habit_id=habit.id,
            name=habit.name,
            cadence=habit.cadence,
            current_streak=streak,
            longest_streak=longest,
            period_check_ins=period_check_ins,
            target_per_period=habit.target_per_period,
            target_met=target_met,
            last_check_in=check_in_keys[-1] if check_in_keys else None,
            next_due=next_due,
            at_risk=at_risk,
            goal_id=habit.goal_id,
        )

    def _emit(
        self,
        alert_type: str,
        severity: str,
        subject: str,
        message: str,
        metadata: dict[str, Any] | None = None,
    ) -> GrowthAlert:
        alert = GrowthAlert(
            id=f"alert-{uuid.uuid4().hex[:8]}",
            alert_type=alert_type,
            severity=getattr(severity, "value", severity),
            subject=subject,
            message=message,
            metadata=metadata or {},
        )
        self._alerts.append(alert)
        return alert

    async def _publish(
        self, event_type: str, subject: str, message: str, payload: dict[str, Any]
    ) -> bool:
        try:
            from backend.app.core.event_bus import Event, event_bus

            await event_bus.publish(
                Event(
                    event_type=event_type,
                    payload={"subject": subject, "message": message, **payload},
                )
            )
            return True
        except Exception:
            logger.debug("Failed to publish habit alert", exc_info=True)
            return False


# ----------------------------------------------------------------------
# Module helpers
# ----------------------------------------------------------------------


def _as_utc(moment: datetime) -> datetime:
    return moment.astimezone(UTC) if moment.tzinfo else moment.replace(tzinfo=UTC)


def _period_key(moment: datetime, cadence: str) -> str:
    iso_year, iso_week, iso_day = _as_utc(moment).isocalendar()
    if cadence == HabitCadence.WEEKLY.value:
        return f"{iso_year}-W{iso_week:02d}"
    return f"{iso_year}-W{iso_week:02d}-D{iso_day:02d}"


def _parse_period_key(period_key: str, cadence: str) -> datetime:
    """Convert a period key back into its anchor date."""
    prefix, rest = period_key.split("-W", 1)
    year = int(prefix)
    if "-D" in rest:
        week_part, day_part = rest.split("-D", 1)
        week, day = int(week_part), int(day_part)
    else:
        week, day = int(rest), 1
    anchor = datetime.fromisocalendar(year, week, day)
    return anchor if anchor.tzinfo else anchor.replace(tzinfo=UTC)


def _next_period(period_key: str, cadence: str) -> str:
    step = timedelta(days=7 if cadence == HabitCadence.WEEKLY.value else 1)
    return _period_key(_parse_period_key(period_key, cadence) + step, cadence)


def _previous_period(period_key: str, cadence: str) -> str:
    step = timedelta(days=7 if cadence == HabitCadence.WEEKLY.value else 1)
    return _period_key(_parse_period_key(period_key, cadence) - step, cadence)


def _period_distance(earlier: str, later: str, cadence: str) -> int:
    """Number of periods between two period keys (0 when equal)."""
    if earlier == later:
        return 0
    step = 7 if cadence == HabitCadence.WEEKLY.value else 1
    delta = (_parse_period_key(later, cadence) - _parse_period_key(earlier, cadence)).days
    return max(0, round(delta / step))


def _consecutive_period_streak(keys: list[str], current: str, cadence: str) -> int:
    """Streak of consecutive checked-in periods ending at the current period."""
    if current not in keys:
        return 0
    streak = 0
    cursor = current
    key_set = set(keys)
    while cursor in key_set:
        streak += 1
        cursor = _previous_period(cursor, cadence)
    return streak


def _longest_period_streak(keys: list[str], cadence: str) -> int:
    """Longest run of consecutive periods in the check-in history."""
    if not keys:
        return 0
    longest = 0
    run = 0
    previous: str | None = None
    for key in keys:
        if previous is not None and _period_distance(previous, key, cadence) == 1:
            run += 1
        else:
            run = 1
        longest = max(longest, run)
        previous = key
    return longest


def _status_payload(status: HabitStatus) -> dict[str, Any]:
    return {
        "habit_id": status.habit_id,
        "name": status.name,
        "cadence": status.cadence,
        "current_streak": status.current_streak,
        "longest_streak": status.longest_streak,
        "period_check_ins": status.period_check_ins,
        "target_per_period": status.target_per_period,
        "target_met": status.target_met,
        "last_check_in": status.last_check_in,
        "next_due": status.next_due,
        "at_risk": status.at_risk,
        "goal_id": status.goal_id,
    }


def _record_growth_alert(alert: GrowthAlert, delivered: bool) -> None:
    """Mirror a growth alert into the observability alert pipeline."""
    try:
        from backend.app.core.telemetry.aggregator import aggregator

        aggregator.record_growth_alert(
            event_id=alert.id,
            alert_type=alert.alert_type,
            severity=alert.severity,
            subject=alert.subject,
            message=alert.message,
            details=dict(alert.metadata),
            status="published" if delivered else "failed",
        )
    except Exception:
        logger.debug("Failed to record growth alert", exc_info=True)


def _record_growth_metrics(alerts: list[GrowthAlert]) -> None:
    """Publish growth alert counters to the RFC-0001 metrics collector."""
    try:
        from backend.app.core.observability import metrics_collector

        reminders = sum(1 for a in alerts if a.alert_type == "habit_reminder")
        drift = sum(1 for a in alerts if a.alert_type == "goal_drift")
        metrics_collector.gauge("self_development.habit_reminders", reminders)
        metrics_collector.gauge("self_development.goal_drift_alerts", drift)
    except Exception:
        logger.debug("Growth alert metrics unavailable", exc_info=True)


habit_tracker = HabitTracker()
