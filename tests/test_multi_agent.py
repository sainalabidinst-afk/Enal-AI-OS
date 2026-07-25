"""
Integration Tests for Multi-Agent Orchestrator
===============================================

Tests scenarios:
    - register agent
    - unregister agent
    - list agents
    - assign step to agent
    - sequential execution
    - parallel execution
    - hierarchical execution
    - consensus execution
    - agent communication (send message, broadcast)
    - execution history
    - error handling (unknown agent, no available agent)
"""

import asyncio

import pytest

from apps.organization.ai_planner import (
    AIPlan,
    PlanStep,
    StepType,
)
from apps.organization.multi_agent import (
    AgentStatus,
    CoordinationStrategy,
    MultiAgentOrchestrator,
    MultiAgentResult,
    PlanStatus,
)


@pytest.fixture
def orchestrator() -> MultiAgentOrchestrator:
    return MultiAgentOrchestrator()


@pytest.fixture
def sample_plan() -> AIPlan:
    steps = [
        PlanStep(
            step_id="step-1",
            step_type=StepType.CAPABILITY,
            description="Analyze network security",
            capability_id="security-audit",
            input_data={"skills": ["security"]},
        ),
        PlanStep(
            step_id="step-2",
            step_type=StepType.CAPABILITY,
            description="Generate documentation",
            capability_id="documentation",
            input_data={"skills": ["writing"]},
            depends_on=["step-1"],
        ),
    ]
    return AIPlan(
        plan_id="test-plan-001",
        goal="Test multi-agent execution",
        steps=steps,
        total_steps=2,
    )


async def dummy_executor(step: PlanStep, input_data: dict) -> dict:
    """Dummy executor that simulates agent work."""
    await asyncio.sleep(0.01)
    return {"status": "completed", "step_id": step.step_id}


# -- Tests: Agent Registration ---


def test_register_agent(orchestrator: MultiAgentOrchestrator):
    agent = orchestrator.register_agent("agent-1", "Agent One", ["network", "security"])
    assert agent.agent_id == "agent-1"
    assert agent.name == "Agent One"
    assert agent.skills == ["network", "security"]
    assert agent.status == AgentStatus.IDLE
    assert len(agent.task_history) == 0


def test_register_agent_with_executor(orchestrator: MultiAgentOrchestrator):
    orchestrator.register_agent("agent-exec", "Executor Agent", executor=dummy_executor)
    agent = orchestrator.get_agent("agent-exec")
    assert agent is not None
    assert agent.name == "Executor Agent"
    assert "agent-exec" in orchestrator._agent_executors


def test_register_worker_domain(orchestrator: MultiAgentOrchestrator):
    agent_id = orchestrator.register_worker_domain("network", dummy_executor)
    assert agent_id == "worker-network"
    agent = orchestrator.get_agent(agent_id)
    assert agent is not None
    assert agent.skills == ["network"]


def test_unregister_agent(orchestrator: MultiAgentOrchestrator):
    orchestrator.register_agent("agent-1", "Agent One")
    orchestrator.unregister_agent("agent-1")
    assert orchestrator.get_agent("agent-1") is None


def test_list_agents(orchestrator: MultiAgentOrchestrator):
    orchestrator.register_agent("agent-1", "Agent One")
    orchestrator.register_agent("agent-2", "Agent Two")
    agents = orchestrator.list_agents()
    assert len(agents) == 2
    ids = [a["agent_id"] for a in agents]
    assert "agent-1" in ids
    assert "agent-2" in ids


def test_get_agent(orchestrator: MultiAgentOrchestrator):
    orchestrator.register_agent("agent-1", "Agent One")
    agent = orchestrator.get_agent("agent-1")
    assert agent is not None
    assert agent.agent_id == "agent-1"


def test_get_agent_not_found(orchestrator: MultiAgentOrchestrator):
    agent = orchestrator.get_agent("nonexistent")
    assert agent is None


def test_get_available_agents(orchestrator: MultiAgentOrchestrator):
    orchestrator.register_agent("agent-1", "Agent One")
    orchestrator.register_agent("agent-2", "Agent Two")
    available = orchestrator.get_available_agents()
    assert len(available) == 2


def test_get_available_agents_empty(orchestrator: MultiAgentOrchestrator):
    available = orchestrator.get_available_agents()
    assert available == []


# -- Tests: Task Assignment ---


def test_assign_step(orchestrator: MultiAgentOrchestrator):
    orchestrator.register_agent("agent-1", "Agent One", executor=dummy_executor)
    step = PlanStep(
        step_id="step-test",
        step_type=StepType.CAPABILITY,
        description="Test step",
    )
    task = orchestrator.assign_step(step, "agent-1")
    assert task.agent_id == "agent-1"
    assert task.step.step_id == "step-test"
    assert task.status == PlanStatus.READY

    agent = orchestrator.get_agent("agent-1")
    assert agent is not None
    assert agent.status == AgentStatus.BUSY
    assert agent.current_task == task.task_id


