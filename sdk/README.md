# Enal Cognitive Platform (ECP) SDK

Developer SDK for building agents, tools, and workflows on ECP.

## Installation

```bash
pip install -e .
```

## Status: Platform RC (2026-07-27)
- Runtime: 426 tests passing
- Architecture: 92/100 - Cognitive pipeline integrated

## Quick Start

### Create an Agent

```python
from enal_ai import Agent, EnalAI

enal = EnalAI()

class MikrotikAgent(Agent):
    name = "mikrotik"
    description = "Mikrotik network configuration"
    capabilities = ["networking", "mikrotik", "firewall"]
    model = "gpt-4o"
    temperature = 0.3

    async def execute(self, task: str, context: dict | None = None) -> str:
        # Your custom logic here
        return f"Configured: {task}"

agent = MikrotikAgent()
result = await agent.run("Configure hotspot with 3 VLANs")
print(result)
```

### Create a Tool

```python
from enal_ai import Tool

@enal.tool(name="docker_build", description="Build Docker image")
async def docker_build(dockerfile_path: str, image_name: str):
    # Your tool logic
    return {"status": "built", "image": image_name}
```

### Create a Workflow

```python
from enal_ai import Workflow, WorkflowStep

workflow = Workflow(
    name="erp-build",
    description="Build ERP system",
    steps=[
        WorkflowStep(id="1", name="Requirements", agent="analyst", action="analyze"),
        WorkflowStep(id="2", name="Backend", agent="backend-dev", action="build_backend", depends_on=["1"]),
        WorkflowStep(id="3", name="Frontend", agent="frontend-dev", action="build_frontend", depends_on=["1"]),
        WorkflowStep(id="4", name="Deploy", agent="devops", action="deploy", depends_on=["2", "3"]),
    ],
)

result = await workflow.execute({"project_id": "erp-001"})
```

## API Reference

### Agent

```python
class Agent:
    config: AgentConfig
    async def execute(self, task: str, context: dict | None = None) -> str
    async def run(self, task: str, context: dict | None = None) -> dict
    def to_dict(self) -> dict
```

### Tool

```python
class Tool:
    config: ToolConfig
    async def invoke(self, parameters: dict) -> dict
    def to_dict(self) -> dict
```

### Workflow

```python
class Workflow:
    config: WorkflowConfig
    async def execute(self, context: dict | None = None) -> dict
    def to_dict(self) -> dict
```

### EnalAI (SDK Entry Point)

```python
enal = EnalAI(api_url="http://localhost:8000")

# Register agents
enal.agent("my-agent")(MyAgentClass)

# Register tools
enal.tool("my-tool")(my_tool_function)

# Register workflows
enal.workflow("my-workflow")(MyWorkflowClass)

# List registered
enal.list_agents()
enal.list_tools()
enal.list_workflows()
```

## Contracts

All components implement stable contracts:

- `CapabilityContract` — Agent capabilities
- `ToolContract` — Tool invocation
- `ArtifactContract` — Artifact management
- `MemoryContract` — Memory operations
- `WorkflowContract` — Workflow execution
- `WorldModelContract` — World model queries
- `LearningContract` — Learning operations

## Examples

See `examples/` directory:
- `custom_agent.py` — Creating custom agents
- `custom_workflow.py` — Building workflows

## Documentation

See `docs/` directory for:
- Getting Started Guide
- Agent Development Guide
- Tool Development Guide
- Workflow Design Guide
- API Reference
