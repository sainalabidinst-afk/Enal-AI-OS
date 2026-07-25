"""
Integration Tests for Workflow Execution Layer
===============================================

Validates the workflow execution flow.

Test scenarios:
    - workflow success (all steps complete)
    - workflow failure (step fails -> pipeline stops)
    - telemetry aggregation
    - workflow response contract
    - workflow loading (register from dict, JSON, file)
    - invalid workflow (empty steps, missing capability_id)
    - unknown workflow
    - workflow listing
    - execution history
    - summary output
"""

import json
import tempfile
from pathlib import Path

import pytest

from apps.organization.capability_execution_engine import (
    CapabilityExecutionEngine,
    ExecutionStatus,
)
from apps.organization.capability_pipeline import CapabilityPipeline
from apps.organization.workflow_executor import (
    WorkflowDefinition,
    WorkflowExecutor,
    WorkflowResponse,
    WorkflowStep,
    WorkflowStepResult,
)

# -- Fixtures ---


@pytest.fixture
def engine() -> CapabilityExecutionEngine:
    eng = CapabilityExecutionEngine()
    eng.clear_telemetry()
    return eng


@pytest.fixture
def pipeline(engine: CapabilityExecutionEngine) -> CapabilityPipeline:
    return CapabilityPipeline(engine=engine)


@pytest.fixture
def executor(pipeline: CapabilityPipeline) -> WorkflowExecutor:
    return WorkflowExecutor(pipeline=pipeline)


# -- Test workflow definitions ---


SIMPLE_WORKFLOW_DICT = {
    "workflow_id": "test-simple",
    "name": "Simple Test Workflow",
    "description": "Two capabilities: documentation, then automation",
    "ordered_steps": [
        {
            "capability_id": "documentation",
            "input_data": {"skills": ["documentation", "writing"]},
            "alias": "Write Docs",
            "description": "Generate documentation",
        },
        {
            "capability_id": "automation",
            "input_data": {"skills": ["automation", "python"]},
            "alias": "Automate",
            "description": "Create automation scripts",
        },
    ],
    "metadata": {"version": "1.0", "author": "test"},
}

SIMPLE_WORKFLOW_JSON = json.dumps(SIMPLE_WORKFLOW_DICT)

FAILING_WORKFLOW_DICT = {
    "workflow_id": "test-failing",
    "name": "Failing Test Workflow",
    "description": "First step works, second step fails",
    "ordered_steps": [
        {
            "capability_id": "documentation",
            "input_data": {"skills": ["documentation"]},
            "alias": "Good Step",
        },
        {
            "capability_id": "non-existent-capability-xyz",
            "input_data": {},
            "alias": "Bad Step",
        },
        {
            "capability_id": "documentation",
            "input_data": {"skills": ["documentation"]},
            "alias": "Should Not Run",
        },
    ],
}

THREE_STEP_WORKFLOW_DICT = {
    "workflow_id": "test-three-step",
    "name": "Three Step Workflow",
    "description": "documentation, automation, data-analysis",
    "ordered_steps": [
        {
            "capability_id": "documentation",
            "input_data": {"skills": ["documentation"]},
            "alias": "Doc",
        },
        {
            "capability_id": "automation",
            "input_data": {"skills": ["automation", "python"]},
            "alias": "Auto",
        },
        {
            "capability_id": "data-analysis",
            "input_data": {"skills": ["data-analysis", "statistics"]},
            "alias": "Data",
        },
    ],
}


# -- Helpers ---


def assert_valid_workflow_response(response: WorkflowResponse) -> None:
    assert isinstance(response, WorkflowResponse)
    assert isinstance(response.workflow_id, str) and len(response.workflow_id) > 0
    assert isinstance(response.workflow_name, str)
    assert isinstance(response.execution_id, str) and len(response.execution_id) > 0
    assert isinstance(response.status, ExecutionStatus)
    assert isinstance(response.step_count, int)
    assert isinstance(response.steps, list)
    assert isinstance(response.total_time_ms, float)
    assert response.total_time_ms >= 0.0
    assert len(response.steps) == response.step_count

    for s in response.steps:
        assert isinstance(s, WorkflowStepResult)
        assert isinstance(s.step_index, int)
        assert isinstance(s.capability_id, str)
        assert isinstance(s.status, ExecutionStatus)
        assert isinstance(s.execution_time_ms, (int, float))

    if response.status == ExecutionStatus.COMPLETED:
        assert response.error is None
        assert response.failed_step is None
        for s in response.steps:
            assert s.status == ExecutionStatus.COMPLETED, (
                f"Step {s.step_index} ({s.alias}) failed: {s.error}"
            )

    if response.status == ExecutionStatus.FAILED:
        err = response.error
        assert err is not None
        assert response.failed_step is not None


# -- Tests: Registration / Loading ---


def test_register_workflow_from_dict(executor: WorkflowExecutor):
    workflow = executor.register_from_dict(SIMPLE_WORKFLOW_DICT)
    assert workflow.workflow_id == "test-simple"
    assert workflow.name == "Simple Test Workflow"
    assert len(workflow.ordered_steps) == 2


