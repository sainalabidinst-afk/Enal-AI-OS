# ADR-005: Cloud Architect Capability Pack Architecture

|Bidang|Nilai|
|-------|-------|
|**ID ADR**|ADR-005|
|**Status**|Accepted|
|**Date**|2026-10-02|
|**Decision Maker**|Platform Architecture Board|
|**Related RFC**|RFC-0026|

## Context

The Cloud Architect capability pack needs to integrate with existing infrastructure and security packs while maintaining the Capability First Rule.

## Decision

1. Cloud Architect pack will reside in `apps/cloud_architect/` following the standard pack structure (engine, schemas, worker, knowledge modules)
2. Cloud Architect imports from Infrastructure Engineer (lower-level), not from Security Engineer (peer) — uses shared contracts
3. All cloud provider APIs are accessed lazily to avoid hard dependencies
4. The pack uses the Runtime facade (`backend.app.runtime`) for Core access

## Consequences

- Cloud Architect can leverage Infrastructure Engineer's HA/DR knowledge
- No circular dependencies with Security Engineer
- Cloud provider APIs remain optional dependencies
- All Core access goes through the Runtime facade (governance compliant)

## Cross-Capability Proof

- Infrastructure Engineer provides HA/DR patterns (consumer → provider)
- Security Engineer provides threat models (consumer → provider via Runtime)
- DevOps Assistant provides infrastructure state data (provider → consumer via contracts)
