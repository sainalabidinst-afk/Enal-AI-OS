# RFC-0030: Finance Analyst Capability Pack

| Field | Value |
|-------|-------|
| **RFC ID** | RFC-0030 |
| **Status** | Draft |
| **Version** | 0.1.0 |
| **Capability Pack** | Finance Analyst |
| **Capability ID** | `finance-analyst` |
| **Category** | Finance |
| **Related ADR** | ADR-010 |

## Summary

Add an optional Finance Analyst pack for evidence-backed financial analysis,
scenario modeling, and finance-control checks. The pack is conditional: it is
not registered or shipped until a project need, domain owner, and governance
review are confirmed.

## Motivation

Projects may need repeatable analysis of financial statements, cash flows,
budget assumptions, and risk scenarios without coupling domain logic to Core.
This proposal establishes a bounded pack design and measurable baseline before
any runtime implementation.

## Scope

- Normalize user-provided financial data and state assumptions and units.
- Calculate ratios, cash-flow measures, and sensitivity or scenario outcomes.
- Identify risk indicators and map supplied evidence to a configurable control
  checklist.
- Produce traceable summaries with calculations, source references, uncertainty,
  and missing-data warnings.

Out of scope: investment recommendations, trading execution, tax or audit
opinions, credit decisions, and claims of regulatory compliance without
jurisdiction- and date-specific evidence. The pack must not fabricate figures
or fill missing inputs with silent defaults.

## Detailed Design

### Engine

`FinanceAnalystEngine` should be a deterministic orchestration layer with
separate operations for `financial_summary`, `risk_model`, `scenario_analysis`,
and `control_check`. Calculations should use explicit typed inputs, declared
units, time periods, and assumptions. LLM output may explain results but must
not be the source of arithmetic; outputs should expose formulae, input lineage,
and limitations.

### Tools and contracts

- `FinancialDataNormalizer`: validates currencies, periods, signs, and required
  fields; rejects ambiguous units.
- `RatioCalculator`: computes documented ratios and reports undefined
  denominators.
- `ScenarioModel`: runs bounded sensitivity cases from user-specified
  assumptions; no hidden forecasts.
- `FinanceControlMapper`: matches evidence to a versioned, supplied control
  checklist; returns unknown where evidence is insufficient.
- Define request/response schemas in the pack; tool calls must be allowlisted,
  auditable, and read-only by default. External data connectors require separate
  project approval and provenance metadata.

### Governance and boundaries

- Any future pack code imports permitted Core services only through
  `backend.app.runtime`; no imports from `backend.app.core` internals.
- No direct imports from other capability packs. Cross-pack work uses approved
  runtime contracts.
- Before activation, add the pack to the standard registration and boundary
  checks, provide an `apps/finance_analyst/` package, benchmark/golden assets,
  and a project-specific `real_cases/` directory with approved, non-sensitive
  examples.
- Review `docs/GOVERNANCE_CHARTER.md`, `docs/GOVERNANCE.md`, package boundaries,
  capability-first rules, data handling, and the relevant ADR before merging.

### Benchmark and golden baseline

`benchmarks/vertical_industry_scenarios.json` defines ten baseline scenarios.
The executable-shaped golden suite is
`golden_tests/finance_analyst/golden_test_suite.json`; each benchmark scenario
maps one-to-one to a golden test. These are acceptance specifications, not
measured results. A runnable benchmark and CI gate are required only when an
implementation is approved.

## Alternatives Considered

1. Implement and register all vertical packs together — rejected because demand,
   datasets, and domain review are not yet established.
2. Add finance logic to an existing general-purpose pack — rejected because it
   weakens capability ownership and domain-specific validation.
3. Use an LLM for all calculations — rejected because financial outputs require
   reproducible arithmetic and auditable assumptions.

## Compatibility

This is a proposal and adds no runtime behavior or public API. Existing packs
remain unaffected. Future schemas must be versioned and opt-in.

## Security and Safety Considerations

Treat financial records as sensitive. Minimize retention, redact identifiers in
logs, validate external files, and keep connectors read-only unless separately
authorized. Clearly distinguish calculated facts, assumptions, and
interpretations; require human review for consequential decisions.

## Testing Strategy

- Validate all ten scenario-to-golden-test references and suite structure.
- On implementation, add deterministic unit tests for calculations, invalid and
  missing inputs, reproducibility, provenance, and boundary enforcement.
- Require domain-owner review of scenario data and thresholds before CI
  certification. Do not present draft scores as benchmark results.

## Governance Checklist

- [ ] Confirm project demand and a finance domain owner.
- [ ] Review this RFC and ADR-010 through the documented RFC/ADR process.
- [ ] Verify Runtime-facade-only Core access and package boundaries.
- [ ] Approve data sources, retention, jurisdiction, and human-review policy.
- [ ] Implement at least ten reviewed scenarios and a runnable golden-test gate.
- [ ] Add real cases only with documented provenance and authorization.

## Timeline

Draft and benchmark specification only. Implementation is conditional on
project demand and completion of the governance checklist.

## References

- [Governance Charter](../GOVERNANCE_CHARTER.md)
- [Governance](../GOVERNANCE.md)
- [RFC process](README.md)
- [ADR-010](../adr/ADR-010-finance-analyst.md)
