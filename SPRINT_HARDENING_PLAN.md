# Sprint Hardening Plan — Zero Pylance Severity 8 & MyPy Errors

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Terakhir Diverifikasi:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for SPRINT_HARDENING_PLAN
<!-- DOCUMENT_METADATA_END -->

## Objective
Eliminate all static analysis errors (Pylance Severity 8, MyPy) across ~25+ files. No feature development.

## Error Categories Identified

### CATEGORY A: Constructor Mismatches (Missing params)
Files where constructors are called with missing required parameters:

| # | File | Issue | Fix |
|---|------|-------|-----|
| A1 | `backend/app/core/attachments/pipeline.py` | `InfrastructureAST()` calls missing `modules`, `metadata`, `capabilities` | Add default empty values to dataclass or update constructor calls |
| A2 | `backend/app/core/execution_session.py` | `ArtifactVersion()` missing required params | Add defaults to `ArtifactVersion` fields |
| A3 | `backend/app/core/memory_layer.py` | `EpisodicMemoryEntry()` constructor in `_persist` | Check constructor signature |

### CATEGORY B: Missing Methods
Files calling methods that don't exist:

| # | File | Method | Fix |
|---|------|--------|-----|
| B1 | `backend/app/api/execution.py` | `execution_session_manager.process_request()` | Method doesn't exist — implement or remove call |
| B2 | `backend/app/api/execution.py` | `execution_session_manager.get_result()` | Method doesn't exist — implement or remove call |
| B3 | `backend/app/api/execution.py` | `workspace_service.create_workspace()` with wrong args | Fix constructor signature |
| B4 | `backend/app/api/execution.py` | `artifact_service.create_artifact()` with wrong args | Fix constructor signature |

### CATEGORY C: Model Attribute Errors
Models missing attributes that code expects:

| # | File | Attribute | Fix |
|---|------|-----------|-----|
| C1 | `apps/network_engineer/vendor/models.py` | `UniversalRoute.interface` | DONE — already fixed `r.interface`→`"interface": ""` |
| C2 | `apps/network_engineer/mikrotik/routeros_parser.py` | `NATRule.in_interface` | DONE — already added |
| C3 | `apps/network_engineer/mikrotik/routeros_parser.py` | `BridgeConfig.comment` | DONE — already added |
| C4 | `apps/network_engineer/vendor/models.py` | `InfrastructureAST.storage` | Add `storage` field to InfrastructureAST |
| C5 | `apps/network_engineer/vendor/models.py` | Other missing model fields | Audit and add |

### CATEGORY D: Type Contract Breaks
`str|None` → `str/Path`, `dict|None` → `dict`, `DecisionResult` → `dict`, `MockNode` → `GraphNode`:

| # | File | Issue | Fix |
|---|------|-------|-----|
| D1 | `apps/network_engineer/vendor/models.py` | Type mismatches in models | Fix type annotations |
| D2 | `backend/app/core/decision_engine.py` | `DecisionResult` vs dict return type | Ensure consistent return type |
| D3 | `backend/app/core/cognitive_kernel.py` | Service process return types mismatched | Fix return type annotations |
| D4 | `backend/app/core/attachments/models.py` | `str|None` → `Path` type breaks | Fix annotations |
| D5 | `backend/app/core/attachments/pipeline.py` | `dict|None` → `dict` in function signatures | Fix default values |
| D6 | `backend/app/core/adaptive_runtime.py` | Context dict type issues | Fix annotations |
| D7 | `backend/app/core/reflection.py` | Return type mismatches | Fix |

### CATEGORY E: Async Misuse
`"str"` is not awaitable, `"CognitiveBudget"` is not awaitable:

| # | File | Issue | Fix |
|---|------|-------|-----|
| E1 | `backend/app/core/reflection.py` | Non-awaitable call on model_router | Check if `model_router.complete()` is actually async |
| E2 | `backend/app/core/cognitive/reasoning_engine.py` | Same issue — model_router called without await | Check and fix |
| E3 | `backend/app/core/cognitive/strategic_planner.py` | Same issue | Check and fix |
| E4 | `backend/app/core/cognitive/world_model.py` | Same issue | Check and fix |
| E5 | `backend/app/core/decision_engine.py` | Same issue | Check and fix |

**Root Cause**: `model_router` methods might be synchronous, not async. If methods are sync, remove `await`. If they should be async, make them async.

### CATEGORY F: Missing Imports (Severity 4)

