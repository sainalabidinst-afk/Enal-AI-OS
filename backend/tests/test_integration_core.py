import logging

import pytest

from apps.integration.context import CapabilityContext
from apps.integration.evidence_adapter import EvidenceAdapter, UnifiedEvidence, EvidenceSource, EvidenceType
from apps.integration.registry import CapabilityRegistry, CapabilityDescriptor
from apps.integration.workflow import WorkflowEngine, WorkflowStep


def test_registry_returns_default_descriptors():
    registry = CapabilityRegistry()
    descriptors = registry.all()
    ids = [d.capability_id for d in descriptors]
    assert "trading-analysis" in ids
    assert "knowledge-query" in ids
    assert "reasoning" in ids
    assert "network-design-review" in ids


def test_registry_resolve_by_domain():
    registry = CapabilityRegistry()
    trading = registry.resolve_by_domain("trading")
    assert any(d.capability_id == "trading-analysis" for d in trading)


def test_registry_requires_and_provides():
    registry = CapabilityRegistry()
    descriptor = registry.resolve("trading-analysis")
    assert descriptor is not None
    assert "market_data_provider" in descriptor.requires
    assert "market_evidence" in descriptor.provides


def test_context_input_output_flow():
    context = CapabilityContext(workflow_type="test")
    context.set_input("symbol", "BTCUSDT")
    context.set_output("summary", "bullish")

    assert context.get_input("symbol") == "BTCUSDT"
    assert context.get_output("summary") == "bullish"
    assert context.get_input("missing", "default") == "default"


def test_context_evidence_collection():
    context = CapabilityContext()
    evidence = UnifiedEvidence(
        id="ev1",
        source=EvidenceSource.TRADING,
        type=EvidenceType.OBSERVATION,
        content="test",
        confidence=0.8,
    )
    context.add_evidence(evidence)
    assert len(context.evidences) == 1
    assert context.evidences[0].id == "ev1"


def test_workflow_engine_runs_steps_in_order():
    engine = WorkflowEngine()
    calls = []

    async def step_a(context):
        calls.append("a")
        context.set_output("step", "a")
        return context

    async def step_b(context):
        calls.append("b")
        assert context.get_output("step") == "a"
        context.set_output("step", "b")
        return context

    engine.register_step(WorkflowStep(name="a", func=step_a))
    engine.register_step(WorkflowStep(name="b", func=step_b))

    import asyncio

    context = CapabilityContext(workflow_type="test")
    result = asyncio.run(engine.run("test", [engine._steps["a"], engine._steps["b"]], context))

    assert result.success is True
    assert calls == ["a", "b"]
    assert context.get_output("step") == "b"


def test_workflow_engine_stops_on_failure():
    engine = WorkflowEngine()

    async def failing_step(context):
        raise RuntimeError("boom")
        return context

    engine.register_step(WorkflowStep(name="fail", func=failing_step))

    import asyncio

    context = CapabilityContext(workflow_type="test")
    result = asyncio.run(engine.run("test", [engine._steps["fail"]], context))

    assert result.success is False
    assert "boom" in (result.error or "")


def test_evidence_adapter_aggregate():
    adapter = EvidenceAdapter()
    evidences = [
        UnifiedEvidence(id="e1", source=EvidenceSource.TRADING, type=EvidenceType.OBSERVATION, content="a", confidence=0.8),
        UnifiedEvidence(id="e2", source=EvidenceSource.KNOWLEDGE, type=EvidenceType.FACT, content="b", confidence=0.6),
    ]
    aggregated = adapter.aggregate(evidences)
    assert aggregated.confidence == pytest.approx(0.7)
    assert aggregated.type == EvidenceType.DERIVED
