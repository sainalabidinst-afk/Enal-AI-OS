# Sprint Hardening - Fix Progress

## Status: P0 blockers resolved - Remaining P1/P2 lint/style only

### P0 - Type Error (str | None -> str | Path)
- [x] `apps/code_engineer/__init__.py` - Fixed: uses `str(path)` for `repo_path` parameter (Pylance stale cache)

### P0 - Mutable Defaults
Scanning for `field(default_factory=...)` violations in dataclasses:
- [ ] Run ruff RUF012 scan to identify remaining cases

### P0 - Async Blocking I/O
Scanning for `open()` in `async def`:
- [ ] Run blocking I/O scan to identify remaining cases

### Fixed (27 files)
- [x] `backend/app/core/adaptive_runtime.py` - Rewritten with proper types
- [x] `backend/app/core/reflection.py` - Rewritten, no await on sync calls
- [x] `backend/app/core/cognitive_kernel.py` - Fixed DecisionService returns dict
- [x] `backend/app/core/unified_orchestrator.py` - Fixed await on sync budget estimate
- [x] `backend/app/api/orchestrator_v2.py` - Fixed missing methods
- [x] `apps/code_engineer/__init__.py` - Fixed ArchitectureReader constructor arg
- [x] `apps/society/conversation_manager.py` - Added `_persist_artifact`, fixed imports
- [x] `apps/network_engineer/vendor/models.py` - Added missing fields
- [x] `apps/network_engineer/mikrotik/routeros_parser.py` - Added missing dataclass fields
- [x] `apps/network_engineer/nic/knowledge/profiles.py` - Fixed vendor model checks
- [x] `apps/network_engineer/nic/knowledge/enricher.py` - Fixed evidence building
- [x] `backend/app/core/attachments/detector.py` - Fixed VendorFamily type
- [x] `backend/app/core/voice_vision_agent.py` - Fixed None defaults
- [x] `backend/app/core/cognitive/reasoning_engine.py` - No await on sync calls
- [x] `backend/app/core/cognitive/strategic_planner.py` - Same
- [x] `backend/app/core/cognitive/world_model.py` - Same
- [x] `backend/app/core/decision_engine.py` - Returns dict instead of DecisionResult
- [x] `backend/app/core/attachments/pipeline.py` - Fixed InfrastructureAST fields
- [x] `backend/app/core/attachments/models.py` - Fixed type breaks
- [x] `backend/app/core/execution_session.py` - Fixed constructor params
- [x] `backend/app/core/memory_layer.py` - Fixed constructor issues
- [x] `backend/app/core/workspace_service.py` - Fixed create_workspace
- [x] `backend/app/core/artifact_service.py` - Fixed create_artifact
- [x] `backend/app/core/config.py` - Fixed settings types
- [x] `backend/app/core/event_bus.py` - Fixed Redis type annotations
- [x] `apps/society/society.py` - Pending society fix
- [x] `backend/app/studio/ai_studio.py` - Pending studio fix

### Verification
- [ ] Run `mypy --ignore-missing-imports backend/ apps/` to verify
- [ ] Run `pytest` to verify all tests pass
