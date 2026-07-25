"""
AI Planner
==========

Advanced planner that decomposes high-level goals into executable workflow plans.

Planner menggunakan:
    - WorkflowCatalog untuk menemukan workflow yang sesuai
    - IntentResolver untuk mapping intent → workflow
    - TaskPlanner untuk subtask decomposition
    - ExecutionPlanner untuk execution ordering
    - CapabilityGraph untuk skill/capability awareness

Planner BUKAN replacement untuk TaskPlanner atau ExecutionPlanner.
Planner adalah layer strategis yang memilih workflow dan menyusun
rencana eksekusi multi-langkah.

Flow:
    Goal / Vision
        ↓
    AI Planner
        ↓
    ├── Analyze goal → decompose into sub-goals
    ├── Select workflows from catalog
    ├── Build execution plan (ordered workflow steps)
    ├── Assign resources (teams/agents)
    └── Return AIPlan with validation
"""

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from apps.organization.capability_graph import capability_graph
from apps.organization.communication import Event, event_bus
from apps.organization.intent_resolver import (
    IntentResolver,
    intent_resolver,
)
from apps.organization.workflow_catalog import (
    WorkflowCatalog,
    workflow_catalog,
)
from apps.society.intent_router import (
    Intent,
    IntentComplexity,
    intent_router,
)

logger = logging.getLogger(__name__)

# ─── Telemetry Events ───

PLAN_CREATED = "PlanCreated"
PLAN_STEP_ASSIGNED = "PlanStepAssigned"
PLAN_EXECUTION_STARTED = "PlanExecutionStarted"
PLAN_COMPLETED = "PlanCompleted"
PLAN_FAILED = "PlanFailed"

# ─── Enums ───


class PlanStatus(str, Enum):
    DRAFT = "draft"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StepType(str, Enum):
    WORKFLOW = "workflow"
    CAPABILITY = "capability"
    SUB_PLAN = "sub_plan"
    DECISION = "decision"
    PARALLEL = "parallel"


# ─── Data Classes ───


@dataclass
class PlanStep:
    """A single step in an AI plan.

    Attributes:
        step_id: Unique identifier for this step.
        step_type: Type of step (workflow, capability, sub_plan, etc.).
        description: Human-readable description.
        workflow_id: The workflow to execute (if step_type == WORKFLOW).
        capability_id: The capability to execute (if step_type == CAPABILITY).
        intent_id: The intent that resolved to this step.
        input_data: Input data for this step.
        depends_on: List of step_ids that must complete before this step.
        assigned_team_id: Team assigned to execute this step.
        status: Current status of this step.
        result: Execution result (populated after completion).
        error: Error message if failed.
        metadata: Additional metadata.
    """
    step_id: str
    step_type: StepType
    description: str
    workflow_id: str | None = None
    capability_id: str | None = None
    intent_id: str | None = None
    input_data: dict[str, Any] = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)
    assigned_team_id: str | None = None
    status: PlanStatus = PlanStatus.DRAFT
    result: Any = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.step_id:
            self.step_id = f"step-{uuid.uuid4().hex[:8]}"


@dataclass
class AIPlan:
    """A complete AI-generated execution plan.

    Attributes:
        plan_id: Unique identifier.
        goal: The original goal/vision description.
        steps: Ordered list of plan steps (topological order).
        status: Overall plan status.
        estimated_duration_minutes: Estimated total execution time.
        total_steps: Total number of steps.
        completed_steps: Number of completed steps.
        failed_steps: Number of failed steps.
        created_at: When the plan was created.
        updated_at: When the plan was last updated.
        metadata: Additional metadata (domain, complexity, etc.).
    """
    plan_id: str
    goal: str
    steps: list[PlanStep] = field(default_factory=list)
    status: PlanStatus = PlanStatus.DRAFT
    estimated_duration_minutes: int = 0
    total_steps: int = 0
    completed_steps: int = 0
    failed_steps: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def progress(self) -> float:
        """Calculate progress as a percentage (0.0 - 1.0)."""
        if self.total_steps == 0:
            return 0.0
        return (self.completed_steps + self.failed_steps) / self.total_steps

    @property
    def is_complete(self) -> bool:
        """Check if the plan is fully complete."""
        return self.status in (PlanStatus.COMPLETED, PlanStatus.FAILED, PlanStatus.CANCELLED)

    @property
    def is_stuck(self) -> bool:
        """Check if the plan has failed steps that block progress."""
        return self.failed_steps > 0 and self.status == PlanStatus.IN_PROGRESS


