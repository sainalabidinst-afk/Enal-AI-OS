"""
Self Development API Endpoints
==============================

Growth engine endpoints:
- GET  /api/v1/self-development/report        — Combined growth report
- GET  /api/v1/self-development/progress       — Learning analytics snapshot
- GET  /api/v1/self-development/progress/chart — ASCII chart + chart series
- POST /api/v1/self-development/activities     — Record a learning activity
- GET  /api/v1/self-development/activities     — List recorded activities
- GET  /api/v1/self-development/goals          — List development goals
- POST /api/v1/self-development/goals          — Register a development goal
- GET  /api/v1/self-development/goals/progress — Goal coverage and hours
- POST /api/v1/self-development/goals/validate — Activity-goal relevance check
- POST /api/v1/self-development/goals/align    — Re-align all activities
- GET  /api/v1/self-development/recommendations — Next project/skill suggestions
- GET  /api/v1/self-development/habits         — Habit streaks and reminders
- POST /api/v1/self-development/habits         — Create a habit
- POST /api/v1/self-development/habits/{id}/check-in — Habit check-in
- GET  /api/v1/self-development/habits/reminders — Due habit reminders
- POST /api/v1/self-development/alerts/dispatch — Publish growth alerts
- GET  /api/v1/self-development/learning-projects — Cross-pack project catalog
- POST /api/v1/self-development/learning-projects/{id}/run — Run a learning project
"""

from datetime import datetime
from typing import Any

from apps.self_development.worker import self_development_worker
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/self-development", tags=["self-development"])


class ActivityRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    kind: str = Field(
        default="project", description="project | study | habit | certification | research"
    )
    duration_minutes: float = Field(default=0.0, ge=0.0, le=100000.0)
    skills: list[str] = Field(default_factory=list)
    goal_id: str | None = None
    source_pack: str | None = None
    completed_at: datetime | None = None
    notes: str = ""


class GoalRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    kind: str = Field(
        default="milestone", description="milestone | certification | portfolio | career"
    )
    target_skills: list[str] = Field(default_factory=list)
    success_criteria: list[str] = Field(default_factory=list)
    target_date: str | None = None
    core_goal_id: str | None = Field(
        default=None, description="Mirror an existing Goal Management goal id"
    )


class RelevanceRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    skills: list[str] = Field(default_factory=list)
    goal_id: str | None = None


class HabitRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    cadence: str = Field(default="daily", description="daily | weekly")
    target_per_period: int = Field(default=1, ge=1, le=50)
    goal_id: str | None = None
    reminder_hour: int = Field(default=9, ge=0, le=23)


class CheckInRequest(BaseModel):
    note: str = ""
    completed_at: datetime | None = None


class RunProjectRequest(BaseModel):
    params: dict[str, Any] = Field(default_factory=dict)
    duration_minutes: float = Field(default=60.0, ge=0.0, le=100000.0)
    goal_id: str | None = None
    notes: str = ""


@router.get("/report")
async def growth_report(weeks: int = Query(default=12, ge=1, le=52)):
    """Combined growth report: progress, goals, habits, and recommendations."""
    return {
        "progress": await self_development_worker.get_progress("week", weeks),
        "goals": await self_development_worker.list_goals(),
        "habits": await self_development_worker.habit_statuses(),
        "recommendations": await self_development_worker.recommend_next(),
    }


@router.get("/progress")
async def get_progress(
    granularity: str = Query(default="week", pattern="^(week|month)$"),
    weeks: int = Query(default=12, ge=1, le=52),
):
    """Learning analytics snapshot with week/month buckets and skill levels."""
    return await self_development_worker.get_progress(granularity, weeks)


@router.get("/progress/chart")
async def get_progress_chart(
    granularity: str = Query(default="week", pattern="^(week|month)$"),
    weeks: int = Query(default=12, ge=1, le=52),
    metric: str = Query(default="hours", pattern="^(hours|projects|skills)$"),
):
    """Console-friendly progress chart plus a chart series for the frontend."""
    return await self_development_worker.render_progress_chart(granularity, weeks, metric)


@router.get("/activities")
async def list_activities(
    kind: str | None = None,
    skill: str | None = None,
    goal_id: str | None = None,
):
    """List recorded learning activities."""
    from apps.self_development.growth_repository import activity_payload
    from apps.self_development.learning_analytics import learning_analytics

    activities = learning_analytics.list_activities(kind=kind, skill=skill, goal_id=goal_id)
    return {
        "count": len(activities),
        "activities": [activity_payload(a) for a in activities],
    }


@router.post("/activities")
async def record_activity(req: ActivityRequest):
    """Record a learning activity and validate it against development goals."""
    return await self_development_worker.record_activity(**req.model_dump())


@router.get("/goals")
async def list_goals():
    """List development goals (certification, portfolio, milestone) with progress."""
    return await self_development_worker.list_goals()


@router.post("/goals")
async def create_goal(req: GoalRequest):
    """Register a long-term development goal."""
    return await self_development_worker.create_goal(**req.model_dump())


@router.get("/goals/progress")
async def goals_progress():
    """Per-goal coverage, invested hours, and missing skills."""
    payload = await self_development_worker.list_goals()
    return {"progress": payload["progress"]}


@router.post("/goals/validate")
async def validate_relevance(req: RelevanceRequest):
    """Validate whether a planned activity is relevant to a development goal."""
    return await self_development_worker.validate_relevance(req.title, req.skills, req.goal_id)


@router.post("/goals/align")
async def align_goals():
    """Re-align every stored activity against the registered goals."""
    return await self_development_worker.align_goals()


@router.get("/recommendations")
async def recommendations(
    limit: int = Query(default=5, ge=1, le=20),
    goal_id: str | None = None,
):
    """Next project or skill recommendations from progress, goals, and knowledge."""
    return await self_development_worker.recommend_next(limit, goal_id)


@router.get("/habits")
async def list_habits():
    """Habit streaks, period progress, and open reminders."""
    return await self_development_worker.habit_statuses()


@router.post("/habits")
async def create_habit(req: HabitRequest):
    """Create a recurring learning habit."""
    try:
        return await self_development_worker.create_habit(**req.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/habits/reminders")
async def habit_reminders():
    """Due habit reminders for habits whose current period is not satisfied."""
    payload = await self_development_worker.habit_statuses()
    return {"reminders": payload["reminders"]}


@router.post("/habits/{habit_id}/check-in")
async def check_in_habit(habit_id: str, req: CheckInRequest):
    """Check in to a habit and return the updated streak status."""
    try:
        return await self_development_worker.check_in_habit(habit_id, req.note, req.completed_at)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/alerts/dispatch")
async def dispatch_alerts():
    """Evaluate habit and goal alerts and publish them on the event bus."""
    return await self_development_worker.dispatch_growth_alerts()


@router.get("/learning-projects")
async def learning_projects(goal_id: str | None = None):
    """Catalog of real projects run through other packs but counted as learning."""
    return await self_development_worker.learning_projects(goal_id)


@router.post("/learning-projects/{project_id}/run")
async def run_learning_project(project_id: str, req: RunProjectRequest):
    """Run a learning project through its capability pack and record the progress."""
    try:
        return await self_development_worker.run_learning_project(
            project_id,
            req.params,
            req.duration_minutes,
            req.goal_id,
            req.notes,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
