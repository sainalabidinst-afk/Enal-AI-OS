"""
Tests for CapabilityGraph, TaskPlanner, and ExecutionPlanner
ensuring the "General Intelligence Layer" behaves correctly.
"""

import pytest

from apps.organization.capability_graph import (
    capability_graph,
)
from apps.organization.execution_planner import (
    execution_planner,
)
from apps.organization.task_planner import SubTask, TaskPlan, task_planner
from apps.society.intent_router import Intent, IntentComplexity, IntentDomain


@pytest.fixture(autouse=True)
def reset_graph():
    yield
    capability_graph._capabilities.clear()
    capability_graph._subtask_templates.clear()
    capability_graph._register_defaults()


def build_intent(domain: IntentDomain, raw_input: str = "Build a web app", complexity: IntentComplexity = IntentComplexity.MEDIUM) -> Intent:
    return Intent(
        raw_input=raw_input,
        domain=domain,
        complexity=complexity,
        confidence=0.8,
        entities=["python"],
        constraints=[],
    )


#region CapabilityGraph


def test_get_subtask_templates_returns_coding_templates():
    templates = capability_graph.get_subtask_templates("code")
    assert len(templates) > 0
    names = [t.name for t in templates]
    assert "Requirement Analysis" in names
    assert "Architecture Design" in names


def test_get_subtask_templates_fallback_for_unknown_domain():
    templates = capability_graph.get_subtask_templates("unknown-domain")
    assert templates == []


def test_get_required_skills_for_capability():
    skills = capability_graph.get_required_skills("config-analysis")
    assert "config-analysis" in skills
    assert "parsing" in skills


def test_get_dependencies_returns_empty_for_root_capabilities():
    deps = capability_graph.get_dependencies("network-design")
    assert deps == []


def test_get_dependencies_returns_parents_for_dependent_capabilities():
    deps = capability_graph.get_dependencies("security-audit")
    assert "config-analysis" in deps


def test_get_related_capabilities_returns_siblings():
    related = capability_graph.get_related_capabilities("security-audit")
    assert "compliance-check" in related


def test_suggest_capabilities_scores_by_skill_overlap():
    suggestions = capability_graph.suggest_capabilities(["python", "database"])
    assert len(suggestions) > 0
    assert isinstance(suggestions[0], str)


def test_get_all_capabilities_returns_nonempty_list():
    caps = capability_graph.get_all_capabilities()
    assert len(caps) > 0
    assert "config-analysis" in caps


#endregion


#region TaskPlanner


def test_task_planner_returns_plan_for_coding_intent():
    intent = build_intent(IntentDomain.CODE, "Build a REST API", IntentComplexity.COMPLEX)
    plan = task_planner.plan(intent)
    assert plan is not None
    assert plan.domain == IntentDomain.CODE.value
    assert len(plan.subtasks) > 0


def test_task_planner_returns_plan_for_network_intent():
    intent = build_intent(IntentDomain.NETWORK, "Analyze routers", IntentComplexity.MEDIUM)
    plan = task_planner.plan(intent)
    assert plan is not None
    assert plan.domain == IntentDomain.NETWORK.value
    assert len(plan.subtasks) > 0


def test_task_planner_returns_simple_plan_for_unknown_domain():
    intent = build_intent(IntentDomain.GENERAL)
    plan = task_planner.plan(intent)
    assert plan is not None
    assert len(plan.subtasks) >= 1
    assert plan.strategy == "serial"


def test_task_planner_complexity_impacts_subtask_count():
    simple = build_intent(IntentDomain.CODE, complexity=IntentComplexity.SIMPLE)
    complex_ = build_intent(IntentDomain.CODE, complexity=IntentComplexity.COMPLEX)
    plan_simple = task_planner.plan(simple)
    plan_complex = task_planner.plan(complex_)
    assert len(plan_complex.subtasks) >= len(plan_simple.subtasks)


def test_task_planner_refine_limits_by_latency():
    intent = build_intent(IntentDomain.CODE)
    plan = task_planner.plan(intent)
    refined = task_planner.refine(plan, {"max_latency_minutes": 30})
    assert all(s.estimated_duration_minutes <= 30 for s in refined.subtasks)


#endregion


#region ExecutionPlanner


def test_execution_planner_serial_strategy_produces_serial_stages():
    plan = TaskPlan(intent=build_intent(IntentDomain.CODE), subtasks=[], strategy="serial")
    plan.subtasks = [
        SubTask(subtask_id="a", name="A", description="A", priority=1, can_parallelize=False, depends_on=[]),
        SubTask(subtask_id="b", name="B", description="B", priority=2, can_parallelize=False, depends_on=["a"]),
    ]
    plan.estimated_total_minutes = sum(s.estimated_duration_minutes for s in plan.subtasks)
    result = execution_planner.plan(plan)
    assert len(result.stages) == 2
    assert all(stage.mode == "serial" for stage in result.stages)


def test_execution_planner_parallel_strategy_produces_single_stage():
    plan = TaskPlan(intent=build_intent(IntentDomain.CODE), subtasks=[], strategy="parallel")
    plan.subtasks = [
        SubTask(subtask_id="a", name="A", description="A", can_parallelize=True),
        SubTask(subtask_id="b", name="B", description="B", can_parallelize=True),
    ]
    plan.estimated_total_minutes = sum(s.estimated_duration_minutes for s in plan.subtasks)
    result = execution_planner.plan(plan)
    assert len(result.stages) == 1
    assert result.stages[0].mode == "parallel"


def test_execution_planner_mixed_strategy_groups_serial_then_parallel():
    plan = TaskPlan(intent=build_intent(IntentDomain.CODE), subtasks=[], strategy="mixed")
    plan.subtasks = [
        SubTask(subtask_id="a", name="A", description="A", priority=1, can_parallelize=False),
        SubTask(subtask_id="b", name="B", description="B", priority=2, can_parallelize=True),
        SubTask(subtask_id="c", name="C", description="C", priority=3, can_parallelize=True),
    ]
    plan.estimated_total_minutes = sum(s.estimated_duration_minutes for s in plan.subtasks)
    result = execution_planner.plan(plan)
    assert len(result.stages) == 2
    modes = [stage.mode for stage in result.stages]
    assert "serial" in modes
    assert "parallel" in modes


#endregion