def test_register_workflow_from_json(executor: WorkflowExecutor):
    workflow = executor.register_from_json(SIMPLE_WORKFLOW_JSON)
    assert workflow.workflow_id == "test-simple"
    assert len(workflow.ordered_steps) == 2


def test_register_workflow_from_file(executor: WorkflowExecutor):
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as f:
        json.dump(SIMPLE_WORKFLOW_DICT, f)
        filepath = f.name
    try:
        workflow = executor.register_from_file(filepath)
        assert workflow.workflow_id == "test-simple"
        assert len(workflow.ordered_steps) == 2
    finally:
        Path(filepath).unlink(missing_ok=True)


def test_register_workflow_directly(executor: WorkflowExecutor):
    definition = WorkflowDefinition(
        workflow_id="direct-wf",
        name="Direct Registration",
        ordered_steps=[
            WorkflowStep(
                capability_id="documentation",
                input_data={"skills": ["documentation"]},
                alias="Doc Step",
            ),
        ],
    )
    executor.register(definition)
    wf = executor.get("direct-wf")
    assert wf is not None
    assert wf.name == "Direct Registration"


def test_register_invalid_workflow_empty_steps(executor: WorkflowExecutor):
    with pytest.raises(ValueError, match="at least one step"):
        executor.register(WorkflowDefinition(
            workflow_id="empty-wf",
            name="Empty",
            ordered_steps=[],
        ))


def test_register_invalid_workflow_empty_capability_id(executor: WorkflowExecutor):
    with pytest.raises(ValueError, match="empty capability_id"):
        executor.register(WorkflowDefinition(
            workflow_id="bad-step-wf",
            name="Bad Step",
            ordered_steps=[
                WorkflowStep(capability_id="", input_data={}),
            ],
        ))


def test_list_workflows(executor: WorkflowExecutor):
    executor.register_from_dict(SIMPLE_WORKFLOW_DICT)
    executor.register_from_dict(FAILING_WORKFLOW_DICT)
    workflows = executor.list_workflows()
    assert len(workflows) >= 2
    ids = [w["workflow_id"] for w in workflows]
    assert "test-simple" in ids
    assert "test-failing" in ids


def test_get_workflow(executor: WorkflowExecutor):
    executor.register_from_dict(SIMPLE_WORKFLOW_DICT)
    wf = executor.get("test-simple")
    assert wf is not None
    assert wf.name == "Simple Test Workflow"


def test_get_unknown_workflow(executor: WorkflowExecutor):
    wf = executor.get("nonexistent")
    assert wf is None


# -- Tests: Execution ---


@pytest.mark.asyncio
async def test_workflow_success(executor: WorkflowExecutor):
    executor.register_from_dict(SIMPLE_WORKFLOW_DICT)
    response = await executor.execute("test-simple")

    assert response.status == ExecutionStatus.COMPLETED
    assert response.step_count == 2
    assert response.failed_step is None
    assert response.error is None
    assert response.workflow_id == "test-simple"
    assert response.workflow_name == "Simple Test Workflow"
    assert_valid_workflow_response(response)

    assert response.steps[0].status == ExecutionStatus.COMPLETED
    assert response.steps[0].capability_id == "documentation"
    assert response.steps[0].alias == "Write Docs"

    assert response.steps[1].status == ExecutionStatus.COMPLETED
    assert response.steps[1].capability_id == "automation"
    assert response.steps[1].alias == "Automate"


@pytest.mark.asyncio
async def test_workflow_success_three_steps(executor: WorkflowExecutor):
    executor.register_from_dict(THREE_STEP_WORKFLOW_DICT)
    response = await executor.execute("test-three-step")

    assert response.status == ExecutionStatus.COMPLETED
    assert response.step_count == 3
    assert_valid_workflow_response(response)

    assert response.steps[0].alias == "Doc"
    assert response.steps[1].alias == "Auto"
    assert response.steps[2].alias == "Data"


@pytest.mark.asyncio
async def test_workflow_failure_propagation(executor: WorkflowExecutor):
    executor.register_from_dict(FAILING_WORKFLOW_DICT)
    response = await executor.execute("test-failing")

    assert response.status == ExecutionStatus.FAILED
    assert response.failed_step == 1
    err = response.error
    assert err is not None
    assert "not found" in err.lower()

    assert response.steps[0].status == ExecutionStatus.COMPLETED
    assert response.steps[0].capability_id == "documentation"

    assert response.steps[1].status == ExecutionStatus.FAILED
    assert response.steps[1].capability_id == "non-existent-capability-xyz"

    assert response.step_count == 2
    assert len(response.steps) == 2
    assert_valid_workflow_response(response)


@pytest.mark.asyncio
async def test_workflow_unknown_workflow(executor: WorkflowExecutor):
    response = await executor.execute("non-existent-workflow")

    assert response.status == ExecutionStatus.FAILED
    assert response.step_count == 0
    assert response.failed_step == 0
    err = response.error
    assert err is not None
    assert "not found" in err.lower()
    assert_valid_workflow_response(response)


