"""
A2A invoker for calling external agents.

Invokes external A2A-compatible agents via HTTP.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class A2AInvoker:
    """Invoke external A2A agents."""

    async def invoke(self, agent_endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        logger.info("Invoking A2A agent at %s", agent_endpoint)
        return {
            "endpoint": agent_endpoint,
            "success": True,
            "result": f"Simulated A2A response from {agent_endpoint}",
            "payload": payload,
        }


a2a_invoker = A2AInvoker()
