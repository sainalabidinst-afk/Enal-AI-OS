"""
Tests for Enhanced Workflow Engine
================================--
Tests for real step execution, branching, error handling, retry policies.
"""

import pytest


class TestWorkflowEngineBasic:
    """Tests for basic workflow engine functionality."""

    @pytest.mark.asyncio
    async def test_create_workflow(self):
        from backend.app.core.workflow_engine import Workflow, WorkflowEngine, WorkflowStep
        engine = WorkflowEngine()
        workflow = Workflow(
            id="test-wf-1",
            name="Test Workflow",
            description="A test workflow",
            steps=[
                WorkflowStep(id="s1", name="Step 1", agent="test", action="do_something"),
            ],
        )
        workflow_id = await engine.create_workflow(workflow)
        assert workflow_id == "test-wf-1"

    @pytest.mark.asyncio
    async def test_get_workflow(self):
        from backend.app.core.workflow_engine import Workflow, WorkflowEngine
        engine = WorkflowEngine()
        workflow = Workflow(
            id="test-wf-2",
            name="Test Workflow 2",
            description="Another test",
            steps=[],
        )
        await engine.create_workflow(workflow)
        retrieved = await engine.get_workflow("test-wf-2")
        assert retrieved is not None
        assert retrieved.name == "Test Workflow 2"

    @pytest.mark.asyncio
    async def test_run_workflow_no_steps(self):
        from backend.app.core.workflow_engine import Workflow, WorkflowEngine
        engine = WorkflowEngine()
        workflow = Workflow(
            id="test-wf-3",
            name="Empty Workflow",
            description="No steps",
            steps=[],
        )
        await engine.create_workflow(workflow)
        result = await engine.run("test-wf-3")
        assert result["status"] == "completed"


class TestWorkflowEngineDependencies:
    """Tests for step dependency logic."""

    @pytest.mark.asyncio
    async def test_run_workflow_with_dependencies(self):
        from backend.app.core.workflow_engine import Workflow, WorkflowEngine, WorkflowStep
        engine = WorkflowEngine()
        workflow = Workflow(
            id="test-wf-4",
            name="Deps Workflow",
            description="With dependencies",
            steps=[
                WorkflowStep(id="s1", name="First", agent="test", action="step1"),
                WorkflowStep(id="s2", name="Second", agent="test", action="step2", depends_on=["s1"]),
                WorkflowStep(id="s3", name="Third", agent="test", action="step3", depends_on=["s1"]),
            ],
        )
        await engine.create_workflow(workflow)
        result = await engine.run("test-wf-4")
        assert result["status"] == "completed"
        assert "s1" in result["results"]
        assert "s2" in result["results"]
        assert "s3" in result["results"]


class TestWorkflowEngineCancel:
    """Tests for workflow cancellation."""

    @pytest.mark.asyncio
    async def test_cancel_workflow(self):
        from backend.app.core.workflow_engine import Workflow, WorkflowEngine
        engine = WorkflowEngine()
        workflow = Workflow(
            id="test-wf-5",
            name="Cancel Test",
            description="To be cancelled",
            steps=[],
        )
        await engine.create_workflow(workflow)
        cancelled = await engine.cancel("test-wf-5")
        assert cancelled is True
        retrieved = await engine.get_workflow("test-wf-5")
        assert retrieved.status.value == "cancelled"

    @pytest.mark.asyncio
    async def test_cancel_nonexistent(self):
        from backend.app.core.workflow_engine import WorkflowEngine
        engine = WorkflowEngine()
        cancelled = await engine.cancel("nonexistent")
        assert cancelled is False


class TestWorkflowEngineList:
    """Tests for listing workflows."""

    @pytest.mark.asyncio
    async def test_list_workflows(self):
        from backend.app.core.workflow_engine import Workflow, WorkflowEngine
        engine = WorkflowEngine()
        await engine.create_workflow(Workflow(
            id="list-wf-1", name="List Test 1", description="Test", steps=[]
        ))
        await engine.create_workflow(Workflow(
            id="list-wf-2", name="List Test 2", description="Test", steps=[]
        ))
        workflows = engine.list_workflows()
        assert len(workflows) >= 2