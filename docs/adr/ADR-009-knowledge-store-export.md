# ADR-009: Knowledge Store Public Export

|Bidang|Nilai|
|-------|-------|
|**ID ADR**|ADR-009|
|**Status**|Accepted|
|**Date**|2026-10-01|
|**Decision Maker**|Platform Architecture Board|

## Context

The `KnowledgeStore` class was implemented but not exported from `backend.app.core.knowledge.__init__.py`, causing import errors when capability packs tried to use it via the Runtime facade.

## Decision

1. Export `KnowledgeStore` from `backend/app/core/knowledge/__init__.py`
2. Add `KnowledgeStore` to the `__all__` list for public API completeness

## Consequences

- Capability packs can now import `KnowledgeStore` via the Runtime facade
- No breaking changes — this is an additive export fix
- The Runtime facade (`backend.app.runtime`) re-exports this for app access

## Cross-Capability Proof

- Knowledge Engineer pack uses `KnowledgeStore` for ontology persistence
- Data Engineer pack uses `KnowledgeStore` for dataset metadata
- Research Assistant pack uses `KnowledgeStore` for literature knowledge base
