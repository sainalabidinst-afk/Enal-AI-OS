# ENAL AI OS - COMPREHENSIVE AUDIT - 2026-09-21

## 1. Executive Verdict

Release classification: **D - NOT READY**.

The repository contains meaningful working components, but it is not currently
certifiable for production. The fresh audit confirms that all 19 canonical
capability entrypoints load. The remaining blockers are runtime configuration,
model-provider routing, a failing full-stack capability contract, false-success
integration behavior, incomplete quality gates, unavailable frontend
dependencies, unavailable Docker runtime, and stale readiness claims.

No engineering score, certification score, or benchmark score is issued.

## 2. Audit Baseline

- Date: 2026-09-21, Asia/Singapore.
- Branch: `main`.
- HEAD: `ffea74414f84f35000b9f9f8b413c778f611b7a1`.
- Version file: `v1.0.0-developer-preview`.
- The worktree was already dirty before this audit. Existing user files and
  audit artifacts were not reverted.
- The shell-visible checkout did not contain `.env`. No secret value was read,
  printed, replaced, or committed.
- Process-only placeholder secrets were used only for import and API smoke
  checks; they were not written to disk.

## 3. Evidence Summary

| Area | Fresh result | Classification |
|---|---|---|
| Python compile | `compileall` passed for `backend`, `apps`, `benchmarks` | PASS |
| Backend import without secret | Fails with `SECRET_KEY is required` | BLOCKED |
| Backend import with process-only secret | Pass | PASS, not deployment proof |
| API smoke with process-only secret | `/`, `/health`, `/api/v1/capabilities` 200; protected health 401 | PARTIAL PASS |
| Canonical capability registry | 19 registered, 19 loadable | PASS |
| Entrypoint regression test | 1 passed | PASS |
| Pytest onboarding rerun | 109 passed, 1 skipped, 1 failed; stopped at first failure | FAIL |
| Ruff | 3,442 errors | FAIL |
| Mypy | 86 errors in 29 files, 632 files checked | FAIL |
| Flake8 | Non-zero, 73,696 output lines | FAIL |
| Black | 2,066 files would be reformatted; 28 failed to reformat | FAIL |
| Isort | Non-zero | FAIL |
| Bandit | Non-zero; syntax errors in generated `real_cases` files | FAIL |
| Safety | Exit 64; no vulnerability verdict | INCONCLUSIVE |
| Real performance benchmark | Exit 1 before measurements | BLOCKED |
| Docker Compose config | Fails because required `SECRET_KEY` is absent | BLOCKED |
| Docker daemon | Cannot connect to Linux engine named pipe | BLOCKED |
| Frontend build | `next` not found because dependencies are not installed | BLOCKED |
| Integration trading smoke | `success=True`, `error=None`, `outputs=[]` with reasoning error log | FAIL |

Fresh command output is stored under `audit_output/current_*`. The previous
onboarding output is under `onboarding_output/` and is not treated as a release
certificate.

## 4. Findings

### P1-01: Model Provider and Benchmark Are Not Runnable

`python -m benchmarks.performance_benchmark` failed before producing raw
measurements. LiteLLM received `claude-3-5-sonnet-20240620` without an explicit
provider and reported `LLM Provider NOT provided`.

Relevant code:

- `backend/app/core/config.py:22` defaults the reasoning model to the Claude
  model name without a provider prefix.
- `backend/app/core/model_router.py` maps Gemini models to `GOOGLE_API_KEY`,
  while the benchmark does not select an explicit Gemini model.
- `.github/workflows/ci.yml:90` runs the real benchmark as an unconditional CI
  job without configuring a provider secret.

Impact: no current benchmark score can be used as evidence. Stored scores remain
stale or unverified.

### P1-02: Runtime Requires a Secret That Is Not Available to This Checkout

`backend.app.main` fails without `SECRET_KEY`. `docker compose config` also
fails at `docker-compose.yml:103`, where `SECRET_KEY` is required. The compose
file additionally warns that `POSTGRES_PASSWORD` is unset.

This is not a reason to replace the user's saved secret. The remediation must
load the existing secret from the intended local environment or secret store and
must never print it.

### P1-03: Full-Stack Architecture Score Uses Conflicting Scales

The architecture result schema limits `architecture_score` to `0.0..1.0` at
`apps/full_stack_engineer/schemas.py:78`. The architecture engine computes a
weighted score on a `0..100` scale at
`apps/full_stack_engineer/architecture_review_engine.py:637` and renders it as
`/100` at line 799. The observed test failure passes `84.1` into the `0..1`
contract.

