"""
Society Runtime
===============

Top-level container for AI organizations.
Combines Organization Runtime, Team Builder, Communication, Collective Memory, and Metrics.

Usage:
    society = Society("My AI Company")
    society.register_agent(CEOA(...))
    society.assign_role("ceo-1", AgentRole.CEO, Department.ENGINEERING)
    society.assign_role("cto-1", AgentRole.DIRECTOR, Department.ENGINEERING, manager_id="ceo-1")
    
    team = society.form_team_for_task("Build a web application")
    result = await society.run_project("proj-1", team.team_id, {"type": "build", "target": "webapp"})
"""

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from apps.organization.communication import blackboard, mailbox
from apps.organization.economics import organizational_economics
from apps.organization.execution_planner import (
    ExecutionPlanner,
    execution_planner,
)
from apps.organization.execution_runtime import (
    ExecutionContext,
    execution_runtime,
)
from apps.organization.kernel import ConflictRecord, ResourceRequest, organization_kernel
from apps.organization.learning import organizational_learning
from apps.organization.metrics import organizational_metrics
from apps.organization.optimizer import workforce_optimizer
from apps.organization.registry import (
    AgentRecord,
    AgentRole,
    Department,
    agent_registry,
)
from apps.organization.runtime import organization_runtime
from apps.organization.task_planner import SubTask, TaskPlan, task_planner
from apps.organization.team_builder import TaskRequirement, Team, team_builder
from apps.society.intent_router import Intent, IntentComplexity, IntentDomain, intent_router
from apps.society.workers import network_worker

logger = logging.getLogger(__name__)


def _build_worker_registry() -> dict[str, Any]:
    registry: dict[str, Any] = {
        "network": network_worker,
    }
    try:
        from apps.society.workers.code_worker import code_worker
        registry["code"] = code_worker
    except Exception:
        pass
    try:
        from apps.society.workers.research_worker import research_worker
        registry["research"] = research_worker
    except Exception:
        pass
    try:
        from apps.society.workers.devops_worker import devops_worker
        registry["devops"] = devops_worker
    except Exception:
        pass
    try:
        from apps.society.workers.trading_worker import trading_worker
        registry["trading"] = trading_worker
    except Exception:
        pass
    try:
        from apps.society.workers.self_development_worker import self_development_worker
        registry["self-development"] = self_development_worker
    except Exception:
        pass
    return registry


WORKER_REGISTRY: dict[str, Any] = _build_worker_registry()



@dataclass
class SocietyConfig:
    name: str
    description: str = ""
    default_department: Department = Department.ENGINEERING


@dataclass
class Project:
    project_id: str
    name: str
    team_id: str
    status: str = "pending"
    result: dict[str, Any] | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)


