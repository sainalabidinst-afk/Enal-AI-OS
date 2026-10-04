"""
Export Service
===============

Exports the self-development progress summary as JSON or HTML so
users can download a portable snapshot of their learning progress,
goals, habits, and recommendations.

Output is written to ``artifacts/self_development/`` and the full
content is also returned in-memory for API responses.
"""

from __future__ import annotations

import html
import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.self_development.goal_aligner import GoalAligner, goal_aligner
from apps.self_development.habit_tracker import HabitTracker, habit_tracker
from apps.self_development.learning_analytics import (
    LearningAnalytics,
    learning_analytics,
)
from apps.self_development.recommendation_engine import (
    RecommendationEngine,
    recommendation_engine,
)

logger = logging.getLogger(__name__)

DEFAULT_EXPORT_DIR = Path("artifacts/self_development")

EXPORT_FORMATS = ("json", "html")


class ExportService:
    """Builds and persists user-facing progress reports."""

    def __init__(
        self,
        export_dir: Path | None = None,
        analytics: LearningAnalytics | None = None,
        aligner: GoalAligner | None = None,
        tracker: HabitTracker | None = None,
        recommender: RecommendationEngine | None = None,
    ) -> None:
        self._export_dir = export_dir or DEFAULT_EXPORT_DIR
        self._analytics = analytics or learning_analytics
        self._aligner = aligner or goal_aligner
        self._tracker = tracker or habit_tracker
        self._recommender = recommender or recommendation_engine

    def export_report(
        self,
        format: str = "json",
        weeks: int = 12,
        granularity: str = "week",
    ) -> dict[str, Any]:
        """Build a progress report and persist it as JSON or HTML."""
        if format not in EXPORT_FORMATS:
            raise ValueError(f"Unsupported export format: {format}")
        report = self.build_report(weeks=weeks, granularity=granularity)
        if format == "json":
            content = self.render_json(report)
            filename = f"progress-report-{_stamp()}.json"
        else:
            content = self.render_html(report)
            filename = f"progress-report-{_stamp()}.html"
        path = self._write(filename, content)
        return {
            "format": format,
            "filename": filename,
            "path": str(path),
            "generated_at": report["generated_at"],
            "summary": report["summary"],
            "content": content,
        }

    def build_report(
        self, weeks: int = 12, granularity: str = "week"
    ) -> dict[str, Any]:
        """Assemble the full progress report payload."""
        snapshot = self._analytics.snapshot(granularity, weeks)
        goals = self._aligner.list_goals()
        habits = self._tracker.all_statuses()
        reminders = self._tracker.due_reminders()
        drift = self._tracker.goal_drift_alerts()
        recommendations = self._recommender.recommend(limit=5)
        return {
            "generated_at": datetime.now(UTC).isoformat(),
            "summary": {
                "total_activities": snapshot.total_activities,
                "total_projects": snapshot.total_projects,
                "total_hours": round(snapshot.total_minutes / 60.0, 2),
                "active_skills": snapshot.active_skills,
                "current_streak_weeks": snapshot.current_streak_weeks,
                "alignment_rate": round(snapshot.alignment_rate, 2),
                "aligned_activities": snapshot.aligned_activities,
                "unaligned_activities": snapshot.unaligned_activities,
                "open_goals": len(goals),
                "active_habits": len(habits),
                "due_reminders": len(reminders),
                "goal_drift_alerts": len(drift),
            },
            "progress": {
                "buckets": [
                    {
                        "period": b.period,
                        "activities": b.activities,
                        "projects_completed": b.projects_completed,
                        "minutes_spent": round(b.minutes_spent, 1),
                        "new_skills": b.new_skills,
                    }
                    for b in snapshot.buckets
                ],
                "skills": [
                    {
                        "skill": s.skill,
                        "level": s.level,
                        "activities": s.activities,
                        "projects_completed": s.projects_completed,
                        "minutes_spent": round(s.minutes_spent, 1),
                        "last_practiced": (
                            s.last_practiced.isoformat() if s.last_practiced else None
                        ),
                    }
                    for s in snapshot.skills
                ],
                "series": self._analytics.series(granularity, weeks),
            },
            "goals": [_goal_payload(g, self._aligner) for g in goals],
            "habits": habits,
            "alerts": {
                "reminders": [_alert_payload(a) for a in reminders],
                "goal_drift": [_alert_payload(a) for a in drift],
            },
            "recommendations": [
                {
                    "id": r.id,
                    "kind": r.kind,
                    "title": r.title,
                    "rationale": r.rationale,
                    "skills_gained": r.skills_gained,
                    "difficulty": r.difficulty,
                    "estimated_hours": r.estimated_hours,
                    "confidence": round(r.confidence, 2),
                }
                for r in recommendations
            ],
        }

    def render_json(self, report: dict[str, Any]) -> str:
        return json.dumps(report, indent=2, default=str)

    def render_html(self, report: dict[str, Any]) -> str:
        summary = report["summary"]
        esc = html.escape
        skills_rows = "\n".join(
            "<tr>"
            f"<td>{esc(str(s['skill']))}</td>"
            f"<td>{esc(str(s['level']))}</td>"
            f"<td>{s['activities']}</td>"
            f"<td>{s['projects_completed']}</td>"
            f"<td>{s['minutes_spent']:.1f}</td>"
            "</tr>"
            for s in report["progress"]["skills"]
        )
        bucket_rows = "\n".join(
            "<tr>"
            f"<td>{esc(str(b['period']))}</td>"
            f"<td>{b['activities']}</td>"
            f"<td>{b['projects_completed']}</td>"
            f"<td>{b['minutes_spent']:.1f}</td>"
            f"<td>{esc(', '.join(b['new_skills']))}</td>"
            "</tr>"
            for b in report["progress"]["buckets"]
        )
        goal_items = "\n".join(
            "<li>"
            f"<strong>{esc(g['title'])}</strong> ({esc(g['kind'])}) — "
            f"progress {g['progress']:.0f}%"
            "</li>"
            for g in report["goals"]
        ) or "<li>No goals registered yet.</li>"
        habit_items = "\n".join(
            "<li>"
            f"<strong>{esc(h['name'])}</strong> — streak {h['current_streak']}, "
            f"{h['period_check_ins']}/{h['target_per_period']} this period"
            + (" <em>(at risk)</em>" if h["at_risk"] else "")
            + "</li>"
            for h in report["habits"]
        ) or "<li>No habits registered yet.</li>"
        rec_items = "\n".join(
            "<li>"
            f"<strong>{esc(r['title'])}</strong> ({esc(r['kind'])}) — "
            f"{esc(r['rationale'])}"
            "</li>"
            for r in report["recommendations"]
        ) or "<li>No recommendations available.</li>"
        cards = "\n".join(
            _summary_card(value, label)
            for value, label in _summary_cards(summary)
        )
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Self Development Progress Report</title>
<style>
  body {{ font-family: system-ui, -apple-system, sans-serif; margin: 2rem auto;
         max-width: 900px; color: #1a1a1a; line-height: 1.5; }}
  h1 {{ border-bottom: 2px solid #2563eb; padding-bottom: .5rem; }}
  h2 {{ color: #2563eb; margin-top: 2rem; }}
  .cards {{ display: flex; flex-wrap: wrap; gap: 1rem; }}
  .card {{ background: #f1f5f9; border-radius: 8px; padding: 1rem 1.5rem;
          min-width: 140px; }}
  .card .value {{ font-size: 1.6rem; font-weight: 700; }}
  .card .label {{ color: #64748b; font-size: .85rem; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #e2e8f0; padding: .5rem .75rem; text-align: left; }}
  th {{ background: #f8fafc; }}
  .meta {{ color: #64748b; font-size: .85rem; }}
</style>
</head>
<body>
<h1>Self Development Progress Report</h1>
<p class="meta">Generated {esc(report["generated_at"])}</p>

<h2>Summary</h2>
<div class="cards">
{cards}
</div>

<h2>Weekly Progress</h2>
<table>
  <thead>{_table_header(["Period", "Activities", "Projects", "Minutes", "New skills"])}</thead>
  <tbody>{bucket_rows}</tbody>
</table>

<h2>Skill Progress</h2>
<table>
  <thead>{_table_header(["Skill", "Level", "Activities", "Projects", "Minutes"])}</thead>
  <tbody>{skills_rows}</tbody>
</table>

<h2>Goals</h2>
<ul>{goal_items}</ul>

<h2>Habits</h2>
<ul>{habit_items}</ul>

<h2>Recommendations</h2>
<ul>{rec_items}</ul>

</body>
</html>"""

    def _write(self, filename: str, content: str) -> Path:
        self._export_dir.mkdir(parents=True, exist_ok=True)
        path = self._export_dir / filename
        path.write_text(content, encoding="utf-8")
        return path


def _stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%d-%H%M%S")


def _summary_cards(summary: dict[str, Any]) -> list[tuple[Any, str]]:
    """Summary metric value/label pairs rendered as HTML cards."""
    return [
        (summary["total_activities"], "Activities"),
        (summary["total_projects"], "Projects"),
        (f"{summary['total_hours']:.1f}", "Hours"),
        (summary["active_skills"], "Active skills"),
        (summary["current_streak_weeks"], "Week streak"),
        (f"{summary['alignment_rate']:.0%}", "Goal alignment"),
        (summary["open_goals"], "Goals"),
        (summary["active_habits"], "Habits"),
        (summary["due_reminders"], "Due reminders"),
        (summary["goal_drift_alerts"], "Goal drift alerts"),
    ]


def _summary_card(value: Any, label: str) -> str:
    return (
        f'  <div class="card"><div class="value">{value}</div>'
        f'<div class="label">{html.escape(label)}</div></div>'
    )


def _table_header(columns: list[str]) -> str:
    cells = "".join(f"<th>{html.escape(c)}</th>" for c in columns)
    return f"<tr>{cells}</tr>"


def _goal_payload(goal: Any, aligner: GoalAligner) -> dict[str, Any]:
    progress = aligner.goal_progress(goal.id)
    return {
        "id": goal.id,
        "title": goal.title,
        "kind": goal.kind,
        "target_skills": goal.target_skills,
        "success_criteria": goal.success_criteria,
        "target_date": goal.target_date,
        "progress": round(goal.progress, 2),
        "source": goal.source,
        "core_goal_id": goal.core_goal_id,
        "coverage": progress,
    }


def _alert_payload(alert: Any) -> dict[str, Any]:
    return {
        "id": alert.id,
        "alert_type": alert.alert_type,
        "severity": alert.severity,
        "subject": alert.subject,
        "message": alert.message,
        "created_at": (
            alert.created_at.isoformat()
            if hasattr(alert, "created_at") and alert.created_at
            else None
        ),
        "metadata": getattr(alert, "metadata", {}) or {},
    }


export_service = ExportService()
