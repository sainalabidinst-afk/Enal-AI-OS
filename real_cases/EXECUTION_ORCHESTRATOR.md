# EXECUTION ORCHESTRATOR

## Standard Execution Lifecycle

```
CREATED
   ↓
QUEUED (pending)
   ↓
RUNNING
   ↓
┌─────────────┬───────────┐
↓             ↓           ↓
COMPLETED    FAILED     CANCELLED
```

---

## State Transitions

| From | To | Trigger |
|------|-----|---------|
| created | pending | Session created |
| pending | running | Scheduler starts task |
| running | completed | Task finishes successfully |
| running | failed | Exception thrown |
| running | cancelled | Cancel endpoint called |
| pending | cancelled | Cancel before start |

---

## Timeout Policy

| Component | Default Timeout |
|-----------|-----------------|
| HTTP request | 60s (httpx.Timeout) |
| Individual task | None (async) |
| Benchmark suite | None (async) |

Override: Timeouts can be configured per-request via httpx client settings.

---

## Retry Policy

| Error Type | Retryable | Behavior |
|------------|-----------|----------|
| Network timeout | Yes | Retry on 5xx |
| JSON parse error | No | Fail immediately |
| Missing file | No | Fail immediately |
| Vendor detection | No | Fail immediately |

Max retry: Implementation-specific (currently no automatic retry).

---

## Output Contract

Standard response format:
```json
{
    "status": "success" | "failed",
    "result": {...} | null,
    "error": null | "message"
}
```

With telemetry:
```json
{
    "status": "success",
    "execution_time_ms": 123,
    "session_id": "uuid",
    "artifacts": [...]
}
```