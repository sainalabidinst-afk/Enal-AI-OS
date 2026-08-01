# Agent Development Guide

## Status
Platform RC (2026-07-27) - 426 tests passing

## Creating an Agent (Worker)

```python
from enal_ai import Agent

class MyWorker(Agent):
    name = "my-worker"
    description = "Description of what this worker does"
    capabilities = ["capability1", "capability2"]
    # Do NOT set model - Runtime selects based on capabilities

    async def execute(self, task: str, context: dict | None = None) -> str:
        return f"Processed: {task}"

agent = MyWorker()
result = await agent.run("Do something")
```

## Agent Lifecycle

```
Created → Idle → Assigned → Executing → Review → Complete
                                    ↘ Failed → Retry (max 3)
```

## Memory Integration

```python
# Query collective memory from Blackboard
context = blackboard.get("project-context")

# Store learnings to Project Memory
await memory.store("my-learning", {"pattern": "discovered"})
```

## Workflow Integration

```python
from apps.organization.workflow_executor import WorkflowExecutor

executor = WorkflowExecutor()
result = await executor.execute({"goal": "Your goal here"})
```

## Best Practices

- Define clear capabilities (not models) - Runtime handles model selection
- Query Blackboard before acting for shared context
- Use collective memory for team knowledge
- Log confidence levels in outputs
- Escalate blockers via Mailbox to Lead