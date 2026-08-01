# ECP Network Engineer — Baseline Freeze

**Baseline Tag:** `v1.0.0-dev+network-sprint2`
**Status:** Accepted
**Date:** 2026-07-09
**Note:** Historical sprints are preserved for baseline integrity. Current development uses "Milestone" terminology.

## Definition of Done — Met

### Milestone 1 — Network Engineer MVP (Sprint 1)
- [x] Upload `.rsc` file
- [x] Parse RouterOS configuration
- [x] Build internal topology
- [x] Detect configuration problems (45 rules)
- [x] Generate recommendations (P0–P3 with Why/Impact/Confidence)
- [x] Generate improved configuration
- [x] Produce deployment documentation (Markdown)
- [x] Pass all Golden Tests (31/31 scenarios)

### Milestone 1.5 — Hardening (Sprint 1.5)
- [x] 31 golden test scenarios (7 original + 24 new)
- [x] Regression dataset: broken-config, invalid-syntax, partial-config, old-v6, new-v7
- [x] Rule coverage tracker (hit count, precision, recall, F1)
- [x] Performance benchmarks (500/5k/50k lines)
- [x] Confidence calibration from evidence
- [x] All tests passing

### Milestone 2 — Controlled Deployment (Sprint 2)
- [x] Semantic Configuration Diff Engine
- [x] Backup Manager (export → hash → timestamp → artifact store)
- [x] Risk Scoring Engine (config/rollback/security/downtime risk)
- [x] Verification Engine (interface, gateway, DNS, DHCP, routes)
- [x] Audit Trail (all steps recorded as artifacts)
- [x] Controlled Deployment Orchestrator
- [x] Deployment Runbook UX (Changes/Risk/Pre-Deployment/Deployment/Post-Deployment/Recovery)
- [x] Deployment Timeline (visual step progress)
- [x] Explain Before Deploy (process-oriented, not binary yes/no)
- [x] Rollback Status: Pending / Ready / Unavailable / Completed
- [x] Human approval required in v1.0-dev
- [x] All Milestone 2 tests pass (7/7)

## Baseline Artifacts

- Golden Test Scenarios: `golden/mikrotik/` (31 scenarios)
- Golden Test Runner: `tests/reference/test_network_engineer.py`
- Controlled Deployment Tests: `tests/reference/test_controlled_deployment.py`
- Performance Benchmark: `benchmarks/network_performance_benchmark.py`
- Rule Coverage Tracker: `apps/network_engineer/rule_coverage_tracker.py`
- Core Modules:
  - `apps/network_engineer/mikrotik/routeros_parser.py`
  - `apps/network_engineer/analyzer.py`
  - `apps/network_engineer/graph_builder.py`
  - `apps/network_engineer/recommendation_engine.py`
  - `apps/network_engineer/docs_generator.py`
  - `apps/network_engineer/diff_engine.py`
  - `apps/network_engineer/backup_manager.py`
  - `apps/network_engineer/risk_scorer.py`
  - `apps/network_engineer/verification_engine.py`
  - `apps/network_engineer/audit_trail.py`
  - `apps/network_engineer/controlled_deployment.py`

## Known Limitations

- Parser: RouterOS v6/v7 basic sections only (no advanced routing protocols yet)
- Analyzer: 45 rules, domain-specific to basic networking
- Deployment: Simulated only (no live SSH/API to MikroTik devices)
- Documentation: Markdown only (no HTML/PDF/Draw.io yet)
- No multi-router orchestration
- No parallel deployment

## Next Phase: Dogfooding → Network Operations

See `docs/ROADMAP.md` for next steps.