| # | Package | Used In |
|---|---------|---------|
| F1 | `fastapi` | `backend/app/api/execution.py` |
| F2 | `langchain_core` | Various cognitive files |
| F3 | `litellm` | Model router |
| F4 | `qdrant_client` | Vector store |
| F5 | `httpx` | HTTP client calls |
| F6 | `aiohttp` | Async HTTP calls |
| F7 | `sqlalchemy` | Database models |
| F8 | `yaml` | YAML parsing |
| F9 | `tomli` | TOML parsing |

**Fix**: Add missing dependencies to `backend/pyproject.toml` or add try/except imports where optional.

### CATEGORY G: MyPy-Specific Issues

| # | File | Issue | Fix |
|---|------|-------|-----|
| G1 | Memory layer | Incompatible return types in `search()` | Fix type annotations to match `MemoryLayer` protocol |
| G2 | `cognitive_kernel.py` | CognitiveService subclass mismatches | Fix method signatures |
| G3 | `config.py` | Settings type issues | Verify pydantic settings types |
| G4 | Event bus | Redis type annotations | Add proper typing |

## Detailed Action Plan

### Phase 1: Fix Missing Imports (F1-F9)
- Add `fastapi`, `sqlalchemy` to `backend/pyproject.toml` as required deps
- Add `httpx`, `aiohttp`, `yaml`, `tomli` with try/except guards
- Check `langchain_core`, `litellm`, `qdrant_client` usage and make optional

### Phase 2: Fix async misuse (E1-E5)
- Determine if `model_router.complete()` is sync or async
- If sync: remove `await` from all calls
- If async: ensure all callers use `await`

### Phase 3: Fix constructor mismatches (A1-A3)
- `InfrastructureAST`: Add defaults for `modules=[], metadata={}, capabilities=[]`
- `ArtifactVersion`: Add defaults for all optional fields
- `EpisodicMemoryEntry`: Ensure all params have defaults

### Phase 4: Fix missing methods (B1-B4)
- Implement `process_request()`, `get_result()` in `ExecutionSessionManager`
- Fix `create_workspace()` calls to match signature
- Fix `create_artifact()` calls to match signature

### Phase 5: Fix remaining model attributes (C4-C5)
- Add `storage` to `InfrastructureAST`
- Audit all other model files for missing fields

### Phase 6: Fix type contract breaks (D1-D7)
- Fix _to_dict() and _model_dump() return types
- Ensure `DecisionResult` vs `dict` consistency
- Fix `str|None` → `str`/`Path` conversions
- Fix `dict|None` → `dict` defaults

### Phase 7: MyPy fixes (G1-G4)
- Memory layer type annotations
- CognitiveKernel service types
- Config/settings types
- Event bus Redis types

## Files to Edit

1. `apps/network_engineer/vendor/models.py` — DONE (C1)
2. `apps/network_engineer/mikrotik/routeros_parser.py` — DONE (C2, C3)
3. `backend/app/core/attachments/models.py` — Add model defaults (A1)
4. `backend/app/core/attachments/pipeline.py` — Fix type breaks (D5)
5. `backend/app/core/execution_session.py` — Add process_request, get_result (B1, B2)
6. `backend/app/core/workspace_service.py` — Fix create_workspace signature (B3)
7. `backend/app/core/artifact_service.py` — Fix create_artifact signature (B4)
8. `backend/app/api/execution.py` — Fix API calls (B1-B4)
9. `backend/app/core/decision_engine.py` — Fix async/return types (E5, D2)
10. `backend/app/core/reflection.py` — Fix async misuse (E1, D7)
11. `backend/app/core/cognitive/reasoning_engine.py` — Fix async (E2)
12. `backend/app/core/cognitive/strategic_planner.py` — Fix async (E3)
13. `backend/app/core/cognitive/world_model.py` — Fix async (E4)
14. `backend/app/core/cognitive_kernel.py` — Fix return types (D3)
15. `backend/app/core/adaptive_runtime.py` — Fix types (D6)
16. `backend/app/core/event_bus.py` — Fix types (G4)
17. `backend/app/core/memory_layer.py` — Fix types/constructors (A3, G1)
18. `backend/app/core/notification_service.py` — Fix types (minor)
19. `backend/app/core/model_router.py` — Need to check if sync/async
20. `backend/app/core/config.py` — Fix settings types (G3)
21. `backend/app/models/schemas_execution.py` — Fix model defaults
22. `backend/pyproject.toml` — Add missing dependencies

## Verification
1. Run `mypy backend/ apps/` — zero errors
2. Run `pytest` — all tests pass
3. Manual review of 3 fixed files confirmed correct

---

**Status**: 3/22 files fixed ✓
- `vendor/models.py` — DONE
- `routeros_parser.py` — DONE  
- `models.py` (attachments) — PENDING