# ─── AI Planner ───


class AIPlanner:
    """Advanced planner that creates multi-step execution plans from goals.

    The AI Planner:
        1. Analyzes the goal using IntentRouter
        2. Decomposes into sub-goals
        3. Finds matching workflows from the catalog
        4. Orders steps based on dependencies
        5. Assigns teams/resources
        6. Returns a validated AIPlan

    This is NOT a dynamic workflow generator.
    It selects from registered workflows and capabilities.
    """

    def __init__(
        self,
        catalog: WorkflowCatalog | None = None,
        resolver: IntentResolver | None = None,
    ):
        self._catalog = catalog or workflow_catalog
        self._resolver = resolver or intent_resolver
        self._plans: dict[str, AIPlan] = {}

    # ─── Planning ───

    def plan_from_goal(self, goal: str, context: dict[str, Any] | None = None) -> AIPlan:
        """Create a full execution plan from a high-level goal.

        Args:
            goal: The high-level goal or vision.
            context: Optional context (domain hints, constraints, etc.).

        Returns:
            AIPlan with ordered execution steps.
        """
        context = context or {}
        plan_id = f"plan-{uuid.uuid4().hex[:12]}"

        # 1. Analyze the goal
        intent = intent_router.route(goal, context)
        domain = intent.domain.value

        logger.info("Planning for goal: '%s' (domain=%s, complexity=%s)",
                     goal[:80], domain, intent.complexity.value)

        # 2. Decompose into sub-goals (derived from task planner templates)
        sub_goals = self._decompose_goal(intent, context)

        # 3. Find workflows for each sub-goal
        steps: list[PlanStep] = []
        previous_step_id: str | None = None

        for i, sub_goal in enumerate(sub_goals):
            step_id = f"step-{i+1}-{uuid.uuid4().hex[:6]}"

            # Try to resolve intent to a workflow
            result = self._resolver.resolve(sub_goal.get("intent_id", ""))

            if result.found and result.workflow_id:
                # Found a workflow
                step = PlanStep(
                    step_id=step_id,
                    step_type=StepType.WORKFLOW,
                    description=sub_goal.get("description", sub_goal.get("intent_id", "")),
                    workflow_id=result.workflow_id,
                    intent_id=sub_goal.get("intent_id", ""),
                    input_data=sub_goal.get("input_data", {}),
                    depends_on=[previous_step_id] if previous_step_id else [],
                    status=PlanStatus.READY,
                    metadata={
                        "confidence": result.confidence,
                        "reason": result.reason,
                        "sub_goal_index": i,
                    },
                )
            else:
                # Fallback: try capability directly
                cap_id = sub_goal.get("capability_id", "")
                step = PlanStep(
                    step_id=step_id,
                    step_type=StepType.CAPABILITY,
                    description=sub_goal.get("description", cap_id),
                    capability_id=cap_id or None,
                    intent_id=sub_goal.get("intent_id", ""),
                    input_data=sub_goal.get("input_data", {}),
                    depends_on=[previous_step_id] if previous_step_id else [],
                    status=PlanStatus.READY,
                    metadata={
                        "fallback": True,
                        "sub_goal_index": i,
                    },
                )

            steps.append(step)
            previous_step_id = step_id

        # 4. Build the plan
        plan = AIPlan(
            plan_id=plan_id,
            goal=goal,
            steps=steps,
            total_steps=len(steps),
            estimated_duration_minutes=self._estimate_duration(steps, intent),
            status=PlanStatus.READY,
            metadata={
                "domain": domain,
                "complexity": intent.complexity.value,
                "confidence": intent.confidence,
                "entities": intent.entities,
                "constraints": intent.constraints,
            },
        )

        self._plans[plan_id] = plan
        self._emit_plan_created(plan, intent)
        logger.info("Plan created: %s with %d steps", plan_id, len(steps))

        return plan

    def plan_with_workflows(
        self,
        goal: str,
        workflow_ids: list[str],
        context: dict[str, Any] | None = None,
    ) -> AIPlan:
        """Create a plan from explicitly specified workflows.

        Args:
            goal: The goal description.
            workflow_ids: Ordered list of workflow IDs to execute.
            context: Optional context.

        Returns:
            AIPlan with the specified workflows as steps.
        """
        context = context or {}
        plan_id = f"plan-{uuid.uuid4().hex[:12]}"

        steps: list[PlanStep] = []
        previous_step_id: str | None = None

        for i, wf_id in enumerate(workflow_ids):
            step_id = f"step-{i+1}-{uuid.uuid4().hex[:6]}"
            entry = self._catalog.get_entry(wf_id)

            step = PlanStep(
                step_id=step_id,
                step_type=StepType.WORKFLOW,
                description=entry.display_name if entry else wf_id,
                workflow_id=wf_id,
                input_data=context.get("input_data", {}),
                depends_on=[previous_step_id] if previous_step_id else [],
                status=PlanStatus.READY,
            )
            steps.append(step)
            previous_step_id = step_id

        plan = AIPlan(
            plan_id=plan_id,
            goal=goal,
            steps=steps,
            total_steps=len(steps),
            status=PlanStatus.READY,
        )

        self._plans[plan_id] = plan
        return plan

    # ─── Execution Management ───

    async def execute_step(
        self,
        plan_id: str,
        step_index: int,
        executor: Any,
    ) -> Any:
        """Execute a single step of a plan.

        Args:
            plan_id: The plan ID.
            step_index: Index of the step to execute.
            executor: The WorkflowExecutor instance.

        Returns:
            Execution result.
        """
        plan = self._plans.get(plan_id)
        if plan is None:
            raise ValueError(f"Plan not found: {plan_id}")

        if step_index < 0 or step_index >= len(plan.steps):
            raise ValueError(f"Invalid step index: {step_index}")

        step = plan.steps[step_index]

        # Check dependencies
        for dep_id in step.depends_on:
            dep_step = next((s for s in plan.steps if s.step_id == dep_id), None)
            if dep_step and dep_step.status != PlanStatus.COMPLETED:
                raise ValueError(
                    f"Step {step.step_id} depends on {dep_id} which is not completed"
                )

        # Execute based on step type
        step.status = PlanStatus.IN_PROGRESS
        self._emit_step_assigned(plan, step, step_index)

        try:
            if step.step_type == StepType.WORKFLOW and step.workflow_id:
                response = await executor.execute(
                    step.workflow_id,
                    input_data=step.input_data,
                )
                step.result = response
                step.status = PlanStatus.COMPLETED
                plan.completed_steps += 1
                logger.info("Step %s completed: workflow=%s", step.step_id, step.workflow_id)

            elif step.step_type == StepType.CAPABILITY and step.capability_id:
                # Execute single capability via pipeline
                from apps.organization.capability_pipeline import (
                    PipelineRequest,
                    PipelineStep,
                    capability_pipeline,
                )
                pipeline_step = PipelineStep(
                    capability_id=step.capability_id,
                    input_data=step.input_data,
                    alias=step.description,
                )
                pipeline_request = PipelineRequest(steps=[pipeline_step])
                response = await capability_pipeline.execute(pipeline_request)
                step.result = response
                step.status = PlanStatus.COMPLETED
                plan.completed_steps += 1
                logger.info("Step %s completed: capability=%s", step.step_id, step.capability_id)

            else:
                step.status = PlanStatus.FAILED
                plan.failed_steps += 1
                step.error = f"Unsupported step type: {step.step_type}"
                return None

        except Exception as exc:
            step.status = PlanStatus.FAILED
            plan.failed_steps += 1
            step.error = str(exc)
            logger.error("Step %s failed: %s", step.step_id, exc)

        # Update overall plan status
        self._update_plan_status(plan)
        return step.result

    async def execute_plan(self, plan_id: str, executor: Any) -> AIPlan:
        """Execute all steps of a plan in order.

        Args:
            plan_id: The plan ID.
            executor: The WorkflowExecutor instance.

        Returns:
            Updated AIPlan with execution results.
        """
        plan = self._plans.get(plan_id)
        if plan is None:
            raise ValueError(f"Plan not found: {plan_id}")

        plan.status = PlanStatus.IN_PROGRESS
        self._emit_execution_started(plan)

        for i in range(len(plan.steps)):
            step = plan.steps[i]
            if step.status != PlanStatus.READY:
                continue

            await self.execute_step(plan_id, i, executor)

            if step.status == PlanStatus.FAILED:
                logger.warning("Plan %s failed at step %d: %s", plan_id, i, step.error)
                break

        # Final status update
        self._update_plan_status(plan)
        if plan.status == PlanStatus.COMPLETED:
            self._emit_plan_completed(plan)
        elif plan.status == PlanStatus.FAILED:
            self._emit_plan_failed(plan)

        return plan

    # ─── Plan Management ───

    def get_plan(self, plan_id: str) -> AIPlan | None:
        """Get a plan by ID."""
        return self._plans.get(plan_id)

    def list_plans(self) -> list[dict[str, Any]]:
        """List all plans (summary)."""
        return [
            {
                "plan_id": p.plan_id,
                "goal": p.goal[:80],
                "status": p.status.value,
                "total_steps": p.total_steps,
                "completed": p.completed_steps,
                "failed": p.failed_steps,
                "progress": round(p.progress * 100, 1),
                "domain": p.metadata.get("domain", "unknown"),
            }
            for p in self._plans.values()
        ]

    def cancel_plan(self, plan_id: str) -> None:
        """Cancel a plan."""
        plan = self._plans.get(plan_id)
        if plan:
            plan.status = PlanStatus.CANCELLED
            for step in plan.steps:
                if step.status in (PlanStatus.DRAFT, PlanStatus.READY, PlanStatus.IN_PROGRESS):
                    step.status = PlanStatus.CANCELLED
            logger.info("Plan cancelled: %s", plan_id)

    def get_plan_summary(self, plan_id: str) -> dict[str, Any] | None:
        """Get a detailed summary of a plan."""
        plan = self._plans.get(plan_id)
        if plan is None:
            return None

        return {
            "plan_id": plan.plan_id,
            "goal": plan.goal,
            "status": plan.status.value,
            "progress": round(plan.progress * 100, 1),
            "total_steps": plan.total_steps,
            "completed_steps": plan.completed_steps,
            "failed_steps": plan.failed_steps,
            "estimated_duration_minutes": plan.estimated_duration_minutes,
            "steps": [
                {
                    "step_id": s.step_id,
                    "step_type": s.step_type.value,
                    "description": s.description,
                    "workflow_id": s.workflow_id,
                    "capability_id": s.capability_id,
                    "status": s.status.value,
                    "depends_on": s.depends_on,
                    "error": s.error,
                }
                for s in plan.steps
            ],
            "metadata": plan.metadata,
            "created_at": plan.created_at.isoformat(),
            "updated_at": plan.updated_at.isoformat(),
        }

    # ─── Internal ───

    def _decompose_goal(
        self,
        intent: Intent,
        context: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Decompose a goal into sub-goals based on domain and complexity."""
        domain = intent.domain.value
        sub_goals: list[dict[str, Any]] = []

        # Get subtask templates for the domain
        templates = capability_graph.get_subtask_templates(domain)

        if templates:
            # Use templates to generate sub-goals
            for template in templates:
                sub_goal = {
                    "description": template.name,
                    "intent_id": template.subtask_id,
                    "capability_id": template.subtask_id,
                    "input_data": {
                        "skills": template.required_skills,
                        "produces_artifact": template.produces_artifact,
                    },
                }
                sub_goals.append(sub_goal)
        else:
            # Fallback: use intent entities
            entities = intent.entities if intent.entities else [domain]
            for entity in entities[:5]:
                sub_goals.append({
                    "description": f"Process {entity}",
                    "intent_id": entity,
                    "capability_id": entity,
                    "input_data": {"skills": [entity]},
                })

        # Limit based on complexity
        complexity_limits = {
            IntentComplexity.SIMPLE: 3,
            IntentComplexity.MEDIUM: 5,
            IntentComplexity.COMPLEX: 8,
        }
        max_sub_goals = complexity_limits.get(intent.complexity, 5)
        return sub_goals[:max_sub_goals]

    def _estimate_duration(
        self,
        steps: list[PlanStep],
        intent: Intent,
    ) -> int:
        """Estimate total duration in minutes."""
        base_time = len(steps) * 30
        if intent.complexity == IntentComplexity.COMPLEX:
            base_time = int(base_time * 1.5)
        elif intent.complexity == IntentComplexity.SIMPLE:
            base_time = int(base_time * 0.5)
        return base_time

    def _update_plan_status(self, plan: AIPlan) -> None:
        """Update the overall plan status based on step statuses."""
        all_completed = all(
            s.status == PlanStatus.COMPLETED for s in plan.steps
        )
        any_failed = any(
            s.status == PlanStatus.FAILED for s in plan.steps
        )

        if all_completed:
            plan.status = PlanStatus.COMPLETED
        elif any_failed:
            plan.status = PlanStatus.FAILED
        else:
            plan.status = PlanStatus.IN_PROGRESS

        plan.updated_at = datetime.now(timezone.utc)

    # ─── Telemetry ───

    def _emit_plan_created(self, plan: AIPlan, intent: Intent) -> None:
        event = Event(
            event_type=PLAN_CREATED,
            source="ai_planner",
            data={
                "plan_id": plan.plan_id,
                "goal": plan.goal[:100],
                "domain": intent.domain.value,
                "complexity": intent.complexity.value,
                "steps": len(plan.steps),
            },
        )
        event_bus.publish(event)

    def _emit_step_assigned(self, plan: AIPlan, step: PlanStep, index: int) -> None:
        event = Event(
            event_type=PLAN_STEP_ASSIGNED,
            source="ai_planner",
            data={
                "plan_id": plan.plan_id,
                "step_id": step.step_id,
                "step_index": index,
                "step_type": step.step_type.value,
                "workflow_id": step.workflow_id,
                "capability_id": step.capability_id,
            },
        )
        event_bus.publish(event)

    def _emit_execution_started(self, plan: AIPlan) -> None:
        event = Event(
            event_type=PLAN_EXECUTION_STARTED,
            source="ai_planner",
            data={
                "plan_id": plan.plan_id,
                "goal": plan.goal[:100],
                "total_steps": plan.total_steps,
            },
        )
        event_bus.publish(event)

    def _emit_plan_completed(self, plan: AIPlan) -> None:
        event = Event(
            event_type=PLAN_COMPLETED,
            source="ai_planner",
            data={
                "plan_id": plan.plan_id,
                "total_steps": plan.total_steps,
                "completed_steps": plan.completed_steps,
                "duration_minutes": plan.estimated_duration_minutes,
            },
        )
        event_bus.publish(event)

    def _emit_plan_failed(self, plan: AIPlan) -> None:
        event = Event(
            event_type=PLAN_FAILED,
            source="ai_planner",
            data={
                "plan_id": plan.plan_id,
                "total_steps": plan.total_steps,
                "completed_steps": plan.completed_steps,
                "failed_steps": plan.failed_steps,
            },
        )
        event_bus.publish(event)


# ─── Singleton ───

ai_planner = AIPlanner()

