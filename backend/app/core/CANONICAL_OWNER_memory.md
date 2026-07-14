# CANONICAL_OWNER

## Service: Memory

**Canonical:** `backend/app/core/memory.py`  
**Legacy:** `backend/app/modules/memory.py`  
**Status:** canonical / deleted

---

## Migration History

| Date | Action | By |
|------|--------|----|
| 2026-07-11 | Created `core/memory.py` as canonical Redis-backed conversation store | Canonical Consolidation Epic 3 |
| 2026-07-11 | Migrated `conversation_manager.py` from `modules/memory` → `core/memory` | Canonical Consolidation Epic 3 |

## Canonical Consumers

- `apps/society/conversation_manager.py`

## Notes

`core/memory.py` exposes `conversation_store` with `get_conversation()`, `append_message()`, and `clear_conversation()` methods, all backed by Redis with the key prefix `conversation:`. This matches the interface that `conversation_manager.py` requires.
