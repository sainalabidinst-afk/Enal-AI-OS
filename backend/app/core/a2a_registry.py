"""
A2A registry for external agent connections.

Manages registration and discovery of external A2A-compatible agents.
"""

from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


class A2ARegistry:
    """Registry for external A2A agents."""

    def __init__(self) -> None:
        self._agents: dict[str, dict[str, Any]] = {}

    def register(
        self,
        name: str,
        endpoint: str,
        capabilities: list[str] | None = None,
    ) -> dict[str, Any]:
        agent_id = str(uuid.uuid4())
        agent = {
            "id": agent_id,
            "name": name,
            "endpoint": endpoint,
            "capabilities": capabilities or [],
            "status": "registered",
            "created_at": datetime.now(UTC).isoformat(),
        }
        self._agents[agent_id] = agent
        logger.info("Registered A2A agent %s at %s", name, endpoint)
        return agent

    def get(self, agent_id: str) -> dict[str, Any] | None:
        return self._agents.get(agent_id)

    def list(self) -> list[dict[str, Any]]:
        return list(self._agents.values())

    def unregister(self, agent_id: str) -> bool:
        if agent_id in self._agents:
            del self._agents[agent_id]
            return True
        return False


a2a_registry = A2ARegistry()
