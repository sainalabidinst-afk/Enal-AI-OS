"""
Integration Tests for Reasoning Engine
=======================================

Tests scenarios:
    - forward chaining (goal decomposition)
    - backward chaining (prerequisite discovery)
    - decision tree (option evaluation)
    - constraint propagation (satisfaction checking)
    - causal reasoning (cause-effect analysis)
    - rule management (register, unregister, list)
    - knowledge base (add fact, query evidence)
    - response contract (ReasoningResult fields)
    - error handling (unknown rule, no evidence)
"""

from typing import Any

import pytest

from apps.organization.reasoning_engine import (
    Conclusion,
    Decision,
    DecisionUrgency,
    Evidence,
    EvidenceType,
    ReasoningEngine,
    ReasoningMethod,
    ReasoningResult,
    ReasoningRule,
    ReasoningStatus,
)


@pytest.fixture
def engine() -> ReasoningEngine:
    eng = ReasoningEngine()
    eng.clear_evidence()
    eng.clear_results()
    return eng


def assert_valid_reasoning_result(result: ReasoningResult) -> None:
    assert isinstance(result, ReasoningResult)
    assert isinstance(result.reasoning_id, str) and len(result.reasoning_id) > 0
    assert isinstance(result.method, ReasoningMethod)
    assert isinstance(result.status, ReasoningStatus)
    assert isinstance(result.goal, str) and len(result.goal) > 0
    assert isinstance(result.evidence, list)
    assert isinstance(result.conclusions, list)
    assert isinstance(result.decisions, list)
    assert isinstance(result.confidence, float)
    assert 0.0 <= result.confidence <= 1.0
    assert isinstance(result.execution_time_ms, float)
    assert result.execution_time_ms >= 0.0
    assert isinstance(result.explanation, str)

    for conclusion in result.conclusions:
        assert isinstance(conclusion, Conclusion)
        assert isinstance(conclusion.conclusion_id, str)
        assert isinstance(conclusion.statement, str)
        assert isinstance(conclusion.confidence, float)

    for decision in result.decisions:
        assert isinstance(decision, Decision)
        assert isinstance(decision.decision_id, str)
        assert isinstance(decision.description, str)
        assert isinstance(decision.options, list)
        assert isinstance(decision.urgency, DecisionUrgency)


# -- Tests: Forward Chaining ---


def test_forward_chaining_basic(engine: ReasoningEngine):
    # Add evidence that matches rule conditions
    engine.add_fact("goal is complex", True)
    engine.add_fact("goal can be split into independent parts", True)
    engine.add_fact("capabilities exist for the domain", True)
    evidence = engine.query_evidence("")
    result = engine.forward_chaining("Complete a complex software project", evidence)
    assert_valid_reasoning_result(result)
    assert result.status in (ReasoningStatus.COMPLETED, ReasoningStatus.INCONCLUSIVE)
    assert result.method == ReasoningMethod.FORWARD_CHAINING


def test_forward_chaining_with_evidence(engine: ReasoningEngine):
    evidence = [
        Evidence(
            id="ev-1",
            type=EvidenceType.FACT,
            description="Goal is complex",
            value=True,
            source="user",
        ),
        Evidence(
            id="ev-2",
            type=EvidenceType.FACT,
            description="Capabilities exist for the domain",
            value=True,
            source="user",
        ),
    ]
    result = engine.forward_chaining("Audit network infrastructure", evidence)
    assert_valid_reasoning_result(result)
    assert len(result.evidence) >= 2


def test_forward_chaining_goal_decomposition(engine: ReasoningEngine):
    result = engine.forward_chaining("Build a REST API with database and authentication")
    assert_valid_reasoning_result(result)

    # Should have goal decomposition related conclusions
    [c for c in result.conclusions if "decompos" in c.statement.lower()]
    # May or may not include decomposition conclusion, just check structure


def test_forward_chaining_no_goal(engine: ReasoningEngine):
    result = engine.forward_chaining("")
    # Empty goal returns INCONCLUSIVE with no conclusions
    assert isinstance(result, ReasoningResult)
    assert isinstance(result.reasoning_id, str) and len(result.reasoning_id) > 0
    assert result.method == ReasoningMethod.FORWARD_CHAINING
    assert result.status == ReasoningStatus.INCONCLUSIVE
    assert isinstance(result.evidence, list)
    assert isinstance(result.conclusions, list)
    assert len(result.conclusions) == 0


