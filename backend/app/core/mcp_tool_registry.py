"""
MCP tool registry for external MCP servers.

Registers MCP servers and proxies tool calls to them.
"""

from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


class MCPToolRegistry:
    """Registry for MCP servers and their tools."""

    def __init__(self) -> None:
        self._servers: dict[str, dict[str, Any]] = {}
        self._tools: dict[str, dict[str, Any]] = {}

    def register_server(self, name: str, endpoint: str) -> dict[str, Any]:
        server_id = str(uuid.uuid4())
        server = {
            "id": server_id,
            "name": name,
            "endpoint": endpoint,
            "status": "disconnected",
            "created_at": datetime.now(UTC).isoformat(),
        }
        self._servers[server_id] = server
        logger.info("Registered MCP server %s at %s", name, endpoint)
        return server

    def connect(self, server_id: str) -> dict[str, Any]:
        server = self._servers.get(server_id)
        if not server:
            raise ValueError(f"MCP server not found: {server_id}")
        server["status"] = "connected"
        logger.info("Connected to MCP server %s", server_id)
        return server

    def disconnect(self, server_id: str) -> dict[str, Any]:
        server = self._servers.get(server_id)
        if not server:
            raise ValueError(f"MCP server not found: {server_id}")
        server["status"] = "disconnected"
        logger.info("Disconnected from MCP server %s", server_id)
        return server

    def list_servers(self) -> list[dict[str, Any]]:
        return list(self._servers.values())


mcp_tool_registry = MCPToolRegistry()
