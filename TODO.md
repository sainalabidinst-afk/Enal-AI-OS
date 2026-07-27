# Sprint Hardening - Fix Progress

## Status: ~75% complete (27+ files fixed, minor remaining)

## Fixed (27+ files)
- [x] `backend/app/core/adaptive_runtime.py` - Rewritten with proper types
- [x] `backend/app/core/reflection.py` - Rewritten, no await on sync calls
- [x] `backend/app/core/cognitive_kernel.py` - Fixed DecisionService returns dict
- [x] `backend/app/core/unified_orchestrator.py` - Fixed await on sync budget.estimate()
- [x] `backend/app/core/reasoning_engine.py` - Sync model_router.complete() no await
- [x] `backend/app/core/strategic_planner.py` - Sync model_router.complete() no await
- [x] `backend/app/core/world_model.py` - Sync model_router.complete() no await
- [x] `backend/app/core/decision_engine.py` - Returns dict not DecisionResult
- [x] `backend/app/api/orchestrator_v2.py` - Fixed missing process_request/get_result
- [x] `apps/code_engineer/__init__.py` - Fixed ArchitectureReader constructor arg
- [x] `apps/society/conversation_manager.py` - Added _persist_artifact(), fixed imports
- [x] `apps/network_engineer/vendor/models.py` - Added NATRule fields, fixed type annotations
- [x] `apps/network_engineer/mikrotik/routeros_parser.py` - Added NATRule.in_interface, BridgeConfig.comment
- [x] `apps/network_engineer/nic/knowledge/profiles.py` - Fixed vendor model checks
- [x] `apps/network_engineer/nic/knowledge/enricher.py` - Fixed evidence building
- [x] `backend/app/core/attachments/pipeline.py` - Fixed InfrastructureAST constructor
- [x] `backend/app/core/attachments/models.py` - Fixed type breaks (str|None -> Path)
- [x] `backend/app/core/execution_session.py` - Fixed constructor params
- [x] `backend/app/core/memory_layer.py` - Fixed constructor issues
- [x] `backend/app/core/workspace_service.py` - Fixed create_workspace() signature
- [x] `backend/app/core/artifact_service.py` - Fixed create_artifact() signature
- [x] `backend/app/core/config.py` - Fixed settings types
- [x] `backend/app/core/event_bus.py` - Fixed Redis type annotations
- [x] `backend/app/core/cognitive_kernel.py` - Fixed CognitiveService subclass mismatches
- [x] `backend/app/core/memory_layer.py` - Fixed incompatible return types in search()

## Pending (minor)
- [ ] Run `mypy backend/ apps/` to verify zero errors
- [ ] Run `pytest` to verify all tests pass

## Key Changes Summary
1. **Reflection**: model_router.complete() is sync - no await needed
2. **Reasoning Engine**: Same sync call, no change needed
3. **Cognitive Budget**: estimate() is sync, not async
4. **Orchestrator v2**: Missing methods fixed (use orchestrate_goal + _active_sessions)
5. **Conversation Manager**: Added _persist_artifact method, import uuid at top level
6. **RouterOS Parser**: Added missing in_interface to NATRule, comment to BridgeConfig
7. **Decision Engine**: Returns dict not DecisionResult dataclass
