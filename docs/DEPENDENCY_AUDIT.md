# Dependency Audit Report

**Date:** 2026-07-18
**Scope:** Backend packaging + dependency consistency + CI/Makefile/Dockerfile alignment

---

## 1. Backend Packaging

| Item | Status |
|------|--------|
| `backend/pyproject.toml` | ✅ Created |
| `backend/__init__.py` | ✅ Created |
| Build backend | hatchling |
| Dev dependencies | pytest, pytest-asyncio, ruff, black, mypy |
| Runtime dependencies | fastapi, uvicorn, sqlalchemy, qdrant-client, redis, pydantic, pydantic-settings, litellm, langchain-openai, langchain-core, httpx, pyyaml, aiohttp, python-multipart, psycopg2-binary |

---

## 2. Module Usage vs Declaration

| Module | Status | Action |
|--------|--------|--------|
| `fastapi` | ✅ OK | Used in `main.py`, `api/*` |
| `uvicorn` | ✅ OK | Used in Dockerfile, Makefile |
| `sqlalchemy` | ✅ OK | Used in `db/session.py` |
| `qdrant-client` | ✅ OK | Used in `core/vector_store.py` |
| `redis` | ✅ OK | Used in `core/memory.py`, `core/memory_layer.py`, `core/event_bus.py` |
| `pydantic` | ✅ OK | Used in `models/schemas.py` |
| `pydantic-settings` | ✅ OK | Used in `core/config.py` |
| `litellm` | ✅ OK | Used in `core/model_router.py` |
| `langchain-openai` | ✅ OK | Used in `agents/core/executor_agent.py` |
| `langchain-core` | ✅ OK | Used in `agents/core/*` |
| `httpx` | ✅ OK | Used in `core/benchmark/runner.py` |
| `pyyaml` | ✅ OK | Used in `core/skill_registry.py` |
| `python-multipart` | ⚠️ Indirect | Required by FastAPI for `UploadFile`/`File`/`Form`; no direct `import multipart` found |
| `aiohttp` | ⚠️ Unused | Declared but no direct import found |
| `psycopg2-binary` | ⚠️ Unused | Declared but no direct import found (SQLAlchemy abstracts driver) |

### Unused Declared Dependencies

| Dependency | Action |
|------------|--------|
| `aiohttp` | Remove from `backend/pyproject.toml` |
| `psycopg2-binary` | Keep or remove — SQLAlchemy does not require direct psycopg2 import, but PostgreSQL driver is still needed at runtime. Recommended: keep for explicit Postgres support. |

---

## 3. Circular Import Check

| Pattern | Status |
|---------|--------|
| `cognitive/__init__.py` → `adaptive_runtime.py` → `cognitive_kernel.py` → `cognitive/world_model.py` | ✅ Linear chain, not circular |
| `meta_cognition.py` → `adaptive_runtime.py` → `cognitive_kernel.py` | ✅ Linear chain, not circular |
| `core/__init__.py` | ✅ Empty — no import side effects |
| Top-level `backend.app.*` imports | ✅ No circular dependencies detected |

**Verdict:** No circular imports detected among top-level module imports.

---

## 4. Package Structure

| Path | Status |
|------|--------|
| `backend/__init__.py` | ✅ Present |
| `backend/app/__init__.py` | ✅ Present |
| `backend/app/core/__init__.py` | ✅ Present |
| `backend/app/api/__init__.py` | ✅ Present |
| `backend/app/agents/__init__.py` | ✅ Present |
| `backend/app/models/__init__.py` | ✅ Present |
| `backend/app/db/__init__.py` | ✅ Present |
| `backend/tests/__init__.py` | ✅ Present |

---

## 5. CI / Makefile / Dockerfile Alignment

| File | Issue | Action |
|------|-------|--------|
| `.github/workflows/ci.yml` | Installed only root `.[dev]` but ran backend tests/mypy | ✅ Fixed — added `pip install -e backend/` |
| `Makefile` | Used `poetry install` but backend has no `pyproject.toml` | ✅ Fixed — replaced with `pip install -e ".[dev]"` |
| `backend/Dockerfile` | Used `poetry install` with hatchling build backend | ✅ Fixed — replaced with `pip install -e ".[dev]"` |
| `docker-compose.yml` | No `build` context for backend service | ⚠️ Acceptable — services run prebuilt images or local dev servers |
| Root `pyproject.toml` | Defined `enal-cognitive-platform` package with no actual code | ✅ Fixed — converted to workspace-only metadata |

---

## 6. Cleaned Dependency Graph

```
core
├── fastapi
├── uvicorn[standard]
├── pydantic
├── pydantic-settings
└── python-multipart

ai
├── litellm
├── langchain-openai
└── langchain-core

database
├── sqlalchemy
└── psycopg2-binary

queue
└── redis

vector
└── qdrant-client

telemetry
└── httpx

config
└── pyyaml

dev
├── pytest
├── pytest-asyncio
├── ruff
├── black
└── mypy
```

---

## 7. Recommended Actions

1. **Remove `aiohttp` from `backend/pyproject.toml`** — no direct usage found.
2. **Re-evaluate `psycopg2-binary`** — keep if PostgreSQL direct driver access is planned; otherwise remove to reduce image size.
3. **Run `pip install -e backend/` in all CI jobs that import backend code** — already fixed.
4. **Verify Docker build** — run `docker build backend` after changes.
5. **Add `python-multipart` direct import verification** — ensure FastAPI file upload endpoints are covered by tests.

---

## 8. Next Sprint

Proceed to **Frontend MVP completion** with a stable, audited backend dependency graph.
