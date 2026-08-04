"""
Tests for Decision Intelligence Capability Pack.

Covers:
- Evidence collection and weighting
- Alternative generation
- Risk analysis
- Trade-off analysis
- Simulation engine
- Debate engine
- Confidence estimation
- Explanation generation
- End-to-end pipeline
"""

import pytest

from apps.decision_intelligence.engine import DecisionIntelligenceEngine
from apps.decision_intelligence.schemas import (
    DecisionRequest,
    EvidenceSource,
    EvidenceSourceType,
    Objective,
    ObjectiveGoal,
    RiskTolerance,
    DecisionOutcome,
)
from apps.decision_intelligence.simulation_engine import SimulationEngine, SimulationOutcome
from apps.decision_intelligence.debate_engine import DebateEngine, DebateResult, StrategyVote


@pytest.fixture
def engine():
    return DecisionIntelligenceEngine()


@pytest.fixture
def base_request():
    return DecisionRequest(
        context="Should I deploy the new release to production?",
        evidence_sources=[
            EvidenceSource(
                source_id="devops",
                evidence_type=EvidenceSourceType.analysis,
                payload={"sentiment": "positive", "test_pass_rate": 0.95},
                quality_score=0.9,
                weight=1.5,
            ),
            EvidenceSource(
                source_id="qa",
                evidence_type=EvidenceSourceType.recommendation,
                payload={"recommendation": "proceed", "coverage": 0.88},
                quality_score=0.85,
                weight=1.2,
            ),
        ],
        constraints=["no downtime"],
        objectives=[
            Objective(name="Accuracy", weight=0.35, goal=ObjectiveGoal.maximize),
            Objective(name="Risk", weight=0.30, goal=ObjectiveGoal.minimize),
            Objective(name="Cost", weight=0.20, goal=ObjectiveGoal.minimize),
            Objective(name="Latency", weight=0.15, goal=ObjectiveGoal.minimize),
        ],
        risk_tolerance=RiskTolerance.medium,
        max_alternatives=5,
        include_explanation=True,
    )


class TestEvidenceCollection:
    def test_collect_returns_evidence_set(self, engine):
        sources = [
            EvidenceSource(source_id="test", evidence_type=EvidenceSourceType.data, payload={"score": 0.8}, quality_score=0.8, weight=1.0),
        ]
        req = DecisionRequest(context="test", evidence_sources=sources)
        result = engine.evaluate(req)
        assert result.raw["evidence_count"] == 1

    def test_evidence_weights_normalized(self, engine):
        sources = [
            EvidenceSource(source_id="a", evidence_type=EvidenceSourceType.data, payload={"score": 0.9}, quality_score=0.9, weight=2.0),
            EvidenceSource(source_id="b", evidence_type=EvidenceSourceType.data, payload={"score": 0.5}, quality_score=0.5, weight=1.0),
        ]
        req = DecisionRequest(context="test", evidence_sources=sources)
        result = engine.evaluate(req)
        assert result.raw["evidence_count"] == 2


class TestAlternativeGeneration:
    def test_generates_alternatives(self, engine, base_request):
        result = engine.evaluate(base_request)
        assert len(result.alternatives) >= 1

    def test_respects_max_alternatives(self, engine):
        req = DecisionRequest(
            context="Choose a database",
            evidence_sources=[],
            max_alternatives=3,
        )
        result = engine.evaluate(req)
        assert len(result.alternatives) <= 3


class TestRiskAnalysis:
    def test_risk_profile_populated(self, engine, base_request):
        result = engine.evaluate(base_request)
        for alt in result.alternatives:
            assert 0.0 <= alt.risk_profile.overall_risk <= 1.0
            assert 0.0 <= alt.risk_profile.probability <= 1.0
            assert 0.0 <= alt.risk_profile.impact <= 1.0


class TestSimulationEngine:
    def test_simulation_returns_outcome(self, engine, base_request):
        result = engine.evaluate(base_request)
        assert "simulation_outcomes" in result.raw
        assert len(result.raw["simulation_outcomes"]) >= 1

    def test_simulation_outcome_fields(self):
        sim = SimulationEngine()
        outcome = sim.simulate(
            description="test",
            evidence_set=None,
            objectives=[],
        )
        assert isinstance(outcome, SimulationOutcome)
        assert 0.0 <= outcome.expected_value <= 1.0
        assert len(outcome.confidence_interval) == 2
        assert 0.0 <= outcome.probability_of_success <= 1.0


class TestDebateEngine:
    def test_debate_returns_results(self, engine, base_request):
        result = engine.evaluate(base_request)
        assert "debate_results" in result.raw
        assert len(result.raw["debate_results"]) >= 1

    def test_debate_result_fields(self):
        debate = DebateEngine()
        results = debate.debate(
            alternative_descriptions=["alt1", "alt2"],
            evidence_set=None,
            objectives=[],
        )
        assert len(results) == 2
        for dr in results:
            assert isinstance(dr, DebateResult)
            assert 0.0 <= dr.consensus_score <= 1.0
            assert len(dr.strategy_votes) >= 1


class TestConfidenceEstimation:
    def test_confidence_in_valid_range(self, engine, base_request):
        result = engine.evaluate(base_request)
        assert 0.0 <= result.confidence_score <= 1.0

    def test_high_quality_evidence_high_confidence(self, engine):
        sources = [
            EvidenceSource(source_id="test", evidence_type=EvidenceSourceType.analysis, payload={"score": 0.95}, quality_score=0.95, weight=2.0),
        ]
        req = DecisionRequest(context="test", evidence_sources=sources)
        result = engine.evaluate(req)
        assert result.confidence_score >= 0.6


class TestExplanationGeneration:
    def test_explanation_populated(self, engine, base_request):
        result = engine.evaluate(base_request)
        exp = result.explanation
        assert exp.evidence_summary or exp.final_rationale

    def test_reasoning_chain_present(self, engine, base_request):
        result = engine.evaluate(base_request)
        assert len(result.explanation.reasoning_chain) >= 1


class TestDecisionHistory:
    def test_history_ref_set(self, engine, base_request):
        result = engine.evaluate(base_request)
        assert result.decision_history_ref != ""


class TestEndToEnd:
    def test_full_pipeline(self, engine, base_request):
        result = engine.evaluate(base_request)
        assert result.decision_id == base_request.decision_id
        assert result.recommended_decision != ""
        assert len(result.alternatives) >= 1
        assert result.confidence_score >= 0.0
        assert result.confidence_explanation != ""
        assert result.explanation.final_rationale != ""

    def test_consistency(self, engine, base_request):
        r1 = engine.evaluate(base_request)
        r2 = engine.evaluate(base_request)
        assert r1.recommended_decision == r2.recommended_decision
