# ADR-006: SRE Engineer Capability Pack Architecture

|Bidang|Nilai|
|-------|-------|
|**ID ADR**|ADR-006|
|**Status**|Accepted|
|**Date**|2026-10-02|
|**Decision Maker**|Platform Architecture Board|
|**Related RFC**|RFC-0027|

## Context

The SRE Engineer capability pack needs to integrate with infrastructure and monitoring systems while maintaining the Capability First Rule.

## Decision

1. SRE Engineer pack will reside in `apps/sre_engineer/` following the standard pack structure
2. SRE Engineer imports from Infrastructure Engineer (consumer relationship)
3. Monitoring integrations (Prometheus, Grafana, Datadog) are accessed via contracts, not direct imports
4. The pack uses the Runtime facade (`backend.app.runtime`) for Core access

## Consequences

- SRE Engineer can leverage Infrastructure Engineer's cluster designs
- No circular dependencies with monitoring tool vendors
- Observability tools remain pluggable dependencies
- All Core access goes through the Runtime facade (governance compliant)

## Cross-Capability Proof

- Infrastructure Engineer provides cluster topology (provider → consumer)
- System Architect provides SLO patterns from architecture reviews (provider → consumer)
- DevOps Assistant provides deployment information (provider → consumer via contracts)
