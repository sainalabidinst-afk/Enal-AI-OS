"""
Tests for Knowledge K3 — Evidence Intelligence
and Knowledge K4 — Experience Memory.
"""

from datetime import UTC, datetime

import pytest

from apps.organization.evidence_intelligence import (
    EvidenceIntelligenceEngine,
    EvidenceSource,
    EvidenceType,
)
from apps.organization.experience_memory import (
    ExperienceMemory,
)

# ─── K3 Tests ───


def test_create_evidence_record():
    engine = EvidenceIntelligenceEngine()
    evidence = engine.create(
        claim_id="claim-1",
        content="Market is bullish",
        source=EvidenceSource.TRADING,
        evidence_type=EvidenceType.OBSERVATION,
        confidence=0.8,
        capability="trading-analyst",
    )
    assert evidence.id
    assert evidence.claim_id == "claim-1"
    assert evidence.source == EvidenceSource.TRADING
    assert evidence.confidence == 0.8


def test_evidence_versioning():
    engine = EvidenceIntelligenceEngine()
    evidence = engine.create("claim-1", "v1", confidence=0.5)
    updated = engine.update(evidence.id, "v2", confidence=0.7)
    assert updated.version == 2
    assert updated.content == "v2"
    assert updated.confidence == 0.7
    assert len(updated.versions) == 1
    assert updated.versions[0].content == "v1"


def test_evidence_citation_chain():
    engine = EvidenceIntelligenceEngine()
    a = engine.create("claim-1", "Bullish", confidence=0.8)
    b = engine.create("claim-1", "Supporting bullish", confidence=0.9)
    engine.add_citation(a.id, b.id)
    assert b.id in a.citations
    assert a.id in b.supporting_ids


def test_conflict_detection_within_claim():
    engine = EvidenceIntelligenceEngine()
    bullish = engine.create("claim-1", "Bullish", confidence=0.8, source=EvidenceSource.TRADING)
    bearish = engine.create("claim-1", "Bearish", confidence=0.7, source=EvidenceSource.KNOWLEDGE)
    engine.add_citation(bullish.id, bearish.id)
    conflicts = engine.detect_conflicts_for_claim("claim-1")
    assert len(conflicts) >= 1


def test_cross_capability_conflict_exposure():
    engine = EvidenceIntelligenceEngine()
    trading_bullish = engine.create("claim-1", "Bullish", confidence=0.85, source=EvidenceSource.TRADING)
    knowledge_bearish = engine.create("claim-1", "Bearish divergence detected", confidence=0.75, source=EvidenceSource.KNOWLEDGE)
    engine.register_conflict(trading_bullish.id, knowledge_bearish.id)
    enriched = engine.enrich_for_reasoning("claim-1")
    assert enriched["contradicting_count"] >= 1
    assert len(enriched["conflicts"]) >= 1


def test_confidence_propagation():
    engine = EvidenceIntelligenceEngine()
    engine.create("claim-1", "A", confidence=0.9)
    engine.create("claim-2", "B", confidence=0.6)
    confidence = engine.propagate_confidence("claim-1")
    assert confidence == 0.9


def test_enrich_for_reasoning():
    engine = EvidenceIntelligenceEngine()
    engine.create("claim-1", "Strong buy signal", confidence=0.9)
    engine.create("claim-1", "Supporting volume confirmation", confidence=0.8)
    enriched = engine.enrich_for_reasoning("claim-1")
    assert enriched["claim_id"] == "claim-1"
    assert enriched["evidence_count"] == 2
    assert enriched["supporting_count"] == 2
    assert enriched["confidence"] > 0


# ─── K4 Tests ───


def test_record_execution():
    memory = ExperienceMemory()
    now = datetime.now(UTC)
    record = memory.record_execution(
        capability_id="trading-analyst",
        subtask_id="subtask-1",
        status="completed",
        started_at=now,
        finished_at=now,
        output={"result": "ok"},
    )
    assert record.execution_id
    assert record.duration_seconds == 0.0
    assert record.status == "completed"


