"""
Agent Communication
====================

Internal mailbox, event system, and blackboard for inter-agent communication.
Enables agents to collaborate without always going through a central planner.
"""

import logging
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class MessageType(str, Enum):
    TASK = "task"
    REPLY = "reply"
    QUERY = "query"
    RESULT = "result"
    ERROR = "error"
    EVENT = "event"
    DELEGATION = "delegation"


class Priority(int, Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4


@dataclass
class Message:
    id: str
    sender_id: str
    recipient_id: str
    type: MessageType
    subject: str
    body: Any
    priority: Priority = Priority.NORMAL
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    reply_to: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class Mailbox:
    """Per-agent mailbox for direct communication."""

    def __init__(self):
        self._inboxes: dict[str, list[Message]] = {}
        self._sent: dict[str, list[Message]] = {}

    def send(self, message: Message) -> None:
        self._inboxes.setdefault(message.recipient_id, []).append(message)
        self._sent.setdefault(message.sender_id, []).append(message)
        logger.debug(f"Message sent: {message.sender_id} -> {message.recipient_id}: {message.subject}")

    def receive(self, agent_id: str) -> list[Message]:
        messages = self._inboxes.get(agent_id, [])
        self._inboxes[agent_id] = []
        return messages

    def peek(self, agent_id: str) -> list[Message]:
        return list(self._inboxes.get(agent_id, []))


class Event:
    """System-wide event."""

    def __init__(self, event_type: str, source: str, data: Any):
        self.id = str(uuid.uuid4())
        self.type = event_type
        self.source = source
        self.data = data
        self.timestamp = datetime.now(timezone.utc)


class EventBus:
    """Publish-subscribe event bus for organization-wide events."""

    def __init__(self):
        self._subscribers: dict[str, list[Callable[[Any], None]]] = {}

    def subscribe(self, event_type: str, callback: Callable[[Any], None]) -> None:
        self._subscribers.setdefault(event_type, []).append(callback)

    def publish(self, event: Event) -> None:
        callbacks = self._subscribers.get(event.type, [])
        for callback in callbacks:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"Event callback error: {e}")
        logger.debug(f"Event published: {event.type} from {event.source}")


class Blackboard:
    """Shared blackboard system - all agents can read and write."""

    def __init__(self):
        self._entries: dict[str, Any] = {}
        self._lock: bool = False

    def write(self, key: str, value: Any) -> None:
        self._entries[key] = value
        logger.debug(f"Blackboard write: {key}")

    def read(self, key: str) -> Any | None:
        return self._entries.get(key)

    def read_all(self) -> dict[str, Any]:
        return dict(self._entries)

    def clear(self) -> None:
        self._entries.clear()


mailbox = Mailbox()
event_bus = EventBus()
blackboard = Blackboard()
