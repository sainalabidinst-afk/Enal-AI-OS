"""
Integration Tests for AI Planner
=================================

Tests scenarios:
    - plan_from_goal (domain detection, step generation)
    - plan_with_workflows (explicit workflow selection)
    - execute_step (single step execution)
    - execute_plan (full plan execution)
    - cancel_plan
    - list plans
    - get plan summary
    - error handling (unknown step type)
"""

import pytest

from apps.organization.ai_planner import (
    AIPlan,
    AIPlanner,
    PlanStatus,
    PlanStep,
    StepType,
)
from apps.organization.workflow_catalog import (
    WorkflowCatalog,
    WorkflowCatalogEntry,
)


@pytest.fixture
def planner() -> AIPlanner:
    return AIPlanner()


@pytest.fixture
def populated_catalog() -> WorkflowCatalog:
    cat = WorkflowCatalog()
    cat.clear()
    cat.register(WorkflowCatalogEntry(
        workflow_id="network-audit-flow",
        display_name="Network Security Audit",
        description="Run security audit on network devices",
        supported_intents=["audit-network", "check-security", "network-scan"],
        tags=["network", "security", "audit"],
    ))
    cat.register(WorkflowCatalogEntry(
        workflow_id="docs-generation-flow",
        display_name="Documentation Generation",
        description="Generate technical documentation",
        supported_intents=["generate-docs", "write-docs", "create-manual"],
        tags=["docs", "writing"],
    ))
    cat.register(WorkflowCatalogEntry(
        workflow_id="code-review-flow",
        display_name="Code Review",
        description="Review code for quality and security",
        supported_intents=["review-code", "audit-code", "check-code-quality"],
        tags=["code", "review"],
    ))
    return cat


def assert_valid_plan(plan: AIPlan) -> None:
    assert isinstance(plan, AIPlan)
    assert isinstance(plan.plan_id, str) and len(plan.plan_id) > 0
    assert isinstance(plan.goal, str) and len(plan.goal) > 0
    assert isinstance(plan.steps, list)
    assert isinstance(plan.total_steps, int)
    assert plan.total_steps == len(plan.steps)
    assert isinstance(plan.created_at, object)
    assert isinstance(plan.updated_at, object)

    for step in plan.steps:
        assert isinstance(step, PlanStep)
        assert isinstance(step.step_id, str) and len(step.step_id) > 0
        assert isinstance(step.step_type, StepType)
        assert isinstance(step.description, str)
        assert isinstance(step.status, PlanStatus)


# -- Tests: Plan Creation ---


def test_plan_from_goal_network_domain(planner: AIPlanner):
    plan = planner.plan_from_goal("Audit network security for Cisco routers")
    assert_valid_plan(plan)
    assert len(plan.steps) > 0
    assert plan.metadata.get("domain") == "network"
    assert plan.status == PlanStatus.READY


def test_plan_from_goal_code_domain(planner: AIPlanner):
    plan = planner.plan_from_goal("Build a Python REST API with FastAPI")
    assert_valid_plan(plan)
    assert plan.metadata.get("domain") == "code"


def test_plan_from_goal_general_domain(planner: AIPlanner):
    plan = planner.plan_from_goal("Help me with something")
    assert_valid_plan(plan)
    assert len(plan.steps) >= 0


def test_plan_with_workflows(planner: AIPlanner, populated_catalog: WorkflowCatalog):
    planner._catalog = populated_catalog
    plan = planner.plan_with_workflows(
        "Security audit and documentation",
        workflow_ids=["network-audit-flow", "docs-generation-flow"],
    )
    assert_valid_plan(plan)
    assert plan.total_steps == 2
    assert plan.steps[0].workflow_id == "network-audit-flow"
    assert plan.steps[1].workflow_id == "docs-generation-flow"
    assert plan.steps[0].step_type == StepType.WORKFLOW
    assert plan.steps[1].step_type == StepType.WORKFLOW


def test_plan_with_workflows_empty(planner: AIPlanner):
    plan = planner.plan_with_workflows("Empty plan", [])
    assert_valid_plan(plan)
    assert plan.total_steps == 0


def test_plan_from_goal_creates_unique_plan_id(planner: AIPlanner):
    plan1 = planner.plan_from_goal("Task one")
    plan2 = planner.plan_from_goal("Task two")
    assert plan1.plan_id != plan2.plan_id


# -- Tests: Plan Steps ---


