"""
Tests for backend/app/core/schemas.py — Pydantic schema models.
"""

import pytest
from pydantic import ValidationError

from backend.app.core.schemas import (
    CONTRACT_VERSION,
    CapabilityEntry,
    CapabilityPackConfig,
    ContractVersion,
    Event,
    EventPriority,
    PipelineStage,
    TaskError,
    TaskIntentRequest,
    TaskResult,
    TaskResultPayload,
)


class TestContractVersion:
    def test_current_version(self):
        assert CONTRACT_VERSION.VERSION == "1.0.0"
        assert CONTRACT_VERSION.MAJOR == 1

    def test_parse_valid(self):
        v = ContractVersion.parse("2.1.3")
        assert v.MAJOR == 2
        assert v.MINOR == 1
        assert v.PATCH == 3

    def test_parse_with_v_prefix(self):
        v = ContractVersion.parse("v1.2.0")
        assert v.MAJOR == 1
        assert v.MINOR == 2

    def test_backward_compatible_same_version(self):
        v1 = ContractVersion.parse("1.0.0")
        assert v1.is_backward_compatible(v1)

    def test_backward_compatible_patch(self):
        v1 = ContractVersion(MAJOR=1, MINOR=0, PATCH=0)
        v2 = ContractVersion(MAJOR=1, MINOR=0, PATCH=1)
        assert v2.is_backward_compatible(v1)

    def test_backward_incompatible_major(self):
        v1 = ContractVersion(MAJOR=1, MINOR=0, PATCH=0)
        v2 = ContractVersion(MAJOR=2, MINOR=0, PATCH=0)
        assert not v2.is_backward_compatible(v1)


class TestTaskIntentRequest:
    def test_default_values(self):
        task = TaskIntentRequest(intent="code_engineer.generate")
        assert task.task_id is not None
        assert task.priority == "normal"
        assert task.timeout_ms == 30000
        assert task.metadata.trace_id is not None
        assert task.metadata.correlation_id is not None

    def test_full_construction(self):
        task = TaskIntentRequest(
            intent="network_engineer.audit",
            context={
                "workspace_path": "/tmp/ws",
                "language": "python",
                "framework": "fastapi",
                "user_input": "Audit security",
            },
            capabilities_required=["network_engineer.audit"],
            priority="high",
            timeout_ms=60000,
        )
        assert task.intent == "network_engineer.audit"
        assert task.context.workspace_path == "/tmp/ws"
        assert task.context.language == "python"
        assert task.priority == "high"
        assert task.timeout_ms == 60000

    def test_invalid_priority(self):
        with pytest.raises(ValidationError):
            TaskIntentRequest(intent="test", priority="invalid")


class TestTaskResult:
    def test_default_result(self):
        result = TaskResult(task_id="t1", intent="test.intent")
        assert result.status == "success"
        assert result.error is None

    def test_with_payload(self):
        result = TaskResult(
            task_id="t1",
            intent="test.intent",
            result=TaskResultPayload(
                output_type="code",
                payload={"file": "main.py"},
                artifacts=["/tmp/main.py"],
                confidence_score=0.95,
            ),
        )
        assert result.result.output_type == "code"
        assert result.result.confidence_score == 0.95
        assert len(result.result.artifacts) == 1

    def test_with_error(self):
        result = TaskResult(
            task_id="t1",
            intent="test.intent",
            status="failure",
            error=TaskError(code="E001", message="Something went wrong", recoverable=True),
        )
        assert result.status == "failure"
        assert result.error.code == "E001"

    def test_invalid_status(self):
        with pytest.raises(ValidationError):
            TaskResult(task_id="t1", intent="test", status="invalid")


class TestEvent:
    def test_event_defaults(self):
        ev = Event(event_type="test.event", payload={"key": "value"})
        assert ev.source == "system"
        assert ev.target == "*"
        assert ev.priority == EventPriority.NORMAL
        assert ev.trace_id is None

    def test_event_with_trace(self):
        ev = Event(
            event_type="pack.started",
            payload={"pack": "code_engineer"},
            source="factory_registry",
            trace_id="trace-123",
            correlation_id="corr-456",
            priority=EventPriority.HIGH,
        )
        assert ev.trace_id == "trace-123"
        assert ev.priority == EventPriority.HIGH


class TestCapabilityPackConfig:
    def test_minimal_manifest(self):
        cfg = CapabilityPackConfig(
            id="code_engineer",
            version="1.0.0",
            display_name="Code Engineer",
            entry_point="apps.code_engineer.engine.CodeEngineerEngine",
        )
        assert cfg.id == "code_engineer"
        assert cfg.maturity_level == 1
        assert len(cfg.capabilities) == 0

    def test_full_manifest(self):
        cfg = CapabilityPackConfig(
            id="trading_analyst",
            version="2.1.0",
            display_name="Trading Analyst",
            description="Market analysis",
            entry_point="apps.trading_analyst.engine.TradingAnalystEngine",
            category="finance",
            maturity_level=3,
            quality_target="A",
            capabilities=[
                CapabilityEntry(
                    id="wyckoff_analysis",
                    name="Wyckoff Analysis",
                    description="Detect Wyckoff accumulation",
                    input_schema="WyckoffRequest",
                    output_schema="WyckoffResult",
                )
            ],
            dependencies={
                "capabilities": ["execution_runtime"],
                "external": [{"name": "pandas", "version": ">=2.0.0"}],
            },
            pipeline=[
                PipelineStage(stage="detect", capability="trading_analyst.detect"),
            ],
            metadata={"author": "Test Team"},
        )
        assert len(cfg.capabilities) == 1
        assert cfg.capabilities[0].id == "wyckoff_analysis"
        assert cfg.dependencies.capabilities == ["execution_runtime"]
        assert len(cfg.pipeline) == 1
        assert cfg.metadata["author"] == "Test Team"
