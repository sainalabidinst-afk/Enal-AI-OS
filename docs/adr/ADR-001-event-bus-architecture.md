# ADR-001: Event Bus Architecture

**Status:** ✅ Accepted  
**Date:** 2024  
**Deciders:** Chief Architect, Engineering Team

---

## Context

The Enal Cognitive Platform requires cross-module communication between:
- Capability Packs (Network Engineer, Code Engineer, etc.)
- Core services (memory, execution, telemetry)
- Orchestration layer
- Frontend

Direct imports between modules would create tight coupling and circular dependencies.

---

## Decision

Use a centralized **Event Bus** pattern for all cross-module communication.

### Chosen Approach

- Publish-Subscribe pattern via `event_bus.py`
- Async event emission using `asyncio`
- Typed event schemas with Pydantic validation
- Lazy singleton instantiation to avoid circular imports at module load

### Key Design

```python
class EventBus:
    _subscribers: dict[str, list[Callable]]
    
    async def publish(self, event_type: str, data: Any) -> None
    def subscribe(self, event_type: str, handler: Callable) -> None
```

---

## Alternatives Considered

| Alternative | Reason Rejected |
|-------------|-----------------|
| Direct function calls | Creates tight coupling between modules |
| RPC/HTTP communication | Unnecessary network overhead for in-process communication |
| Global mutable state | Not thread-safe, hard to test |
| Message queue (Redis Pub/Sub) | Available but reserved for cross-process communication |

---

## Consequences

- **Positive:** Loose coupling, easy to add new event types, testable via mock subscribers
- **Positive:** Circular import prevention via lazy singleton pattern
- **Negative:** Event flow is implicit — requires documentation to trace
- **Negative:** No compile-time checking for event type correctness

---

## Compliance

All cross-module communication MUST use the Event Bus. Direct imports between capability packs or core modules are prohibited without ADR override.

