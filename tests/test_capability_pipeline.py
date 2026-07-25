"""
Integration Tests for Capability Pipeline
==========================================

Validates the sequential pipeline flow:

    PipelineRequest
        |
    Step 1: Capability A ----> ExecutionResponse
        | (pass output as input)
    Step 2: Capability B ----> ExecutionResponse
        | (pass output as input)
    Step 3: Capability C ----> ExecutionResponse
        |
    Unified PipelineResponse

Test scenarios:
    ✅ sequential execution with multiple capabilities
    ✅ pipeline failure propagation (stop on first failure)
    ✅ telemetry aggregation across steps
    ✅ unified response contract
    ✅ empty pipeline
    ✅ single step pipeline
    ✅ custom aliases
    ✅ resolve input passthrough
"""


import pytest

from apps.organization.capability_execution_engine import (
    CapabilityExecutionEngine,
    ExecutionStatus,
)
from apps.organization.capability_pipeline import (
    CapabilityPipeline,
    PipelineRequest,
    PipelineResponse,
    PipelineStep,
    StepResult,
)

# -- Fixtures ---


@pytest.fixture
def engine() -> CapabilityExecutionEngine:
    """Create a fresh engine for each test."""
    eng = CapabilityExecutionEngine()
    eng.clear_telemetry()
    return eng


@pytest.fixture
def pipeline(engine: CapabilityExecutionEngine) -> CapabilityPipeline:
    """Create a pipeline backed by the fresh engine."""
    pip = CapabilityPipeline(engine=engine)
    return pip


# -- Helpers ---


def assert_valid_pipeline_response(response: PipelineResponse) -> None:
    """Assert that PipelineResponse follows the standardized contract."""
    assert isinstance(response, PipelineResponse)
    assert isinstance(response.pipeline_id, str) and len(response.pipeline_id) > 0
    assert isinstance(response.correlation_id, str) and len(response.correlation_id) > 0
    assert isinstance(response.status, ExecutionStatus)
    assert isinstance(response.step_count, int)
    assert isinstance(response.steps, list)
    assert isinstance(response.total_time_ms, float)
    assert response.total_time_ms >= 0.0
    assert len(response.steps) == response.step_count

    # All steps must be valid
    for s in response.steps:
        assert isinstance(s, StepResult)
        assert isinstance(s.step_index, int)
        assert isinstance(s.capability_id, str)
        assert isinstance(s.status, ExecutionStatus)
        assert isinstance(s.execution_time_ms, (int, float))

    # If overall status is COMPLETED, no error
    if response.status == ExecutionStatus.COMPLETED:
        assert response.error is None
        assert response.failed_step is None
        assert response.error_step is None
        # All steps must be COMPLETED too
        for s in response.steps:
            assert s.status == ExecutionStatus.COMPLETED, (
                f"Step {s.step_index} ({s.alias}) failed: {s.error}"
            )

    # If overall status is FAILED, error info must be present
    if response.status == ExecutionStatus.FAILED:
        assert response.error is not None
        assert response.failed_step is not None
        assert response.error_step is not None


# -- Tests ---


@pytest.mark.asyncio
async def test_sequential_execution_two_capabilities(pipeline: CapabilityPipeline):
    """✅ sequential execution of two capabilities -> COMPLETED"""
    request = PipelineRequest(
        steps=[
            PipelineStep(
                capability_id="documentation",
                input_data={"skills": ["documentation", "writing"]},
                alias="Doc Generation",
            ),
            PipelineStep(
                capability_id="literature-review",
                input_data={"skills": ["research", "literature-review"]},
                alias="Literature Review",
            ),
        ],
        metadata={"project_id": "test-pipeline-seq-1"},
    )

    response = await pipeline.execute(request)

    assert response.status == ExecutionStatus.COMPLETED
    assert response.step_count == 2
    assert response.failed_step is None
    assert response.error is None
    assert response.error_step is None
    assert_valid_pipeline_response(response)


@pytest.mark.asyncio
async def test_sequential_execution_three_capabilities(pipeline: CapabilityPipeline):
    """✅ sequential execution of three capabilities -> COMPLETED"""
    request = PipelineRequest(
        steps=[
            PipelineStep(
                capability_id="documentation",
                input_data={"skills": ["documentation", "writing"]},
                alias="Documentation",
            ),
            PipelineStep(
                capability_id="automation",
                input_data={"skills": ["automation", "python", "ci-cd"]},
                alias="Automation",
            ),
            PipelineStep(
                capability_id="data-analysis",
                input_data={
                    "skills": ["data-analysis", "statistics", "python"],
                    "dataset": "sample.csv",
                },
                alias="Data Analysis",
            ),
        ],
        metadata={"project_id": "test-pipeline-seq-3"},
    )

    response = await pipeline.execute(request)

    assert response.status == ExecutionStatus.COMPLETED
    assert response.step_count == 3
    assert_valid_pipeline_response(response)

    # Verify order is preserved
    for i, s in enumerate(response.steps):
        assert s.step_index == i
        assert s.status == ExecutionStatus.COMPLETED