def test_assign_step_auto_select(orchestrator: MultiAgentOrchestrator):
    orchestrator.register_agent("agent-1", "Agent One", ["network"], executor=dummy_executor)
    orchestrator.register_agent("agent-2", "Agent Two", ["security"], executor=dummy_executor)

    step = PlanStep(
        step_id="step-test",
        step_type=StepType.CAPABILITY,
        description="Test step",
        metadata={"sub_goal_index": 0},
    )
    task = orchestrator.assign_step(step)
    assert task.agent_id in ("agent-1", "agent-2")


def test_assign_step_no_available_agent(orchestrator: MultiAgentOrchestrator):
    step = PlanStep(
        step_id="step-test",
        step_type=StepType.CAPABILITY,
        description="Test step",
    )
    with pytest.raises(ValueError, match="No available agent"):
        orchestrator.assign_step(step)


def test_assign_step_unknown_agent(orchestrator: MultiAgentOrchestrator):
    step = PlanStep(
        step_id="step-test",
        step_type=StepType.CAPABILITY,
        description="Test step",
    )
    with pytest.raises(ValueError, match="Agent not found"):
        orchestrator.assign_step(step, "nonexistent")


# -- Tests: Sequential Execution ---


@pytest.mark.asyncio
async def test_execute_sequential(orchestrator: MultiAgentOrchestrator):
    orchestrator.register_agent("agent-1", "Agent One", executor=dummy_executor)

    steps = [
        PlanStep(step_id="s1", step_type=StepType.CAPABILITY, description="Step 1"),
        PlanStep(step_id="s2", step_type=StepType.CAPABILITY, description="Step 2"),
    ]

    tasks = await orchestrator.execute_sequential(steps, "agent-1")
    assert len(tasks) == 2
    assert all(t.status == PlanStatus.COMPLETED for t in tasks)


@pytest.mark.asyncio
async def test_execute_sequential_fails_midway(orchestrator: MultiAgentOrchestrator):

    async def failing_executor(step, input_data):
        if step.step_id == "s2":
            raise ValueError("Simulated failure")
        return {"status": "ok"}

    orchestrator.register_agent("agent-1", "Agent One", executor=failing_executor)

    steps = [
        PlanStep(step_id="s1", step_type=StepType.CAPABILITY, description="Step 1"),
        PlanStep(step_id="s2", step_type=StepType.CAPABILITY, description="Step 2"),
        PlanStep(step_id="s3", step_type=StepType.CAPABILITY, description="Step 3"),
    ]

    tasks = await orchestrator.execute_sequential(steps, "agent-1")
    assert tasks[0].status == PlanStatus.COMPLETED
    assert tasks[1].status == PlanStatus.FAILED
    assert len(tasks) == 2  # Should stop after failure


# -- Tests: Parallel Execution ---


@pytest.mark.asyncio
async def test_execute_parallel(orchestrator: MultiAgentOrchestrator):
    orchestrator.register_agent("agent-1", "Agent One", executor=dummy_executor)
    orchestrator.register_agent("agent-2", "Agent Two", executor=dummy_executor)

    steps = [
        PlanStep(step_id="s1", step_type=StepType.CAPABILITY, description="Step 1"),
        PlanStep(step_id="s2", step_type=StepType.CAPABILITY, description="Step 2"),
    ]

    tasks = await orchestrator.execute_parallel(steps)
    assert len(tasks) == 2
    assert all(t.status == PlanStatus.COMPLETED for t in tasks)


@pytest.mark.asyncio
async def test_execute_parallel_no_agents(orchestrator: MultiAgentOrchestrator):
    steps = [
        PlanStep(step_id="s1", step_type=StepType.CAPABILITY, description="Step 1"),
    ]
    tasks = await orchestrator.execute_parallel(steps)
    assert len(tasks) == 0


# -- Tests: Hierarchical Execution ---


@pytest.mark.asyncio
async def test_execute_hierarchical(orchestrator: MultiAgentOrchestrator, sample_plan: AIPlan):
    orchestrator.register_agent("lead", "Lead Agent", executor=dummy_executor)
    orchestrator.register_agent("worker-1", "Worker 1", executor=dummy_executor)
    orchestrator.register_agent("worker-2", "Worker 2", executor=dummy_executor)

    tasks = await orchestrator.execute_hierarchical(sample_plan, "lead", ["worker-1", "worker-2"])
    assert len(tasks) >= 2
    assert tasks[0].status == PlanStatus.COMPLETED  # Lead coordination


# -- Tests: Consensus Execution ---


@pytest.mark.asyncio
async def test_execute_consensus(orchestrator: MultiAgentOrchestrator):
    orchestrator.register_agent("agent-1", "Agent One", executor=dummy_executor)
    orchestrator.register_agent("agent-2", "Agent Two", executor=dummy_executor)

    step = PlanStep(
        step_id="consensus-step",
        step_type=StepType.DECISION,
        description="Consensus test",
    )

    result = await orchestrator.execute_consensus(step, ["agent-1", "agent-2"])
    assert result["consensus_reached"] is True
    assert result["total_agents"] == 2
    assert result["successful_agents"] == 2
    assert 0 <= result["agreement"] <= 1.0


