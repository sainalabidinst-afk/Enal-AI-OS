# Phase 1.6 — Certification Review

Certification Review is the final governance step before a capability is officially marked **Certified**. It aggregates all previous phase results into a single, reviewable decision record.

## Review Gates

1. Capability Audit
2. Benchmark Audit
3. Golden Test Expansion
4. Real Case Validation
5. Production Readiness Review
6. Certification Review

## Decision Matrix

| Grade | Certification Level | Action |
|-------|---------------------|--------|
| A | Certified | Full certification |
| B | Certified | Certified with minor corrective actions |
| C | Provisional | Conditional certification, re-audit in 90 days |
| D | Experimental | Not certified, major rework required |
| F | Experimental | Failed, return to development |

## Artifact

```
certification/
└── certificates/
    └── {capability_id}-certificate.json
```

## Status

This phase is scaffolding-ready. Execution should begin only after all previous phases pass for a given capability.
