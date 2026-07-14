import logging
from dataclasses import dataclass, field
from typing import Any, Protocol

logger = logging.getLogger(__name__)


class AsyncToolHandler(Protocol):
    async def __call__(self, **kwargs: Any) -> Any: ...


def _empty_dict() -> dict[str, Any]:
    return {}


def _empty_list() -> list[str]:
    return []


@dataclass
class Tool:
    name: str = ""
    description: str = ""
    category: str = ""
    version: str = "1.0.0"
    author: str = ""
    capabilities: list[str] = field(default_factory=_empty_list)
    permissions: list[str] = field(default_factory=_empty_list)
    parameters: dict[str, Any] = field(default_factory=_empty_dict)
    input_schema: dict[str, Any] = field(default_factory=_empty_dict)
    output_schema: dict[str, Any] = field(default_factory=_empty_dict)
    handler: AsyncToolHandler | None = None
    agent: str = "system"
    sandbox: bool = False
    timeout: int = 30
    cost: float = 0.0
    requires_confirmation: bool = False
    retry_policy: dict[str, Any] = field(default_factory=_empty_dict)
    metadata: dict[str, Any] = field(default_factory=_empty_dict)


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}
        self._by_capability: dict[str, list[Tool]] = {}
        self._by_permission: dict[str, list[Tool]] = {}
        self._by_category: dict[str, list[Tool]] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool
        for cap in tool.capabilities:
            self._by_capability.setdefault(cap, []).append(tool)
        for perm in tool.permissions:
            self._by_permission.setdefault(perm, []).append(tool)
        self._by_category.setdefault(tool.category, []).append(tool)
        logger.info("Tool registered: %s (%s)", tool.name, tool.category)

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def get_tools(self, agent_type: str) -> list[dict]:
        agent_types = [agent_type]
        if agent_type in ["coding-agent", "qa-agent", "reviewer"]:
            agent_types.append("reviewer_extra")
        result = [self.to_openai_schema(t) for t in self._tools.values() if t.agent in agent_types]
        if agent_type in ["coding-agent", "qa-agent", "reviewer"]:
            result.append({
                "type": "function",
                "function": {
                    "name": "run_tests",
                    "description": "Run tests for code",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Test path"}
                        },
                        "required": ["path"],
                    },
                },
            })
        return result

    def find_by_capability(self, capability: str) -> list[Tool]:
        return list(self._by_capability.get(capability, []))

    def find_by_capabilities(self, capabilities: list[str]) -> list[Tool]:
        result: list[Tool] = []
        seen: set[str] = set()
        for cap in capabilities:
            for tool in self._by_capability.get(cap, []):
                if tool.name not in seen:
                    result.append(tool)
                    seen.add(tool.name)
        return result

    def find_by_permission(self, permission: str) -> list[Tool]:
        return list(self._by_permission.get(permission, []))

    def list_by_category(self, category: str) -> list[Tool]:
        return list(self._by_category.get(category, []))

    def list_by_agent(self, agent: str) -> list[Tool]:
        return [t for t in self._tools.values() if t.agent == agent]

    def search(self, query: str) -> list[Tool]:
        query_lower = query.lower()
        return [
            t for t in self._tools.values()
            if query_lower in t.name.lower() or query_lower in t.description.lower()
        ]

    def to_openai_schema(self, tool: Tool) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema or tool.parameters,
            },
        }

    def all_schemas(self) -> list[dict[str, Any]]:
        return [self.to_openai_schema(t) for t in self._tools.values()]


tool_registry = ToolRegistry()