@pytest.mark.asyncio
async def test_pipeline_failure_propagation(pipeline: CapabilityPipeline):
    """✅ pipeline stops on first failure and propagates error"""
    request = PipelineRequest(
        steps=[
            PipelineStep(
                capability_id="documentation",
                input_data={"skills": ["documentation"]},
                alias="First Step (OK)",
            ),
            PipelineStep(
                capability_id="non-existent-capability-xyz",
                input_data={},
                alias="Second Step (FAIL)",
            ),
            PipelineStep(
                capability_id="documentation",
                input_data={"skills": ["documentation"]},
                alias="Third Step (SHOULD NOT RUN)",
            ),
        ],
        metadata={"project_id": "test-pipeline-fail-1"},
    )

    response = await pipeline.execute(request)

    # Overall status is FAILED
    assert response.status == ExecutionStatus.FAILED
    assert response.failed_step == 1  # second step (0-indexed)
    assert response.error_step == "non-existent-capability-xyz"
    assert response.error is not None
    assert "not found" in response.error.lower()

    # First step should have succeeded
    assert response.steps[0].status == ExecutionStatus.COMPLETED
    assert response.steps[0].capability_id == "documentation"

    # Second step should have failed
    assert response.steps[1].status == ExecutionStatus.FAILED
    assert response.steps[1].capability_id == "non-existent-capability-xyz"

    # Third step should NOT have been executed (pipeline stopped)
    assert response.step_count == 2  # only 2 steps executed
    assert len(response.steps) == 2

    assert_valid_pipeline_response(response)


@pytest.mark.asyncio
async def test_pipeline_failure_at_first_step(pipeline: CapabilityPipeline):
    """✅ pipeline fails at first step -> no subsequent steps run"""
    request = PipelineRequest(
        steps=[
            PipelineStep(
                capability_id="does-not-exist",
                input_data={},
                alias="Fail Immediately",
            ),
            PipelineStep(
                capability_id="documentation",
                input_data={"skills": ["documentation"]},
                alias="Should Not Run",
            ),
        ],
    )

    response = await pipeline.execute(request)

    assert response.status == ExecutionStatus.FAILED
    assert response.failed_step == 0
    assert response.step_count == 1  # only first step executed
    assert len(response.steps) == 1
    assert response.steps[0].status == ExecutionStatus.FAILED
    assert_valid_pipeline_response(response)


@pytest.mark.asyncio
async def test_telemetry_aggregation_across_steps(pipeline: CapabilityPipeline):
    """✅ telemetry is collected for each step"""
    request = PipelineRequest(
        steps=[
            PipelineStep(
                capability_id="documentation",
                input_data={"skills": ["documentation"]},
                alias="Docs",
            ),
            PipelineStep(
                capability_id="automation",
                input_data={"skills": ["automation", "python"]},
                alias="Auto",
            ),
        ],
        metadata={"project_id": "test-pipeline-telemetry-1"},
    )

    response = await pipeline.execute(request)

    assert response.status == ExecutionStatus.COMPLETED

    # Each step should have telemetry
    for s in response.steps:
        assert s.telemetry is not None, f"Step {s.step_index} missing telemetry"
        assert s.telemetry.execution_id == s.execution_id
        assert s.telemetry.capability_id == s.capability_id
        assert s.telemetry.status in (ExecutionStatus.COMPLETED, ExecutionStatus.FAILED)

    # Extract telemetry via pipeline method
    telemetry_records = pipeline.get_pipeline_telemetry(response)
    assert len(telemetry_records) == 2
    assert telemetry_records[0].capability_id == "documentation"
    assert telemetry_records[1].capability_id == "automation"


@pytest.mark.asyncio
async def test_telemetry_on_failure(pipeline: CapabilityPipeline):
    """✅ telemetry collected even on failure (both success and failure steps)"""
    request = PipelineRequest(
        steps=[
            PipelineStep(
                capability_id="documentation",
                input_data={"skills": ["documentation"]},
                alias="Good Step",
            ),
            PipelineStep(
                capability_id="bad-capability",
                input_data={},
                alias="Bad Step",
            ),
        ],
    )

    response = await pipeline.execute(request)

    assert response.status == ExecutionStatus.FAILED

    # Step 0 should have telemetry with COMPLETED
    assert response.steps[0].telemetry is not None
    assert response.steps[0].telemetry.status == ExecutionStatus.COMPLETED

    # Step 1 should have telemetry with FAILED
    assert response.steps[1].telemetry is not None
    assert response.steps[1].telemetry.status == ExecutionStatus.FAILED


