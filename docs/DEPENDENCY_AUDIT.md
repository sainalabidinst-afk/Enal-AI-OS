<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/DEPENDENCY_AUDIT.md`
- Judul: Dependency Audit
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
<!-- DOCUMENT_METADATA_END -->

# Dependency Audit Report

**Date:** 2026-08-02
**Scope:** Backend packaging + dependency consistency + CI/Makefile/Dockerfile alignment

---

## 1. Backend Packaging

| Item | Status |
|------|--------|
| `backend/pyproject.toml` | âœ… Created |
| `backend/__init__.py` | âœ… Created |
| Build backend | hatchling |
| Dev dependencies | pytest, pytest-asyncio, ruff, black, mypy |
| Runtime dependencies | fastapi, uvicorn, sqlalchemy, qdrant-client, redis, pydantic, pydantic-settings, litellm, langchain-openai, langchain-core, httpx, pyyaml, aiohttp, python-multipart, psycopg2-binary |

---

## 2. Module Usage vs Declaration

| Module | Status | Action |
|--------|--------|--------|
| `fastapi` | âœ… OK | Used in `main.py`, `api/*` |
| `uvicorn` | âœ… OK | Used in Dockerfile, Makefile |
| `sqlalchemy` | âœ… OK | Used in `db/session.py` |
| `qdrant-client` | âœ… OK | Used in `core/vector_store.py` |
| `redis` | âœ… OK | Used in `core/memory.py`, `core/memory_layer.py`, `core/event_bus.py` |
| `pydantic` | âœ… OK | Used in `models/schemas.py` |
| `pydantic-settings` | âœ… OK | Used in `core/config.py` |
| `litellm` | âœ… OK | Used in `core/model_router.py` |
| `langchain-openai` | âœ… OK | Used in `agents/core/executor_agent.py` |
| `langchain-core` | âœ… OK | Used in `agents/core/*` |
| `httpx` | âœ… OK | Used in `core/benchmark/runner.py` |
| `pyyaml` | âœ… OK | Used in `core/skill_registry.py` |
| `python-multipart` | âš ï¸ Indirect | Required by FastAPI for `UploadFile`/`File`/`Form`; no direct `import multipart` found |
| `aiohttp` | âš ï¸ Unused | Declared but no direct import found |
| `psycopg2-binary` | âš ï¸ Unused | Declared but no direct import found (SQLAlchemy abstracts driver) |

### Unused Declared Dependencies

| Dependency | Action |
|------------|--------|
| `aiohttp` | Remove from `backend/pyproject.toml` |
| `psycopg2-binary` | Keep or remove â€” SQLAlchemy does not require direct psycopg2 import, but PostgreSQL driver is still needed at runtime. Recommended: keep for explicit Postgres support. |

---

## 3. Circular Import Check

| Pattern | Status |
|---------|--------|
| `cognitive/__init__.py` â†’ `adaptive_runtime.py` â†’ `cognitive_kernel.py` â†’ `cognitive/world_model.py` | âœ… Linear chain, not circular |
| `meta_cognition.py` â†’ `adaptive_runtime.py` â†’ `cognitive_kernel.py` | âœ… Linear chain, not circular |
| `core/__init__.py` | âœ… Empty â€” no import side effects |
| Top-level `backend.app.*` imports | âœ… No circular dependencies detected |

**Verdict:** No circular imports detected among top-level module imports.

---

## 4. Package Structure

| Path | Status |
|------|--------|
| `backend/__init__.py` | âœ… Present |
| `backend/app/__init__.py` | âœ… Present |
| `backend/app/core/__init__.py` | âœ… Present |
| `backend/app/api/__init__.py` | âœ… Present |
| `backend/app/agents/__init__.py` | âœ… Present |
| `backend/app/models/__init__.py` | âœ… Present |
| `backend/app/db/__init__.py` | âœ… Present |
| `backend/tests/__init__.py` | âœ… Present |

---

## 5. CI / Makefile / Dockerfile Alignment

| File | Issue | Action |
|------|-------|--------|
| `.github/workflows/ci.yml` | Installed only root `.[dev]` but ran backend tests/mypy | âœ… Fixed â€” added `pip install -e backend/` |
| `Makefile` | Used `poetry install` but backend has no `pyproject.toml` | âœ… Fixed â€” replaced with `pip install -e ".[dev]"` |
| `backend/Dockerfile` | Used `poetry install` with hatchling build backend | âœ… Fixed â€” replaced with `pip install -e ".[dev]"` |
| `docker-compose.yml` | No `build` context for backend service | âš ï¸ Acceptable â€” services run prebuilt images or local dev servers |
| Root `pyproject.toml` | Defined `enal-cognitive-platform` package with no actual code | âœ… Fixed â€” converted to workspace-only metadata |

---

## 6. Cleaned Dependency Graph

```
core
â”œâ”€â”€ fastapi
â”œâ”€â”€ uvicorn[standard]
â”œâ”€â”€ pydantic
â”œâ”€â”€ pydantic-settings
â””â”€â”€ python-multipart

ai
â”œâ”€â”€ litellm
â”œâ”€â”€ langchain-openai
â””â”€â”€ langchain-core

database
â”œâ”€â”€ sqlalchemy
â””â”€â”€ psycopg2-binary

queue
â””â”€â”€ redis

vector
â””â”€â”€ qdrant-client

telemetry
â””â”€â”€ httpx

config
â””â”€â”€ pyyaml

dev
â”œâ”€â”€ pytest
â”œâ”€â”€ pytest-asyncio
â”œâ”€â”€ ruff
â”œâ”€â”€ black
â””â”€â”€ mypy
```

---

## 7. Recommended Actions

1. **Remove `aiohttp` from `backend/pyproject.toml`** â€” no direct usage found.
2. **Re-evaluate `psycopg2-binary`** â€” keep if PostgreSQL direct driver access is planned; otherwise remove to reduce image size.
3. **Run `pip install -e backend/` in all CI jobs that import backend code** â€” already fixed.
4. **Verify Docker build** â€” run `docker build backend` after changes.
5. **Add `python-multipart` direct import verification** â€” ensure FastAPI file upload endpoints are covered by tests.

---

## 8. Next Sprint

Proceed to **Frontend MVP completion** with a stable, audited backend dependency graph.
> Terjemahan Indonesia: Proceed untuk Frontend MVP completion dengan sebuah stable, audited backend dependency graph.
