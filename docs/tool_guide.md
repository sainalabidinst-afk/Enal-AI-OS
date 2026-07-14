# Tool Development Guide

## Creating a Tool

```python
from enal_ai import Tool, EnalAI

enal = EnalAI()

@enal.tool(
    name="my_tool",
    description="Description of what this tool does",
    parameters={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "Parameter description"},
            "param2": {"type": "integer", "description": "Another parameter"},
        },
        "required": ["param1"],
    },
    sandbox=True,
    permissions=["read", "write"],
)
async def my_tool(param1: str, param2: int = 0):
    # Your tool logic here
    return {"result": f"Processed {param1}"}
```

## Tool Contracts

All tools must implement:
- `invoke(parameters)` — Execute tool with parameters
- `get_schema()` — Return OpenAI-compatible schema

## Sandboxing

Tools marked with `sandbox=True` run in isolated environment:
- No direct filesystem access
- No network access (unless explicitly allowed)
- Resource limits enforced

## Permissions

Tools require explicit permissions:
- `read` — Read data
- `write` — Write data
- `execute` — Execute code/commands
- `deploy` — Deploy to production
- `admin` — Administrative operations

## Best Practices

- Keep tools single-purpose
- Validate all inputs
- Return structured output
- Document parameters thoroughly
- Use appropriate permissions