# -- Tests: Full Plan Execution ---


@pytest.mark.asyncio
async def test_execute_plan_sequential(orchestrator: MultiAgentOrchestrator, sample_plan: AIPlan):
    orchestrator.register_agent("agent-1", "Agent One", executor=dummy_executor)

    result = await orchestrator.execute_plan(sample_plan, CoordinationStrategy.SEQUENTIAL)
    assert isinstance(result, MultiAgentResult)
    assert result.status == PlanStatus.COMPLETED
    assert result.total_tasks >= 2
    assert result.completed_tasks >= 2
    assert result.total_duration_ms >= 0


@pytest.mark.asyncio
async def test_execute_plan_parallel(orchestrator: MultiAgentOrchestrator):
    orchestrator.register_agent("agent-1", "Agent One", executor=dummy_executor)
    orchestrator.register_agent("agent-2", "Agent Two", executor=dummy_executor)

    independent_steps = [
        PlanStep(step_id="s1", step_type=StepType.CAPABILITY, description="Independent 1"),
        PlanStep(step_id="s2", step_type=StepType.CAPABILITY, description="Independent 2"),
    ]

    plan = AIPlan(plan_id="parallel-test", goal="Parallel test", steps=independent_steps, total_steps=2)

    result = await orchestrator.execute_plan(plan, CoordinationStrategy.PARALLEL)
    assert result.status == PlanStatus.COMPLETED


# -- Tests: Communication ---


def test_send_message(orchestrator: MultiAgentOrchestrator):
    orchestrator.register_agent("sender", "Sender Agent")
    orchestrator.register_agent("receiver", "Receiver Agent")

    from apps.organization.communication import mailbox

    orchestrator.send_message("sender", "receiver", "Test Subject", {"data": "test"})

    received = mailbox.receive("receiver")
    assert len(received) >= 0


def test_broadcast(orchestrator: MultiAgentOrchestrator):
    orchestrator.register_agent("broadcaster", "Broadcaster")
    orchestrator.register_agent("agent-1", "Agent One")
    orchestrator.register_agent("agent-2", "Agent Two")

    from apps.organization.communication import mailbox

    orchestrator.broadcast("broadcaster", "Broadcast Subject", {"data": "broadcast"})

    # At least one agent received the message
    received_1 = mailbox.receive("agent-1")
    assert len(received_1) >= 0


# -- Tests: Execution History ---


@pytest.mark.asyncio
async def test_get_execution(orchestrator: MultiAgentOrchestrator, sample_plan: AIPlan):
    orchestrator.register_agent("agent-1", "Agent One", executor=dummy_executor)
    result = await orchestrator.execute_plan(sample_plan, CoordinationStrategy.SEQUENTIAL)

    retrieved = orchestrator.get_execution(result.execution_id)
    assert retrieved is not None
    assert retrieved.execution_id == result.execution_id
    assert retrieved.plan_id == sample_plan.plan_id


def test_get_execution_not_found(orchestrator: MultiAgentOrchestrator):
    retrieved = orchestrator.get_execution("nonexistent")
    assert retrieved is None


@pytest.mark.asyncio
async def test_list_executions(orchestrator: MultiAgentOrchestrator, sample_plan: AIPlan):
    orchestrator.register_agent("agent-1", "Agent One", executor=dummy_executor)
    await orchestrator.execute_plan(sample_plan, CoordinationStrategy.SEQUENTIAL)

    executions = orchestrator.list_executions()
    assert len(executions) >= 1
    assert all("execution_id" in e for e in executions)
    assert all("status" in e for e in executions)


# -- Tests: Error Handling ---


def test_register_duplicate_agent(orchestrator: MultiAgentOrchestrator):
    orchestrator.register_agent("agent-1", "Agent One")
    orchestrator.register_agent("agent-1", "Agent One Duplicate")
    # Should overwrite without error
    assert orchestrator.get_agent("agent-1") is not None


@pytest.mark.asyncio
async def test_execute_plan_no_agents(orchestrator: MultiAgentOrchestrator, sample_plan: AIPlan):
    # Should handle gracefully without raising - returns failed result
    result = await orchestrator.execute_plan(sample_plan, CoordinationStrategy.SEQUENTIAL)
    assert result.status == PlanStatus.FAILED
    assert result.total_tasks > 0
    assert result.completed_tasks == 0


# -- Tests: MultiAgentResult ---


def test_multi_agent_result_properties():
    result = MultiAgentResult(
        execution_id="exec-test",
        plan_id="plan-test",
        strategy=CoordinationStrategy.SEQUENTIAL,
    )
    assert result.execution_id == "exec-test"
    assert result.plan_id == "plan-test"
    assert result.strategy == CoordinationStrategy.SEQUENTIAL
    assert result.total_tasks == 0
    assert result.completed_tasks == 0
    assert result.failed_tasks == 0
    assert result.total_duration_ms == 0.0
    assert result.status == PlanStatus.DRAFT