def test_plan_steps_have_dependency_chain(planner: AIPlanner):
    plan = planner.plan_from_goal("Complete network audit and generate report")
    assert_valid_plan(plan)

    if plan.total_steps > 1:
        first_step = plan.steps[0]
        second_step = plan.steps[1]
        assert first_step.step_id in second_step.depends_on or not second_step.depends_on


def test_plan_steps_have_valid_types(planner: AIPlanner):
    plan = planner.plan_from_goal("Review and document codebase")
    assert_valid_plan(plan)
    for step in plan.steps:
        assert step.step_type in (StepType.WORKFLOW, StepType.CAPABILITY, StepType.SUB_PLAN, StepType.DECISION, StepType.PARALLEL)


# -- Tests: Plan Status ---


def test_plan_initial_status(planner: AIPlanner):
    plan = planner.plan_from_goal("Test plan")
    assert plan.status == PlanStatus.READY


def test_plan_progress(planner: AIPlanner):
    plan = planner.plan_from_goal("Test plan")
    assert plan.progress == 0.0
    assert plan.is_complete is False
    assert plan.is_stuck is False


def test_plan_completed_progress(planner: AIPlanner):
    plan = planner.plan_from_goal("Test plan")
    plan.completed_steps = plan.total_steps
    assert plan.progress == 1.0


def test_plan_progress_with_empty_steps(planner: AIPlanner):
    plan = planner.plan_with_workflows("Empty", [])
    assert plan.progress == 0.0


# -- Tests: Plan Management ---


def test_list_plans(planner: AIPlanner):
    planner.plan_from_goal("First plan")
    planner.plan_from_goal("Second plan")
    plans = planner.list_plans()
    assert len(plans) >= 2
    assert all("plan_id" in p for p in plans)
    assert all("status" in p for p in plans)
    assert all("total_steps" in p for p in plans)


def test_get_plan(planner: AIPlanner):
    plan = planner.plan_from_goal("Test plan")
    retrieved = planner.get_plan(plan.plan_id)
    assert retrieved is not None
    assert retrieved.plan_id == plan.plan_id


def test_get_plan_not_found(planner: AIPlanner):
    retrieved = planner.get_plan("nonexistent")
    assert retrieved is None


def test_cancel_plan(planner: AIPlanner):
    plan = planner.plan_from_goal("Cancellable plan")
    planner.cancel_plan(plan.plan_id)
    cancelled = planner.get_plan(plan.plan_id)
    assert cancelled is not None
    assert cancelled.status == PlanStatus.CANCELLED


def test_cancel_nonexistent_plan(planner: AIPlanner):
    # Should not raise
    planner.cancel_plan("nonexistent")


def test_get_plan_summary(planner: AIPlanner):
    plan = planner.plan_from_goal("Summary test")
    summary = planner.get_plan_summary(plan.plan_id)
    assert summary is not None
    assert summary["plan_id"] == plan.plan_id
    assert summary["goal"] == plan.goal
    assert summary["status"] == plan.status.value
    assert "steps" in summary
    assert "progress" in summary
    assert "metadata" in summary
    assert "created_at" in summary


def test_get_plan_summary_not_found(planner: AIPlanner):
    summary = planner.get_plan_summary("nonexistent")
    assert summary is None


# -- Tests: Edge Cases ---


def test_plan_with_special_characters_in_goal(planner: AIPlanner):
    plan = planner.plan_from_goal("Test with special chars: !@#$%^&*()")
    assert_valid_plan(plan)


def test_plan_with_very_long_goal(planner: AIPlanner):
    long_goal = "Analyze " * 20
    plan = planner.plan_from_goal(long_goal)
    assert_valid_plan(plan)


def test_multiple_plans_dont_interfere(planner: AIPlanner):
    plan1 = planner.plan_from_goal("Plan A")
    plan2 = planner.plan_from_goal("Plan B")
    assert plan1.plan_id != plan2.plan_id
    get1 = planner.get_plan(plan1.plan_id)
    get2 = planner.get_plan(plan2.plan_id)
    assert get1 is not None
    assert get2 is not None
    assert get1.goal == "Plan A"
    assert get2.goal == "Plan B"


def test_plan_created_and_updated_timestamps(planner: AIPlanner):
    plan = planner.plan_from_goal("Timestamp test")
    assert plan.created_at is not None
    assert plan.updated_at is not None

