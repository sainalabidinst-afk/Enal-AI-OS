<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary

Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `agents/core/README.md`
- Judul: Readme
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Core Agents (Phase 1)

These are the 10 core agents implemented in Phase 1:
> Terjemahan Indonesia: These adalah 10 core agen implemented dalam Phase 1:

1. **Planner** - Analyzes requests and creates structured plans
2. **Coding Agent** - Writes and reviews code in multiple languages
3. **Research Agent** - Gathers information from web and documents
4. **Data Agent** - Handles databases, data analysis, and migrations
5. **UI Agent** - Designs and builds user interfaces
6. **Trading Agent** - Analyzes markets and executes trades
7. **Network Agent** - Configures networking and security
8. **Writer Agent** - Creates documentation and content
9. **QA Agent** - Tests and validates outputs
10. **Security Agent** - Audits code and infrastructure
11. **Reviewer** - Reviews and merges results

## Usage

```python
from backend.app.agents.orchestrator import orchestrator

result = await orchestrator.run("Build me a full-stack todo app", "conv-123")
print(result["final_result"])
```
