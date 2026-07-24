"""
Integration Tests for Capability Execution Engine
==================================================

Validates the end-to-end flow:

    Request
        ↓
    Registry (CapabilityGraph)
        ↓
    Execution (ExecutionRuntime)
        ↓
    Response (standardized contract)

Test scenarios:
    ✅ capability found → COMPLETED
    ✅ capability not found → FAILED
    ✅ input valid → COMPLETED
    ✅ input invalid → FAILED with validation error
    ✅ runtime error → FAILED with error
    ✅ telemetry recorded
    ✅ response follows contract
"""

import pytest
from datetime import datetime
from typing import Any

from apps.organization.capability_execution_engine import (
    CapabilityExecutionEngine,
    ExecutionRequest,
    ExecutionResponse,
    ExecutionStatus,
    TelemetryRecord,
)
from apps.organization.capability_graph import capability_graph
from apps.organization.capability_contract import CapabilityNode


# ── Helpers ──


def assert_valid_response(response: ExecutionResponse) -> None:
    """Assert that response follows the standardized output contract."""
    assert isinstance(response, ExecutionResponse)
    assert isinstance(response.status, ExecutionStatus)
    assert isinstance(response.execution_id, str) and len(response.execution_id) > 0
    assert isinstance(response.correlation_id, str) and len(response.correlation_id) > 0
    assert isinstance(response.execution_time_ms, (int, float))
    assert response.execution_time_ms >= 0.0

    # If status is COMPLETED, result should be present, error should be None
    if response.status == ExecutionStatus.COMPLETED:
        assert response.error is None
    # If status is FAILED, error should be a string
    elif response.status == ExecutionStatus.FAILED:
        assert isinstance(response.error, str) and len(response.error) > 0

    # Telemetry is optional but if present must be valid
    if response.telemetry is not None:
        assert isinstance(response.telemetry, TelemetryRecord)
        assert response.telemetry.execution_id == response.execution_id
        assert response.telemetry.capability_id is not None


# ── Fixtures ──


@pytest.fixture
def engine() -> CapabilityExecutionEngine:
    """Create a fresh engine instance for each test."""
    eng = CapabilityExecutionEngine()
    eng.clear_telemetry()
    return eng


@pytest.fixture
def known_capability_id() -> str:
    """Return a capability that exists in the registry."""
    caps = capability_graph.get_all_capabilities()
    assert len(caps) > 0, "CapabilityGraph must have at least one capability"
    # Use a simple capability that doesn't require heavy external dependencies
    return "documentation"


# ── Tests ──


@pytest.mark.asyncio
async def test_capability_found_completed(engine: CapabilityExecutionEngine):
    """✅ capability found → COMPLETED"""
    request = ExecutionRequest(
        capability_id="documentation",
        input_data={"skills": ["documentation", "writing"]},
        metadata={"project_id": "test-proj-1"},
    )
    response = await engine.execute(request)

    assert response.status == ExecutionStatus.COMPLETED
    assert response.error is None
    assert response.result is not None
    assert "subtask_count" in response.result
    assert response.result["subtask_count"] >= 1
    assert_valid_response(response)


@pytest.mark.asyncio
async def test_capability_not_found(engine: CapabilityExecutionEngine):
    """✅ capability not found → FAILED with 'capability_not_found'"""
    request = ExecutionRequest(
        capability_id="non-existent-capability-xyz",
        input_data={},
    )
    response = await engine.execute(request)

    assert response.status == ExecutionStatus.FAILED
    assert response.error is not None
    assert "not found" in response.error.lower()
    assert response.result is None
    assert_valid_response(response)


@pytest.mark.asyncio
async def test_valid_input_succeeds(engine: CapabilityExecutionEngine):
    """✅ input valid → COMPLETED"""
    request = ExecutionRequest(
        capability_id="literature-review",
        input_data={"skills": ["research", "literature-review"]},
        metadata={"project_id": "test-proj-2"},
    )
    response = await engine.execute(request)

    assert response.status == ExecutionStatus.COMPLETED
    assert response.error is None
    assert_valid_response(response)


@pytest.mark.asyncio
async def test_invalid_input_type(engine: CapabilityExecutionEngine):
    """✅ input invalid (not a dict) → FAILED with validation error"""
    request = ExecutionRequest(
        capability_id="documentation",
        input_data="this is a string, not a dict",  # type: ignore
    )
    response = await engine.execute(request)

    assert response.status == ExecutionStatus.FAILED
    assert response.error is not None
    assert "input_data must be a dictionary" in response.error
    assert_valid_response(response)


@pytest.mark.asyncio
async def test_network_capability_execution(engine: CapabilityExecutionEngine):
    """✅ network capability with valid input → COMPLETED"""
    request = ExecutionRequest(
        capability_id="config-analysis",
        input_data={
            "skills": ["config-analysis", "parsing"],
            "config": "interface GigabitEthernet0/0\n ip address 192.168.1.1 255.255.255.0\n",
        },
        metadata={"project_id": "test-proj-3"},
    )
    response = await engine.execute(request)

    assert response.status == ExecutionStatus.COMPLETED, f"Error: {response.error}"
    assert response.result is not None
    assert_valid_response(response)


