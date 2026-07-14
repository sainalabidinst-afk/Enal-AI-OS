import logging
from dataclasses import dataclass, field
from typing import Any
from enum import Enum

logger = logging.getLogger(__name__)


class MCPResourceType(str, Enum):
    FILE = "file"
    DATABASE = "database"
    API = "api"
    SERVICE = "service"
    SECRET = "secret"


@dataclass
class MCPResource:
    uri: str
    name: str
    description: str
    resource_type: MCPResourceType
    permissions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MCPTool:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: Any = None
    permissions: list[str] = field(default_factory=list)
    sandbox: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MCPPlugin:
    id: str
    name: str
    version: str
    description: str
    tools: list[MCPTool] = field(default_factory=list)
    resources: list[MCPResource] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class MCPRegistry:
    def __init__(self):
        self._plugins: dict[str, MCPPlugin] = {}
        self._tools: dict[str, MCPTool] = {}
        self._resources: dict[str, MCPResource] = {}

    def register_plugin(self, plugin: MCPPlugin):
        self._plugins[plugin.id] = plugin
        for tool in plugin.tools:
            self._tools[tool.name] = tool
        for resource in plugin.resources:
            self._resources[resource.uri] = resource
        logger.info(f"MCP plugin registered: {plugin.id} ({len(plugin.tools)} tools)")

    def get_tool(self, name: str) -> MCPTool | None:
        return self._tools.get(name)

    def get_plugin(self, plugin_id: str) -> MCPPlugin | None:
        return self._plugins.get(plugin_id)

    def list_tools(self, permissions: list[str] | None = None) -> list[MCPTool]:
        tools = list(self._tools.values())
        if permissions:
            tools = [t for t in tools if any(p in t.permissions for p in permissions)]
        return tools

    def list_plugins(self) -> list[MCPPlugin]:
        return list(self._plugins.values())

    def to_openai_schema(self, tool: MCPTool) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema,
            },
        }

    def all_schemas(self) -> list[dict[str, Any]]:
        return [self.to_openai_schema(t) for t in self._tools.values()]


mcp_registry = MCPRegistry()
