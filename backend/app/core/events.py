from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Event:
    event_type: str
    payload: dict[str, Any]
    source: str = "system"
    target: str = "*"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    correlation_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EventEnvelope:
    event: Event
    stream: str
    id: str | None = None
