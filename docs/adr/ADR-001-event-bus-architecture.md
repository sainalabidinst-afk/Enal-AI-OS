<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English


### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/adr/ADR-001-event-bus-architecture.md`
- Judul: Adr 001 Event Bus Architecture
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# ADR-001: Event Bus Architecture


**Status:** ✅ Accepted  
**Date:** 2024  
**Deciders:** Chief Architect, Engineering Team

---

## Context

The Enal Cognitive Platform requires cross-module communication between:
> Terjemahan Indonesia: Enal kognitif platform requires cross-module communication between:
- Capability Packs (Network Engineer, Code Engineer, etc.)
- Core services (memory, execution, telemetry)
- Orchestration layer
- Frontend

Direct imports between modules would create tight coupling and circular dependencies.
> Terjemahan Indonesia: Direct imports between modules would membuat tight coupling dan circular dependencies.

---

## Decision

Use a centralized **Event Bus** pattern for all cross-module communication.
> Terjemahan Indonesia: Use sebuah centralized Event Bus pattern untuk all cross-module communication.

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
> Terjemahan Indonesia: All cross-module communication MUST use Event Bus. Direct imports between kapabilitas packs or core modules adalah prohibited without ADR override.