class SocietyRuntime:
    """Top-level runtime for AI organizations."""

    def __init__(self, config: SocietyConfig):
        self.config = config
        self._registry = agent_registry
        self._org_runtime = organization_runtime
        self._team_builder = team_builder
        self._worker_registry = dict(WORKER_REGISTRY)
        self._agent_instances: dict[str, Any] = {}
        self._teams: dict[str, Team] = {}
        self._projects: dict[str, Project] = {}

    def _kernel_request_resource(self, requester_id: str, resource_type: str, description: str, estimated_cost: float = 0.0) -> ResourceRequest:
        return organization_kernel.request_resource(requester_id, resource_type, description, estimated_cost)

    def _kernel_detect_conflict(self, level: int, parties: list[str], description: str) -> ConflictRecord:
        return organization_kernel.detect_conflict(level, parties, description)

    def _kernel_resolve_conflict(self, conflict_id: str, resolution: str, resolved_by: str) -> ConflictRecord | None:
        return organization_kernel.resolve_conflict(conflict_id, resolution, resolved_by)

    def _kernel_set_budget(self, total: float, currency: str = "USD") -> None:
        organization_kernel.set_budget(total, currency)

    def _get_worker(self, domain: str) -> Any | None:
        return self._worker_registry.get(domain)

    def register_worker(self, domain: str, worker: Any) -> None:
        self._worker_registry[domain] = worker

    def get_economics_analysis(self, analysis_type: str, **kwargs) -> dict[str, Any]:
        if analysis_type == "team_formation":
            analysis = organizational_economics.analyze_team_formation(
                team_size=kwargs.get("team_size", 3),
                avg_cost_per_worker=kwargs.get("avg_cost_per_worker", 0.001),
                estimated_duration_hours=kwargs.get("estimated_duration_hours", 8),
                expected_quality=kwargs.get("expected_quality", 0.8),
            )
        elif analysis_type == "model_selection":
            analysis = organizational_economics.analyze_model_selection(
                model_cost_per_1k=kwargs.get("model_cost_per_1k", 0.001),
                estimated_tokens=kwargs.get("estimated_tokens", 10000),
                quality_score=kwargs.get("quality_score", 0.85),
                latency_ms=kwargs.get("latency_ms", 500),
            )
        elif analysis_type == "meeting":
            analysis = organizational_economics.analyze_meeting_cost(
                participants=kwargs.get("participants", 3),
                duration_minutes=kwargs.get("duration_minutes", 30),
            )
        else:
            return {"error": f"Unknown analysis type: {analysis_type}"}

        return {
            "decision": analysis.decision,
            "roi": round(analysis.roi, 2),
            "net_value": round(analysis.net_value, 2),
            "recommendation": analysis.recommendation,
            "confidence": analysis.confidence,
            "costs": [{"item": c.item, "cost": c.estimated_cost} for c in analysis.costs],
            "benefits": [{"item": b.item, "value": b.estimated_value} for b in analysis.benefits],
        }

    def get_optimization_suggestions(self, category: str | None = None) -> list[dict[str, Any]]:
        suggestions = workforce_optimizer.get_suggestions(category)
        return [
            {
                "id": s.id,
                "category": s.category,
                "description": s.description,
                "expected_impact": s.expected_impact,
                "estimated_savings": s.estimated_savings,
                "priority": s.priority,
            }
            for s in suggestions
        ]

    def record_lesson(self, project_id: str, category: str, description: str, impact: str, recommendation: str) -> dict[str, Any]:
        lesson = organizational_learning.record_lesson(project_id, category, description, impact, recommendation)
        return {
            "lesson_id": lesson.id,
            "category": lesson.category,
            "recommendation": lesson.recommendation,
        }

    def record_mistake(self, project_id: str, severity: str, description: str, root_cause: str, remediation: str) -> dict[str, Any]:
        mistake = organizational_learning.record_mistake(project_id, severity, description, root_cause, "", remediation)
        return {
            "mistake_id": mistake.id,
            "severity": mistake.severity,
            "remediation": mistake.remediation,
        }

    def get_project_learning(self, project_id: str) -> dict[str, Any]:
        return organizational_learning.get_learning_summary(project_id)

    async def process_user_request(self, user_input: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}

        intent = intent_router.route(user_input, context)
        capability_pack = intent_router.get_capability_pack(intent.domain)

        task_plan = task_planner.plan(intent, capability_pack)
        execution_plan = execution_planner.plan(task_plan) if task_plan else None

        team_skills: list[str] = []
        if execution_plan:
            aggregated: list[str] = []
            for stage in execution_plan.stages:
                for subtask in stage.subtasks:
                    aggregated.extend(subtask.required_skills)
            seen: set[str] = set()
            for skill in aggregated:
                if skill not in seen:
                    seen.add(skill)
                    team_skills.append(skill)
            team_skills = team_skills[:3]
        elif capability_pack:
            team_skills = capability_pack.capabilities[:3]

        team = self.form_team_for_task({
            "description": intent.raw_input,
            "required_skills": team_skills,
            "team_size": min(5, max(2, len(team_skills))),
            "min_quality": 0.7,
        })

        project_id = context.get("project_id", f"proj-{uuid.uuid4().hex[:8]}")
        task = {
            "name": project_id,
            "type": intent.domain.value,
            "complexity": intent.complexity.value,
            "intent": intent.raw_input,
            "entities": intent.entities,
            "constraints": intent.constraints,
            "task_plan": {
                "subtasks": [
                    {
                        "id": s.subtask_id,
                        "name": s.name,
                        "required_skills": s.required_skills,
                        "priority": s.priority,
                        "produces_artifact": s.produces_artifact,
                    }
                    for s in (task_plan.subtasks if task_plan else [])
                ],
                "strategy": task_plan.strategy if task_plan else "none",
                "estimated_total_minutes": task_plan.estimated_total_minutes if task_plan else 0,
            },
            "execution_plan": {
                "stages": [
                    {
                        "stage_id": stage.stage_id,
                        "mode": stage.mode,
                        "subtasks": [s.subtask_id for s in stage.subtasks],
                        "estimated_duration_minutes": stage.estimated_duration_minutes,
                    }
                    for stage in (execution_plan.stages if execution_plan else [])
                ],
                "total_duration_minutes": execution_plan.total_duration_minutes if execution_plan else 0,
                "parallelism_factor": execution_plan.parallelism_factor if execution_plan else 1.0,
            },
        }

        result = await self.run_project(project_id, team.team_id, task)
        self._record_learning(project_id, intent, result)

        return {
            "intent": {
                "domain": intent.domain.value,
                "complexity": intent.complexity.value,
                "confidence": intent.confidence,
                "entities": intent.entities,
            },
            "team_id": team.team_id,
            "team_size": len(team.members),
            "project_id": project_id,
            "task_plan": task.get("task_plan"),
            "execution_plan": task.get("execution_plan"),
            "result": result,
            "status": "completed",
        }

    def _record_learning(self, project_id: str, intent: Intent, result: dict[str, Any]) -> None:
        success = "error" not in str(result).lower()
        if not success:
            organizational_learning.record_mistake(
                project_id=project_id,
                severity="medium",
                description=f"Intent routing issue for domain {intent.domain.value}",
                root_cause="Low confidence intent classification",
                impact="Medium impact on user satisfaction",
                remediation="Improve intent classification with more examples",
            )

    async def _execute_agent(self, subtask: SubTask, task_context: dict[str, Any]) -> dict[str, Any]:
        subtask_info = task_context.get("subtask", {})
        name = subtask_info.get("name", "")
        for agent_id, agent in self._agent_instances.items():
            if agent_id in name:
                return await agent.execute({
                    "subtask": subtask_info,
                    "task": task_context,
                })
        return {"agent_id": "unknown", "status": "completed", "result": name}

    def register_agent(self, agent: Any) -> None:
        if hasattr(agent, "agent_id") and hasattr(agent, "name"):
            record = AgentRecord(
                id=agent.agent_id,
                name=agent.name,
                role=getattr(agent, "role", AgentRole.WORKER),
                department=getattr(agent, "department", Department.ENGINEERING),
                skills=getattr(agent, "skills", []),
                manager_id=getattr(agent, "manager_id", None),
            )
            self._registry.register(record)
            self._agent_instances[agent.agent_id] = agent
            logger.info(f"Agent registered: {agent.agent_id} ({agent.name})")
        else:
            raise ValueError("Agent must have agent_id and name attributes")

    def assign_role(
        self,
        agent_id: str,
        role: AgentRole,
        department: Department,
        manager_id: str | None = None,
    ) -> None:
        agent = self._registry.get(agent_id)
        if not agent:
            raise ValueError(f"Agent not found: {agent_id}")
        old_department = agent.department
        agent.role = role
        agent.department = department
        if manager_id:
            agent.manager_id = manager_id
        if role == AgentRole.CEO:
            self._org_runtime.bootstrap(agent_id)
        if old_department != department:
            dept_list = self._registry._department_index.get(old_department, [])
            if agent_id in dept_list:
                dept_list.remove(agent_id)
            self._registry._department_index.setdefault(department, []).append(agent_id)
        logger.info(f"Role assigned: {agent_id} -> {role.value} in {department.value}")

    def form_team_for_task(self, task: dict[str, Any]) -> Team:
        requirement = TaskRequirement(
            description=task.get("description", ""),
            required_skills=task.get("required_skills", []),
            team_size=task.get("team_size", 3),
            min_quality=task.get("min_quality", 0.7),
            max_cost=task.get("max_cost", float("inf")),
            max_latency_ms=task.get("max_latency_ms", float("inf")),
        )
        team = self._team_builder.build_team(requirement)
        team_id = str(uuid.uuid4())
        team.team_id = team_id
        self._teams[team_id] = team
        logger.info(
            "Team formed: %s with %d members for task: %s",
            team_id,
            len(team.members),
            requirement.description,
        )
        return team

    async def run_project(self, project_id: str, team_id: str, task: dict[str, Any]) -> dict[str, Any]:
        project = Project(project_id=project_id, name=task.get("name", project_id), team_id=team_id)
        self._projects[project_id] = project

        team = self._teams.get(team_id)
        if not team:
            raise ValueError(f"Team not found: {team_id}")

        team_size = len(team.members)
        self._kernel_set_budget(float(max(1000, team_size * 500)))
        self._kernel_request_resource(project_id, "agent", task.get("intent", task.get("name", project_id)), float(team_size * 100))

        organizational_metrics.start_project(project_id, team_id)
        blackboard.write_sync("current_project", project_id)
        blackboard.write_sync("current_task", task)

        team_members = [self._agent_instances[m.agent.id] for m in team.members if m.agent.id in self._agent_instances]
        domain = task.get("type", IntentDomain.GENERAL.value)
        worker = self._get_worker(domain)

        if worker:
            if not team_members:
                subtasks = [
                    SubTask(
                        subtask_id="subtask-0",
                        name=task.get("intent", task.get("name", project_id)),
                        description=task.get("intent", task.get("name", project_id)),
                        required_skills=[],
                        produces_artifact="result",
                        estimated_duration_minutes=30,
                        priority=1,
                        can_parallelize=False,
                    )
                ]
            else:
                subtasks = [
                    SubTask(
                        subtask_id=f"subtask-{i}",
                        name=f"Execute {task.get('name', project_id)} by {member.agent_id}",
                        description=task.get("intent", task.get("name", project_id)),
                        required_skills=getattr(member, "skills", []) or [],
                        produces_artifact="result",
                        estimated_duration_minutes=30,
                        priority=i + 1,
                        can_parallelize=len(team_members) > 1,
                    )
                    for i, member in enumerate(team_members)
                ]
            execution_plan = ExecutionPlanner().plan(
                TaskPlan(
                    intent=Intent(
                        raw_input=task.get("intent", task.get("name", project_id)),
                        domain=IntentDomain(domain),
                        complexity=IntentComplexity(task.get("complexity", IntentComplexity.MEDIUM.value)),
                    ),
                    subtasks=subtasks,
                    strategy="parallel" if len(team_members) > 1 else "serial",
                )
            )
            context = ExecutionContext(
                execution_id=f"exec-{project_id}",
                plan=execution_plan,
                worker=worker.execute,
                concurrency=min(4, max(1, len(team_members))),
            )
            results = await execution_runtime.execute(context)
        else:
            results = []
            for member in team_members:
                try:
                    result = await member.execute(task)
                    results.append(result)
                    organizational_metrics.record_task(project_id, success=True)
                except Exception as e:
                    logger.error(f"Agent {member.agent_id} failed: {e}")
                    results.append({"agent_id": member.agent_id, "error": str(e)})
                    organizational_metrics.record_task(project_id, success=False)

        project.status = "completed"
        project.result = {"results": results}
        organizational_metrics.end_project(project_id)

        logger.info("Project %s completed with %d results", project_id, len(results))
        return project.result or {}

    def send_message(self, sender_id: str, recipient_id: str, subject: str, body: Any) -> None:
        from apps.organization.communication import Message, MessageType, Priority

        message = Message(
            id=str(uuid.uuid4()),
            sender_id=sender_id,
            recipient_id=recipient_id,
            type=MessageType.TASK,
            subject=subject,
            body=body,
            priority=Priority.NORMAL,
        )
        mailbox.send(message)
        logger.debug("Message sent: %s -> %s: %s", sender_id, recipient_id, subject)

    def broadcast(self, sender_id: str, subject: str, body: Any) -> None:
        for agent in self._registry.list_all():
            if agent.id != sender_id:
                self.send_message(sender_id, agent.id, subject, body)

    def get_project_metrics(self, project_id: str) -> dict[str, Any] | None:
        metrics = organizational_metrics.get_project_metrics(project_id)
        if metrics:
            return {
                "project_id": metrics.project_id,
                "duration_seconds": metrics.duration_seconds,
                "tasks_completed": metrics.tasks_completed,
                "tasks_failed": metrics.tasks_failed,
                "success_rate": metrics.success_rate,
                "total_tokens": metrics.total_tokens,
                "total_cost": metrics.total_cost,
            }
        return None

    def get_team_metrics(self, team_id: str) -> dict[str, Any] | None:
        metrics = organizational_metrics.get_team_metrics(team_id)
        if metrics:
            return {
                "team_id": metrics.team_id,
                "projects_completed": metrics.projects_completed,
                "projects_failed": metrics.projects_failed,
                "average_duration_seconds": metrics.average_duration_seconds,
                "average_quality": metrics.average_quality,
                "average_cost": metrics.average_cost,
            }
        return None

    def get_organization_state(self) -> dict[str, Any]:
        return {
            "total_agents": len(self._registry.list_all()),
            "agents_by_role": {
                role.value: len(self._registry.find_by_role(role))
                for role in AgentRole
            },
            "agents_by_department": {
                dept.value: len(self._registry.find_by_department(dept))
                for dept in Department
            },
            "active_projects": len(self._projects),
            "blackboard_entries": len(blackboard.read_all_sync()),
        }


def create_society(name: str, description: str = "") -> SocietyRuntime:
    config = SocietyConfig(name=name, description=description)
    return SocietyRuntime(config=config)
