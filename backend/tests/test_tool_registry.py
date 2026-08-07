import pytest

from backend.app.core.tool_registry import Tool, ToolRegistry


class TestToolRegistry:
    def test_register_tool(self):
        registry = ToolRegistry()
        tool = Tool(name="scan", category="network", agent="network-agent")
        registry.register(tool)
        assert registry.get("scan") is tool

    def test_get_missing_tool_returns_none(self):
        registry = ToolRegistry()
        assert registry.get("missing") is None

    def test_get_tools_filters_by_agent(self):
        registry = ToolRegistry()
        registry.register(Tool(name="t1", category="a", agent="network-agent"))
        registry.register(Tool(name="t2", category="b", agent="code-agent"))
        tools = registry.get_tools("network-agent")
        assert len(tools) == 1
        assert tools[0]["function"]["name"] == "t1"

    def test_get_tools_includes_reviewer_extra(self):
        registry = ToolRegistry()
        registry.register(Tool(name="t1", category="a", agent="reviewer"))
        tools = registry.get_tools("reviewer")
        assert any(t["function"]["name"] == "run_tests" for t in tools)

    def test_search_by_capability(self):
        registry = ToolRegistry()
        registry.register(Tool(name="t1", capabilities=["scan"], agent="a"))
        registry.register(Tool(name="t2", capabilities=["build"], agent="a"))
        results = registry.find_by_capability("scan")
        assert len(results) == 1
        assert results[0].name == "t1"

    def test_list_by_category(self):
        registry = ToolRegistry()
        registry.register(Tool(name="t1", category="net", agent="a"))
        registry.register(Tool(name="t2", category="code", agent="a"))
        assert len(registry.list_by_category("net")) == 1
        assert len(registry.list_by_category("code")) == 1

    def test_to_openai_schema(self):
        registry = ToolRegistry()
        tool = Tool(name="run", category="ops", parameters={"type": "object"}, agent="ops-agent")
        registry.register(tool)
        schema = registry.to_openai_schema(tool)
        assert schema["type"] == "function"
        assert schema["function"]["name"] == "run"
