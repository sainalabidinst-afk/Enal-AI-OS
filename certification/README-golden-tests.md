# Phase 1.3 — Golden Test Expansion

Golden Tests are formalized, versioned test suites that serve as the executable specification for each Capability Pack. They are the primary regression gate during certification.

## Categories

| Category | Purpose |
|----------|---------|
| Functional | Core happy-path behavior |
| Edge Cases | Boundary values, empty inputs, max limits |
| Invalid Input | Malformed requests, schema violations |
| Regression | Previously fixed bugs that must not return |
| Explainability | Reasoning chain, evidence traceability |
| Performance | Latency, memory, throughput thresholds |
| Contract Compliance | Request/response schema validation |

## Storage

```
certification/
└── golden-tests/
    └── {capability_id}/
        ├── functional.json
        ├── edge-cases.json
        ├── invalid-input.json
        ├── regression.json
        ├── explainability.json
        ├── performance.json
        └── contract-compliance.json
```

## Status

This phase is scaffolding-ready. Full golden test authoring should be done per capability after Phase 1.1 audit findings are resolved.
