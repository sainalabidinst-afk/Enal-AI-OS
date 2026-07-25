"""
Organization Runtime
====================

Defines organizational structure: CEO → Directors → Managers → Leads → Workers.
Each role has specific responsibilities and authority levels.
"""

from dataclasses import dataclass, field
from enum import Enum

from apps.organization.registry import (
    AgentRecord,
    AgentRegistry,
    AgentRole,
    Department,
    agent_registry,
)


class AuthorityLevel(int, Enum):
    STRATEGIC = 5
    TACTICAL = 4
    OPERATIONAL = 3
    SUPERVISORY = 2
    EXECUTION = 1


@dataclass
class OrganizationChart:
    ceo_id: str
    directors: dict[str, list[str]] = field(default_factory=dict)  # director_id -> [manager_ids]
    managers: dict[str, list[str]] = field(default_factory=dict)   # manager_id -> [lead_ids]
    leads: dict[str, list[str]] = field(default_factory=dict)      # lead_id -> [worker_ids]


class OrganizationRuntime:
    """Manages organizational hierarchy and agent relationships."""

    def __init__(self, registry: AgentRegistry):
        self._registry = registry
        self._org_chart: OrganizationChart | None = None

    def bootstrap(self, ceo_id: str) -> OrganizationChart:
        ceo = self._registry.get(ceo_id)
        if not ceo:
            raise ValueError(f"CEO agent not found: {ceo_id}")
        self._org_chart = OrganizationChart(ceo_id=ceo_id)
        return self._org_chart

    def assign_director(self, director_id: str, department: Department) -> None:
        director = self._registry.get(director_id)
        if not director:
            raise ValueError(f"Director agent not found: {director_id}")
        director.role = AgentRole.DIRECTOR
        director.department = department
        if self._org_chart:
            self._org_chart.directors.setdefault(director_id, [])

    def assign_manager(self, manager_id: str, director_id: str) -> None:
        manager = self._registry.get(manager_id)
        if not manager:
            raise ValueError(f"Manager agent not found: {manager_id}")
        manager.role = AgentRole.MANAGER
        manager.manager_id = director_id
        if self._org_chart:
            self._org_chart.managers.setdefault(director_id, []).append(manager_id)

    def assign_lead(self, lead_id: str, manager_id: str) -> None:
        lead = self._registry.get(lead_id)
        if not lead:
            raise ValueError(f"Lead agent not found: {lead_id}")
        lead.role = AgentRole.LEAD
        lead.manager_id = manager_id
        if self._org_chart:
            self._org_chart.leads.setdefault(manager_id, []).append(lead_id)

    def assign_worker(self, worker_id: str, lead_id: str) -> None:
        worker = self._registry.get(worker_id)
        if not worker:
            raise ValueError(f"Worker agent not found: {worker_id}")
        worker.role = AgentRole.WORKER
        worker.manager_id = lead_id

    def get_authority(self, agent_id: str) -> AuthorityLevel:
        agent = self._registry.get(agent_id)
        if not agent:
            raise ValueError(f"Agent not found: {agent_id}")
        mapping = {
            AgentRole.CEO: AuthorityLevel.STRATEGIC,
            AgentRole.DIRECTOR: AuthorityLevel.TACTICAL,
            AgentRole.MANAGER: AuthorityLevel.OPERATIONAL,
            AgentRole.LEAD: AuthorityLevel.SUPERVISORY,
            AgentRole.WORKER: AuthorityLevel.EXECUTION,
            AgentRole.SPECIALIST: AuthorityLevel.EXECUTION,
        }
        return mapping.get(agent.role, AuthorityLevel.EXECUTION)

    def can_delegate(self, delegator_id: str, delegatee_id: str) -> bool:
        delegator_auth = self.get_authority(delegator_id)
        delegatee_auth = self.get_authority(delegatee_id)
        return delegator_auth > delegatee_auth

    def get_department_head(self, department: Department) -> AgentRecord | None:
        for agent in self._registry.list_all():
            if agent.department == department and agent.role == AgentRole.DIRECTOR:
                return agent
        return None

    def get_team(self, agent_id: str) -> list[AgentRecord]:
        return self._registry.get_subordinates(agent_id)

    def get_org_chart(self) -> OrganizationChart | None:
        return self._org_chart


organization_runtime = OrganizationRuntime(agent_registry)
