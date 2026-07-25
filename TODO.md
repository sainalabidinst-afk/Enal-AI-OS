# QUALITY REMEDIATION SPRINT - TODO

## Priority 1: Mypy Errors

- [x] 1.1 `communication.py`: Fix `callable` → `typing.Callable`
- [x] 1.2 `capability_graph.py`: Fix missing type annotation for `related`

## Priority 2: Ruff Issues

### DTZ003 - `datetime.utcnow()` → `datetime.now(timezone.utc)`

- [ ] 2.1 `apps/organization/reasoning_engine.py` — 1 occurrence (Evidence dataclass default)
- [ ] 2.2 `apps/organization/communication.py` — 1 occurrence
- [ ] 2.3 `apps/organization/capability_execution_engine.py` — 5 occurrences
- [ ] 2.4 `apps/organization/execution_runtime.py` — 3 occurrences
- [ ] 2.5 `apps/organization/kernel.py` — 4 occurrences
- [ ] 2.6 `apps/organization/meeting.py` — 3 occurrences
- [ ] 2.7 `apps/organization/metrics.py` — 3 occurrences
- [ ] 2.8 `apps/organization/multi_agent.py` — 3 occurrences
- [ ] 2.9 `apps/organization/ai_planner.py` — 2 occurrences
- [ ] 2.10 `apps/organization/registry.py` — 1 occurrence

### BLE001 - Blind `except Exception`

- [ ] 2.11 `apps/organization/ai_planner.py` — 1 occurrence
- [ ] 2.12 `apps/organization/communication.py` — 1 occurrence
- [ ] 2.13 `apps/organization/execution_runtime.py` — 1 occurrence
- [ ] 2.14 `apps/organization/multi_agent.py` — 2 occurrences

### TRY401 - Redundant exception in logging.exception

- [ ] 2.15 `apps/organization/capability_pipeline.py` — 1 occurrence

## Priority 3: Markdownlint

- [ ] 3.1 Fix heading spacing
- [ ] 3.2 Fix blank lines
- [ ] 3.3 Fix table formatting
- [ ] 3.4 Fix strong style

## Validation

- [ ] 4.1 Run mypy
- [ ] 4.2 Run ruff
- [ ] 4.3 Run pytest
- [ ] 4.4 Generate QUALITY_REMEDIATION_REPORT.md

