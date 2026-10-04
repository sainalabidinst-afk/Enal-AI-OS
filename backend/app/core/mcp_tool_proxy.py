"""
MCP tool proxy for invoking tools on external MCP servers.

Proxies tool calls to registered MCP servers via real HTTP requests.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from backend.app.core.mcp_tool_registry import mcp_tool_registry

logger = logging.getLogger(__name__)


class MCPToolProxy:
    """Proxy tool calls to MCP servers via real HTTP."""

    async def call_tool(
        self,
        server_id: str,
        tool_name: str,
        parameters: dict[str, Any],
    ) -> dict[str, Any]:
        logger.info("Calling MCP tool %s on server %s", tool_name, server_id)
        try:
            server = mcp_tool_registry._servers.get(server_id)
            if not server:
                return {
                    "server_id": server_id,
                    "tool": tool_name,
                    "parameters": parameters,
                    "success": False,
                    "error": f"MCP server {server_id} not found",
                }
            endpoint = server.get("endpoint", "")
            if not endpoint:
                return {
                    "server_id": server_id,
                    "tool": tool_name,
                    "parameters": parameters,
                    "success": False,
                    "error": f"MCP server {server_id} has no endpoint",
                }
            tool_url = f"{endpoint.rstrip('/')}/tools/{tool_name}"
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(tool_url, json=parameters)
                response.raise_for_status()
                try:
                    result_data = response.json()
                except Exception:
                    result_data = response.text
                return {
                    "server_id": server_id,
                    "tool": tool_name,
                    "parameters": parameters,
                    "success": True,
                    "result": result_data,
                    "http_status": response.status_code,
                }
        except Exception as exc:
            logger.error("MCP tool call to %s/%s failed: %s", server_id, tool_name, exc)
            return {
                "server_id": server_id,
                "tool": tool_name,
                "parameters": parameters,
                "success": False,
                "error": str(exc),
            }


mcp_tool_proxy = MCPToolProxy()
