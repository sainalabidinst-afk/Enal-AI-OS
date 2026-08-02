# Panduan Pengembangan Agent

## Status

Platform RC (2026-07-27) — 426 test lulus

## Membuat Agent (Worker)

```python
from enal_ai import Agent

class MyWorker(Agent):
    name = "my-worker"
    description = "Description of what this worker does"
    capabilities = ["capability1", "capability2"]
    # JANGAN set model - Runtime memilih berdasarkan capabilities

    async def execute(self, task: str, context: dict | None = None) -> str:
        return f"Processed: {task}"

agent = MyWorker()
result = await agent.run("Do something")
```

## Siklus Hidup Agent

```
Created → Idle → Assigned → Executing → Review → Complete
                                    ↘ Failed → Retry (max 3)
```

## Integrasi Memory

```python
# Query collective memory dari Blackboard
context = blackboard.get("project-context")

# Simpan learning ke Project Memory
await memory.store("my-learning", {"pattern": "discovered"})
```

## Integrasi Workflow

```python
from apps.organization.workflow_executor import WorkflowExecutor

executor = WorkflowExecutor()
result = await executor.execute({"goal": "Your goal here"})
```

## Praktik Terbaik

- Definisikan capabilities secara jelas (bukan model) — Runtime menangani pemilihan model
- Query Blackboard sebelum bertindak untuk konteks bersama
- Gunakan collective memory untuk knowledge tim
- Catat confidence level pada output
- Tingkatkan blocking issue melalui Mailbox ke Lead