@pytest.mark.asyncio
async def test_workflow_with_base_input(executor: WorkflowExecutor):
    executor.register_from_dict(SIMPLE_WORKFLOW_DICT)
    response = await executor.execute(
        "test-simple",
        input_data={"project": "test-project"},
    )
    assert response.status == ExecutionStatus.COMPLETED
    assert response.step_count == 2


@pytest.mark.asyncio
async def test_workflow_custom_ids(executor: WorkflowExecutor):
    executor.register_from_dict(SIMPLE_WORKFLOW_DICT)
    response = await executor.execute(
        "test-simple",
        execution_id="my-exec-001",
        correlation_id="my-corr-001",
    )
    assert response.execution_id == "my-exec-001"
    assert response.correlation_id == "my-corr-001"


@pytest.mark.asyncio
async def test_workflow_auto_generated_ids(executor: WorkflowExecutor):
    executor.register_from_dict(SIMPLE_WORKFLOW_DICT)
    response = await executor.execute("test-simple")
    assert len(response.execution_id) > 0
    assert response.execution_id.startswith("wf-")
    assert response.correlation_id == response.execution_id


# -- Tests: Telemetry ---


@pytest.mark.asyncio
async def test_workflow_telemetry(executor: WorkflowExecutor):
    executor.register_from_dict(SIMPLE_WORKFLOW_DICT)
    response = await executor.execute("test-simple")
    assert response.status == ExecutionStatus.COMPLETED
    for s in response.steps:
        assert s.execution_time_ms >= 0.0


@pytest.mark.asyncio
async def test_workflow_telemetry_on_failure(executor: WorkflowExecutor):
    executor.register_from_dict(FAILING_WORKFLOW_DICT)
    response = await executor.execute("test-failing")
    assert response.status == ExecutionStatus.FAILED
    assert response.steps[0].execution_time_ms >= 0.0
    assert response.steps[1].execution_time_ms >= 0.0


# -- Tests: Response Contract ---


@pytest.mark.asyncio
async def test_workflow_response_contract_success(executor: WorkflowExecutor):
    executor.register_from_dict(SIMPLE_WORKFLOW_DICT)
    response = await executor.execute("test-simple")
    assert_valid_workflow_response(response)
    assert response.status == ExecutionStatus.COMPLETED
    assert response.workflow_id == "test-simple"
    assert response.workflow_name == "Simple Test Workflow"
    assert response.failed_step is None
    assert response.error is None
    assert response.step_count == 2


@pytest.mark.asyncio
async def test_workflow_response_contract_failure(executor: WorkflowExecutor):
    executor.register_from_dict(FAILING_WORKFLOW_DICT)
    response = await executor.execute("test-failing")
    assert_valid_workflow_response(response)
    assert response.status == ExecutionStatus.FAILED
    assert response.failed_step is not None
    err = response.error
    assert err is not None
    assert response.step_count == 2


# -- Tests: History ---


@pytest.mark.asyncio
async def test_execution_history(executor: WorkflowExecutor):
    executor.register_from_dict(SIMPLE_WORKFLOW_DICT)
    executor.register_from_dict(THREE_STEP_WORKFLOW_DICT)

    resp1 = await executor.execute("test-simple")
    await executor.execute("test-three-step")

    history1 = executor.get_execution(resp1.execution_id)
    assert history1 is not None
    assert history1.workflow_id == "test-simple"

    all_history = executor.get_history()
    assert len(all_history) >= 2

    simple_history = executor.get_history(workflow_id="test-simple")
    assert len(simple_history) >= 1
    assert simple_history[0].workflow_id == "test-simple"


@pytest.mark.asyncio
async def test_summary_output(executor: WorkflowExecutor):
    executor.register_from_dict(SIMPLE_WORKFLOW_DICT)
    response = await executor.execute("test-simple")
    summary = executor.summarize(response)

    assert isinstance(summary, dict)
    assert summary["workflow_id"] == "test-simple"
    assert summary["workflow_name"] == "Simple Test Workflow"
    assert summary["status"] == "completed"
    assert summary["failed"] is False
    assert summary["steps_executed"] == 2
    assert len(summary["details"]) == 2
    assert summary["details"][0]["capability"] == "documentation"
    assert summary["details"][1]["capability"] == "automation"


@pytest.mark.asyncio
async def test_workflow_with_input_data(executor: WorkflowExecutor):
    wf_def = WorkflowDefinition(
        workflow_id="input-test",
        name="Input Test",
        ordered_steps=[
            WorkflowStep(
                capability_id="documentation",
                input_data={"skills": ["documentation"]},
                alias="Doc",
            ),
        ],
    )
    executor.register(wf_def)
    response = await executor.execute(
        "input-test",
        input_data={"project_name": "my-project"},
    )
    assert response.status == ExecutionStatus.COMPLETED
    assert response.step_count == 1
    assert_valid_workflow_response(response)