Impact: the full-stack capability crashes during a normal architecture review.
The canonical score scale must be selected and applied consistently to models,
serialization, thresholds, reports, and tests.

### P1-04: Integration Workflow Reports Success With No Outputs

The fresh trading integration smoke produced:

- `success=True`
- `error=None`
- `outputs=[]`
- intermediate data existed, but the reasoning step logged
  `UnifiedEvidence object has no attribute description`

`apps/integration/workflow.py:114` marks a workflow successful after all step
functions return. Several steps catch errors and store them as intermediate
data instead of failing the workflow. This allows an unavailable upstream or a
degraded step to look successful.

Impact: callers can persist or display an empty result as a successful analysis.

### P2-01: Quality Gates Are Far From Green

The current repository gate results are 3,442 Ruff errors and 86 Mypy errors in
29 files. Black and Isort also fail. Bandit encounters syntax-invalid generated
fixture sources. The full test run did not reach a final all-tests summary; the
max-fail run stopped at the full-stack failure.

The old README claims `MyPy=0`, Ruff clean, and 166 collected tests. Those claims
are not current evidence.

### P2-02: Frontend Cannot Be Built From This Checkout

`frontend/package-lock.json` exists, but `frontend/node_modules` is absent and
`npm run build` fails with `next is not recognized`. The route inventory also
shows:

- `frontend/app/trading/page.tsx:1` renders `TestComponent`.
- `frontend/app/workspace/page.tsx:9` redirects directly to trading.
- No chat route exists under `frontend/app`.

This is both an environment setup gap and a product completeness gap.

### P2-03: CI Does Not Model External Dependencies Safely

The CI workflow runs a model-backed benchmark without a provider secret and
does not run the frontend build. The CCE workflow starts the full Docker stack,
but no visible mechanism supplies the required `SECRET_KEY` and provider
configuration. A clean CI checkout will therefore fail for environment reasons
before proving product behavior.

### P3-01: Release Identity and Documentation Are Inconsistent

`VERSION`, `pyproject.toml`, backend settings, frontend package metadata,
release files, and older audit documents use different version identities.
README and capability documents contain production-ready, 100/100, and old
benchmark claims that conflict with current runtime evidence. These documents
must be labeled historical or reconciled before any release statement is
published.

### P3-02: Audit Artifacts Are Not Ignored

`audit_output/`, `onboarding_output/`, and their archives were visible as
untracked files during this audit. The repository now ignores these generated
locations so reports cannot accidentally enter a product commit. Existing
artifacts remain local evidence and are not release inputs.

## 5. Verified Strengths

- All 19 canonical capability packages expose a loadable `get_app()` contract.
- Python compilation succeeds for the main backend, apps, and benchmark trees.
- API routing and authentication behavior respond correctly in a process-only
  smoke environment.
- The repository has explicit CI, compose, benchmark, and capability test
  surfaces that can become reliable gates after reconciliation.

## 6. Release Decision

Do not certify production, do not reuse stored benchmark scores, and do not
claim an enterprise or Grade A platform status. The next release audit should
start only after the P1 findings have tests proving their corrected behavior.

## 7. Remediation Status - 2026-09-22

The following changes have been implemented after the baseline above:

- Full-stack architecture scores are normalized to the documented 0..1 contract,
  with regression coverage for the report boundary.
- Integration evidence is adapted to the reasoning contract, and unavailable
  market data or reasoning failures now fail the workflow instead of returning
  a successful empty result.
- Gemini routing supports `gemini/gemini-2.5-flash` and the
  `GEMINI_API_KEY`/`GOOGLE_API_KEY` compatibility path without logging values.
- The benchmark emits `BENCHMARK BLOCKED` and no score when provider
  configuration is absent or the provider call cannot complete.
- Compose now requires database credentials and uses the internal database
  service URL; the saved `SECRET_KEY` was not replaced.
- The audit index is consolidated, duplicate roll-ups are removed, and
  generated audit output is ignored by Git.

Still open and not certified:

- A real provider-backed benchmark with an authorized key has not produced
  fresh measurements in this run.
- Full Ruff, Mypy, and pytest gates still require completion and remediation.
- Frontend dependency installation/lint and Docker service health remain
  environment-dependent and were not declared passing without evidence.
- The frontend trading placeholder, workspace redirect, and missing chat route
  remain product-completeness work.
