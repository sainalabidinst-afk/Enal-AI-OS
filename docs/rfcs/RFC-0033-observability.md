# RFC-0033: Observability Capability Pack

| Field | Value |
|-------|-------|
| **RFC ID** | RFC-0033 |
| **Status** | Draft |
| **Version** | 0.1.0 |
| **Capability Pack** | Observability |
| **Capability ID** | `observability` |
| **Category** | Platform |
| **Target Version** | ECP v2.3.0 |
| **Related ADR** | ADR-013 |

## Summary

Add an Observability capability pack for metrics collection, distributed trace
analysis, log analysis, and anomaly detection. The pack is opt-in and advisory:
it summarizes signals and raises threshold breaches but does not replace
runbooks, incident response, or root-cause diagnosis.

## Motivation

Platform teams need consistent, traceable observability analysis that stays
decoupled from Core. Existing packs (SRE Engineer, System Architect) consume
observability data but no bounded pack standardizes metric, trace, log, and
anomaly analysis with explicit assumptions, source references, and safety
boundaries.

## Scope

- Normalize supplied metric samples, trace spans, and log entries.
- Summarize metrics with average/max/min and evaluate threshold breaches.
- Summarize distributed traces with error rate, p95 latency, and health status.
- Group log entries into patterns by matched pattern or level.
- Detect anomalies by comparing observed values to an explicit baseline.
- Preserve source provenance and declare assumptions for every calculation.

Out of scope: operational control or automated remediation, root-cause
attribution, declaring a system healthy/safe, certification or compliance
claims, and fabricating values when required inputs are missing. The pack must
not silently default missing thresholds, baselines, or identifiers.

## Detailed Design

### Engine

`ObservabilityAnalystEngine` is a deterministic orchestration layer that
delegates to `ObservabilityAnalysisEngine` for:
- `metrics_collect` — `collect_metrics`
- `trace_analyze` — `analyze_trace`
- `log_analyze` — `analyze_log`
- `anomaly_detect` — `detect_anomaly`

All calculations use explicit inputs and declared formulae; LLM output may
explain results but must not be the source of arithmetic. Outputs expose
formulae, input lineage, and limitations.

### Tools and contracts

- `MetricCollector`: aggregates samples into summaries and evaluates
  threshold breaches with explicit direction; reports undefined thresholds.
- `TraceAnalyzer`: summarizes trace spans, computes error rate and p95 latency,
  and derives a health flag from an explicit error budget.
- `LogAnalyzer`: groups log entries by pattern or level and maps severity.
- `AnomalyDetector`: compares current value to an explicit baseline and
  threshold; never invents a baseline or threshold.
- Define request/response schemas in the pack; tool calls must be allowlisted
  and auditable and read-only by default.

### Governance and boundaries

- Pack code imports permitted Core services only through `backend.app.runtime`;
  no imports from `backend.app.core` internals.
- No direct imports from other capability packs. Cross-pack work uses approved
  runtime contracts.
- Before activation, register the pack and boundary checks, provide an
  `apps/observability/` package, benchmark/golden assets, and a
  `real_cases/observability/` directory with approved examples.
- Review `docs/GOVERNANCE_CHARTER.md`, `docs/GOVERNANCE.md`, package boundaries,
  operational safety, and data policies before merge.
- Anomaly and threshold outputs must be advisory; they cannot trigger automated
  operational control without a separate safety case and explicit authorization.

### Benchmark and golden baseline

`benchmarks/observability_benchmark.py` defines ten baseline scenarios across six
dimensions. The executable-shaped golden suite is
`golden_tests/observability/golden_test_suite.json`; each scenario maps
one-to-one to a golden test. These are acceptance specifications, not measured
results. A runnable benchmark and CI gate require domain-owner review and an
approved implementation.

## Alternatives Considered

1. Reuse the SRE Engineer pack for all observability — rejected because it
   conflates SRE design with generic signal analysis and weakens ownership.
2. Automated remediation on anomaly detection — rejected because automated
   operational control requires a separate safety case and can worsen incidents.
3. Infer baselines from arbitrary history — rejected because baselines must be
   explicit to remain auditable and reproducible.

## Compatibility

This proposal adds no runtime behavior or public API to existing packs. Future
schemas must be versioned and opt-in under `apps/observability/`.

## Security and Safety Considerations

Treat telemetry, traces, and logs as sensitive. Minimize retention, redact
identifiers in logs, validate external inputs, and keep data sources read-only
unless separately authorized. Surface uncertainty and escalate critical
breaches to established incident procedures; the pack must never represent its
output as a substitute for incident response or root-cause diagnosis.

## Testing Strategy

- Validate all ten scenario-to-golden-test references and suite structure.
- On implementation, add deterministic unit tests for calculations, invalid and
  missing inputs, threshold boundaries, reproducibility, provenance, and
  advisory-only behavior.
- Require domain-owner review of scenario data and thresholds before CI
  certification. Do not present draft scores as benchmark results.

## Governance Checklist

- [ ] Confirm project demand and a platform/observability domain owner.
- [ ] Review this RFC and ADR-013 through the documented RFC/ADR process.
- [ ] Verify Runtime-facade-only Core access and package boundaries.
- [ ] Approve data sources, retention, jurisdiction, and human-in-the-loop policy.
- [ ] Implement at least ten reviewed scenarios and a runnable golden-test gate.
- [ ] Add real cases only with documented provenance and authorization.

## Timeline

Draft and benchmark specification only. Implementation is conditional on
project demand and completion of the governance checklist.

## References

- [Governance Charter](../GOVERNANCE_CHARTER.md)
- [Governance](../GOVERNANCE.md)
- [RFC process](README.md)
- [ADR-013](../adr/ADR-013-observability.md)
