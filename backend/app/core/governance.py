import logging
from dataclasses import dataclass, field
from typing import Any
from enum import Enum

logger = logging.getLogger(__name__)


class Permission(str, Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DEPLOY = "deploy"
    ADMIN = "admin"


@dataclass
class Policy:
    id: str
    name: str
    agent: str
    permissions: list[Permission]
    tools: list[str]
    conditions: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class PolicyEngine:
    def __init__(self):
        self._policies: dict[str, Policy] = {}

    def add_policy(self, policy: Policy):
        self._policies[policy.id] = policy
        logger.info(f"Policy added: {policy.id} for {policy.agent}")

    def can_execute(self, agent: str, tool: str, permission: Permission) -> bool:
        policy = next((p for p in self._policies.values() if p.agent == agent), None)
        if not policy:
            return False
        if permission not in policy.permissions:
            return False
        if tool and tool not in policy.tools:
            return False
        return True

    def get_policy(self, agent: str) -> Policy | None:
        return next((p for p in self._policies.values() if p.agent == agent), None)


policy_engine = PolicyEngine()