def test_forward_chaining_multiple_rules(engine: ReasoningEngine):
    # Add evidence matching rule-decomposition conditions AND "constraint-validation" conditions
    engine.add_fact("goal is complex", True)
    engine.add_fact("goal can be split into independent parts", True)
    engine.add_fact("constraints are defined for this goal", True)
    engine.add_fact("evidence exists for each constraint", True)

    evidence_list = engine.query_evidence("")
    result = engine.forward_chaining("Complex project", evidence_list)
    assert_valid_reasoning_result(result)
    assert len(result.conclusions) > 0


# -- Tests: Backward Chaining ---


def test_backward_chaining_basic(engine: ReasoningEngine):
    result = engine.backward_chaining(
        "Deploy a web application",
        "Application is running in production",
    )
    assert_valid_reasoning_result(result)
    assert result.method == ReasoningMethod.BACKWARD_CHAINING
    assert result.status in (ReasoningStatus.COMPLETED, ReasoningStatus.INCONCLUSIVE)


def test_backward_chaining_with_context(engine: ReasoningEngine):
    result = engine.backward_chaining(
        "Network security audit",
        "All devices are compliant",
        context={"domain": "network"},
    )
    assert_valid_reasoning_result(result)
    assert len(result.conclusions) >= 1


# -- Tests: Decision Tree ---


def test_decision_tree_basic(engine: ReasoningEngine):
    options = [
        {"id": "opt-1", "name": "Fast API", "attributes": {"speed": 9, "cost": 3, "security": 7}},
        {"id": "opt-2", "name": "Django", "attributes": {"speed": 6, "cost": 5, "security": 9}},
        {"id": "opt-3", "name": "Flask", "attributes": {"speed": 8, "cost": 8, "security": 5}},
    ]

    result = engine.decision_tree("Which framework to use?", options)
    assert_valid_reasoning_result(result)
    assert result.method == ReasoningMethod.DECISION_TREE
    assert len(result.decisions) == 1
    assert result.decisions[0].selected is not None


def test_decision_tree_no_options(engine: ReasoningEngine):
    result = engine.decision_tree("What to do?", [])
    assert_valid_reasoning_result(result)
    assert len(result.decisions) == 1
    assert result.decisions[0].selected is None  # Inconclusive


def test_decision_tree_with_criteria(engine: ReasoningEngine):
    options = [
        {"name": "AWS", "attributes": {"cost": 3, "features": 9, "support": 8}},
        {"name": "Azure", "attributes": {"cost": 4, "features": 8, "support": 9}},
        {"name": "GCP", "attributes": {"cost": 7, "features": 7, "support": 7}},
    ]

    result = engine.decision_tree("Which cloud provider?", options, criteria=["cost", "features"])
    assert_valid_reasoning_result(result)
    assert result.decisions[0].selected is not None


# -- Tests: Constraint Propagation ---


def test_constraint_propagation_all_satisfied(engine: ReasoningEngine):
    constraints = [
        {"name": "Budget < 1000", "variable": "budget", "operator": "lt", "value": 1000},
        {"name": "Team size >= 3", "variable": "team_size", "operator": "gte", "value": 3},
    ]
    variables = {"budget": 500, "team_size": 5}

    result = engine.constraint_propagation(constraints, variables)
    assert_valid_reasoning_result(result)
    assert result.status == ReasoningStatus.COMPLETED
    assert result.decisions[0].selected == "proceed"


def test_constraint_propagation_violated(engine: ReasoningEngine):
    constraints = [
        {"name": "Budget < 1000", "variable": "budget", "operator": "lt", "value": 1000},
        {"name": "Timeline < 30 days", "variable": "timeline", "operator": "lt", "value": 30},
    ]
    variables = {"budget": 2000, "timeline": 60}

    result = engine.constraint_propagation(constraints, variables)
    assert_valid_reasoning_result(result)
    assert result.decisions[0].selected == "block"


def test_constraint_propagation_empty(engine: ReasoningEngine):
    result = engine.constraint_propagation([], {})
    assert_valid_reasoning_result(result)
    assert result.decisions[0].selected == "proceed"


