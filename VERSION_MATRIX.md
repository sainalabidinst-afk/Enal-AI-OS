## Component Versions

| Component | Version | Status | Notes |
|-----------|---------|--------|-------|
| Backend Baseline | v1.0.0-dev | Baseline | Active 2026-07-11 |
| Product Intelligence | v1.0.0-dev | Active | Active 2026-07-14 |
| Product Contract | v1 | Locked | Effective 2026-07-11 |
| Frontend MVP | v1.0.0-dev | Active | Product MVP phase |
| Capability Packs | v1.0.0-dev | Active | Evolving through dogfooding |
| API Contracts | v1 | Stable | See `docs/frontend/API_MAPPING.md` for single source of truth |
| Benchmark Framework | v1.0.0-dev | Active | Async runner with concurrency, capability scoring, CCE |
| Telemetry | v1.0.0-dev | Active | JSONL metrics collector, KPI aggregation |

Version matrix is now tied to the Product Contract. Frontend must not introduce new API contracts without updating this matrix and the Product Contract.
