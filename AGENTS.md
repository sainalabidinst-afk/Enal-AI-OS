# AGENTS.md — Enal Cognitive Platform (ECP)

## Project Overview

ECP is a modular cognitive platform with a stable contract core (RFC-0001) that
all Capability Packs implement. The core lives in `backend/app/core/` and packs
live in `apps/`.

## Test Commands

### Stable Contract Tests (RFC-0001)
```bash
# All stable contract golden tests + unit tests
python -m pytest tests/test_stable_contract_*.py -v

# Golden tests only (10 scenarios)
python -m pytest tests/test_stable_contract_golden.py -v

# Run golden tests standalone (prints JSON results)
python -m tests.test_stable_contract_golden
```

### Full Test Suite
```bash
python -m pytest tests/ -v
```

### Benchmark
```bash
python benchmarks/stable_contract_benchmark.py
# Results saved to benchmarks/reports/stable_contract_benchmark.json
```

## Core Module Layout

```
backend/app/core/
├── schemas.py           # Pydantic schemas (Task/Intent, Event, skills.yaml)
├── base_app.py           # BaseApp abstract contract
├── event_bus.py          # StableEventBus (typed, in-memory, optional Redis)
├── factory_registry.py   # FactoryRegistry (dynamic pack loading)
├── pipeline_engine.py    # PipelineEngine (cognitive pipeline orchestration)
├── skills_registry.py    # SkillsRegistry (skills.yaml parsing/validation)
├── contract_validator.py # ContractValidator (pack compliance + circular imports)
├── version_manager.py    # VersionManager (backward-compatible versioning)
└── observability.py      # StructuredLogger, MetricsCollector, Observability
```

## Coding Standards

- Python 3.11+
- Pydantic v2 for all schemas (use `ConfigDict`, avoid deprecated `class Config`)
- `@abstractmethod` for all BaseApp contract methods
- Snake_case for functions/methods, PascalCase for classes
- All public classes must have docstrings
- No comments in code unless explicitly required

## Quick Start

```python
from backend.app.core.event_bus import StableEventBus
from backend.app.core.pipeline_engine import PipelineEngine, PipelineStage
from backend.app.core.schemas import Event, TaskIntentRequest

# Event Bus
bus = StableEventBus(use_redis=False)
await bus.publish(Event(event_type="test.event", payload={"msg": "hello"}))

# Pipeline
engine = PipelineEngine(bus)
engine.define_pipeline("my_pack", [
    PipelineStage(name="parse", capability="parse"),
    PipelineStage(name="output", capability="output"),
])
```

## Lint/Format

```bash
python -m ruff check .
python -m ruff format .
```
