"""
Tests for the Self Development growth engine (learning analytics, goal alignment,
recommendations, habit tracking, cross-pack learning projects).

Every test runs against an isolated GrowthRepository backed by tmp_path so the
real growth.json store is never touched.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest

from apps.self_development.cross_pack_bridge import CrossPackBridge
from apps.self_development.goal_aligner import GoalAligner
from apps.self_development.growth_repository import GrowthRepository
from apps.self_development.habit_tracker import HabitTracker
from apps.self_development.learning_analytics import LearningAnalytics
from apps.self_development.recommendation_engine import RecommendationEngine
from apps.self_development.schemas import (
    ActivityKind,
    GoalVerdict,
    Granularity,
    HabitCadence,
    SkillLevel,
)

NOW = datetime(2026, 3, 2, 10, 0, tzinfo=UTC)


@pytest.fixture
def repo(tmp_path: Path) -> GrowthRepository:
    return GrowthRepository(storage_path=tmp_path / "growth.json")


@pytest.fixture
def analytics(repo: GrowthRepository) -> LearningAnalytics:
    return LearningAnalytics(repository=repo)


@pytest.fixture
def aligner(repo: GrowthRepository) -> GoalAligner:
    return GoalAligner(repository=repo)


@pytest.fixture
def habits(repo: GrowthRepository) -> HabitTracker:
    return HabitTracker(repository=repo)


@pytest.fixture
def recommender(repo: GrowthRepository, aligner) -> RecommendationEngine:
    return RecommendationEngine(repository=repo, aligner=aligner)


# ---------------------------------------------------------------------------
# Learning Analytics
# ---------------------------------------------------------------------------


class TestLearningAnalytics:
    def test_record_activity_normalizes_duration(self, analytics: LearningAnalytics) -> None:
        activity = analytics.record_activity("Study", duration_minutes=-30)
        assert activity.duration_minutes == 0.0

    def test_week_buckets_group_activities(self, analytics: LearningAnalytics) -> None:
        analytics.record_activity(
            "Project A", duration_minutes=60, skills=["python"], completed_at=NOW
        )
        analytics.record_activity(
            "Project B", duration_minutes=30, skills=["sql"], completed_at=NOW + timedelta(days=2)
        )
        buckets = analytics.bucket(Granularity.WEEK.value)
        assert len(buckets) == 1
        assert buckets[0].activities == 2
        assert buckets[0].projects_completed == 2
        assert buckets[0].minutes_spent == 90.0
        assert sorted(buckets[0].new_skills) == ["python", "sql"]

    def test_month_bucket_splits_weeks(self, analytics: LearningAnalytics) -> None:
        analytics.record_activity(
            "Project A", duration_minutes=60, completed_at=datetime(2026, 3, 2, tzinfo=UTC)
        )
        analytics.record_activity(
            "Project B", duration_minutes=60, completed_at=datetime(2026, 4, 2, tzinfo=UTC)
        )
        buckets = analytics.bucket(Granularity.MONTH.value)
        assert [b.period for b in buckets] == ["2026-03", "2026-04"]

    def test_bucket_rejects_unknown_granularity(self, analytics: LearningAnalytics) -> None:
        with pytest.raises(ValueError, match="Unsupported granularity"):
            analytics.bucket("decade")

    def test_week_gaps_are_filled(self, analytics: LearningAnalytics) -> None:
        analytics.record_activity(
            "Old", duration_minutes=30, completed_at=datetime(2026, 1, 5, tzinfo=UTC)
        )
        analytics.record_activity(
            "New", duration_minutes=30, completed_at=datetime(2026, 3, 2, tzinfo=UTC)
        )
        buckets = analytics.bucket(Granularity.WEEK.value)
        assert len(buckets) > 2
        assert any(b.activities == 0 for b in buckets)

    def test_skill_progress_derives_level(self, analytics: LearningAnalytics) -> None:
        for i in range(6):
            analytics.record_activity(f"Python project {i}", duration_minutes=45, skills=["python"])
        skills = {s.skill: s for s in analytics.skill_progress()}
        assert skills["python"].level == SkillLevel.INTERMEDIATE.value
        assert skills["python"].projects_completed == 6
        assert skills["python"].minutes_spent == 270.0

    def test_study_kind_is_not_counted_as_project(self, analytics: LearningAnalytics) -> None:
        analytics.record_activity(
            "Read docs", kind=ActivityKind.STUDY.value, duration_minutes=30, skills=["python"]
        )
        snapshot = analytics.snapshot()
        assert snapshot.total_projects == 0
        assert snapshot.total_activities == 1

    def test_snapshot_reports_streak_and_alignment(self, analytics: LearningAnalytics) -> None:
        analytics.record_activity(
            "This week", duration_minutes=60, skills=["python"], completed_at=NOW
        )
        snapshot = analytics.snapshot()
        assert snapshot.current_streak_weeks >= 0
        assert snapshot.alignment_rate == 0.0

    def test_weekly_hours_and_sparkline(self, analytics: LearningAnalytics) -> None:
        analytics.record_activity("Now", duration_minutes=120, completed_at=NOW)
        assert analytics.weekly_hours(weeks=4)[-1] == 2.0
        assert analytics.render_sparkline(weeks=4).endswith("@")

    def test_render_chart_handles_empty_state(self, analytics: LearningAnalytics) -> None:
        assert analytics.render_chart() == "No learning activity recorded yet."

    def test_render_chart_supports_metrics(self, analytics: LearningAnalytics) -> None:
        analytics.record_activity(
            "Project", duration_minutes=60, skills=["python"], completed_at=NOW
        )
        assert "projects" in analytics.render_chart(metric="projects")
        assert "new skills" in analytics.render_chart(metric="skills")

    def test_series_payload(self, analytics: LearningAnalytics) -> None:
        analytics.record_activity(
            "Project", duration_minutes=60, skills=["python"], completed_at=NOW
        )
        series = analytics.series()
        assert series["granularity"] == "week"
        assert series["hours"][-1] == 1.0
        assert series["projects"][-1] == 1
        assert series["new_skills"][-1] == 1


# ---------------------------------------------------------------------------
# Goal Alignment
# ---------------------------------------------------------------------------


class TestGoalAligner:
    def test_aligned_activity_scores_high(self, aligner) -> None:
        goal = aligner.create_goal(
            title="Sertifikasi Python Data Analyst",
            kind="certification",
            target_skills=["python", "data-analysis"],
        )
        alignment = aligner.align(
            "Belajar python data analysis untuk sertifikasi",
            ["python", "data-analysis"],
            goal.id,
        )
        assert alignment.verdict == GoalVerdict.ALIGNED.value
        assert alignment.goal_title == goal.title
        assert "python" in alignment.matched_terms

    def test_partially_covered_activity_scores_partial(self, aligner) -> None:
        goal = aligner.create_goal(
            title="Sertifikasi Python Data Analyst",
            kind="certification",
            target_skills=["python", "data-analysis"],
        )
        alignment = aligner.align("Belajar python untuk sertifikasi", ["python"], goal.id)
        assert alignment.verdict == GoalVerdict.PARTIAL.value
        assert alignment.suggestions

    def test_unrelated_activity_is_flagged_with_suggestion(self, aligner) -> None:
        goal = aligner.create_goal(title="Sertifikasi Python", target_skills=["python", "sql"])
        alignment = aligner.align("Bermain gitar", ["music"], goal.id)
        assert alignment.verdict == GoalVerdict.UNRELATED.value
        assert alignment.suggestions

    def test_align_without_goals_returns_guidance(self, aligner) -> None:
        alignment = aligner.align("Project apa saja", ["python"])
        assert alignment.goal_id is None
        assert alignment.suggestions

    def test_unknown_goal_id_is_handled(self, aligner) -> None:
        alignment = aligner.align("Project", ["python"], "goal-does-not-exist")
        assert alignment.verdict == GoalVerdict.UNRELATED.value

    def test_validate_relevance_payload(self, aligner) -> None:
        goal = aligner.create_goal(title="Portofolio Arsitektur", target_skills=["ddd"])
        result = aligner.validate_relevance("Refactor bounded context", ["ddd"], goal.id)
        assert result["is_relevant"] is True
        assert result["goal_id"] == goal.id

    def test_goal_progress_tracks_coverage(self, aligner, analytics) -> None:
        goal = aligner.create_goal(
            title="Data Engineer",
            target_skills=["python", "sql", "etl"],
            success_criteria=["Sertifikasi Data Engineering"],
        )
        activity = analytics.record_activity("ETL pipeline", skills=["python", "sql"])
        aligner.record_activity_alignment(activity)
        progress = aligner.goal_progress(goal.id)
        assert progress["found"] is True
        assert progress["skill_coverage"] == pytest.approx(0.67, abs=0.01)
        assert progress["missing_skills"] == ["etl"]

    def test_goal_progress_unknown_goal(self, aligner) -> None:
        assert aligner.goal_progress("nope")["found"] is False

    def test_mirrors_core_goals(self, aligner) -> None:
        from backend.app.core.goal_engine import Goal, goal_engine

        core_goal = Goal(
            id="goal-core-1",
            description="Become a certified data analyst",
            success_criteria=["pass exam"],
        )
        goal_engine._goals[core_goal.id] = core_goal
        try:
            titles = [g.title for g in aligner.list_goals()]
            assert "Become a certified data analyst" in titles
            assert aligner.resolve_goal("goal-core-1") is not None
        finally:
            goal_engine._goals.pop(core_goal.id, None)

    def test_link_habits_to_goals(self, aligner, habits) -> None:
        goal = aligner.create_goal(title="Belajar python tiap hari", target_skills=["python"])
        habit = habits.create_habit(name="Latihan python", goal_id=goal.id)
        report = aligner.link_habits_to_goals()
        entry = next(r for r in report if r["habit_id"] == habit.id)
        assert entry["goal_id"] == goal.id


# ---------------------------------------------------------------------------
# Recommendation Engine
# ---------------------------------------------------------------------------


class TestRecommendationEngine:
    def test_no_recommendations_without_progress(self, recommender: RecommendationEngine) -> None:
        assert recommender.recommend() == []

    def test_ladder_unlocks_after_threshold(
        self, recommender: RecommendationEngine, analytics: LearningAnalytics
    ) -> None:
        for i in range(3):
            analytics.record_activity(f"Python project {i}", skills=["python"])
        titles = [r.title for r in recommender.recommend()]
        assert any("Data Engineering" in title for title in titles)

    def test_ladder_explains_state(
        self, recommender: RecommendationEngine, analytics: LearningAnalytics
    ) -> None:
        analytics.record_activity("Python project", skills=["python"])
        state = recommender.explain()
        python_step = next(s for s in state["ladder"] if s["skill"] == "python")
        assert python_step["current_projects"] == 1
        assert python_step["unlocked"] is False

    def test_goal_gap_recommendation(self, recommender: RecommendationEngine, aligner) -> None:
        goal = aligner.create_goal(
            title="Sertifikasi Kubernetes", target_skills=["kubernetes", "helm"]
        )
        titles = [r.title for r in recommender.recommend(goal_id=goal.id)]
        assert any("Sertifikasi Kubernetes" in title for title in titles)

    def test_knowledge_signal_is_merged(
        self, recommender: RecommendationEngine, analytics: LearningAnalytics
    ) -> None:
        from backend.app.core.knowledge.learning import LearningEngine

        learning = LearningEngine()
        learning.record_success(
            domain="self-development",
            context={},
            action_taken="bangun ETL",
            outcome="berhasil",
            confidence=0.9,
        )
        analytics.record_activity("ETL practice", skills=["python"])
        recommender.set_learning_engine(learning)
        sources = {r.source for r in recommender.recommend()}
        assert "knowledge" in sources

    def test_broken_learning_engine_is_tolerated(self, recommender: RecommendationEngine) -> None:
        class _Broken:
            def recommend(self, domain: str, context: dict[str, Any]):
                raise RuntimeError("offline")

        recommender.set_learning_engine(_Broken())
        assert recommender.recommend() == []


# ---------------------------------------------------------------------------
# Habit Tracker
# ---------------------------------------------------------------------------


class TestHabitTracker:
    def test_create_habit_validates_cadence(self, habits: HabitTracker) -> None:
        with pytest.raises(ValueError, match="Unsupported cadence"):
            habits.create_habit("Read", cadence="hourly")

    def test_create_habit_validates_target(self, habits: HabitTracker) -> None:
        with pytest.raises(ValueError, match="target_per_period"):
            habits.create_habit("Read", target_per_period=0)

    def test_daily_streak_increments(self, habits: HabitTracker) -> None:
        habit = habits.create_habit("Read 20 minutes", cadence=HabitCadence.DAILY.value)
        first = habits.check_in(habit.id, checked_at=NOW)
        second = habits.check_in(habit.id, checked_at=NOW + timedelta(days=1))
        assert first["current_streak"] == 1
        assert second["current_streak"] == 2
        assert second["longest_streak"] == 2

    def test_streak_resets_after_gap(self, habits: HabitTracker) -> None:
        habit = habits.create_habit("Read 20 minutes", cadence=HabitCadence.DAILY.value)
        habits.check_in(habit.id, checked_at=NOW)
        habits.check_in(habit.id, checked_at=NOW + timedelta(days=3))
        status = habits.status(habit.id, now=NOW + timedelta(days=3))
        assert status.current_streak == 1
        assert status.longest_streak == 1

    def test_duplicate_check_in_same_period_is_idempotent(self, habits: HabitTracker) -> None:
        habit = habits.create_habit("Read", cadence=HabitCadence.DAILY.value)
        habits.check_in(habit.id, checked_at=NOW)
        habits.check_in(habit.id, checked_at=NOW + timedelta(hours=2))
        status = habits.status(habit.id, now=NOW)
        assert status.period_check_ins == 1

    def test_weekly_target(self, habits: HabitTracker) -> None:
        habit = habits.create_habit(
            "Review", cadence=HabitCadence.WEEKLY.value, target_per_period=3
        )
        payload = habits.check_in(habit.id, checked_at=NOW)
        assert payload["target_met"] is False
        assert payload["period_check_ins"] == 1

    def test_unknown_habit_raises(self, habits: HabitTracker) -> None:
        with pytest.raises(KeyError):
            habits.status("habit-missing")

    def test_reminders_only_for_unmet_targets(self, habits: HabitTracker) -> None:
        habit = habits.create_habit("Read", cadence=HabitCadence.DAILY.value)
        assert len(habits.due_reminders(now=NOW)) == 1
        habits.check_in(habit.id, checked_at=NOW)
        assert habits.due_reminders(now=NOW) == []

    def test_goal_drift_alerts(self, habits: HabitTracker, repo: GrowthRepository) -> None:
        from apps.self_development.schemas import LearningActivity

        repo.add_activity(
            LearningActivity(
                id="act-1",
                title="Unrelated activity",
                kind="project",
                duration_minutes=30,
                skills=["music"],
                goal_verdict=GoalVerdict.UNRELATED.value,
            )
        )
        alerts = habits.goal_drift_alerts()
        assert len(alerts) == 1
        assert alerts[0].alert_type == "goal_drift"

    def test_at_risk_when_period_missed(self, habits: HabitTracker) -> None:
        habit = habits.create_habit("Read", cadence=HabitCadence.DAILY.value)
        habits.check_in(habit.id, checked_at=NOW)
        status = habits.status(habit.id, now=NOW + timedelta(days=1))
        assert status.at_risk is True

    def test_delete_habit(self, habits: HabitTracker) -> None:
        habit = habits.create_habit("Read")
        assert habits.delete_habit(habit.id) is True
        assert habits.delete_habit(habit.id) is False

    def test_dispatch_publishes_events(self, habits: HabitTracker) -> None:
        published: list[str] = []

        async def fake_publish(event_type: str, subject: str, message: str, payload: dict):
            published.append(event_type)
            return True

        habits._publish = fake_publish  # type: ignore[method-assign]
        habits.create_habit("Read", cadence=HabitCadence.DAILY.value)
        result = asyncio.run(habits.dispatch_alerts(now=NOW))
        assert result[0]["published"] is True
        assert "self_development.habit.reminder" in published

    def test_evaluate_alerts_caches_result(self, habits: HabitTracker) -> None:
        habits.create_habit("Read", cadence=HabitCadence.DAILY.value)
        alerts = habits.evaluate_alerts(now=NOW)
        assert len(habits.list_alerts()) == len(alerts)
        habits.clear_alerts()
        assert habits.list_alerts() == []


# ---------------------------------------------------------------------------
# Cross-Pack Bridge
# ---------------------------------------------------------------------------


class TestCrossPackBridge:
    @pytest.fixture
    def bridge(self, analytics: LearningAnalytics, aligner) -> CrossPackBridge:
        return CrossPackBridge(analytics=analytics, aligner=aligner)

    def test_catalog_lists_cross_pack_projects(self, bridge: CrossPackBridge) -> None:
        ids = {p["id"] for p in bridge.catalog()}
        assert {"trading-backtest", "architecture-review", "data-pipeline-etl"} <= ids

    def test_catalog_can_score_against_goal(self, bridge: CrossPackBridge, aligner) -> None:
        goal = aligner.create_goal(
            title="Keahlian kuantitatif", target_skills=["statistics", "backtesting"]
        )
        entries = {p["id"]: p for p in bridge.catalog(goal_id=goal.id)}
        assert entries["trading-backtest"]["goal_verdict"] == GoalVerdict.ALIGNED.value

    def test_unknown_project_raises(self, bridge: CrossPackBridge) -> None:
        with pytest.raises(KeyError):
            asyncio.run(bridge.run("does-not-exist"))

    def test_run_records_activity_even_when_pack_input_missing(
        self, bridge: CrossPackBridge, analytics: LearningAnalytics
    ) -> None:
        result = asyncio.run(bridge.run("trading-backtest", params={}, duration_minutes=30))
        assert result["status"] == "completed"
        assert result["result"]["status"] == "skipped"
        assert analytics.list_activities()[0].source_pack == "trading-analyst"

    def test_run_delegates_to_knowledge_engineer(
        self, bridge: CrossPackBridge, analytics: LearningAnalytics
    ) -> None:
        result = asyncio.run(
            bridge.run("knowledge-graph", params={"domain": "learning"}, duration_minutes=45)
        )
        assert result["result"]["status"] == "executed"
        assert result["result"]["ontology_classes"] >= 1
        activity = analytics.list_activities()[0]
        assert activity.kind == ActivityKind.CROSS_PACK.value
        assert activity.metadata["learning_project_id"] == "knowledge-graph"

    def test_run_captures_pack_failure(self, bridge: CrossPackBridge) -> None:
        result = asyncio.run(
            bridge.run("architecture-review", params={"workspace_path": "does/not/exist"})
        )
        assert result["result"]["status"] in {"failed", "skipped"}


# ---------------------------------------------------------------------------
# Engine integration
# ---------------------------------------------------------------------------


class TestEngineIntegration:
    @pytest.fixture
    def engine(self, monkeypatch, analytics: LearningAnalytics, aligner, habits, tmp_path):
        from apps.self_development import engine as engine_module
        from apps.self_development.cross_pack_bridge import cross_pack_bridge as shared_bridge

        repo = GrowthRepository(storage_path=tmp_path / "engine.json")
        test_analytics = LearningAnalytics(repository=repo)
        test_aligner = GoalAligner(repository=repo)
        test_habits = HabitTracker(repository=repo)
        test_recommender = RecommendationEngine(repository=repo, aligner=test_aligner)
        instance = engine_module.SelfDevelopmentEngine()
        monkeypatch.setattr(engine_module, "learning_analytics", test_analytics)
        monkeypatch.setattr(engine_module, "goal_aligner", test_aligner)
        monkeypatch.setattr(engine_module, "habit_tracker", test_habits)
        monkeypatch.setattr(engine_module, "recommendation_engine", test_recommender)
        monkeypatch.setattr(engine_module, "cross_pack_bridge", shared_bridge)
        return instance

    def test_record_activity_returns_alignment(self, engine) -> None:
        goal = asyncio.run(engine.create_goal(title="Belajar python", target_skills=["python"]))
        payload = asyncio.run(
            engine.record_activity(
                "Latihan python", duration_minutes=30, skills=["python"], goal_id=goal["id"]
            )
        )
        assert payload["alignment"]["verdict"] == GoalVerdict.ALIGNED.value
        assert payload["activity"]["goal_id"] == goal["id"]

    def test_progress_and_chart(self, engine) -> None:
        asyncio.run(engine.record_activity("Project", duration_minutes=60, skills=["python"]))
        progress = asyncio.run(engine.get_progress())
        assert progress["total_activities"] == 1
        assert progress["total_hours"] == 1.0
        assert "Learning progress per week" in progress["chart"]
        chart = asyncio.run(engine.render_progress_chart())
        assert chart["series"]["labels"]

    def test_recommend_and_habits_flow(self, engine) -> None:
        for i in range(3):
            asyncio.run(engine.record_activity(f"Python {i}", skills=["python"]))
        recommendations = asyncio.run(engine.recommend_next())
        assert recommendations["recommendations"]
        assert recommendations["ladder"]["skill_project_counts"]["python"] == 3

        habit = asyncio.run(engine.create_habit(name="Baca", cadence="daily"))
        checked = asyncio.run(engine.check_in_habit(habit["id"]))
        assert checked["current_streak"] == 1
        assert asyncio.run(engine.habit_statuses())["habits"]
        assert asyncio.run(engine.dispatch_growth_alerts())["count"] >= 1

    def test_align_goals_and_learning_projects(self, engine) -> None:
        asyncio.run(engine.create_goal(title="Data", target_skills=["sql"]))
        asyncio.run(engine.record_activity("Latihan sql", skills=["sql"]))
        report = asyncio.run(engine.align_goals())
        assert report["activities_checked"] == 1
        assert asyncio.run(engine.learning_projects())["projects"]

    def test_app_routes_growth_requests(self, engine, monkeypatch) -> None:
        from apps.self_development import SelfDevelopmentApp

        monkeypatch.setattr("apps.self_development.self_development_engine", engine)
        app = SelfDevelopmentApp()
        assert app.is_growth_request("berapa progres belajar saya?") is True
        assert app.is_growth_request("analyze this project") is False
        result = asyncio.run(app.run("rekomendasi project berikutnya"))
        assert result["result"]["mode"] == "growth_engine"

    def test_ecp_mode_takes_precedence(self, engine, monkeypatch) -> None:
        from apps.self_development import SelfDevelopmentApp

        called: list[str] = []

        async def fake_analyze(ecp_root: str | None = None) -> dict[str, object]:
            called.append("analyze_ecp")
            return {}

        async def fake_capabilities(ecp_root: str | None = None) -> list[dict[str, object]]:
            called.append("propose_capabilities")
            return []

        async def fake_improvements(ecp_root: str | None = None) -> list[dict[str, object]]:
            called.append("propose_improvements")
            return []

        monkeypatch.setattr("apps.self_development.self_development_engine", engine)
        monkeypatch.setattr(engine, "analyze_ecp", fake_analyze)
        monkeypatch.setattr(engine, "propose_capabilities", fake_capabilities)
        monkeypatch.setattr(engine, "propose_improvements", fake_improvements)
        app = SelfDevelopmentApp()
        result = asyncio.run(app.run("cek progres ECP platform"))
        assert result["result"]["mode"] == "ecp_meta_analysis"
        assert called == ["analyze_ecp", "propose_capabilities", "propose_improvements"]


# ---------------------------------------------------------------------------
# HTTP API
# ---------------------------------------------------------------------------


class TestSelfDevelopmentApi:
    @pytest.fixture
    def client(self, monkeypatch, tmp_path):
        from fastapi.testclient import TestClient

        from apps.self_development import engine as engine_module
        from apps.self_development.cross_pack_bridge import cross_pack_bridge as shared_bridge
        from backend.app.main import app

        repo = GrowthRepository(storage_path=tmp_path / "api.json")
        test_aligner = GoalAligner(repository=repo)
        monkeypatch.setattr(engine_module, "learning_analytics", LearningAnalytics(repository=repo))
        monkeypatch.setattr(engine_module, "goal_aligner", test_aligner)
        monkeypatch.setattr(engine_module, "habit_tracker", HabitTracker(repository=repo))
        monkeypatch.setattr(
            engine_module, "recommendation_engine", RecommendationEngine(repo, test_aligner)
        )
        monkeypatch.setattr(engine_module, "cross_pack_bridge", shared_bridge)
        return TestClient(app)

    @pytest.fixture
    def headers(self, client) -> dict[str, str]:
        response = client.post(
            "/api/v1/auth/login", data={"username": "admin", "password": "secret"}
        )
        assert response.status_code == 200, f"Login failed: {response.text}"
        return {"Authorization": f"Bearer {response.json()['access_token']}"}

    def test_endpoints_require_auth(self, client) -> None:
        assert client.get("/api/v1/self-development/progress").status_code == 401

    def test_progress_and_chart_endpoints(self, client, headers) -> None:
        client.post(
            "/api/v1/self-development/goals",
            json={"title": "Belajar python", "target_skills": ["python"]},
            headers=headers,
        )
        created = client.post(
            "/api/v1/self-development/activities",
            json={
                "title": "Latihan python",
                "duration_minutes": 45,
                "skills": ["python"],
            },
            headers=headers,
        )
        assert created.status_code == 200
        assert created.json()["alignment"]["verdict"] == GoalVerdict.ALIGNED.value

        progress = client.get("/api/v1/self-development/progress?weeks=6", headers=headers)
        assert progress.status_code == 200
        assert progress.json()["total_activities"] == 1

        chart = client.get("/api/v1/self-development/progress/chart", headers=headers)
        assert chart.status_code == 200
        assert chart.json()["series"]["granularity"] == "week"

    def test_goal_validation_and_alignment_endpoints(self, client, headers) -> None:
        client.post(
            "/api/v1/self-development/goals",
            json={"title": "Sertifikasi SQL", "target_skills": ["sql"]},
            headers=headers,
        )
        validated = client.post(
            "/api/v1/self-development/goals/validate",
            json={"title": "Latihan sql", "skills": ["sql"]},
            headers=headers,
        )
        assert validated.status_code == 200
        assert validated.json()["is_relevant"] is True

        aligned = client.post("/api/v1/self-development/goals/align", headers=headers)
        assert aligned.status_code == 200
        assert "verdicts" in aligned.json()
        assert (
            client.get("/api/v1/self-development/goals/progress", headers=headers).status_code
            == 200
        )

    def test_habit_lifecycle_endpoints(self, client, headers) -> None:
        created = client.post(
            "/api/v1/self-development/habits",
            json={"name": "Baca 20 menit", "cadence": "daily"},
            headers=headers,
        )
        assert created.status_code == 200
        habit_id = created.json()["id"]

        checked = client.post(
            f"/api/v1/self-development/habits/{habit_id}/check-in",
            json={"note": "selesai"},
            headers=headers,
        )
        assert checked.status_code == 200
        assert checked.json()["current_streak"] == 1

        assert client.get("/api/v1/self-development/habits", headers=headers).status_code == 200
        assert (
            client.get("/api/v1/self-development/habits/reminders", headers=headers).status_code
            == 200
        )
        assert (
            client.post("/api/v1/self-development/alerts/dispatch", headers=headers).status_code
            == 200
        )

    def test_habit_errors(self, client, headers) -> None:
        missing = client.post(
            "/api/v1/self-development/habits/habit-missing/check-in", json={}, headers=headers
        )
        assert missing.status_code == 404
        invalid = client.post(
            "/api/v1/self-development/habits",
            json={"name": "X", "cadence": "hourly"},
            headers=headers,
        )
        assert invalid.status_code == 400

    def test_learning_project_endpoints(self, client, headers) -> None:
        catalog = client.get("/api/v1/self-development/learning-projects", headers=headers)
        assert catalog.status_code == 200
        assert catalog.json()["projects"]

        unknown = client.post(
            "/api/v1/self-development/learning-projects/nope/run", json={}, headers=headers
        )
        assert unknown.status_code == 404

        run = client.post(
            "/api/v1/self-development/learning-projects/trading-backtest/run",
            json={"params": {}, "duration_minutes": 30},
            headers=headers,
        )
        assert run.status_code == 200
        assert run.json()["status"] == "completed"

    def test_report_and_recommendations_endpoints(self, client, headers) -> None:
        for i in range(3):
            client.post(
                "/api/v1/self-development/activities",
                json={"title": f"Python project {i}", "skills": ["python"], "duration_minutes": 60},
                headers=headers,
            )
        recommendations = client.get("/api/v1/self-development/recommendations", headers=headers)
        assert recommendations.status_code == 200
        assert recommendations.json()["recommendations"]

        report = client.get("/api/v1/self-development/report", headers=headers)
        assert report.status_code == 200
        assert set(report.json()) == {"progress", "goals", "habits", "recommendations"}
