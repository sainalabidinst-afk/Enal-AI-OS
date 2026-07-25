# Stabilization Sprint - Type Safety & Architecture Consistency

## TODO Checklist

### PHASE 1: CRITICAL FIXES (High Severity)

- [x] 1. Create STATIC_ANALYSIS_CLASSIFICATION.md
- [ ] 2. `apps/organization/task_planner.py` - Add missing `Intent` import
- [ ] 3. `apps/organization/meeting.py` - Add missing `blackboard` import & fix init
- [ ] 4. `apps/organization/communication.py` - Fix `callable` → `Callable` type annotation
- [ ] 5. `apps/society/society.py` - Add `team_id` field to `Team` dataclass
- [ ] 6. `apps/society/society.py` - Fix line 455 type mismatch (`dict` vs `SubtaskResult`)
- [ ] 7. `apps/society/conversation_manager.py` - Add missing `_persist_artifact` method

### PHASE 2: TYPE ANNOTATION FIXES (Medium Severity)

- [ ] 8. `apps/organization/capability_graph.py` - Add `list[str]` type annotation for `related`
- [ ] 9. `apps/society/intent_router.py` - Fix `max()` key function
- [ ] 10. `apps/organization/workflow_executor.py` - Remove unused `TelemetryRecord` import

### PHASE 3: NETWORK VENDOR MODEL CONSISTENCY

- [ ] 11. `apps/network_engineer/vendor/cisco_ios.py` - Fix `UniversalBGP` references
- [ ] 12. `apps/network_engineer/vendor/mikrotik.py` - Fix all undefined model refs & type assignments
- [ ] 13. `apps/network_engineer/vendor/models.py` - Fix `UniversalRoute.interface` field

### PHASE 4: VALIDATION

- [ ] 14. Run `ruff check --fix`
- [ ] 15. Run `mypy` to verify fixes
- [ ] 16. Run `pytest` to ensure no regressions
- [ ] 17. Create TYPE_FIX_REPORT.md
- [ ] 18. Create ARCHITECTURE_CONSISTENCY_REPORT.md
