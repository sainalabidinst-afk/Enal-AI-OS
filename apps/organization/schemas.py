"""
Organization Capability Schemas
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentRole:
    role_id: str
    name: str
    capabilities: list[str] = field(default_factory=list)


@dataclass
class AgentRegistry:
    agents: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class Team:
    team_id: str
    name: str
    members: list[str] = field(default_factory=list)
