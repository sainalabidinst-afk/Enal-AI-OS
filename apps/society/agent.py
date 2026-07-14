"""
Agent Base Class
=================

Base class for all Society agents.
Each agent has identity, role, department, skills, tools, and lifecycle methods.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from apps.organization.registry import (
    AgentRecord,
    AgentRole,
    Department,
    AgentRegistry,
    agent_registry,
)


@dataclass
class AgentContext:
    agent_id: str
    task: dict[str, Any] | None = None
    memory: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class Agent(ABC):
    """Base class for all micro-agents in the Society."""

    def __init__(
        self,
        agent_id: str,
        name: str,
        role: AgentRole,
        department: Department,
        skills: list[str] | None = None,
        manager_id: str | None = None,
        tools: list[dict[str, Any]] | None = None,
    ):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.department = department
        self.skills = skills or []
        self.manager_id = manager_id
        self.tools = tools or []
        self.context = AgentContext(agent_id=agent_id)
        self._registry = agent_registry

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        self.context.task = task
        result = await self._execute(task)
        self._update_metrics(success=True)
        return result

    @abstractmethod
    async def _execute(self, task: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    async def receive_message(self, message: dict[str, Any]) -> dict[str, Any]:
        self.context.memory.append(message)
        return await self._handle_message(message)

    async def _handle_message(self, message: dict[str, Any]) -> dict[str, Any]:
        return {"status": "acknowledged", "agent_id": self.agent_id}

    def _update_metrics(self, success: bool, tokens: int = 0, cost: float = 0.0) -> None:
        self._registry.update_metrics(
            self.agent_id,
            tasks_completed=1 if success else 0,
            tasks_failed=0 if success else 1,
            total_tokens=tokens,
            total_cost=cost,
            last_active=datetime.utcnow(),
        )
