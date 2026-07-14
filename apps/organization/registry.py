"""
Agent Registry
==============

Central registry for all agents in the organization.
Each agent has identity, role, department, skills, cost, quality, latency,
availability, memory, tools, and manager.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class AgentRole(str, Enum):
    CEO = "ceo"
    DIRECTOR = "director"
    MANAGER = "manager"
    LEAD = "lead"
    WORKER = "worker"
    SPECIALIST = "specialist"


class AgentStatus(str, Enum):
    IDLE = "idle"
    BUSY = "busy"
    OFFLINE = "offline"
    ERROR = "error"


class Department(str, Enum):
    ENGINEERING = "engineering"
    NETWORK = "network"
    AI = "ai"
    DEVOPS = "devops"
    RESEARCH = "research"
    DOCUMENTATION = "documentation"
    QUALITY = "quality"
    SECURITY = "security"
    INFRASTRUCTURE = "infrastructure"


@dataclass
class AgentTool:
    name: str
    description: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentMemory:
    total_tokens: int = 0
    available_tokens: int = 0
    context_window: int = 0
    history: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AgentMetrics:
    tasks_completed: int = 0
    tasks_failed: int = 0
    average_latency_ms: float = 0.0
    total_cost: float = 0.0
    quality_score: float = 1.0
    last_active: datetime | None = None


@dataclass
class AgentRecord:
    id: str
    name: str
    role: AgentRole
    department: Department
    skills: list[str] = field(default_factory=list)
    cost_per_token: float = 0.0
    latency_ms: float = 0.0
    availability: float = 1.0
    status: AgentStatus = AgentStatus.IDLE
    manager_id: str | None = None
    tools: list[AgentTool] = field(default_factory=list)
    memory: AgentMemory = field(default_factory=AgentMemory)
    metrics: AgentMetrics = field(default_factory=AgentMetrics)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


class AgentRegistry:
    """Central registry for all agents."""

    def __init__(self):
        self._agents: dict[str, AgentRecord] = {}
        self._skill_index: dict[str, list[str]] = {}
        self._department_index: dict[Department, list[str]] = {}

    def register(self, agent: AgentRecord) -> None:
        self._agents[agent.id] = agent
        for skill in agent.skills:
            self._skill_index.setdefault(skill.lower(), []).append(agent.id)
        self._department_index.setdefault(agent.department, []).append(agent.id)

    def unregister(self, agent_id: str) -> bool:
        if agent_id not in self._agents:
            return False
        agent = self._agents.pop(agent_id)
        for skill in agent.skills:
            self._skill_index.get(skill.lower(), []).remove(agent_id)
        dept_list = self._department_index.get(agent.department, [])
        if agent_id in dept_list:
            dept_list.remove(agent_id)
        return True

    def get(self, agent_id: str) -> AgentRecord | None:
        return self._agents.get(agent_id)

    def find_by_skill(self, skill: str) -> list[AgentRecord]:
        agent_ids = self._skill_index.get(skill.lower(), [])
        return [self._agents[aid] for aid in agent_ids if aid in self._agents]

    def find_by_department(self, department: Department) -> list[AgentRecord]:
        agent_ids = self._department_index.get(department, [])
        return [self._agents[aid] for aid in agent_ids if aid in self._agents]

    def find_by_role(self, role: AgentRole) -> list[AgentRecord]:
        return [a for a in self._agents.values() if a.role == role]

    def get_subordinates(self, manager_id: str) -> list[AgentRecord]:
        return [a for a in self._agents.values() if a.manager_id == manager_id]

    def get_chain_of_command(self, agent_id: str) -> list[AgentRecord]:
        chain = []
        current = self._agents.get(agent_id)
        while current:
            chain.append(current)
            current = self._agents.get(current.manager_id) if current.manager_id else None
        return chain

    def list_all(self) -> list[AgentRecord]:
        return list(self._agents.values())

    def update_metrics(self, agent_id: str, **kwargs) -> None:
        agent = self._agents.get(agent_id)
        if agent:
            for key, value in kwargs.items():
                if hasattr(agent.metrics, key):
                    setattr(agent.metrics, key, value)


agent_registry = AgentRegistry()
