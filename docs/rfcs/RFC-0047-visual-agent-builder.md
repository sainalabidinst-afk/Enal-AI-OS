# RFC-0047: Visual Agent Builder

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Frontend Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-03
**Versi:** 1.0.0
**Status:** Draft → Proposed
**SSOT:** Rancangan visual agent builder untuk membuat dan mengonfigurasi agent tanpa menulis kode
<!-- DOCUMENT_METADATA_END -->

## Abstrak

RFC ini mendefinisikan Visual Agent Builder untuk ECP, yang memungkinkan user membuat dan mengonfigurasi agent melalui UI drag-drop tanpa menulis kode. Builder ini mengintegrasikan dengan AgentFactory, AgentValidator, dan AgentRuntime di backend.

## Konteks

Setelah Visual Builder Foundation (RFC-0046) selesai, langkah selanjutnya adalah Agent Builder khusus. User perlu dapat:
1. Drag-drop agent node di canvas
2. Konfigurasi name, description, model, prompt, temperature, max_tokens
3. Attach tools dan knowledge bases
4. Test agent di playground
5. Save/deploy agent

## Keputusan

### 1. Agent Builder UI

**Layout:**
- Header: Back button, title "Agent Builder", Save/Run buttons
- Main area: BuilderCanvas (kiri) + AgentConfigPanel (kanan, 384px)

**AgentConfigPanel tabs:**
- General: name, description, system prompt
- Model: model selection, temperature slider, max tokens
- Tools: checklist tools (web_search, file_read, file_write, email_send, calendar, database_query)
- Knowledge Bases: checklist KBs (kb_docs, kb_policies, kb_products, kb_faq)

### 2. Backend Integration

**AgentFactory** (`backend/app/core/agent_factory.py`):
- `create(blueprint)` → base_config dict dengan name, model, temperature, prompt, tools, knowledge_base_ids

**AgentValidator** (`backend/app/core/agent_validator.py`):
- Validasi: name tidak kosong, model terpilih, prompt tidak kosong, temperature 0-2, max_tokens > 0

**AgentRuntime** (`backend/app/core/agent_runtime.py`):
- `run(blueprint, task, context)` → validate → create → return success/error dengan latency

### 3. API Endpoints

Menggunakan existing `/api/v1/blueprints/agent` endpoints dari RFC-0046.

### 4. Frontend Route

`/builder/agent` — `AgentBuilderPage` rendering `AgentBuilder`

## Implementasi

### Frontend Components

- `AgentBuilder.tsx` — Main builder page dengan canvas + config panel
- `AgentConfigPanel.tsx` — Sidebar config dengan tabs General/Model/Tools/Knowledge

### Backend Modules

- `backend/app/core/agent_factory.py` — AgentFactory
- `backend/app/core/agent_validator.py` — AgentValidator
- `backend/app/core/agent_runtime.py` — AgentRuntime

## Dependencies

- RFC-0046: Visual Builder Foundation
- Existing: Decorator SDK, Pipeline Engine

## Testing

- TypeScript: 0 errors
- Ruff: 0 errors
- Mypy: 0 errors

## References

- RFC-0046: Visual Builder Foundation
- SimplAI Agent Builder: https://simplai.ai/docs/agents/
