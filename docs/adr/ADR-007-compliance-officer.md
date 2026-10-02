# ADR-007: Compliance Officer Capability Pack Architecture

|Bidang|Nilai|
|-------|-------|
|**ID ADR**|ADR-007|
|**Status**|Accepted|
|**Date**|2026-10-02|
|**Decision Maker**|Platform Architecture Board|
|**Related RFC**|RFC-0028|

## Context

The Compliance Officer capability pack needs to assess compliance across all other packs while maintaining the Capability First Rule.

## Decision

1. Compliance Officer pack will reside in `apps/compliance_officer/` following the standard pack structure
2. Compliance Officer imports from Security Engineer (consumer relationship) for threat models
3. Compliance frameworks (ISO 27001, NIST, PCI-DSS, GDPR, SOC2) are defined as knowledge base, not direct imports
4. The pack uses the Runtime facade (`backend.app.runtime`) for Core access

## Consequences

- Compliance Officer can leverage Security Engineer's vulnerability assessments
- No direct imports from business packs (trading, healthcare, etc.)
- Compliance frameworks are data-driven, enabling easy extension
- All Core access goes through the Runtime facade (governance compliant)

## Cross-Capability Proof

- Security Engineer provides vulnerability assessments and threat models (provider → consumer)
- System Architect provides architecture reviews for compliance checking (provider → consumer)
- Business Analyst provides requirement documentation for audit scope (provider → consumer)
