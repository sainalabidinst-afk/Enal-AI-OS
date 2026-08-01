# Repository Restructure to Enterprise Monorepo — Implementation Steps

## ✅ Step 1: docker-compose.yml
- [x] Change backend build context from `./backend` to `.`
- [x] Set `dockerfile: backend/Dockerfile`

## ✅ Step 2: backend/Dockerfile
- [x] Rewrite to build from repository root
- [x] Preserve monorepo directory layout: `/app/backend`, `/app/apps`, `/app/workspace`, `/app/plugins`
- [x] Set `WORKDIR /app`
- [x] Set `ENV PYTHONPATH=/app`
- [x] Install backend via `pip install -e backend/`
- [x] Keep `CMD ["uvicorn", "backend.app.main:app", ...]`

## ✅ Step 3: backend/.dockerignore
- [x] Update for root-level build context (exclude unnecessary files)

## ✅ Step 4: workspace/__init__.py
- [x] Add `__init__.py` so `workspace` is resolvable as namespace

## ✅ Step 5: plugins/__init__.py
- [x] Add `__init__.py` so `plugins` is resolvable as namespace

## ✅ Step 6: Root .dockerignore
- [x] Create root-level `.dockerignore` (build context is now repo root)

## Validation Steps
- [x] Validate: `python -c "import backend"` PASS
- [x] Validate: `python -c "import backend.app"` PASS
- [x] Validate: `python -c "from backend.app.main import app"` PASS
- [x] Validate: `python -c "import apps"` PASS
- [x] Validate: `python -c "import plugins"` PASS
- [x] Validate: `python -c "import workspace"` PASS
- [x] Validate: `docker compose build` PASS
- [x] Validate: `docker compose up` PASS
- [x] Validate: `docker exec backend ls /app` shows `backend`, `apps`, `workspace`, `plugins`
- [x] Validate: Full test suite — 426 tests passing, 0 failures

