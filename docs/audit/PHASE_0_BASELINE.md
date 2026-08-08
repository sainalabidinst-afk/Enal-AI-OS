# ENAL AI OS - PHASE 0 BASELINE

Audit phase: Phase 0 - Baseline Reconstruction and Remediation Freeze

Audit date: 2026-08-08

Scope rule: no product-code remediation was performed in Phase 0. The only changes present in the worktree are audit-document changes from the prior audit and this baseline report.

## Repository State

| Item | Current evidence | Status |
|---|---|---|
| Branch | `main` | VERIFIED |
| HEAD | `bfa168753998e4955c9575705359b7496faff7e5` | VERIFIED |
| HEAD subject | `refactor(planner): implement safe context serialization for strategy creation` | VERIFIED |
| Tag at HEAD | None | VERIFIED |
| Worktree | Modified/untracked files are confined to `docs/audit/` | VERIFIED |
| Product-code diff | No changes under `backend`, `apps`, `benchmarks`, `tests`, `frontend`, Docker, version or environment files | VERIFIED |

The worktree is not clean because the audit artifacts are uncommitted. This does not represent product-code remediation.

## Version State

| Source | Value | Status |
|---|---|---|
| `VERSION` | `v1.0.0-developer-preview` | VERIFIED |
| `pyproject.toml` | `1.0.0` | VERIFIED |
| Backend settings | `1.0.0-dev` | VERIFIED |
| `frontend/package.json` | `0.1.0` | VERIFIED |
| `VERSION_MATRIX.md` capability-pack claim | `v1.1.0`, 19 packs certified | VERIFIED as documentation content, not as current certification truth |
| Git release tag | None at HEAD | VERIFIED |

Version identity remains inconsistent. No version was changed.

## Canonical Capability Registry

Source of truth: `apps/__init__.py`.

- Registered entries: 19.
- Loader: `_load_app(name)` imports `apps.<name>` and calls `module.get_app()`.
- Registration map: `APPS` in `apps/__init__.py`.
- Infrastructure packages `integration`, `organization` and `society` are not registered user-facing capabilities.

## Capability Loadability Matrix

The probe imported each package independently, called `get_app()`, and checked the returned object name and type.

| Capability package | Registered | Package import | `get_app()` | Returned object | Current result |
|---|---|---|---|---|---|
| `trading_analyst` | Yes | PASS | PASS | `TradingAnalystApp`, `trading-analyst` | LOADABLE |
| `network_engineer` | Yes | PASS | PASS | `NetworkEngineerApp`, `network-engineer` | LOADABLE |
| `devops_assistant` | Yes | PASS | PASS | `DevOpsAssistantApp`, `devops-assistant` | LOADABLE |
| `code_engineer` | Yes | PASS | PASS | `CodeEngineerApp`, `code-engineer` | LOADABLE |
| `research_assistant` | Yes | PASS | PASS | `ResearchAssistantApp`, `research-assistant` | LOADABLE |
| `full_stack_engineer` | Yes | PASS | PASS | `FullStackEngineerApp`, `full-stack-engineer` | LOADABLE |
| `self_development` | Yes | PASS | PASS | `SelfDevelopmentApp`, `self-development` | LOADABLE |
| `decision_intelligence` | Yes | PASS | FAIL | No object | `AttributeError: module 'apps.decision_intelligence' has no attribute 'get_app'` |
| `system_architect` | Yes | PASS | FAIL | No object | `AttributeError: module 'apps.system_architect' has no attribute 'get_app'` |
| `security_engineer` | Yes | PASS | FAIL | No object | `AttributeError: module 'apps.security_engineer' has no attribute 'get_app'` |
| `data_engineer` | Yes | PASS | FAIL | No object | `AttributeError: module 'apps.data_engineer' has no attribute 'get_app'` |
| `database_engineer` | Yes | PASS | FAIL | No object | `AttributeError: module 'apps.database_engineer' has no attribute 'get_app'` |
| `qa_engineer` | Yes | PASS | FAIL | No object | `AttributeError: module 'apps.qa_engineer' has no attribute 'get_app'` |
| `business_analyst` | Yes | PASS | FAIL | No object | `AttributeError: module 'apps.business_analyst' has no attribute 'get_app'` |
| `documentation_engineer` | Yes | PASS | PASS | `DocumentationEngineerApp`, `documentation-engineer` | LOADABLE |
| `product_manager` | Yes | PASS | PASS | `ProductManagerApp`, `product-manager` | LOADABLE |
| `infrastructure_engineer` | Yes | PASS | FAIL | No object | `AttributeError: module 'apps.infrastructure_engineer' has no attribute 'get_app'` |
| `ai_engineer` | Yes | PASS | FAIL | No object | `AttributeError: module 'apps.ai_engineer' has no attribute 'get_app'` |
| `ui_ux_designer` | Yes | PASS | FAIL | No object | `AttributeError: module 'apps.ui_ux_designer' has no attribute 'get_app'` |

Summary: 19 registered, 19 package imports, 9 loadable, 10 not loadable. The ten failures are code-level entrypoint contract mismatches, not silent skips.

## Benchmark State

Command:

```text
python -m benchmarks.performance_benchmark
```

Current result: BLOCKED before measurement collection.

Exact error:

