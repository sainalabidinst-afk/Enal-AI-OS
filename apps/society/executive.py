"""
Executive Intelligence
=======================

The reasoning layer for the CEO and top-level leadership.
Transforms user vision into business goals, organizational design, budget, and execution plans.
"""

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from apps.organization.economics import organizational_economics
from apps.organization.kernel import organization_kernel

logger = logging.getLogger(__name__)


class GoalType(str, Enum):
    BUILD = "build"
    IMPROVE = "improve"
    FIX = "fix"
    AUDIT = "audit"
    RESEARCH = "research"
    OPTIMIZE = "optimize"


class ConstraintType(str, Enum):
    BUDGET = "budget"
    TIMELINE = "timeline"
    TECHNOLOGY = "technology"
    COMPLIANCE = "compliance"
    RESOURCE = "resource"
    QUALITY = "quality"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Constraint:
    type: ConstraintType
    description: str
    value: Any = None
    hard: bool = True


@dataclass
class Risk:
    id: str
    description: str
    level: RiskLevel
    mitigation: str = ""
    owner: str = ""


@dataclass
class BusinessGoal:
    id: str
    description: str
    goal_type: GoalType
    success_criteria: list[str] = field(default_factory=list)
    constraints: list[Constraint] = field(default_factory=list)
    risks: list[Risk] = field(default_factory=list)
    estimated_duration_days: int = 0
    estimated_budget: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionPlan:
    goal_id: str
    phases: list[dict[str, Any]] = field(default_factory=list)
    milestones: list[dict[str, Any]] = field(default_factory=list)
    budget_allocation: dict[str, float] = field(default_factory=dict)
    timeline: dict[str, datetime] = field(default_factory=dict)


