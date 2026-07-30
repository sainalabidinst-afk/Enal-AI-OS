# Knowledge K2 — Hybrid Retrieval & Context Builder

## Status: Implemented

## Overview

K2 builds on K1 (Knowledge Graph + Registry + Evidence) to provide hybrid retrieval
that combines graph similarity, registry search, and evidence lookup into a unified
context for the AI.

## Components

### HybridRetrieval

Combines three retrieval strategies:
- **Graph similarity** via `KnowledgeGraph.similarity()`
- **Registry search** via `KnowledgeRegistry.find_by_name()` and `find_by_domain()`
- **Evidence lookup** via `EvidenceStore.get()`

### ContextBuilder

Constructs structured `KnowledgeContext` from retrieval results:
- Primary concepts
- Related concepts (via graph traversal)
- Supporting evidence
- Contradicting evidence
- Aggregate confidence
- Source tracking

### KnowledgeContext

Standardized output contract:
```json
{
  "query": "string",
  "primary_concepts": [],
  "related_concepts": [],
  "supporting_evidence": [],
  "contradicting_evidence": [],
  "confidence": 0.0,
  "sources": [],
  "metadata": {}
}
```

## Usage

```python
from apps.organization.knowledge_retrieval import create_context_builder

builder = create_context_builder()
context = builder.build("Clean Architecture", domain="code")
print(context.to_dict())
```

## Integration

- Used by reasoning engine to enrich prompts with relevant knowledge
- Used by capability workers to augment execution context
- Feeds into K3 Evidence Intelligence for conflict detection
- Feeds into K4 Experience Memory for lesson extraction
