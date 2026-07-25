# STATIC ANALYSIS CLASSIFICATION

## Classification Date: Current Sprint
## Scope: `apps/organization/`, `apps/society/`, `apps/network_engineer/vendor/`

---

## 1. ENVIRONMENT ISSUES

These are dependency/configuration issues, NOT source code issues.

| # | Issue | File | Details |
|---|-------|------|---------|
| E1 | `ruff` not installed | N/A | Need `pip install ruff` |
| E2 | `mypy` may need packages | `pyproject.toml` | `mypy>=1.8.0` in dev deps |
| E3 | FastAPI/httpx/redis not in workspace deps | `pyproject.toml` | Used by backend not core org |
| E4 | `pytest` may be missing | N/A | Need `pip install pytest pytest-asyncio` |

**Decision**: These are environment setup issues, not source code bugs. Documented for CI pipeline.

---

## 2. MISSING IMPORT

| # | Severity | File | Line | Error | Resolution |
|---|----------|------|------|-------|------------|
| M1 | ❌ HIGH | `apps/organization/task_planner.py` | 1,40,59 | `Name "Intent" is not defined` - Used in `TaskPlan` dataclass and `plan()` method but never imported | Add `from apps.society.intent_router import Intent` |
| M2 | ❌ HIGH | `apps/organization/meeting.py` | 172 | `Name "blackboard" is not defined` - Used in `MeetingSystem.__init__` and singleton instantiation | Add `from apps.organization.communication import blackboard` |
| M3 | ❌ HIGH | `apps/network_engineer/vendor/cisco_ios.py` | 376,386 | `Name "UniversalBGP" is not defined` | Check if model exists or was removed |
| M4 | ❌ HIGH | `apps/network_engineer/vendor/mikrotik.py` | 199 | `Name "UniversalBGP" is not defined` | Same as M3 |
| M5 | ❌ HIGH | `apps/network_engineer/vendor/mikrotik.py` | 213 | `Name "UniversalMPLS" is not defined; did you mean "UniversalDNS"?` | Check if model exists |
| M6 | ❌ HIGH | `apps/network_engineer/vendor/mikrotik.py` | 223 | `Name "UniversalCAPsMAN" is not defined` | Check if model exists |
| M7 | ❌ HIGH | `apps/network_engineer/vendor/mikrotik.py` | 234 | `Name "UniversalWireGuard" is not defined` | Check if model exists |

---

## 3. UNDEFINED SYMBOL / TYPE ERROR

| # | Severity | File | Line | Error | Resolution |
|---|----------|------|------|-------|------------|
| T1 | ❌ HIGH | `apps/organization/communication.py` | 89 | `Function "builtins.callable" is not valid as a type` | Change `callable` to `Callable` from `typing` |
| T2 | ❌ HIGH | `apps/organization/communication.py` | 96 | `callable? not callable` | Fix type annotation to use `Callable` |
| T3 | ❌ HIGH | `apps/society/society.py` | 277,287,370 | `"Team" has no attribute "team_id"` | Add `team_id` field to `Team` dataclass |
| T4 | ❌ HIGH | `apps/society/society.py` | 455 | `Argument 1 to "append" has incompatible type "dict[str, Any]"; expected "SubtaskResult"` | Fix type mismatch |
| T5 | ❌ MEDIUM | `apps/society/conversation_manager.py` | 214 | `"ConversationManager" has no attribute "_persist_artifact"` | Implement missing method |
| T6 | ❌ MEDIUM | `apps/organization/capability_graph.py` | 726 | `Need type annotation for "related"` | Add `list[str]` annotation |
| T7 | ❌ MEDIUM | `apps/network_engineer/vendor/mikrotik.py` | 130 | `Incompatible types in assignment: NATRule vs FirewallFilterRule` | Fix type assignment |
| T8 | ❌ MEDIUM | `apps/network_engineer/vendor/mikrotik.py` | 185 | `"BridgeConfig" has no attribute "comment"` | Add field or fix access |
| T9 | ❌ MEDIUM | `apps/network_engineer/vendor/mikrotik.py` | 313 | `Incompatible types: UniversalNATRule vs UniversalFirewallRule` | Fix type assignment |
| T10 | ❌ MEDIUM | `apps/network_engineer/vendor/models.py` | 314 | `"UniversalRoute" has no attribute "interface"` | Add field or fix access |
| T11 | ❌ LOW | `apps/society/intent_router.py` | 161 | `Argument "key" to "max" has incompatible type` | Use `key=lambda d: domain_scores[d]` instead of `domain_scores.get` |