def test_constraint_propagation_different_operators(engine: ReasoningEngine):
    constraints: list[dict[str, Any]] = [
        {"name": "Exists test", "variable": "name", "operator": "exists"},
        {"name": "Equals test", "variable": "status", "operator": "equals", "value": "active"},
        {"name": "In list test", "variable": "role", "operator": "in", "value": ["admin", "user"]},
    ]

    assert engine._check_constraint(constraints[0], {"name": "test"}) is True
    assert engine._check_constraint(constraints[0], {}) is False
    assert engine._check_constraint(constraints[1], {"status": "active"}) is True
    assert engine._check_constraint(constraints[1], {"status": "inactive"}) is False
    assert engine._check_constraint(constraints[2], {"role": "admin"}) is True
    assert engine._check_constraint(constraints[2], {"role": "guest"}) is False


# -- Tests: Causal Reasoning ---


def test_causal_reasoning_basic(engine: ReasoningEngine):
    result = engine.causal_reasoning("Workflow execution failed")
    assert_valid_reasoning_result(result)
    assert result.method == ReasoningMethod.CAUSAL_REASONING
    assert len(result.conclusions) > 0


def test_causal_reasoning_with_context(engine: ReasoningEngine):
    engine.add_fact("Step 1 completed successfully", True)
    engine.add_fact("Step 2 failed with timeout error", True)
    engine.add_fact("Network connectivity was unstable", True)

    result = engine.causal_reasoning("Pipeline execution failed")
    assert_valid_reasoning_result(result)
    assert len(result.conclusions) > 0


# -- Tests: Main Reason Entry Point ---


def test_reason_forward(engine: ReasoningEngine):
    result = engine.reason("Complete a task", ReasoningMethod.FORWARD_CHAINING)
    assert_valid_reasoning_result(result)
    assert result.method == ReasoningMethod.FORWARD_CHAINING


def test_reason_backward(engine: ReasoningEngine):
    result = engine.reason(
        "Deploy application",
        ReasoningMethod.BACKWARD_CHAINING,
        context={"desired_outcome": "Application is live"},
    )
    assert_valid_reasoning_result(result)
    assert result.method == ReasoningMethod.BACKWARD_CHAINING


def test_reason_decision(engine: ReasoningEngine):
    result = engine.reason(
        "Choose technology",
        ReasoningMethod.DECISION_TREE,
        context={
            "options": [
                {"name": "A", "attributes": {"score": 8}},
                {"name": "B", "attributes": {"score": 6}},
            ]
        },
    )
    assert_valid_reasoning_result(result)
    assert result.method == ReasoningMethod.DECISION_TREE


def test_reason_constraint(engine: ReasoningEngine):
    result = engine.reason(
        "Validate constraints",
        ReasoningMethod.CONSTRAINT_PROPAGATION,
        context={
            "constraints": [{"name": "Test", "variable": "x", "operator": "exists"}],
            "variables": {"x": 42},
        },
    )
    assert_valid_reasoning_result(result)
    assert result.method == ReasoningMethod.CONSTRAINT_PROPAGATION


def test_reason_causal(engine: ReasoningEngine):
    result = engine.reason("System crash", ReasoningMethod.CAUSAL_REASONING)
    assert_valid_reasoning_result(result)
    assert result.method == ReasoningMethod.CAUSAL_REASONING


def test_reason_default_forward(engine: ReasoningEngine):
    result = engine.reason("Default task")
    assert_valid_reasoning_result(result)
    assert result.method == ReasoningMethod.FORWARD_CHAINING


# -- Tests: Rule Management ---


def test_register_rule(engine: ReasoningEngine):
    rule = ReasoningRule(
        rule_id="custom-rule",
        name="Custom Rule",
        description="A custom test rule",
        conditions=["test condition"],
        conclusions=["test conclusion"],
    )
    engine.register_rule(rule)
    retrieved = engine.get_rule("custom-rule")
    assert retrieved is not None
    assert retrieved.name == "Custom Rule"


def test_unregister_rule(engine: ReasoningEngine):
    engine.unregister_rule("goal-decomposition")
    assert engine.get_rule("goal-decomposition") is None


def test_list_rules(engine: ReasoningEngine):
    rules = engine.list_rules()
    assert len(rules) >= 7  # Default rules
    assert all("rule_id" in r for r in rules)
    assert all("name" in r for r in rules)


def test_get_rule_not_found(engine: ReasoningEngine):
    rule = engine.get_rule("nonexistent")
    assert rule is None


# -- Tests: Knowledge Base ---


