# ENAL AI OS - REMEDIATION PLAN - 2026-09-21

This plan follows the fresh comprehensive audit in
`docs/audit/COMPREHENSIVE_AUDIT_2026-09-21.md`. It is an execution order, not a
release certification.

## Guardrails

- Do not replace the user's saved `SECRET_KEY`.
- Do not print, commit, or copy secret values into audit artifacts.
- Do not convert blocked benchmarks into scores.
- Do not mass-format the repository before separating product code from
  generated fixtures and historical artifacts.
- Keep the existing dirty worktree changes intact and review them separately.

## Phase 0: Reproducible Runtime Preflight

### Work

1. Confirm the intended repository root and load the existing local secret from
   the user's actual environment or secret manager. Do not generate a
   replacement secret.
2. Add a preflight command that checks only presence and provider/model
   compatibility, never values.
3. Make compose configuration fail with an actionable message for both
   `SECRET_KEY` and database credentials.
4. Decide the canonical Gemini variable name. Either keep `GOOGLE_API_KEY` and
   document it, or support `GEMINI_API_KEY` as an explicit alias without
   logging either value.

### Acceptance

```text
backend.app.main imports with the existing configured secret
docker compose config exits 0 without printing secret values
the preflight reports provider, model, and missing-variable names only
```

## Phase 1: Correctness Blockers

### 1A. Normalize Full-Stack Score Contract

Choose one canonical scale. Recommended: keep public scores on `0..1` and
convert the architecture engine's `0..100` result at the boundary, then render
`score * 100` for human reports. Update:

- `apps/full_stack_engineer/schemas.py`
- `apps/full_stack_engineer/architecture_review_engine.py`
- `apps/full_stack_engineer/engine.py`
- serialization and threshold tests

Add a regression test that runs a real architecture review and proves both the
Pydantic range and the rendered percentage are correct.

### 1B. Make Integration Failure Semantics Truthful

1. Define required outputs for each workflow descriptor.
2. Treat unavailable market data, empty required output, and reasoning adapter
   errors as failed or explicitly degraded results, not success.
3. Fix the `UnifiedEvidence` adapter contract so the reasoning engine consumes
   fields that actually exist.
4. Prevent knowledge persistence when required evidence is absent.
5. Add tests for upstream refusal, empty output, partial output, and successful
   output.

### 1C. Repair Explicit Provider Routing

1. Use an explicit LiteLLM model identifier such as the supported Gemini
   provider/model form selected by the project configuration.
2. Ensure the model router selects the matching API key field.
3. Add a provider preflight test that checks routing without making a network
   call.
4. Keep raw latency/token/success measurements separate from any score formula.
5. Run the real benchmark only when the authorized provider credential is
   present; otherwise emit `BLOCKED` and exit non-zero without a score.

### Acceptance

```text
full-stack architecture review test passes
integration failure tests return success=False or an explicit degraded status
benchmark produces raw executions > 0 only with an authorized provider
benchmark output contains no fabricated final score when blocked
```

## Phase 2: Quality Gate Recovery

### Work order

1. Fix Ruff errors in product code by package, starting with import and syntax
   errors, then correctness findings, then style-only findings.
2. Fix Mypy errors by package and add annotations at public boundaries.
3. Decide whether generated `real_cases` sources are executable fixtures. If
   they are fixtures, exclude them consistently from Black, Bandit, and runtime
   scanners; if executable, repair their syntax and test them.
4. Replace legacy Flake8, Black, Isort, and Safety commands in CI with the
   supported project gates, or document them as supplemental checks.
5. Run pytest in focused groups first, then the complete suite with a final
   summary and a bounded timeout.

### Acceptance

```text
ruff check backend apps benchmarks tests: exit 0
mypy backend apps benchmarks: exit 0
pytest: final summary with zero unexpected failures
security scan: a version-compatible command returns a real verdict
```

## Phase 3: Frontend and Docker Runtime

### Work

1. Install frontend dependencies from `frontend/package-lock.json` in a clean
   environment, then run build and lint non-interactively.
2. Replace the trading `TestComponent` with the intended production screen or
   explicitly mark it as a developer-preview placeholder.
3. Implement or remove the workspace redirect contract and add the missing chat
   route if chat is part of the product contract.
4. Start Docker only after preflight has loaded the existing secret and database
   password. Verify health endpoints for every service.
5. Add a smoke test for authenticated frontend-to-API execution with one
   capability, artifact creation, and telemetry response.

### Acceptance

```text
npm ci && npm run build: exit 0
frontend lint: non-interactive and exit 0
docker compose config: exit 0
all required services healthy
authenticated end-to-end smoke: pass with non-empty, truthful output
```

## Phase 4: CI, Documentation, and Release Hygiene

### Work

1. Split CI into deterministic offline gates and an explicitly authorized
   provider-backed benchmark workflow.
2. Pass provider credentials through protected CI secrets only; never use
   placeholder values for release verification.
3. Add the frontend build to CI.
4. Add generated audit directories and archives to `.gitignore`, while keeping
   durable audit reports under `docs/audit`.
5. Select one release identity and reconcile `VERSION`, package metadata,
   backend settings, frontend metadata, tags, release notes, and certification
   files.
6. Mark old benchmark and readiness documents as historical, or regenerate them
   from a fresh evidence run.

## Definition Of Done

The repository can leave developer-preview status only when all of the following
are true:

- P1 findings have passing regression tests.
- Runtime preflight and Docker configuration pass with the existing secret.
- All 19 capability entrypoints load and representative executions return valid
  output.
- Full pytest, Ruff, and Mypy gates finish with documented results.
- The authorized real benchmark has raw measurements and reproducible metadata.
- Frontend build/lint and authenticated end-to-end smoke pass.
- CI reproduces the local gates without hidden interactive prompts.
- Release/version documentation contains no unsupported score or readiness
  claim.

Until then, keep the release classification at **D - NOT READY**.

## Execution Status - 2026-09-22

Completed in the current remediation pass:

- Phase 1 score-contract and integration failure-semantics fixes, with focused
  regression tests.
- Gemini model/key routing and truthful benchmark blocking behavior.
- Compose credential preflight changes without replacing the saved secret.
- Audit-document consolidation and generated-output ignore rules.
- Provider-backed benchmark CI changed to explicit opt-in through the
  `RUN_PROVIDER_BENCHMARK` repository variable.

The release gate remains open. Fresh provider measurements, green Ruff/Mypy,
and Docker health evidence are still required. The complete pytest gate now
has a final result: `939 passed, 2 skipped, 152 warnings` from 941 collected
tests. Frontend lint and build also have passing evidence, with non-fatal lint
warnings documented in the audit.
