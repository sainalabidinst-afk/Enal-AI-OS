# Getting Started with Enal Cognitive Platform

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- pip

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/sainalabidinst-afk/Enal-AI-OS.git
cd Enal-AI-OS
```

### 2. Install Core

```bash
pip install -e .
```

### 3. Install SDK (Optional)

```bash
cd sdk
pip install -e .
```

### 4. Run Tests

```bash
pytest tests/ -v
# 368 tests passing
```

## Your First Agent

```python
from enal_ai import Agent

class MyAgent(Agent):
    name = "my-first-agent"
    capabilities = ["custom"]

    async def execute(self, task: str) -> str:
        return f"Processed: {task}"

agent = MyAgent()
result = await agent.run("Your task here")
print(result)
```

## Your First Workflow (with Checkpoint/Resume)

```python
from apps.organization.workflow_executor import WorkflowExecutor

# Create executor with checkpoint support
executor = WorkflowExecutor()

# Execute workflow
result = await executor.execute({"goal": "Configure network"})

# Checkpoint for later resume
checkpoint = await executor.create_checkpoint("work-001")

# Resume from checkpoint
await executor.resume_from_checkpoint("work-001")
```

## Cognitive Pipeline

```python
# Full pipeline available via orchestrator
from backend.app.agents.orchestrator_v2 import AIOrchestrator

orchestrator = AIOrchestrator()
result = await orchestrator.orchestrate_goal("Configure BGP on Cisco router")
```

## Capability Examples

| Capability | Usage |
|------------|-------|
| Network Engineer | `apps/network_engineer/config_generator.py` |
| Code Engineer | `apps/code_engineer/__init__.py` |
| Research Assistant | `apps/research/rag.py` |
| DevOps Assistant | `apps/devops/docker_manager.py` |

## Next Steps

1. [Agent Development Guide](agent_guide.md)
2. [Architecture Overview](architecture.md)
3. [API Reference](api_reference.md)
4. Run: `pytest tests/reference/ -v` (reference tests suite)