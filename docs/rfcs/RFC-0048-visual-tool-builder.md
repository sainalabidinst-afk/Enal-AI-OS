# RFC-0048: Visual Tool Builder

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Frontend Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-03
**Versi:** 1.0.0
**Status:** Draft → Proposed
**SSOT:** Rancangan visual tool builder dengan step graph untuk membuat tool tanpa menulis kode
<!-- DOCUMENT_METADATA_END -->

## Abstrak

RFC ini mendefinisikan Visual Tool Builder untuk ECP, yang memungkinkan user membuat tool dengan step graph (LLM Call, Python Code, API Call, KB Search, Web Scraper, Conditional, Delay) melalui UI visual.

## Konteks

Setelah Agent Builder (RFC-0047) selesai, langkah selanjutnya adalah Tool Builder. Tool memerlukan step graph yang lebih kompleks dari agent, dengan branching, conditional logic, dan error handling.

## Keputusan

### 1. Tool Builder UI

**Layout:**
- Header: Back button, title "Tool Builder", Save/Run buttons
- Main area: BuilderCanvas (kiri) + StepConfigPanel (kanan, 384px)

**Step Types:**
| Type | Icon | Description |
|------|------|-------------|
| `llm_call` | Brain | LLM inference |
| `python_code` | Code | Python code execution |
| `api_call` | Globe | HTTP API call |
| `kb_search` | Book | Knowledge base search |
| `web_scraper` | Globe | Web scraping |
| `conditional` | GitBranch | If/else branching |
| `delay` | Clock | Time delay |

**StepConfigPanel:**
- Step ID, Label, Type dropdown
- Configuration JSON editor
- Save/Delete buttons

### 2. Backend Integration

**StepExecutor** (`backend/app/core/step_executor.py`):
- Execute individual step by type
- Support: llm_call, python_code, api_call, kb_search, web_scraper, conditional, delay

**StepValidator** (`backend/app/core/step_validator.py`):
- Validate: name tidak kosong, steps tidak kosong, step IDs unique, step types valid

**ToolEngine** (`backend/app/core/tool_engine.py`):
- `run(blueprint, context)` → validate → execute steps sequentially → return results dengan latency

### 3. API Endpoints

Menggunakan existing `/api/v1/blueprints/tool` endpoints dari RFC-0046.

### 4. Frontend Route

`/builder/tool` — `ToolBuilderPage` rendering `ToolBuilder`

## Implementasi

### Frontend Components

- `ToolBuilder.tsx` — Main builder page
- `StepConfigPanel.tsx` — Step configuration sidebar

### Backend Modules

- `backend/app/core/step_executor.py` — StepExecutor
- `backend/app/core/step_validator.py` — StepValidator
- `backend/app/core/tool_engine.py` — ToolEngine

## Dependencies

- RFC-0046: Visual Builder Foundation
- Existing: Pipeline Engine

## Testing

- TypeScript: 0 errors
- Ruff: 0 errors
- Mypy: 0 errors

## References

- RFC-0046: Visual Builder Foundation
- SimplAI Tool Builder: https://simplai.ai/docs/tools/
