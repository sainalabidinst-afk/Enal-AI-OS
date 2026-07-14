# CANONICAL_OWNER

## Service: Workspace

**Canonical:** `backend/app/core/workspace_service.py`  
**Legacy:** `backend/app/core/workspace.py`  
**Status:** canonical / deleted

---

## Migration History

| Date | Action | By |
|------|--------|----|
| 2026-07-11 | Migrated `orchestrator_v2.py` to `workspace_service.add_memory()` | Canonical Consolidation Epic 2 |
| 2026-07-11 | Deleted `workspace.py` (filesystem workspace, legacy) | Canonical Consolidation Epic 2 |

## Canonical Consumers

- `backend/app/api/workspace.py`
- `backend/app/api/execution.py`
- `backend/app/api/chat.py`
- `backend/app/core/execution_integration.py`

## Migration Notes

`workspace.py` stored data on the filesystem (`./workspace/`) using `ProjectWorkspace` and `WorkspaceManager`. `workspace_service.py` uses in-memory Pydantic schemas. Migration was direct because `orchestrator_v2.py` only called `workspace_manager.get(project_id).save_memory(key, value)`, which maps 1:1 to `workspace_service.add_memory(workspace_id, key, value)`.
