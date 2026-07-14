# CANONICAL_OWNER

## Service: Model Router

**Canonical:** `backend/app/core/model_router.py`  
**Auxiliary:** `backend/app/core/model_gateway.py` (health/status API — NOT a duplicate)  
**Legacy (Dead):** N/A — deleted  
**Status:** canonical / auxiliary / legacy-purged

---

## Migration History

| Date | Action | By |
|------|--------|----|
| 2026-07-11 | Removed 6 dead imports of `model_router` in cognitive_kernel, cost_optimizer, evaluation, meta_cognition, modules/rag, modules/tools | Canonical Consolidation Epic 1 |
| 2026-07-11 | Deleted `apps/society/model_router.py` (0 importers, 189 lines dead code) | Canonical Consolidation Epic 2 |

## Canonical Consumers

21 files import `model_router`. 15 active callers invoke `.complete()`.

## Important Distinction

`model_gateway.py` is NOT a duplicate of `model_router.py`. It serves a different purpose:

| File | Purpose | Endpoint |
|------|---------|----------|
| `model_router.py` | LLM execution (`.complete()`) | N/A (internal) |
| `model_gateway.py` | Health/status API | `/api/v1/models/health`, `/api/v1/models/providers` |

Keep `model_gateway.py`.
