"""
Society Capability Schemas
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Agent:
    agent_id: str
    name: str
    role: str
    memory: list[str] = field(default_factory=list)


@dataclass
class Conversation:
    conversation_id: str
    participants: list[str] = field(default_factory=list)
    messages: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class Society:
    society_id: str
    agents: list[Agent] = field(default_factory=list)
    conversations: list[Conversation] = field(default_factory=list)