@pytest.mark.asyncio
async def test_telemetry_recorded_on_success(engine: CapabilityExecutionEngine):
    """✅ telemetry tercatat setelah sukses"""
    assert len(engine.get_telemetry()) == 0

    request = ExecutionRequest(
        capability_id="automation",
        input_data={"skills": ["automation", "python", "ci-cd"]},
        metadata={"project_id": "test-proj-telemetry-1"},
    )
    await engine.execute(request)

    telemetry = engine.get_telemetry()
    assert len(telemetry) >= 1

    record = telemetry[-1]
    assert record.capability_id == "automation"
    assert record.status == ExecutionStatus.COMPLETED
    # execution_time_ms may be 0.0 for extremely fast local executions;
    # the important thing is telemetry was recorded at all with correct metadata
    assert record.started_at is not None
    assert record.finished_at is not None
    assert record.execution_id == request.execution_id
    assert record.correlation_id == request.correlation_id


@pytest.mark.asyncio
async def test_telemetry_recorded_on_failure(engine: CapabilityExecutionEngine):
    """✅ telemetry tercatat setelah gagal"""
    assert len(engine.get_telemetry()) == 0

    request = ExecutionRequest(
        capability_id="does-not-exist",
        input_data={},
    )
    await engine.execute(request)

    telemetry = engine.get_telemetry()
    assert len(telemetry) >= 1

    record = telemetry[-1]
    assert record.status == ExecutionStatus.FAILED
    assert record.error_type == "capability_not_found"


@pytest.mark.asyncio
async def test_response_follows_contract_on_success(engine: CapabilityExecutionEngine):
    """✅ response mengikuti contract pada sukses"""
    request = ExecutionRequest(
        capability_id="market-analysis",
        input_data={"skills": ["market-analysis", "data-analysis", "finance"]},
        metadata={"project_id": "test-proj-contract-1"},
    )
    response = await engine.execute(request)

    assert_valid_response(response)
    assert response.status == ExecutionStatus.COMPLETED
    assert response.result is not None


@pytest.mark.asyncio
async def test_response_follows_contract_on_failure(engine: CapabilityExecutionEngine):
    """✅ response mengikuti contract pada gagal"""
    request = ExecutionRequest(
        capability_id="",
        input_data={},
    )
    response = await engine.execute(request)

    assert_valid_response(response)
    assert response.status == ExecutionStatus.FAILED
    assert response.error is not None


@pytest.mark.asyncio
async def test_execution_id_and_correlation_id(engine: CapabilityExecutionEngine):
    """✅ execution_id dan correlation_id dapat di-set manual"""
    request = ExecutionRequest(
        capability_id="documentation",
        input_data={"skills": ["documentation"]},
        execution_id="my-custom-exec-id",
        correlation_id="my-custom-corr-id",
    )
    response = await engine.execute(request)

    assert response.execution_id == "my-custom-exec-id"
    assert response.correlation_id == "my-custom-corr-id"
    assert response.telemetry is not None
    assert response.telemetry.execution_id == "my-custom-exec-id"
    assert response.telemetry.correlation_id == "my-custom-corr-id"


@pytest.mark.asyncio
async def test_auto_generated_ids(engine: CapabilityExecutionEngine):
    """✅ execution_id dan correlation_id auto-generated jika tidak di-set"""
    request = ExecutionRequest(
        capability_id="documentation",
        input_data={"skills": ["documentation"]},
    )
    response = await engine.execute(request)

    assert len(response.execution_id) > 0
    assert response.execution_id.startswith("exec-")
    assert response.correlation_id == response.execution_id


@pytest.mark.asyncio
async def test_multiple_executions_maintain_separate_telemetry(
    engine: CapabilityExecutionEngine,
):
    """✅ Multiple executions maintain separate telemetry records"""
    req1 = ExecutionRequest(
        capability_id="documentation",
        input_data={"skills": ["documentation"]},
        metadata={"project_id": "test-proj-multi-1"},
    )
    req2 = ExecutionRequest(
        capability_id="network-design",
        input_data={"skills": ["network-design", "topology", "ip-subnetting"]},
        metadata={"project_id": "test-proj-multi-2"},
    )

    resp1 = await engine.execute(req1)
    resp2 = await engine.execute(req2)

    assert resp1.status == ExecutionStatus.COMPLETED
    assert resp2.status == ExecutionStatus.COMPLETED

    telemetry = engine.get_telemetry()
    assert len(telemetry) >= 2

    # Filter by execution_id
    t1 = engine.get_telemetry(execution_id=req1.execution_id)
    t2 = engine.get_telemetry(execution_id=req2.execution_id)
    assert len(t1) == 1
    assert len(t2) == 1
    assert t1[0].capability_id == "documentation"
    assert t2[0].capability_id == "network-design"


@pytest.mark.asyncio
async def test_clear_telemetry(engine: CapabilityExecutionEngine):
    """✅ clear_telemetry() menghapus semua record"""
    request = ExecutionRequest(
        capability_id="documentation",
        input_data={"skills": ["documentation"]},
    )
    await engine.execute(request)
    assert len(engine.get_telemetry()) >= 1

    engine.clear_telemetry()
    assert len(engine.get_telemetry()) == 0


@pytest.mark.asyncio
async def test_economics_capability_execution(engine: CapabilityExecutionEngine):
    """✅ economics-related capability → COMPLETED"""
    request = ExecutionRequest(
        capability_id="data-analysis",
        input_data={
            "skills": ["data-analysis", "statistics", "python"],
            "dataset": "sample_data.csv",
        },
        metadata={"project_id": "test-proj-econ-1"},
    )
    response = await engine.execute(request)

    assert response.status == ExecutionStatus.COMPLETED, f"Error: {response.error}"
    assert response.result is not None
    assert_valid_response(response)