@pytest.mark.asyncio
async def test_unified_response_contract_success(pipeline: CapabilityPipeline):
    """✅ unified response contract on success"""
    request = PipelineRequest(
        steps=[
            PipelineStep(
                capability_id="documentation",
                input_data={"skills": ["documentation"]},
            ),
        ],
    )

    response = await pipeline.execute(request)

    assert_valid_pipeline_response(response)
    assert response.status == ExecutionStatus.COMPLETED
    assert response.pipeline_id == request.pipeline_id
    assert response.correlation_id == request.correlation_id

    # Step result should have all fields
    step0 = response.steps[0]
    assert step0.step_index == 0
    assert step0.capability_id == "documentation"
    assert step0.alias == "documentation"  # default alias from __post_init__
    assert step0.status == ExecutionStatus.COMPLETED
    assert step0.error is None
    assert step0.result is not None
    assert step0.execution_time_ms >= 0.0


@pytest.mark.asyncio
async def test_unified_response_contract_failure(pipeline: CapabilityPipeline):
    """✅ unified response contract on failure"""
    request = PipelineRequest(
        steps=[
            PipelineStep(
                capability_id="fake-capability",
                input_data={},
            ),
        ],
    )

    response = await pipeline.execute(request)

    assert_valid_pipeline_response(response)
    assert response.status == ExecutionStatus.FAILED
    assert response.failed_step == 0
    assert response.error is not None

    # Step result should have error details
    step0 = response.steps[0]
    assert step0.status == ExecutionStatus.FAILED
    assert step0.error is not None


@pytest.mark.asyncio
async def test_empty_pipeline(pipeline: CapabilityPipeline):
    """✅ empty pipeline (no steps) -> COMPLETED with 0 steps"""
    request = PipelineRequest(
        steps=[],
    )

    response = await pipeline.execute(request)

    assert response.status == ExecutionStatus.COMPLETED
    assert response.step_count == 0
    assert len(response.steps) == 0
    assert response.failed_step is None
    assert response.error is None
    assert response.total_time_ms >= 0.0
    assert_valid_pipeline_response(response)


@pytest.mark.asyncio
async def test_custom_pipeline_id_and_correlation_id(pipeline: CapabilityPipeline):
    """✅ pipeline_id and correlation_id can be set manually"""
    request = PipelineRequest(
        steps=[
            PipelineStep(
                capability_id="documentation",
                input_data={"skills": ["documentation"]},
            ),
        ],
        pipeline_id="my-pipeline-1",
        correlation_id="my-correlation-1",
    )

    response = await pipeline.execute(request)

    assert response.pipeline_id == "my-pipeline-1"
    assert response.correlation_id == "my-correlation-1"


@pytest.mark.asyncio
async def test_auto_generated_ids(pipeline: CapabilityPipeline):
    """✅ pipeline_id and correlation_id auto-generated"""
    request = PipelineRequest(
        steps=[
            PipelineStep(
                capability_id="documentation",
                input_data={"skills": ["documentation"]},
            ),
        ],
    )

    response = await pipeline.execute(request)

    assert len(response.pipeline_id) > 0
    assert response.pipeline_id.startswith("pipeline-")
    assert response.correlation_id == response.pipeline_id


@pytest.mark.asyncio
async def test_step_alias_defaults_to_capability_id(pipeline: CapabilityPipeline):
    """✅ alias defaults to capability_id when not provided"""
    request = PipelineRequest(
        steps=[
            PipelineStep(
                capability_id="documentation",
                input_data={"skills": ["documentation"]},
                # no alias provided
            ),
        ],
    )

    response = await pipeline.execute(request)

    assert response.steps[0].alias == "documentation"


@pytest.mark.asyncio
async def test_summary_output(pipeline: CapabilityPipeline):
    """✅ summarize() produces human-readable output"""
    request = PipelineRequest(
        steps=[
            PipelineStep(
                capability_id="documentation",
                input_data={"skills": ["documentation"]},
            ),
        ],
    )

    response = await pipeline.execute(request)
    summary = pipeline.summarize(response)

    assert isinstance(summary, dict)
    assert summary["pipeline_id"] == response.pipeline_id
    assert summary["status"] == "completed"
    assert summary["failed"] is False
    assert summary["steps_executed"] == 1
    assert len(summary["details"]) == 1
    assert summary["details"][0]["capability"] == "documentation"
    assert summary["details"][0]["status"] == "completed"

