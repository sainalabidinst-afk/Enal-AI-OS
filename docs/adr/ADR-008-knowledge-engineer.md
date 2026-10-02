# ADR-008: Knowledge Engineer Capability Pack Architecture

|Bidang|Nilai|
|-------|-------|
|**ID ADR**|ADR-008|
|**Status**|Accepted|
|**Date**|2026-10-02|
|**Decision Maker**|Platform Architecture Board|
|**Related RFC**|RFC-0029|

## Context

The Knowledge Engineer capability pack needs to provide knowledge infrastructure for all other packs while maintaining the Capability First Rule.

## Decision

1. Knowledge Engineer pack will reside in `apps/knowledge_engineer/` following the standard pack structure
2. Knowledge Engineer has no direct consumer relationships (it's an infrastructure pack)
3. Ontology and knowledge graph data are stored as domain-specific knowledge bases
4. The pack uses the Runtime facade (`backend.app.runtime`) for Core access

## Consequences

- Knowledge Engineer provides foundational knowledge services to all packs
- No circular dependencies possible due to infrastructure role
- Domain knowledge is pluggable and extensible
- All Core access goes through the Runtime facade (governance compliant)

## Cross-Capability Proof

- Research Assistant consumes ontology for literature domains (provider → consumer)
- Decision Intelligence consumes knowledge graph for reasoning context (provider → consumer)
- Data Engineer consumes entity resolution for data catalogs (provider → consumer)
- Trading Analyst consumes financial instrument knowledge graph (provider → consumer)
- System Architect consumes architecture decision records knowledge graph (provider → consumer)
