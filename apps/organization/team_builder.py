"""
Team Builder
============

Dynamically forms teams based on task requirements.
Searches the Agent Registry for the best agents for each role needed.
"""

from dataclasses import dataclass, field
from typing import Any

from apps.organization.registry import (
    AgentRecord,
    AgentRole,
    Department,
    AgentRegistry,
    agent_registry,
)
from apps.organization.runtime import OrganizationRuntime, organization_runtime


@dataclass
class TaskRequirement:
    description: str
    required_skills: list[str] = field(default_factory=list)
    department: Department | None = None
    team_size: int = 3
    min_quality: float = 0.7
    max_cost: float = float("inf")
    max_latency_ms: float = float("inf")


@dataclass
class TeamMember:
    agent: AgentRecord
    role_in_team: str
    reason: str


@dataclass
class Team:
    task: TaskRequirement
    members: list[TeamMember]
    lead_id: str | None = None
    estimated_cost: float = 0.0
    estimated_latency_ms: float = 0.0


class TeamBuilder:
    """Dynamically forms teams based on task requirements."""

    def __init__(self, registry: AgentRegistry, runtime: OrganizationRuntime):
        self._registry = registry
        self._runtime = runtime

    def build_team(self, requirement: TaskRequirement) -> Team:
        members = []
        candidates = self._registry.list_all()

        skill_candidates = []
        for skill in requirement.required_skills:
            matched = self._registry.find_by_skill(skill)
            skill_candidates.extend(matched)
        if not skill_candidates:
            skill_candidates = candidates

        scored = []
        for agent in skill_candidates:
            if agent.status.value == "offline":
                continue
            if agent.availability < 0.5:
                continue
            if agent.metrics.quality_score < requirement.min_quality:
                continue
            if agent.cost_per_token > requirement.max_cost:
                continue
            if agent.latency_ms > requirement.max_latency_ms:
                continue
            score = self._score_agent(agent, requirement)
            scored.append((score, agent))

        scored.sort(key=lambda x: x[0], reverse=True)
        selected = [agent for _, agent in scored[: requirement.team_size]]

        for i, agent in enumerate(selected):
            members.append(TeamMember(
                agent=agent,
                role_in_team=f"role_{i}",
                reason=f"matched {len(set(agent.skills) & set(requirement.required_skills))} skills",
            ))

        total_cost = sum(a.cost_per_token for a in selected)
        total_latency = max(a.latency_ms for a in selected) if selected else 0.0

        return Team(
            task=requirement,
            members=members,
            estimated_cost=total_cost,
            estimated_latency_ms=total_latency,
        )

    def _score_agent(self, agent: AgentRecord, requirement: TaskRequirement) -> float:
        skill_match = len(set(agent.skills) & set(requirement.required_skills))
        quality = agent.metrics.quality_score
        availability = agent.availability
        cost_score = max(0, 1 - agent.cost_per_token / max(requirement.max_cost, 1))
        latency_score = max(0, 1 - agent.latency_ms / max(requirement.max_latency_ms, 1))
        return (
            0.3 * (skill_match / max(len(requirement.required_skills), 1))
            + 0.25 * quality
            + 0.2 * availability
            + 0.15 * cost_score
            + 0.1 * latency_score
        )


team_builder = TeamBuilder(agent_registry, organization_runtime)