```text
litellm.BadRequestError: LLM Provider NOT provided.
You passed model=claude-3-5-sonnet-20240620
```

Current configuration:

- Default model: `gpt-4o`.
- Default reasoning model: `claude-3-5-sonnet-20240620`.
- `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` and `GOOGLE_API_KEY` are empty in the local `.env`.
- No credentials were created or injected.
- Raw executions: 0.
- Raw measurements: none.

The stored 96.99 benchmark values remain stale/unverified. The targeted benchmark adapter tests are not a substitute for a real benchmark execution.

## Docker State

| Check | Result |
|---|---|
| `docker compose config` | PASS |
| Rendered backend `SECRET_KEY` | `your-secret-key-here-change-in-production` |
| Current `docker compose ps -a` | No containers |
| Latest `docker compose up -d --build` attempt | Timed out after 604 seconds before creating containers/images |
| Service health | BLOCKED; no service reached a verified runtime state |

The compose configuration is syntactically valid, but configuration success is not runtime health.

## Frontend State

`npm run build` completed successfully with Next.js 14.2.0 and generated 39 static routes. The current build took 212.3 seconds.

| Route or surface | Current state | Evidence |
|---|---|---|
| `/trading` | PLACEHOLDER | Renders `TestComponent` |
| `/workspace` | REDIRECT | Immediately redirects to `/workspace/trading` |
| `/chat` | MISSING | `frontend/app/chat/page.tsx` does not exist |
| `/integration` | IMPLEMENTED/PARTIAL | Route exists; backend integration behavior is not reliable |
| Launcher registry | PARTIAL | 11 entries are marked `Coming Soon`; it is not the canonical 19-entry registry |
| `npm run lint` | BLOCKED | `next lint` opens an interactive ESLint setup prompt |

## Test State

Command:

```text
python -m pytest --collect-only -q
```

Result: 938 tests collected in 31.07 seconds.

Collection warnings remain for five imported classes whose names begin with `Test` but have constructors. They are collection warnings, not counted as test failures.

The last complete-suite attempt remains the current runtime baseline because no product code changed after that audit:

- `python -m pytest -q`: timed out after 604 seconds without a final summary.
- Separate `tests` and `backend/tests` runs: each timed out after 304 seconds without a final summary.
- Full-suite passed, failed, skipped and error counts: unavailable because pytest did not finish.
- Targeted `tests/test_performance_benchmark.py`: 4 passed in 14.35 seconds.

## Lint State

Command:

```text
python -m ruff check backend apps benchmarks tests
```

Result: FAIL, 3,442 errors. The output includes import ordering, unused imports, line length, wildcard imports and missing-newline violations.

## Type-Check State

Command:

```text
python -m mypy backend apps benchmarks
```

Result: FAIL, 86 errors in 29 files across 632 checked source files.

## Security Configuration State

- Empty `SECRET_KEY` is rejected by the Pydantic settings validator.
- `.env` is ignored by Git and is not tracked.
- Local `.env` contains the known placeholder `your-secret-key-here-change-in-production`.
- `docker compose config` renders that placeholder into the backend service.
- No real credential was read into this report or written to source control.

Security state: PARTIAL. Fail-fast validation exists, but the effective local deployment value is not safe for deployment.

## Integration State

The `trading_analysis_with_knowledge('BTCUSDT')` workflow was invoked directly.

- Returned `success=True`.
- Returned `error=None`.
- Returned no output keys.
- Logged a reasoning failure: `UnifiedEvidence` has no attribute `description`.

This remains a false-success risk: an incomplete workflow can report success. No integration code was modified in Phase 0.

## Backend State

`backend.app.main` imports successfully. FastAPI TestClient results:

| Endpoint | Result |
|---|---|
| `/` | 200 |
| `/health` | 200 |
| `/api/v1/health` without token | 401 |
| `/api/v1/capabilities` | 200 |

This is local application evidence only. Database, Redis, Qdrant, Ollama and model-backed runtime dependencies were not verified healthy.

## Discrepancies Against Previous Audit

| Previous finding | Current Phase 0 result | Discrepancy |
|---|---|---|
| 19 registered / 9 loadable / 10 missing `get_app()` | Same exact result and exceptions | None |
| Benchmark blocked by LiteLLM provider resolution | Same model and error; zero executions | None |
| Docker configuration passes but runtime is blocked | Config passes; no containers after prior timeout | None |
| Frontend build passes; `/trading` placeholder; `/workspace` redirect; `/chat` missing | Same route truth; build still passes | None |
| 938 tests collected | 938 collected with same warning family | None |
| Ruff 3,442 errors | 3,442 errors | None |
| MyPy 86 errors in 29 files | 86 errors in 29 files | None |
| Integration can return success with incomplete output | Still returns `success=True`, `error=None`, no outputs, with a reasoning error | No material improvement |
| Previous report described a clean baseline | Current worktree is dirty from audit documents | Snapshot difference; no product-code change |

## Phase 0 Gate

**PASS for Phase 0 baseline documentation.** The current repository state and prior audit findings are independently reconciled and documented.

**STOP.** No Phase 1 capability remediation was started. The next authorized phase is Phase 1 only: remediate the ten `get_app()` entrypoint contract failures, then stop if the 19/19 loadability gate is not achieved.
