import pytest

from backend.app.core.goal_engine import AutonomousGoalEngine, Goal


class TestGoal:
    def test_defaults(self):
        goal = Goal(id="g1", description="desc", success_criteria=["c1"])
        assert goal.constraints == []
        assert goal.status == "active"
        assert goal.progress == 0.0
        assert goal.iterations == 0
        assert goal.max_iterations == 10
        assert goal.project_id is None
        assert goal.metadata == {}

    def test_custom_values(self):
        goal = Goal(id="g1", description="desc", success_criteria=["c1"], constraints=["c2"], max_iterations=5, project_id="p1")
        assert goal.constraints == ["c2"]
        assert goal.max_iterations == 5
        assert goal.project_id == "p1"


class TestAutonomousGoalEngine:
    @pytest.fixture
    def engine(self, monkeypatch):
        import backend.app.core.goal_engine as ge_module
        import backend.app.core.task_queue as tq_module
        import backend.app.core.state_recovery as sr_module
        import backend.app.core.event_bus as eb_module

        fake_tasks = {}
        fake_task_counter = [0]

        class FakeTaskQueue:
            async def enqueue(self, task):
                fake_task_counter[0] += 1
                task_id = f"task-{fake_task_counter[0]}"
                fake_tasks[task_id] = task
                return task_id

            async def get_task(self, task_id):
                task = fake_tasks.get(task_id)
                if task:
                    task.status = type("Status", (), {"value": "completed"})()
                    task.result = "done"
                return task

        async def fake_save(*args, **kwargs):
            return None

        monkeypatch.setattr(ge_module, "task_queue", FakeTaskQueue())
        monkeypatch.setattr(ge_module, "state_recovery", type("SR", (), {"save": fake_save})())
        monkeypatch.setattr(ge_module, "event_bus", type("Bus", (), {
            "subscribe": lambda *a, **k: None,
        })())
        engine = AutonomousGoalEngine()
        return engine

    async def test_create_goal_returns_goal(self, engine):
        goal = await engine.create_goal("test goal", ["criterion 1"], project_id="p1")
        assert goal.description == "test goal"
        assert goal.success_criteria == ["criterion 1"]
        assert goal.project_id == "p1"
        assert goal.id in engine._goals

    async def test_create_goal_generates_unique_id(self, engine):
        from unittest.mock import patch
        import backend.app.core.goal_engine as ge_module
        from datetime import datetime, UTC

        with patch.object(ge_module, "datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
            mock_dt.UTC = UTC
            goal1 = await engine.create_goal("goal1", ["c1"])
            mock_dt.now.return_value = datetime(2024, 1, 1, 12, 0, 1, tzinfo=UTC)
            goal2 = await engine.create_goal("goal2", ["c2"])
        assert goal1.id != goal2.id

    async def test_execute_completes_when_success(self, engine, monkeypatch):
        import backend.app.core.goal_engine as ge_module

        async def fake_acomplete(*args, **kwargs):
            return type("Resp", (), {"choices": [type("Choice", (), {"message": type("Message", (), {"content": '{"success": true, "progress": 100.0, "reasoning": "ok"}'})()})]})()

        monkeypatch.setattr(ge_module, "model_router", type("MR", (), {"acomplete": staticmethod(fake_acomplete)})())
        goal = await engine.create_goal("test goal", ["criterion 1"])
        result = await engine.execute(goal.id)
        assert result["status"] == "completed"
        assert result["goal_id"] == goal.id

    async def test_execute_raises_for_missing_goal(self, engine):
        with pytest.raises(ValueError):
            await engine.execute("missing")

    async def test_evaluate_progress_returns_dict(self, monkeypatch):
        import backend.app.core.goal_engine as ge_module

        async def fake_acomplete(*args, **kwargs):
            return type("Resp", (), {"choices": [type("Choice", (), {"message": type("Message", (), {"content": '{"success": true, "progress": 80.0, "reasoning": "ok"}'})()})]})()

        monkeypatch.setattr(ge_module, "model_router", type("MR", (), {"acomplete": staticmethod(fake_acomplete)})())
        engine = AutonomousGoalEngine()
        goal = Goal(id="g1", description="test", success_criteria=["c1"])
        result = await engine._evaluate_progress(goal, "result data")
        assert result["success"] is True
        assert result["progress"] == 80.0

    async def test_evaluate_progress_returns_fallback_on_bad_json(self, monkeypatch):
        import backend.app.core.goal_engine as ge_module

        async def fake_acomplete(*args, **kwargs):
            return type("Resp", (), {"choices": [type("Choice", (), {"message": type("Message", (), {"content": "not json"})()})]})()

        monkeypatch.setattr(ge_module, "model_router", type("MR", (), {"acomplete": staticmethod(fake_acomplete)})())
        engine = AutonomousGoalEngine()
        goal = Goal(id="g1", description="test", success_criteria=["c1"])
        result = await engine._evaluate_progress(goal, "result data")
        assert result["success"] is False
        assert result["progress"] == 0.0

    async def test_on_task_completed(self, engine):
        event = type("Event", (), {"payload": {}})()
        await engine._on_task_completed(event)

    async def test_on_task_failed(self, engine):
        event = type("Event", (), {"payload": {}})()
        await engine._on_task_failed(event)

    def test_get_goal_returns_none_for_missing(self, engine):
        assert engine.get_goal("missing") is None

    def test_list_goals_empty(self, engine):
        assert engine.list_goals() == []

    async def test_list_goals_filters_by_project(self, engine, monkeypatch):
        import backend.app.core.goal_engine as ge_module
        from datetime import datetime, UTC

        counter = [0]
        base_ts = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC).timestamp()

        def fake_now(cls_or_self, tz=None):
            counter[0] += 1
            return datetime(2024, 1, 1, 12, 0, counter[0], tzinfo=tz or UTC)

        fake_dt = type("dt", (), {"now": staticmethod(fake_now), "UTC": UTC})()
        monkeypatch.setattr(ge_module, "datetime", fake_dt)
        goal1 = await engine.create_goal("g1", ["c1"], project_id="p1")
        goal2 = await engine.create_goal("g2", ["c2"], project_id="p2")
        goals = engine.list_goals(project_id="p1")
        assert len(goals) == 1
        assert goals[0].project_id == "p1"
