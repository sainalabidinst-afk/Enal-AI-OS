"""
Multi-Agent Orchestrator
========================

Coordinates multiple agents/workers to execute plans collaboratively.

Multi-Agent Orchestrator:
    - Manages a pool of workers (agents)
    - Distributes plan steps across workers
    - Handles agent communication and coordination
    - Tracks agent workload and availability
    - Supports parallel and sequential execution
    - Aggregates results from multiple agents

Flow:
    AIPlan with multiple steps
        ↓
    MultiAgentOrchestrator
        ↓
    ├── Assign steps to available agents
    ├── Coordinate dependencies
    ├── Handle agent communication via EventBus
    ├── Monitor progress
    └── Return aggregated results
"""

import asyncio
import logging
import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from apps.organization.ai_planner import (
    AIPlan,
    PlanStatus,
    PlanStep,
    StepType,
)
from apps.organization.communication import (
    Event,
    Message,
    MessageType,
    Priority,
    event_bus,
    mailbox,
)

logger = logging.getLogger(__name__)

# ─── Telemetry Events ───

AGENT_ASSIGNED = "AgentAssigned"
AGENT_TASK_COMPLETED = "AgentTaskCompleted"
AGENT_TASK_FAILED = "AgentTaskFailed"
AGENT_COORDINATION = "AgentCoordination"
MULTI_AGENT_COMPLETED = "MultiAgentCompleted"

# ─── Enums ───


class AgentStatus(str, Enum):
    IDLE = "idle"
    BUSY = "busy"
    OFFLINE = "offline"
    ERROR = "error"


class CoordinationStrategy(str, Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"
    CONSENSUS = "consensus"


# ─── Data Classes ───


@dataclass
class AgentInfo:
    """Information about a registered agent/worker.

    Attributes:
        agent_id: Unique identifier for this agent.
        name: Human-readable name.
        skills: List of skills this agent has.
        status: Current agent status.
        current_task: Current task being executed (if busy).
        task_history: List of completed task IDs.
        capabilities: List of capabilities this agent can execute.
    """
    agent_id: str
    name: str
    skills: list[str] = field(default_factory=list)
    status: AgentStatus = AgentStatus.IDLE
    current_task: str | None = None
    task_history: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)


@dataclass
class AgentTask:
    """A task assigned to an agent.

    Attributes:
        task_id: Unique identifier for this task.
        agent_id: The agent assigned to this task.
        step: The plan step to execute.
        input_data: Input data for this task.
        status: Current status.
        result: Execution result.
        error: Error message if failed.
        started_at: When execution started.
        completed_at: When execution completed.
    """
    task_id: str
    agent_id: str
    step: PlanStep
    input_data: dict[str, Any] = field(default_factory=dict)
    status: PlanStatus = PlanStatus.DRAFT
    result: Any = None
    error: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


@dataclass
class MultiAgentResult:
    """Result of a multi-agent execution.

    Attributes:
        execution_id: Unique identifier for this execution.
        plan_id: The plan that was executed.
        strategy: The coordination strategy used.
        agent_tasks: All tasks assigned to agents.
        aggregated_result: Combined result from all agents.
        total_tasks: Total number of tasks.
        completed_tasks: Number of successfully completed tasks.
        failed_tasks: Number of failed tasks.
        total_duration_ms: Total execution time.
        status: Overall status.
    """
    execution_id: str
    plan_id: str
    strategy: CoordinationStrategy
    agent_tasks: list[AgentTask] = field(default_factory=list)
    aggregated_result: dict[str, Any] = field(default_factory=dict)
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    total_duration_ms: float = 0.0
    status: PlanStatus = PlanStatus.DRAFT


# ─── Multi-Agent Orchestrator ───


