<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/KNOWLEDGE_RETRIEVAL.md`
- Judul: Knowledge Retrieval
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Knowledge K2 â€” Hybrid Retrieval & Context Builder

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for KNOWLEDGE_RETRIEVAL
<!-- DOCUMENT_METADATA_END -->

## Status: Implemented

## Overview

K2 builds on K1 (Knowledge Graph + Registry + Evidence) to provide hybrid retrieval
that combines graph similarity, registry search, and evidence lookup into a unified
context for the AI.
> Terjemahan Indonesia: K2 membangun pada K1 (Knowledge Graph + Registry + Evidence) untuk menyediakan hybrid retrieval itu combines graph similarity, registry search, dan evidence lookup into sebuah unified context untuk AI.

## Components

### HybridRetrieval

Combines three retrieval strategies:
> Terjemahan Indonesia: Menggabungkan tiga strategi pengambilan:
- **Graph similarity** via `KnowledgeGraph.similarity()`
- **Registry search** via `KnowledgeRegistry.find_by_name()` and `find_by_domain()`
- **Evidence lookup** via `EvidenceStore.get()`

### ContextBuilder

Constructs structured `KnowledgeContext` from retrieval results:
> Terjemahan Indonesia: Constructs structured KnowledgeContext dari retrieval results:
- Primary concepts
- Related concepts (via graph traversal)
- Supporting evidence
- Contradicting evidence
- Aggregate confidence
- Source tracking

### KnowledgeContext

Standardized output contract:
> Terjemahan Indonesia: Kontrak keluaran standar:
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
