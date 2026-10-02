# ECP Developer Onboarding Guide

## Quick Setup

### Prerequisites

| Tool | Minimum | Recommended |
|------|---------|-------------|
| Python | 3.11 | 3.12 |
| Node.js | 20.x | 22.x |
| Git | 2.40 | Latest |
| Docker | 24.x | Latest |

### Clone & Install

```bash
git clone https://github.com/your-org/Enal-AI-OS.git
cd Enal-AI-OS

# Backend (Python)
cd backend
pip install -e .
pip install -e "../.[dev]"  # or: pip install -e .[dev] from root

# Frontend
cd ../frontend
npm install

# SDK
cd ../sdk
pip install -e .
```

### Run Local Dev

```bash
# Backend API
cd backend && python -m backend.app.main

# Frontend
cd frontend && npm run dev

# Voice services (optional)
cd ../backend && python -m backend.app.services.stt_service
python -m backend.app.services.tts_service
```

## Project Architecture

```
ECP/
├── apps/                        # Capability packs (37 packs)
│   └── <pack_name>/             # Each pack: schemas, engine, worker, __init__
├── backend/                     # Core services
│   ├── app/core/                # Internal services (STT, TTS, observability)
│   ├── app/runtime/             # Public facade (apps → runtime only)
│   ├── app/sdk/                 # Public SDK
│   └── app/contracts/           # API contracts
├── frontend/                    # Next.js 14 UI
├── sdk/                         # Python SDK
├── benchmarks/                  # Benchmark suites (8+ packs)
├── golden_tests/                # Deterministic golden tests
├── real_cases/                  # Real-world evaluation cases
├── docs/                        # ADRs, RFCs, guides
└── .kilo/                       # Commands and agent definitions
```

## Governance Rules

1. **Boundary Rule**: Apps → `backend.app.runtime` only (never `backend.app.core`)
2. **Capability Isolation**: Packs cannot import from other packs
3. **ADR Required**: Core changes (`backend/app/core`, `backend/app/kernel`, `backend/app/runtime`, `backend/app/sdk`, `backend/app/contracts`, `sdk/`) require an approved ADR

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'backend.app.core'` from a pack | Import via `from backend.app.runtime import stt_service` |
| Ruff E501 line too long | Use line continuations, break dicts across lines |
| Circular imports between engine ↔ voice_engine | Use lazy imports (`from backend.app.runtime import stt_service` inside methods) |
| TypeScript path alias not resolving | Ensure `tsconfig.json` has `"@/*": ["./"]` mapping |
| Pre-commit hooks not installed | Run `pre-commit install` after cloning |

## Best Practices

- Each capability pack must include: `schemas.py`, `engine.py` (or `<pack>_engine.py`), `worker.py`, `__init__.py`, benchmark, 10 golden tests, 10 real cases
- Use `StrEnum` for enums, `BaseModel` for schemas
- Follow the `run_all()` → JSON pattern for benchmarks
- Document all public APIs in `docs/guides/<pack>_usage.md`
- Keep benchmark scores at Grade A (>=90%)

## Tools

```bash
# Run all checks
ecp doctor                    # One-command QA (lint, typecheck, test, governance)
python benchmarks/governance_checks.py     # Governance rules
python benchmarks/package_boundaries.py     # Pack isolation
python -m pytest -v                          # Unit tests

# Pre-commit
pre-commit run --all-files

# Devcontainer
# In VS Code: Remote-Containers: Reopen in Container
```

See also:
- [Voice Interaction Usage Guide](voice_interaction_usage.md)
- [ADR Index](../adr/)
- [RFC Index](../rfcs/)