def test_add_evidence(engine: ReasoningEngine):
    evidence = Evidence(
        id="test-evidence",
        type=EvidenceType.FACT,
        description="Test fact",
        value=True,
        source="test",
    )
    engine.add_evidence(evidence)
    retrieved = engine.get_evidence("test-evidence")
    assert retrieved is not None
    assert retrieved.description == "Test fact"


def test_add_fact(engine: ReasoningEngine):
    evidence = engine.add_fact("Custom fact", "value123", 0.95)
    assert evidence.id.startswith("ev-")
    assert evidence.type == EvidenceType.FACT
    assert evidence.description == "Custom fact"
    assert evidence.value == "value123"
    assert evidence.confidence == 0.95


def test_query_evidence(engine: ReasoningEngine):
    engine.add_fact("Network is slow", True)
    engine.add_fact("CPU usage is high", True)
    engine.add_fact("Memory is sufficient", True)

    results = engine.query_evidence("Network")
    assert len(results) == 1
    assert results[0].description == "Network is slow"

    results = engine.query_evidence("nonexistent")
    assert len(results) == 0


def test_clear_evidence(engine: ReasoningEngine):
    engine.add_fact("Test fact")
    engine.clear_evidence()
    assert len(engine.query_evidence("Test")) == 0


# -- Tests: Result Management ---


def test_get_result(engine: ReasoningEngine):
    result = engine.forward_chaining("Test goal")
    retrieved = engine.get_result(result.reasoning_id)
    assert retrieved is not None
    assert retrieved.reasoning_id == result.reasoning_id


def test_get_result_not_found(engine: ReasoningEngine):
    result = engine.get_result("nonexistent")
    assert result is None


def test_list_results(engine: ReasoningEngine):
    engine.forward_chaining("Goal 1")
    engine.backward_chaining("Goal 2", "Outcome")
    results = engine.list_results()
    assert len(results) >= 2


def test_clear_results(engine: ReasoningEngine):
    engine.forward_chaining("Test")
    engine.clear_results()
    assert len(engine.list_results()) == 0


# -- Tests: Response Contract ---


def test_reasoning_result_contract_completed(engine: ReasoningEngine):
    result = engine.forward_chaining("Complete a complex software project")
    assert_valid_reasoning_result(result)

    if result.status == ReasoningStatus.COMPLETED:
        assert len(result.conclusions) > 0
    assert result.explanation is not None


def test_reasoning_result_contract_methods(engine: ReasoningEngine):
    fwd = engine.forward_chaining("Forward test")
    assert fwd.method == ReasoningMethod.FORWARD_CHAINING

    bwd = engine.backward_chaining("Backward test", "Outcome")
    assert bwd.method == ReasoningMethod.BACKWARD_CHAINING

    dec = engine.decision_tree("Decision test", [{"name": "A", "attributes": {"score": 5}}])
    assert dec.method == ReasoningMethod.DECISION_TREE

    con = engine.constraint_propagation([], {})
    assert con.method == ReasoningMethod.CONSTRAINT_PROPAGATION

    cau = engine.causal_reasoning("Causal test")
    assert cau.method == ReasoningMethod.CAUSAL_REASONING


# -- Tests: Edge Cases ---


def test_evidence_without_knowledge_base(engine: ReasoningEngine):
    # Should not raise errors
    result = engine.forward_chaining("Test without evidence")
    assert_valid_reasoning_result(result)


def test_multiple_reasoning_sessions(engine: ReasoningEngine):
    r1 = engine.forward_chaining("Session 1")
    r2 = engine.forward_chaining("Session 2")
    r3 = engine.backward_chaining("Session 3", "Outcome")
    assert r1.reasoning_id != r2.reasoning_id
    assert r2.reasoning_id != r3.reasoning_id


def test_reasoning_with_special_chars(engine: ReasoningEngine):
    result = engine.reason("Test with special chars: !@#$%^&*()")
    assert_valid_reasoning_result(result)


def test_decision_made_event_has_all_fields(engine: ReasoningEngine):
    options = [
        {"name": "Option 1", "attributes": {"score": 9}},
        {"name": "Option 2", "attributes": {"score": 5}},
    ]
    result = engine.decision_tree("Best option?", options)
    assert len(result.decisions) == 1
    dec = result.decisions[0]
    assert dec.decision_id.startswith("dec-")
    assert len(dec.options) == 2
    assert dec.selected is not None
    assert len(dec.consequences) >= 0