@dataclass
class Vision:
    raw_input: str
    interpreted_goal: str = ""
    domain: str = "general"
    stakeholders: list[str] = field(default_factory=list)
    success_definition: str = ""
    constraints: list[Constraint] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class ExecutiveIntelligence:
    """CEO reasoning engine for vision interpretation and planning."""

    def __init__(self):
        self._vision: Vision | None = None
        self._goals: list[BusinessGoal] = []
        self._plans: dict[str, ExecutionPlan] = {}

    def interpret_vision(self, user_input: str) -> Vision:
        logger.info("Interpreting user vision: %s", user_input[:100])
        self._vision = Vision(raw_input=user_input)

        domain_keywords = {
            "network": ["network", "router", "switch", "firewall", "vpn", "cisco", "mikrotik", "fortinet"],
            "software": ["software", "application", "api", "backend", "frontend", "database", "code"],
            "trading": ["trading", "stock", "crypto", "finance", "market", "investment"],
            "research": ["research", "analysis", "study", "paper", "experiment"],
            "devops": ["devops", "deploy", "kubernetes", "docker", "ci/cd", "infrastructure"],
        }

        lower_input = user_input.lower()
        detected_domain = "general"
        for domain, keywords in domain_keywords.items():
            if any(kw in lower_input for kw in keywords):
                detected_domain = domain
                break

        self._vision.domain = detected_domain
        self._vision.interpreted_goal = self._decompose_goal(user_input)
        self._vision.constraints = self._extract_constraints(user_input)
        self._vision.success_definition = self._define_success(user_input, detected_domain)

        logger.info("Vision interpreted: domain=%s, goal=%s", detected_domain, self._vision.interpreted_goal)
        return self._vision

    def create_goal(self, description: str, goal_type: GoalType = GoalType.BUILD, constraints: list[Constraint] | None = None) -> BusinessGoal:
        goal_id = f"goal-{uuid.uuid4().hex[:8]}"
        goal = BusinessGoal(
            id=goal_id,
            description=description,
            goal_type=goal_type,
            constraints=constraints or [],
        )
        self._goals.append(goal)
        logger.info("Business goal created: %s - %s", goal_id, description)
        return goal

    def create_execution_plan(self, goal: BusinessGoal) -> ExecutionPlan:
        plan = ExecutionPlan(goal_id=goal.id)
        plan.phases = self._generate_phases(goal)
        plan.milestones = self._generate_milestones(goal, plan.phases)
        plan.budget_allocation = self._allocate_budget(goal)
        plan.timeline = self._generate_timeline(goal, plan.phases)

        if plan.budget_allocation:
            total_budget = sum(plan.budget_allocation.values())
            organization_kernel.set_budget(total_budget)
            organization_kernel.allocate_budget(total_budget, "ceo", f"Execution plan for goal {goal.id}")

        self._plans[goal.id] = plan
        logger.info("Execution plan created for goal %s: %d phases, budget=%.2f", goal.id, len(plan.phases), total_budget)
        return plan

    def analyze_roi(self, analysis_type: str, **kwargs) -> dict[str, Any]:
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
        }

    def get_vision(self) -> Vision | None:
        return self._vision

    def get_goals(self) -> list[BusinessGoal]:
        return list(self._goals)

    def get_plan(self, goal_id: str) -> ExecutionPlan | None:
        return self._plans.get(goal_id)

    def _decompose_goal(self, user_input: str) -> str:
        templates = {
            "network": "Design, configure, and validate network infrastructure",
            "software": "Design, build, test, and deploy software application",
            "trading": "Analyze, model, and optimize trading strategy",
            "research": "Conduct research, analyze findings, and produce report",
            "devops": "Design, implement, and automate infrastructure pipeline",
            "general": "Analyze requirements, design solution, implement, and validate",
        }

        lower_input = user_input.lower()
        for domain, template in templates.items():
            if domain in lower_input or any(kw in lower_input for kw in [domain]):
                return template

        return "Analyze requirements, design solution, implement, and validate"

    def _extract_constraints(self, user_input: str) -> list[Constraint]:
        constraints = []
        lower_input = user_input.lower()

        if any(kw in lower_input for kw in ["budget", "cost", "price", "cheap", "murah"]):
            constraints.append(Constraint(type=ConstraintType.BUDGET, description="Budget constraint mentioned", hard=False))
        if any(kw in lower_input for kw in ["fast", "quick", "urgent", "cepat", "segera"]):
            constraints.append(Constraint(type=ConstraintType.TIMELINE, description="Timeline constraint mentioned", hard=True))
        if any(kw in lower_input for kw in ["compliance", "regulation", "standard", "kepatuhan"]):
            constraints.append(Constraint(type=ConstraintType.COMPLIANCE, description="Compliance constraint mentioned", hard=True))
        if any(kw in lower_input for kw in ["secure", "security", "aman", "keamanan"]):
            constraints.append(Constraint(type=ConstraintType.QUALITY, description="Security/quality constraint mentioned", hard=True))

        return constraints

    def _define_success(self, user_input: str, domain: str) -> str:
        success_templates = {
            "network": "Network is operational, secure, and meets performance requirements",
            "software": "Application is deployed, tested, and meets functional requirements",
            "trading": "Strategy is backtested, documented, and ready for live testing",
            "research": "Findings are documented, validated, and actionable",
            "devops": "Pipeline is automated, reliable, and meets deployment SLAs",
            "general": "Solution is implemented, tested, and meets user requirements",
        }
        return success_templates.get(domain, success_templates["general"])

    def _generate_phases(self, goal: BusinessGoal) -> list[dict[str, Any]]:
        phase_templates = {
            GoalType.BUILD: [
                {"name": "Requirements Analysis", "description": "Analyze and document requirements", "duration_days": 3},
                {"name": "Architecture Design", "description": "Design system architecture", "duration_days": 5},
                {"name": "Implementation", "description": "Implement core functionality", "duration_days": 14},
                {"name": "Testing", "description": "Test and validate implementation", "duration_days": 5},
                {"name": "Deployment", "description": "Deploy to production", "duration_days": 2},
            ],
            GoalType.IMPROVE: [
                {"name": "Current State Analysis", "description": "Analyze existing system", "duration_days": 3},
                {"name": "Gap Analysis", "description": "Identify gaps and opportunities", "duration_days": 3},
                {"name": "Implementation", "description": "Implement improvements", "duration_days": 10},
                {"name": "Validation", "description": "Validate improvements", "duration_days": 3},
            ],
            GoalType.AUDIT: [
                {"name": "Scope Definition", "description": "Define audit scope", "duration_days": 2},
                {"name": "Data Collection", "description": "Collect configuration and evidence", "duration_days": 5},
                {"name": "Analysis", "description": "Analyze against standards", "duration_days": 5},
                {"name": "Reporting", "description": "Generate audit report", "duration_days": 3},
            ],
            GoalType.RESEARCH: [
                {"name": "Literature Review", "description": "Review existing research", "duration_days": 5},
                {"name": "Methodology", "description": "Define research methodology", "duration_days": 3},
                {"name": "Execution", "description": "Execute research plan", "duration_days": 10},
                {"name": "Synthesis", "description": "Synthesize findings", "duration_days": 5},
            ],
        }

        return phase_templates.get(goal.goal_type, phase_templates[GoalType.BUILD])

    def _generate_milestones(self, goal: BusinessGoal, phases: list[dict[str, Any]]) -> list[dict[str, Any]]:
        milestones = []
        for i, phase in enumerate(phases):
            milestones.append({
                "id": f"milestone-{i+1}",
                "name": phase["name"],
                "phase": i + 1,
                "criteria": f"Phase {i+1} completed successfully",
            })
        return milestones

    def _allocate_budget(self, goal: BusinessGoal) -> dict[str, float]:
        total = goal.estimated_budget or 10000.0
        phases = self._generate_phases(goal)
        allocation = {}
        per_phase = total / len(phases) if phases else total
        for phase in phases:
            allocation[phase["name"]] = round(per_phase, 2)
        return allocation

    def _generate_timeline(self, goal: BusinessGoal, phases: list[dict[str, Any]]) -> dict[str, datetime]:
        timeline = {}
        current_date = datetime.utcnow()
        for phase in phases:
            timeline[phase["name"]] = current_date
            duration = phase.get("duration_days", 7)
            current_date = datetime(current_date.year, current_date.month, current_date.day + duration)
        return timeline


executive_intelligence = ExecutiveIntelligence()
