# Truth Matrix

| Area | Claim | Actual Evidence | Status | Severity | Action |
|---|---|---|---|---|---|
| Baseline | Repository is v1.0.0 developer preview | `VERSION` says `v1.0.0-developer-preview`; no tag at HEAD | PARTIALLY VERIFIED | P3 | Reconcile release identity before publishing |
| Registry | 19 capabilities are registered | `apps/__init__.py` contains 19 entries | VERIFIED | INFO | Preserve as canonical count |
| Loadability | All registered capabilities are available | Independent probe: 9 loadable, 10 fail `get_app` lookup | INVALID | P1 | Add or reconcile entrypoint contracts |
| Capability execution | Capability code exists | Packages and tests exist; only Trading Analyst direct execution was verified | PARTIALLY VERIFIED | P2 | Execute each loadable capability with supported inputs |
| Capability classification | Integration, organization and society are user capabilities | They are imported platform support packages and absent from canonical registry | INVALID | P3 | Keep infrastructure classification consistent |
| Certification | Stored certificates prove current quality | Artifacts exist but runtime benchmark is blocked and loadability is partial | UNVERIFIED | P1 | Re-certify only from fresh evidence |
| Benchmark | 96.99 is a current measured score | 22 stored files repeat 96.99; current run has zero executions | STALE | P1 | Configure provider and rerun raw benchmark |
| Model routing | Reasoning model is callable | LiteLLM rejects `claude-3-5-sonnet-20240620` without provider | BLOCKED | P1 | Configure explicit provider and authorized key |
| Backend | Backend is implemented | App imports; root and health return 200 locally | PARTIALLY VERIFIED | P2 | Verify full dependency-backed runtime |
| Backend quality | Code passes configured quality gates | `mypy`: 86 errors in 29 files; `ruff`: 3,442 errors | INVALID | P2 | Triage quality failures before release |
| Testing | Full suite is passing | 938 collected; `pytest -q` timed out at 604 seconds without summary | BLOCKED | P1 | Isolate the hanging test and rerun to completion |
| Frontend | Frontend is production complete | Build passes, but `/trading` is a test stub, `/workspace` redirects, `/chat` is missing | PARTIALLY VERIFIED | P2 | Reconcile product routes and backend connectivity |
| Docker | Stack is healthy | `docker compose config` passes; `up -d --build` times out and creates no containers | BLOCKED | P1 | Diagnose image build/start path |
| Security | Secrets fail safely | Pydantic rejects empty `SECRET_KEY`, but local `.env` contains a known placeholder and compose accepts it | PARTIALLY VERIFIED | P1 | Require a non-placeholder deployment secret |
| Documentation | Architecture principles document exists | `docs/ARCHITECTURE_PRINCIPLES.md` is absent | STALE | P3 | Restore or explicitly retire the claim |
| End to end | User request reaches durable result and telemetry | Only local direct capability and partial integration flows were observed | UNVERIFIED | P1 | Run an authenticated dependency-backed E2E flow |
| Release | Production ready / Enterprise Platform | Evidence has blocked runtime, stale scores, partial registry loadability and incomplete suite | INVALID | P1 | Classify as D - NOT READY |
