"""
A2A invoker for calling external agents.

Invokes external A2A-compatible agents via HTTP.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class A2AInvoker:
    """Invoke external A2A agents via real HTTP."""

    async def invoke(self, agent_endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        logger.info("Invoking A2A agent at %s", agent_endpoint)
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(agent_endpoint, json=payload)
                response.raise_for_status()
                try:
                    result_data = response.json()
                except Exception:
                    result_data = response.text
                return {
                    "endpoint": agent_endpoint,
                    "success": True,
                    "result": result_data,
                    "payload": payload,
                    "http_status": response.status_code,
                }
        except Exception as exc:
            logger.error("A2A invocation to %s failed: %s", agent_endpoint, exc)
            return {
                "endpoint": agent_endpoint,
                "success": False,
                "error": str(exc),
                "payload": payload,
            }


a2a_invoker = A2AInvoker()
