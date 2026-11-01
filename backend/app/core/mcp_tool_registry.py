"""
MCP tool registry for external MCP servers.

Registers MCP servers and proxies tool calls to them.

Supports both HTTP-based servers (``endpoint``) and subprocess-based servers
(``command``/``args``/``env``), the latter being used by local toolkits such as
morluto/rea.
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

    def register_server(
        self,
        name: str,
        endpoint: str = "",
        *,
        command: str | None = None,
        args: list[str] | None = None,
        env: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        server_id = str(uuid.uuid4())
        server = {
            "id": server_id,
            "name": name,
            "endpoint": endpoint,
            "command": command,
            "args": args or [],
            "env": env or {},
            "status": "disconnected",
            "created_at": datetime.now(UTC).isoformat(),
        }
        self._servers[server_id] = server
        logger.info("Registered MCP server %s (id=%s)", name, server_id)
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

    def get_server(self, server_id: str) -> dict[str, Any] | None:
        """Return a server record by id, or ``None`` if not found."""
        return self._servers.get(server_id)


mcp_tool_registry = MCPToolRegistry()