def test_record_lesson_from_execution():
    memory = ExperienceMemory()
    now = datetime.now(UTC)
    exec_record = memory.record_execution(
        capability_id="network-engineer",
        subtask_id="subtask-1",
        status="failed",
        started_at=now,
        finished_at=now,
        error="timeout",
    )
    lesson = memory.record_lesson(
        execution_id=exec_record.execution_id,
        capability_id="network-engineer",
        category="timeout",
        situation="Subtask timed out during execution",
        action_taken="Retried with increased timeout",
        outcome="Success after retry",
        quality_score=0.85,
        root_cause="Network latency spike",
        recommendation="Use adaptive timeout based on historical latency",
    )
    assert lesson.execution_id == exec_record.execution_id
    assert lesson.quality_score == 0.85


def test_get_lessons_for_capability():
    memory = ExperienceMemory()
    now = datetime.now(UTC)
    for i in range(3):
        exec_record = memory.record_execution(
            capability_id="code-engineer",
            subtask_id=f"subtask-{i}",
            status="completed",
            started_at=now,
            finished_at=now,
        )
        memory.record_lesson(
            execution_id=exec_record.execution_id,
            capability_id="code-engineer",
            category="performance",
            situation=f"Situation {i}",
            action_taken=f"Action {i}",
            outcome=f"Outcome {i}",
            quality_score=0.7 + i * 0.1,
        )
    lessons = memory.get_lessons_for_capability("code-engineer")
    assert len(lessons) == 3


def test_quality_trend():
    memory = ExperienceMemory()
    now = datetime.now(UTC)
    for i in range(5):
        exec_record = memory.record_execution(
            capability_id="full-stack-engineer",
            subtask_id=f"subtask-{i}",
            status="completed",
            started_at=now,
            finished_at=now,
        )
        memory.record_lesson(
            execution_id=exec_record.execution_id,
            capability_id="full-stack-engineer",
            category="refactoring",
            situation=f"Situation {i}",
            action_taken=f"Action {i}",
            outcome=f"Outcome {i}",
            quality_score=0.5 + i * 0.1,
        )
    trend = memory.get_quality_trend("full-stack-engineer")
    assert trend["count"] == 5
    assert trend["average_quality"] > 0


def test_search_experiences():
    memory = ExperienceMemory()
    now = datetime.now(UTC)
    exec_record = memory.record_execution(
        capability_id="devops-assistant",
        subtask_id="deploy",
        status="completed",
        started_at=now,
        finished_at=now,
        tags=["deployment", "production"],
    )
    memory.record_lesson(
        execution_id=exec_record.execution_id,
        capability_id="devops-assistant",
        category="deployment",
        situation="Production deployment",
        action_taken="Blue-green deployment",
        outcome="Zero downtime",
        quality_score=0.95,
        tags=["deployment", "production"],
    )
    results = memory.search("deployment", capability_id="devops-assistant")
    assert len(results) >= 1


def test_to_knowledge_update():
    memory = ExperienceMemory()
    now = datetime.now(UTC)
    exec_record = memory.record_execution(
        capability_id="trading-analyst",
        subtask_id="analysis",
        status="completed",
        started_at=now,
        finished_at=now,
    )
    memory.record_lesson(
        execution_id=exec_record.execution_id,
        capability_id="trading-analyst",
        category="market_analysis",
        situation="High volatility detected",
        action_taken="Increased confirmation threshold",
        outcome="Reduced false signals by 15%",
        quality_score=0.9,
        recommendation="Use volatility-adjusted thresholds",
    )
    updates = memory.to_knowledge_update("trading-analyst")
    assert len(updates) >= 1
    assert updates[0]["type"] == "lesson_learned"
    assert updates[0]["confidence"] >= 0.7


def test_recent_executions():
    memory = ExperienceMemory()
    now = datetime.now(UTC)
    for i in range(5):
        memory.record_execution(
            capability_id="network-engineer",
            subtask_id=f"subtask-{i}",
            status="completed",
            started_at=now,
            finished_at=now,
        )
    recent = memory.get_recent_executions(capability_id="network-engineer", limit=3)
    assert len(recent) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])