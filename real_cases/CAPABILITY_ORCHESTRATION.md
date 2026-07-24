# CAPABILITY ORCHESTRATION

## Lifecycle

Each capability follows:
1. **Init** - App instantiated via `get_app()`
2. **Register** - Available in registry
3. **Execute** - Called via worker or direct invocation
4. **Monitor** - Telemetry records events
5. **Complete** - Results returned

---

## Execution Flow

```
User Request
    ↓
Adaptive Runtime (perception/memory/reasoning/decision/action)
    ↓
Capability App (NetworkEngineerApp)
    ↓
Worker (NetworkWorker)
    ↓
Result
    ↓
Telemetry (record_analysis_event)
```

---

## Registry

Registered in `apps.society.agent.Agent` base class:
- `agent_registry` maintains agent records
- Each agent has `agent_id`, `name`, `role`, `department`, `skills`

---

## Telemetry Integration

Every capability execution triggers:
- `record_analysis_event()` for attachment analysis
- `record_execution_event()` for execution sessions
- `record_chat_event()` for chat interactions

---

## Error Handling

Standard contract:
```python
{
    "status": "success" | "failed",
    "result": {...} | None,
    "error": str | None
}
```

All workers return this format consistently.