---

## 4. WRONG RETURN TYPE

| # | Severity | File | Line | Error | Resolution |
|---|----------|------|------|-------|------------|
| R1 | ❌ MEDIUM | `apps/network_engineer/__init__.py` | 105 | `Incompatible return value type (got "str \| None", expected "str")` | Fix return type annotation |

---

## 5. OPTIONAL ACCESS

| # | Severity | File | Line | Error | Resolution |
|---|----------|------|------|-------|------------|
| O1 | ❌ MEDIUM | `apps/network_engineer/vendor/cisco_ios.py` | - | Optional access patterns | Audit needed |
| O2 | ❌ MEDIUM | `backend/app/api/attachments.py` | 83-84 | `Item "None" of "X \| None" has no attribute "meta"` | Add None check |
| O3 | ❌ MEDIUM | `backend/app/api/execution.py` | 50 | `Item "None" of "dict \| None" has no attribute "id"` | Add None check |

---

## 6. ATTRIBUTE MISMATCH

| # | Severity | File | Line | Error | Resolution |
|---|----------|------|------|-------|------------|
| A1 | ❌ HIGH | `apps/society/society.py` | 277,287,370 | `"Team" has no attribute "team_id"` | Add `team_id: str = ""` to Team dataclass |
| A2 | ❌ MEDIUM | `backend/app/core/prompt_compiler.py` | 22-24 | `Incompatible types in assignment: list vs dict` | Fix variable types |

---

## 7. API CONTRACT MISMATCH

| # | Severity | File | Line | Error | Resolution |
|---|----------|------|------|-------|------------|
| C1 | ❌ MEDIUM | `backend/app/core/attachments/pipeline.py` | 70 | `Unexpected keyword argument "metadata"` | Add metadata field to AttachmentAnalysisResult |
| C2 | ❌ MEDIUM | `backend/app/studio/ai_studio.py` | 17,23 | Incompatible return value types | Fix return type annotations |
| C3 | ❌ MEDIUM | `backend/app/core/benchmark/runner.py` | 244 | `Argument 1 has incompatible type "dict \| None"; expected "dict"` | Fix parameter type |
| C4 | ❌ MEDIUM | `backend/app/core/cognitive/self_verification.py` | 88 | `Incompatible return value type: tuple[str \| None, ...]` | Fix return type |

---

## 8. DEAD / OBSOLETE CODE

| # | Severity | File | Details |
|---|----------|------|---------|
| D1 | ❌ LOW | `apps/organization/workflow_executor.py` | `TelemetryRecord` imported but never used (F401) |
| D2 | ❌ LOW | `apps/organization/communication.py` | `time` imported but unused |
| D3 | ❌ LOW | `apps/organization/meeting.py` | Check if `blackboard` parameter pattern is dead code |
| D4 | ❌ INFO | Various | `callable` vs `Callable` - leftover from early prototyping |
| D5 | ❌ INFO | Network vendor models | `UniversalBGP`, `UniversalMPLS`, `UniversalCAPsMAN`, `UniversalWireGuard` may be removed models with stale references |

---

## CLASSIFICATION SUMMARY

| Category | Count | Actionable |
|----------|-------|------------|
| Environment | 4 | ✅ Document (no source change) |
| Missing Import | 7 | ✅ Fix imports (HIGH priority) |
| Undefined Symbol | 11 | ✅ Fix types & models |
| Wrong Return Type | 1 | ✅ Fix annotation |
| Optional Access | 3 | ✅ Add None checks |
| Attribute Mismatch | 2 | ✅ Add missing fields |
| API Contract | 4 | ✅ Fix contracts |
| Dead Code | 5 | ✅ Clean up |

**Total actionable: 33 issues** (focusing on organization + society + vendor)

