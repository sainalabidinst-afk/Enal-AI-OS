"""
Enal AI OS SDK
==============

Developer-friendly SDK for building agents, tools, and workflows.

Example:
    from enal_ai import Agent, Tool, Workflow

    class MikrotikAgent(Agent):
        name = "mikrotik"
        capabilities = ["networking", "mikrotik", "firewall"]

        async def execute(self, task: str) -> str:
            return f"Configuring Mikrotik: {task}"

    agent = MikrotikAgent()
    result = await agent.run("Configure hotspot")
"""

from typing import Any, Callable, Awaitable, Optional
from pydantic import BaseModel, Field
import asyncio
import logging

logger = logging.getLogger(__name__)


class AgentConfig(BaseModel):
    name: str = Field(..., description="Unique agent name")
    description: str = Field("", description="Agent description")
    capabilities: list[str] = Field(default_factory=list, description="Agent capabilities")
    model: Optional[str] = Field(None, description="LLM model to use")
    temperature: float = Field(0.7, description="Model temperature")
    max_tokens: int = Field(4096, description="Max tokens")
    tools: list[str] = Field(default_factory=list, description="Allowed tools")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ToolConfig(BaseModel):
    name: str = Field(..., description="Tool name")
    description: str = Field("", description="Tool description")
    parameters: dict[str, Any] = Field(default_factory=dict, description="Tool parameters schema")
    handler: Optional[Callable[..., Awaitable[Any]]] = Field(None, description="Tool handler function")
    sandbox: bool = Field(False, description="Run in sandbox")
    permissions: list[str] = Field(default_factory=list, description="Required permissions")


class WorkflowStep(BaseModel):
    id: str
    name: str
    agent: str
    action: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    depends_on: list[str] = Field(default_factory=list)
    condition: Optional[str] = Field(None, description="Conditional execution")


class WorkflowConfig(BaseModel):
    name: str
    description: str
    steps: list[WorkflowStep]
    metadata: dict[str, Any] = Field(default_factory=dict)


class Agent:
    """Base class for all Enal AI OS agents."""

    config: AgentConfig | None = None

    def __init__(self, **kwargs):
        if self.config is None:
            self.config = AgentConfig(**kwargs)
        else:
            self.config = AgentConfig(**self.config.model_dump(), **kwargs)

    async def execute(self, task: str, context: dict[str, Any] | None = None) -> str:
        raise NotImplementedError

    async def run(self, task: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            result = await self.execute(task, context)
            return {"agent": self.config.name, "task": task, "result": result, "success": True}
        except Exception as e:
            logger.error(f"Agent {self.config.name} failed: {e}")
            return {"agent": self.config.name, "task": task, "result": str(e), "success": False}

    def to_dict(self) -> dict[str, Any]:
        return self.config.model_dump()


class Tool:
    """Base class for all Enal AI OS tools."""

    config: ToolConfig | None = None

    def __init__(self, **kwargs):
        if self.config is None:
            self.config = ToolConfig(**kwargs)
        else:
            self.config = ToolConfig(**self.config.model_dump(), **kwargs)

    async def invoke(self, parameters: dict[str, Any]) -> dict[str, Any]:
        if self.config.handler:
            result = await self.config.handler(**parameters)
            return {"tool": self.config.name, "result": result, "success": True}
        return {"tool": self.config.name, "result": None, "success": False}

    def to_dict(self) -> dict[str, Any]:
        return self.config.model_dump()


class Workflow:
    """Base class for all Enal AI OS workflows."""

    config: WorkflowConfig | None = None

    def __init__(self, **kwargs):
        if self.config is None:
            self.config = WorkflowConfig(**kwargs)
        else:
            self.config = WorkflowConfig(**self.config.model_dump(), **kwargs)

    async def execute(self, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        results = {}
        for step in self.config.steps:
            try:
                results[step.id] = {"status": "completed", "result": None}
            except Exception as e:
                results[step.id] = {"status": "failed", "error": str(e)}
        return {"workflow": self.config.name, "results": results}

    def to_dict(self) -> dict[str, Any]:
        return self.config.model_dump()


class EnalAI:
    """Main SDK entry point."""

    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self._agents: dict[str, Agent] = {}
        self._tools: dict[str, Tool] = {}
        self._workflows: dict[str, Workflow] = {}

    def agent(self, name: str, **kwargs):
        """Decorator to register an agent."""
        def decorator(cls):
            agent_instance = cls(name=name, **kwargs)
            self._agents[name] = agent_instance
            return cls
        return decorator

    def tool(self, name: str, **kwargs):
        """Decorator to register a tool."""
        def decorator(func):
            async def wrapper(**params):
                return await func(**params)
            tool_instance = Tool(name=name, handler=wrapper, **kwargs)
            self._tools[name] = tool_instance
            return wrapper
        return decorator

    def workflow(self, name: str, **kwargs):
        """Decorator to register a workflow."""
        def decorator(cls):
            workflow_instance = cls(name=name, **kwargs)
            self._workflows[name] = workflow_instance
            return cls
        return decorator

    def get_agent(self, name: str) -> Agent | None:
        return self._agents.get(name)

    def get_tool(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def get_workflow(self, name: str) -> Workflow | None:
        return self._workflows.get(name)

    def list_agents(self) -> list[str]:
        return list(self._agents.keys())

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())

    def list_workflows(self) -> list[str]:
        return list(self._workflows.keys())


# Global SDK instance
sdk = EnalAI()
