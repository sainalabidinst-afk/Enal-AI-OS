# Agent Development Guide

## Creating an Agent

```python
from enal_ai import Agent, EnalAI

enal = EnalAI()

class MyAgent(Agent):
    name = "my-agent"
    description = "Description of what this agent does"
    capabilities = ["capability1", "capability2"]
    model = "gpt-4o"
    temperature = 0.7
    max_tokens = 4096
    tools = ["tool1", "tool2"]
    metadata = {"author": "your-name"}

    async def execute(self, task: str, context: dict | None = None) -> str:
        # Your agent logic here
        # Access tools via self.config.tools
        # Access model via self.config.model
        return f"Result for: {task}"

# Register
agent = MyAgent()
enal.agent("my-agent")(MyAgent)

# Run
result = await agent.run("Do something")
```

## Agent Lifecycle

1. **Initialization** — Config loaded, tools registered
2. **Execution** — `execute()` called with task
3. **Reflection** — Optional self-reflection on result
4. **Learning** — Experience stored for future

## Best Practices

- Keep agents focused on one domain
- Use specific capabilities for discovery
- Implement proper error handling
- Add metadata for tracking
