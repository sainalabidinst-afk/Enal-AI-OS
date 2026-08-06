# Phase 1.4 — Real Case Validation

Real Case Validation ensures each Capability performs correctly against realistic, domain-specific scenarios. This is the most important certification gate because it validates capability behavior outside synthetic tests.

## Structure

```
certification/
└── real-cases/
    └── {capability_id}/
        ├── scenarios.json
        └── README.md
```

## Scenario Requirements

1. **Reproducible** — Same input produces same output.
2. **Realistic** — Derived from real-world usage patterns.
3. **Documented** — Business context, expected outcome, pass criteria.
4. **Versioned** — Scenarios evolve with capability version.

## Status

This phase is scaffolding-ready. Real-case scenarios should be authored after Phase 1.1 audit and Phase 1.3 Golden Tests are in place.
