# ADR-013: Observability Capability Pack

| Field | Value |
|-------|-------|
| **ADR ID** | ADR-013 |
| **Status** | Proposed |
| **Date** | 2026-10-02 |
| **Decision Maker** | Pending Platform Architecture Board review |
| **Related RFC** | RFC-0033 |
| **Target Version** | ECP v2.3.0 |

## Context

The Observability pack is proposed to provide metrics collection, trace
analysis, log analysis, and anomaly detection. Signal data can be sensitive,
thresholds can drive incident response, and incorrect automated actions could
escalate incidents. The decision must keep the pack advisory, explicit, and
decoupled from Core.

## Decision

Propose that, if project demand is confirmed:

1. The pack resides in `apps/observability/` and owns its domain engine,
   schemas, and tools.
2. All Core services are accessed through `backend.app.runtime`; direct Core
   internal imports and cross-pack imports are prohibited.
3. Metrics, thresholds, and baselines must be supplied explicitly; missing
   values are reported as unknown rather than fabricated.
4. Anomaly and threshold outputs are advisory: `anomaly_detection_claim = false`,
   `root_cause_attribution = false`, and no certification or compliance claim
   is emitted.
5. Activation requires a platform/observability domain owner review, ten
   benchmark scenarios, golden tests, and governance checks.

## Consequences

- No runtime behavior or operational control is approved by this proposal.
- Outputs are advisory and cannot certify a system healthy or replace incident
  response.
- Telemetry, traces, and logs must be authorized, minimized, de-identified
  where feasible, and provenance-preserving.
- Draft scenarios and scores are not benchmark results.

## Cross-Capability Proof

No cross-pack dependency is proposed. Any future integration must use approved
runtime contracts, include platform and data-handling review, and preserve the
Capability First Rule.