class MultiAgentOrchestrator:
    """Orchestrates multiple agents to execute plans collaboratively.

    The orchestrator:
        1. Registers available agents/workers
        2. Assigns plan steps to agents based on skills
        3. Coordinates execution (sequential, parallel, or hierarchical)
        4. Manages agent communication via EventBus/Mailbox
        5. Tracks progress and aggregates results
    """

    def __init__(self):
        self._agents: dict[str, AgentInfo] = {}
        self._agent_executors: dict[str, Callable[..., Awaitable[Any]]] = {}
        self._executions: dict[str, MultiAgentResult] = {}
        self._task_queue: asyncio.Queue = asyncio.Queue()

    # ─── Agent Registration ───

    def register_agent(
        self,
        agent_id: str,
        name: str,
        skills: list[str] | None = None,
        executor: Callable[..., Awaitable[Any]] | None = None,
        capabilities: list[str] | None = None,
    ) -> AgentInfo:
        """Register an agent/worker with the orchestrator.

        Args:
            agent_id: Unique identifier.
            name: Human-readable name.
            skills: List of skills this agent has.
            executor: Async callable to execute tasks with this agent.
            capabilities: List of capabilities this agent can execute.

        Returns:
            The registered AgentInfo.
        """
        agent = AgentInfo(
            agent_id=agent_id,
            name=name,
            skills=skills or [],
            capabilities=capabilities or [],
        )
        self._agents[agent_id] = agent
        if executor:
            self._agent_executors[agent_id] = executor
        logger.info("Agent registered: %s (%s) with %d skills", agent_id, name, len(agent.skills))
        return agent

    def register_worker_domain(self, domain: str, executor: Callable[..., Awaitable[Any]]) -> str:
        """Register a domain worker as an agent.

        Args:
            domain: The domain (e.g., "network", "code").
            executor: The worker's execute function.

        Returns:
            The agent_id.
        """
        agent_id = f"worker-{domain}"
        self.register_agent(
            agent_id=agent_id,
            name=f"{domain.title()} Worker",
            skills=[domain],
            executor=executor,
            capabilities=[domain],
        )
        return agent_id

    def unregister_agent(self, agent_id: str) -> None:
        """Remove an agent from the orchestrator."""
        self._agents.pop(agent_id, None)
        self._agent_executors.pop(agent_id, None)
        logger.info("Agent unregistered: %s", agent_id)

    def get_agent(self, agent_id: str) -> AgentInfo | None:
        """Get agent info by ID."""
        return self._agents.get(agent_id)

    def list_agents(self) -> list[dict[str, Any]]:
        """List all registered agents."""
        return [
            {
                "agent_id": a.agent_id,
                "name": a.name,
                "skills": a.skills,
                "status": a.status.value,
                "current_task": a.current_task,
                "task_count": len(a.task_history),
            }
            for a in self._agents.values()
        ]

    def get_available_agents(self) -> list[AgentInfo]:
        """Get all agents that are currently idle."""
        return [a for a in self._agents.values() if a.status == AgentStatus.IDLE]

    # ─── Task Assignment ───

    def assign_step(
        self,
        step: PlanStep,
        agent_id: str | None = None,
    ) -> AgentTask:
        """Assign a plan step to an agent.

        Args:
            step: The plan step to assign.
            agent_id: Specific agent to assign to (auto-select if None).

        Returns:
            The created AgentTask.
        """
        if agent_id is None:
            agent = self._select_best_agent(step)
            if agent is None:
                raise ValueError(f"No available agent for step: {step.description}")
            agent_id = agent.agent_id

        agent = self._agents.get(agent_id)
        if agent is None:
            raise ValueError(f"Agent not found: {agent_id}")

        task_id = f"task-{uuid.uuid4().hex[:8]}"
        task = AgentTask(
            task_id=task_id,
            agent_id=agent_id,
            step=step,
            input_data=step.input_data,
            status=PlanStatus.READY,
        )

        agent.status = AgentStatus.BUSY
        agent.current_task = task_id

        logger.info(
            "Task %s assigned to agent %s: %s",
            task_id, agent_id, step.description,
        )
        return task

    def _select_best_agent(self, step: PlanStep) -> AgentInfo | None:
        """Select the best available agent for a step based on skills."""
        available = self.get_available_agents()
        if not available:
            return None

        # Score each agent based on skill match
        scored = []
        required_skills = set()

        # Determine required skills from the step
        if step.metadata:
            sub_goal_meta = step.metadata.get("sub_goal_index")
            if sub_goal_meta is not None:
                required_skills.add(step.step_type.value)

        for agent in available:
            score = len(set(agent.skills) & required_skills)
            scored.append((score, agent))

        # Sort by score (highest first), then by workload (fewest tasks first)
        scored.sort(key=lambda x: (-x[0], len(x[1].task_history)))
        return scored[0][1] if scored else None

    # ─── Coordination Strategies ───

    async def execute_sequential(
        self,
        steps: list[PlanStep],
        agent_id: str | None = None,
    ) -> list[AgentTask]:
        """Execute steps sequentially using one or more agents.

        Args:
            steps: Ordered list of steps to execute.
            agent_id: Specific agent (auto-select if None).

        Returns:
            List of completed AgentTasks.
        """
        tasks: list[AgentTask] = []

        for step in steps:
            task = self.assign_step(step, agent_id)
            tasks.append(task)

            result = await self._execute_task(task)
            if result.status == PlanStatus.FAILED:
                logger.warning("Sequential execution stopped at step: %s", step.description)
                break

        return tasks

    async def execute_parallel(
        self,
        steps: list[PlanStep],
    ) -> list[AgentTask]:
        """Execute steps in parallel using multiple agents.

        Args:
            steps: List of independent steps to execute.

        Returns:
            List of completed AgentTasks.
        """
        tasks: list[AgentTask] = []

        for step in steps:
            agent = self._select_best_agent(step)
            if agent is None:
                continue

            task = self.assign_step(step, agent.agent_id)
            tasks.append(task)

        # Execute all tasks in parallel
        results = await asyncio.gather(
            *[self._execute_task(t) for t in tasks],
            return_exceptions=True,
        )

        # Handle exceptions
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                tasks[i].status = PlanStatus.FAILED
                tasks[i].error = str(result)
                logger.error("Parallel task %s failed: %s", tasks[i].task_id, result)

        return tasks

    async def execute_hierarchical(
        self,
        plan: AIPlan,
        lead_agent_id: str,
        worker_agents: list[str],
    ) -> list[AgentTask]:
        """Execute steps hierarchically: lead agent delegates to workers.

        Args:
            plan: The plan to execute.
            lead_agent_id: The lead agent that coordinates.
            worker_agents: List of worker agent IDs.

        Returns:
            List of completed AgentTasks.
        """
        all_tasks: list[AgentTask] = []

        # Lead agent coordinates
        lead_task = AgentTask(
            task_id=f"lead-{uuid.uuid4().hex[:8]}",
            agent_id=lead_agent_id,
            step=PlanStep(
                step_id="lead-coordination",
                step_type=StepType.DECISION,
                description=f"Coordinate execution of {len(plan.steps)} steps",
                input_data={"plan_id": plan.plan_id},
            ),
            status=PlanStatus.READY,
        )
        all_tasks.append(lead_task)

        # Delegate steps to worker agents
        for i, step in enumerate(plan.steps):
            worker_id = worker_agents[i % len(worker_agents)]
            task = self.assign_step(step, worker_id)
            all_tasks.append(task)

            # Execute worker task
            result = await self._execute_task(task)
            if result.status == PlanStatus.FAILED:
                logger.warning("Worker %s failed at step %d", worker_id, i)

        # Mark lead as completed
        lead_task.status = PlanStatus.COMPLETED
        lead_agent = self._agents.get(lead_agent_id)
        if lead_agent:
            lead_agent.status = AgentStatus.IDLE
            lead_agent.task_history.append(lead_task.task_id)

        return all_tasks

    async def execute_consensus(
        self,
        step: PlanStep,
        agent_ids: list[str],
        agreement_threshold: float = 0.6,
    ) -> dict[str, Any]:
        """Execute a step using consensus among multiple agents.

        Multiple agents execute the same step and results are
        combined using a consensus mechanism (majority vote).

        Args:
            step: The step to execute.
            agent_ids: List of agent IDs to participate.
            agreement_threshold: Fraction of agents that must agree (0.0-1.0).

        Returns:
            Consensus result with aggregated data.
        """
        tasks: list[AgentTask] = []
        for agent_id in agent_ids:
            task = self.assign_step(step, agent_id)
            tasks.append(task)

        results = await asyncio.gather(
            *[self._execute_task(t) for t in tasks],
            return_exceptions=True,
        )

        successful_results = []
        for i, result in enumerate(results):
            if not isinstance(result, Exception) and tasks[i].status == PlanStatus.COMPLETED:
                successful_results.append({
                    "agent_id": tasks[i].agent_id,
                    "result": tasks[i].result,
                })

        agreement = len(successful_results) / len(agent_ids) if agent_ids else 0
        consensus_reached = agreement >= agreement_threshold

        consensus_result = {
            "consensus_reached": consensus_reached,
            "agreement": round(agreement, 2),
            "threshold": agreement_threshold,
            "total_agents": len(agent_ids),
            "successful_agents": len(successful_results),
            "results": successful_results,
            "aggregated": successful_results[0]["result"] if successful_results else None,
        }

        # Emit coordination event
        self._emit_coordination(step, agent_ids, consensus_result)

        return consensus_result

    # ─── Execution ───

    async def execute_plan(
        self,
        plan: AIPlan,
        strategy: CoordinationStrategy = CoordinationStrategy.SEQUENTIAL,
        lead_agent_id: str | None = None,
    ) -> MultiAgentResult:
        """Execute a plan using multi-agent coordination.

        Args:
            plan: The AI plan to execute.
            strategy: The coordination strategy to use.
            lead_agent_id: Lead agent for hierarchical strategy.

        Returns:
            MultiAgentResult with all execution details.
        """
        execution_id = f"ma-{uuid.uuid4().hex[:12]}"
        start_time = __import__("time").time()

        # Select strategy
        agent_tasks: list[AgentTask] = []

        try:
            if strategy == CoordinationStrategy.SEQUENTIAL:
                agent_tasks = await self.execute_sequential(plan.steps)

            elif strategy == CoordinationStrategy.PARALLEL:
                # Only execute independent steps (no dependencies) in parallel
                independent_steps = [s for s in plan.steps if not s.depends_on]
                dependent_steps = [s for s in plan.steps if s.depends_on]

                if independent_steps:
                    parallel_tasks = await self.execute_parallel(independent_steps)
                    agent_tasks.extend(parallel_tasks)

                if dependent_steps:
                    sequential_tasks = await self.execute_sequential(dependent_steps)
                    agent_tasks.extend(sequential_tasks)

            elif strategy == CoordinationStrategy.HIERARCHICAL:
                if not lead_agent_id:
                    # Auto-select first available agent as lead
                    available = self.get_available_agents()
                    if available:
                        lead_agent_id = available[0].agent_id
                    else:
                        raise ValueError("No available agents for hierarchical execution")

                worker_ids = [
                    a.agent_id for a in self.get_available_agents()
                    if a.agent_id != lead_agent_id
                ]
                agent_tasks = await self.execute_hierarchical(plan, lead_agent_id, worker_ids)

            elif strategy == CoordinationStrategy.CONSENSUS:
                # Execute each step with all available agents
                available_ids = [a.agent_id for a in self.get_available_agents()]
                for step in plan.steps:
                    consensus = await self.execute_consensus(step, available_ids)
                    if consensus["consensus_reached"]:
                        task = self.assign_step(step, available_ids[0])
                        task.result = consensus["aggregated"]
                        task.status = PlanStatus.COMPLETED
                        agent_tasks.append(task)

        except (ValueError, RuntimeError, KeyError) as exc:
            logger.error("Multi-agent execution failed: %s", exc)
            # Create failed tasks for remaining steps
            for step in plan.steps:
                if not any(t.step.step_id == step.step_id for t in agent_tasks):
                    task = AgentTask(
                        task_id=f"task-failed-{uuid.uuid4().hex[:6]}",
                        agent_id="system",
                        step=step,
                        status=PlanStatus.FAILED,
                        error=str(exc),
                    )
                    agent_tasks.append(task)

        # Build result
        duration_ms = (__import__("time").time() - start_time) * 1000
        completed = sum(1 for t in agent_tasks if t.status == PlanStatus.COMPLETED)
        failed = sum(1 for t in agent_tasks if t.status == PlanStatus.FAILED)

        result = MultiAgentResult(
            execution_id=execution_id,
            plan_id=plan.plan_id,
            strategy=strategy,
            agent_tasks=agent_tasks,
            total_tasks=len(agent_tasks),
            completed_tasks=completed,
            failed_tasks=failed,
            total_duration_ms=duration_ms,
            status=PlanStatus.COMPLETED if failed == 0 else PlanStatus.FAILED,
        )

        # Aggregate results
        result.aggregated_result = self._aggregate_results(agent_tasks)

        self._executions[execution_id] = result
        self._emit_multi_agent_completed(result)

        logger.info(
            "Multi-agent execution %s: strategy=%s, tasks=%d, completed=%d, failed=%d, time=%.0fms",
            execution_id, strategy.value, len(agent_tasks), completed, failed, duration_ms,
        )

        return result

    # ─── Task Execution ───

    async def _execute_task(self, task: AgentTask) -> AgentTask:
        """Execute a single agent task.

        Args:
            task: The task to execute.

        Returns:
            Updated AgentTask with results.
        """
        agent = self._agents.get(task.agent_id)
        if agent is None:
            task.status = PlanStatus.FAILED
            task.error = f"Agent not found: {task.agent_id}"
            return task

        executor = self._agent_executors.get(task.agent_id)
        if executor is None:
            task.status = PlanStatus.FAILED
            task.error = f"No executor for agent: {task.agent_id}"
            return task

        task.status = PlanStatus.IN_PROGRESS
        task.started_at = datetime.now(UTC)

        try:
            # Execute the agent's executor
            result = await executor(task.step, task.input_data)
            task.result = result
            task.status = PlanStatus.COMPLETED
            task.completed_at = datetime.now(UTC)

            # Update agent status
            agent.status = AgentStatus.IDLE
            agent.current_task = None
            agent.task_history.append(task.task_id)

            # Emit telemetry
            self._emit_task_completed(task)

        except (ValueError, RuntimeError, KeyError) as exc:
            task.status = PlanStatus.FAILED
            task.error = str(exc)
            task.completed_at = datetime.now(UTC)

            agent.status = AgentStatus.ERROR
            agent.current_task = None

            self._emit_task_failed(task)
            logger.error("Task %s failed for agent %s: %s", task.task_id, task.agent_id, exc)

        return task

    # ─── Result Management ───

    def _aggregate_results(self, tasks: list[AgentTask]) -> dict[str, Any]:
        """Aggregate results from multiple agent tasks."""
        aggregated: dict[str, Any] = {
            "total_tasks": len(tasks),
            "completed": sum(1 for t in tasks if t.status == PlanStatus.COMPLETED),
            "failed": sum(1 for t in tasks if t.status == PlanStatus.FAILED),
        }

        step_results = []
        for task in tasks:
            step_results.append({
                "task_id": task.task_id,
                "agent_id": task.agent_id,
                "step_id": task.step.step_id,
                "description": task.step.description,
                "status": task.status.value,
                "error": task.error,
            })

        aggregated["steps"] = step_results

        completed_tasks = [t for t in tasks if t.status == PlanStatus.COMPLETED]
        if completed_tasks:
            aggregated["last_result"] = completed_tasks[-1].result

        return aggregated

    def get_execution(self, execution_id: str) -> MultiAgentResult | None:
        """Get a multi-agent execution result."""
        return self._executions.get(execution_id)

    def list_executions(self) -> list[dict[str, Any]]:
        """List all multi-agent executions."""
        return [
            {
                "execution_id": e.execution_id,
                "plan_id": e.plan_id,
                "strategy": e.strategy.value,
                "total_tasks": e.total_tasks,
                "completed": e.completed_tasks,
                "failed": e.failed_tasks,
                "duration_ms": round(e.total_duration_ms, 2),
                "status": e.status.value,
            }
            for e in self._executions.values()
        ]

    # ─── Communication ───

    def send_message(
        self,
        sender_id: str,
        recipient_id: str,
        subject: str,
        body: Any,
        priority: Priority = Priority.NORMAL,
    ) -> None:
        """Send a message between agents."""
        message = Message(
            id=str(uuid.uuid4()),
            sender_id=sender_id,
            recipient_id=recipient_id,
            type=MessageType.TASK,
            subject=subject,
            body=body,
            priority=priority,
        )
        mailbox.send(message)

    def broadcast(self, sender_id: str, subject: str, body: Any) -> None:
        """Broadcast a message to all agents."""
        for agent_id in self._agents:
            if agent_id != sender_id:
                self.send_message(sender_id, agent_id, subject, body)

    # ─── Telemetry ───

    def _emit_task_completed(self, task: AgentTask) -> None:
        event = Event(
            event_type=AGENT_TASK_COMPLETED,
            source="multi_agent",
            data={
                "task_id": task.task_id,
                "agent_id": task.agent_id,
                "step_id": task.step.step_id,
                "status": task.status.value,
            },
        )
        event_bus.publish(event)

    def _emit_task_failed(self, task: AgentTask) -> None:
        event = Event(
            event_type=AGENT_TASK_FAILED,
            source="multi_agent",
            data={
                "task_id": task.task_id,
                "agent_id": task.agent_id,
                "step_id": task.step.step_id,
                "error": task.error,
            },
        )
        event_bus.publish(event)

    def _emit_coordination(
        self,
        step: PlanStep,
        agent_ids: list[str],
        consensus_result: dict[str, Any],
    ) -> None:
        event = Event(
            event_type=AGENT_COORDINATION,
            source="multi_agent",
            data={
                "step_id": step.step_id,
                "agents": agent_ids,
                "consensus_reached": consensus_result["consensus_reached"],
                "agreement": consensus_result["agreement"],
            },
        )
        event_bus.publish(event)

    def _emit_multi_agent_completed(self, result: MultiAgentResult) -> None:
        event = Event(
            event_type=MULTI_AGENT_COMPLETED,
            source="multi_agent",
            data={
                "execution_id": result.execution_id,
                "plan_id": result.plan_id,
                "strategy": result.strategy.value,
                "total_tasks": result.total_tasks,
                "completed": result.completed_tasks,
                "failed": result.failed_tasks,
                "duration_ms": round(result.total_duration_ms, 2),
            },
        )
        event_bus.publish(event)


# ─── Singleton ───

multi_agent_orchestrator = MultiAgentOrchestrator()

