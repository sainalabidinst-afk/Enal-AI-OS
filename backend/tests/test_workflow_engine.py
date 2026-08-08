import pytest

from backend.app.core.workflow_engine import (
    Workflow,
    WorkflowEngine,
    WorkflowStep,
    WorkflowStatus,
)


class FakeEventBus:
    def __init__(self):
        self.subscribed = []
        self.published = []

    def subscribe(self, event_type, callback):
        self.subscribed.append((event_type, callback))

    async def publish(self, event):
        self.published.append(event)


class FakeEvent:
    def __init__(self, event_type, payload, source):
        self.event_type = event_type
        self.payload = payload
        self.source = source


class TestWorkflowStatus:
    def test_status_values(self):
        assert WorkflowStatus.DRAFT == "draft"
        assert WorkflowStatus.ACTIVE == "active"
        assert WorkflowStatus.RUNNING == "running"
        assert WorkflowStatus.COMPLETED == "completed"
        assert WorkflowStatus.FAILED == "failed"
        assert WorkflowStatus.CANCELLED == "cancelled"


class TestWorkflowStep:
    def test_defaults(self):
        step = WorkflowStep(id="s1", name="Step 1", agent="agent-a", action="act")
        assert step.depends_on == []
        assert step.condition is None
        assert step.retry_policy == {}
        assert step.parameters == {}


class TestWorkflow:
    def test_defaults(self):
        step = WorkflowStep(id="s1", name="Step 1", agent="agent-a", action="act")
        wf = Workflow(id="wf1", name="WF", description="desc", steps=[step])
        assert wf.status == WorkflowStatus.DRAFT
        assert wf.context == {}
        assert wf.metadata == {}
        assert wf.created_at is not None


class TestWorkflowEngine:
    @pytest.fixture
    def engine(self, monkeypatch):
        import backend.app.core.workflow_engine as we_module
        fake_bus = FakeEventBus()
        monkeypatch.setattr(we_module, "event_bus", fake_bus)
        return WorkflowEngine(), fake_bus

    async def test_create_workflow_publishes_event(self, engine):
        eng, bus = engine
        step = WorkflowStep(id="s1", name="Step 1", agent="agent-a", action="act")
        wf = Workflow(id="wf1", name="WF", description="desc", steps=[step])
        wf_id = await eng.create_workflow(wf)
        assert wf_id == "wf1"
        assert "wf1" in eng._workflows
        assert any(e.event_type == "workflow.created" for e in bus.published)

    async def test_run_returns_completed_for_simple_workflow(self, engine):
        eng, bus = engine
        step = WorkflowStep(id="s1", name="Step 1", agent="agent-a", action="act")
        wf = Workflow(id="wf1", name="WF", description="desc", steps=[step])
        await eng.create_workflow(wf)
        result = await eng.run("wf1")
        assert result["status"] == "completed"
        assert "s1" in result["results"]

    async def test_run_raises_for_missing_workflow(self, engine):
        eng, _ = engine
        with pytest.raises(ValueError):
            await eng.run("missing")

    async def test_run_handles_failed_step(self, engine):
        eng, bus = engine

        async def fail_call(agent, action, params):
            raise RuntimeError("boom")

        step = WorkflowStep(id="s1", name="Step 1", agent="agent-a", action="act", retry_policy={"max_retries": 0})
        wf = Workflow(id="wf1", name="WF", description="desc", steps=[step])
        await eng.create_workflow(wf)
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr(eng, "_call_tool", staticmethod(fail_call))
        try:
            result = await eng.run("wf1")
            assert result["status"] == "failed"
        finally:
            monkeypatch.undo()

    async def test_get_workflow_returns_none_for_missing(self, engine):
        eng, _ = engine
        assert await eng.get_workflow("missing") is None

    async def test_list_workflows_empty(self, engine):
        eng, _ = engine
        assert eng.list_workflows() == []

    async def test_cancel_returns_true(self, engine):
        eng, _ = engine
        step = WorkflowStep(id="s1", name="Step 1", agent="agent-a", action="act")
        wf = Workflow(id="wf1", name="WF", description="desc", steps=[step])
        await eng.create_workflow(wf)
        assert await eng.cancel("wf1") is True
        assert (await eng.get_workflow("wf1")).status == WorkflowStatus.CANCELLED

    async def test_cancel_returns_false_for_missing(self, engine):
        eng, _ = engine
        assert await eng.cancel("missing") is False
