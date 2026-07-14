# Getting Started with Enal Cognitive Platform

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Poetry (for backend development)

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/enal-ai-org/ecp.git
cd ecp
```

### 2. Setup Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Start Infrastructure

```bash
docker-compose up -d postgres redis qdrant ollama
```

### 4. Install Backend

```bash
cd backend
poetry install
uvicorn backend.app.main:app --reload
```

### 5. Install SDK

```bash
cd sdk
pip install -e .
```

### 6. Access Platform

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- SDK: `import enal_ai`

## Your First Agent

```python
from enal_ai import Agent

class MyAgent(Agent):
    name = "my-first-agent"
    capabilities = ["custom"]

    async def execute(self, task: str) -> str:
        return f"Hello from {self.name}! You asked: {task}"

agent = MyAgent()
result = await agent.run("Say hello")
print(result)
```

## Your First Workflow

```python
from enal_ai import Workflow, WorkflowStep

workflow = Workflow(
    name="my-workflow",
    description="My first workflow",
    steps=[
        WorkflowStep(id="1", name="Step 1", agent="worker", action="do_something"),
        WorkflowStep(id="2", name="Step 2", agent="worker", action="do_something_else", depends_on=["1"]),
    ],
)

result = await workflow.execute()
```

## Next Steps

1. Read [Agent Development Guide](agent_guide.md)
2. Read [Tool Development Guide](tool_guide.md)
3. Explore [Examples](../examples/)
4. Join the community
