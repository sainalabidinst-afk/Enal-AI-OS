# Application Development Guide — Enal Cognitive Platform

**Version:** 1.0.0  
**Based on:** `docs/REFERENCE_ARCHITECTURE.md`  
**Status:** 🟢 Active  

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Development Environment Setup](#2-development-environment-setup)
3. [Creating a New Capability Pack](#3-creating-a-new-capability-pack)
4. [Adding Custom Cognitive Logic](#4-adding-custom-cognitive-logic)
5. [Registering API Routes](#5-registering-api-routes)
6. [Using Memory](#6-using-memory)
7. [Publishing and Subscribing to Events](#7-publishing-and-subscribing-to-events)
8. [Testing Your Application](#8-testing-your-application)
9. [Debugging and Observability](#9-debugging-and-observability)
10. [Deployment](#10-deployment)
11. [Checklist: Before Merge](#11-checklist-before-merge)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. Introduction

This guide provides **step-by-step instructions** for developers building applications on the Enal Cognitive Platform (ECP). It covers the entire lifecycle from project setup through deployment.

### Prerequisites

- Python 3.11+
- Redis (for Event Bus, Working Memory, Conversation Memory)
- PostgreSQL (for execution sessions, artifacts metadata)
- Git

### Quick Start

```bash
# Clone repository
git clone https://github.com/enal-ai/enal-ai-os
cd enal-ai-os

# Install backend dependencies
cd backend
pip install -e ".[dev]"
cd ..

# Run tests
pytest -v

# Verify MyPy
mypy apps/ backend/ benchmarks/ tests/
```

---

## 2. Development Environment Setup

### 2.1 Python Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or: .venv\Scripts\activate  # Windows

# Install production + dev dependencies
pip install -e backend/
pip install -r backend/requirements-dev.txt  # if exists

# Or use pyproject.toml dev extras
pip install -e "backend/[dev]"
```

### 2.2 Redis Setup

```bash
# Local Redis (Windows - use WSL or Docker)
docker run -d -p 6379:6379 redis:7-alpine

# Verify
redis-cli ping  # Should return PONG
```

### 2.3 Environment Variables

```bash
# .env file (create in project root)
export REDIS_URL=redis://localhost:6379/0
export DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/enal
export OPENAI_API_KEY=sk-...  # Or other LLM provider key
```

### 2.4 Verify Setup

```python
# test_setup.py
import asyncio
from backend.app.core.event_bus import event_bus
from backend.app.core.memory_layer import memory_manager

async def verify():
    # Test Event Bus
    event = Event(event_type="test", payload={"msg": "hello"})
    msg_id = await event_bus.publish(event)
    print(f"✅ Event Bus: published {msg_id}")
    
    # Test Memory
    await memory_manager.store("working", "test-key", {"data": "test"})
    val = await memory_manager.retrieve("working", "test-key")
    print(f"✅ Memory: stored/retrieved {val}")

asyncio.run(verify())
```

---

## 3. Creating a New Capability Pack

### 3.1 Step-by-Step

#### Step 1: Create the App Module

```bash
mkdir -p apps/my_app
```

#### Step 2: Create `__init__.py` with App Class

```python
# apps/my_app/__init__.py
"""
My App — Domain-specific capability pack for [your domain].
"""
import logging
from typing import Any

from apps.base import BaseApp

logger = logging.getLogger(__name__)


class MyApp(BaseApp):
    """My domain application built on ECP."""
    
    @property
    def capabilities(self) -> list[str]:
        return [
            "my-domain:analyze",
            "my-domain:generate",
            "my-domain:validate",
        ]
    
    @property
    def pipeline(self) -> list[str]:
        return ["perception", "memory", "reasoning", "decision", "reflection"]
    
    async def analyze(self, input_data: str, context: dict | None = None) -> dict[str, Any]:
        """Analyze domain-specific input."""
        from backend.app.core.cognitive_kernel import cognitive_kernel
        
        ctx = {"input": input_data, **(context or {})}
        result = await cognitive_kernel.execute_pipeline(self.pipeline, ctx)
        return result
    
    async def generate(self, specification: dict) -> dict[str, Any]:
        """Generate domain artifact from specification."""
        # Custom implementation
        return {"status": "generated", "artifact": specification}


def get_app() -> BaseApp:
    """Factory function required by apps loader."""
    return MyApp()
```

#### Step 3: Implement Domain Logic

```python
# apps/my_app/analyzer.py
"""Domain-specific analysis logic."""

class MyDomainAnalyzer:
    """Analyzes [domain] inputs and produces structured results."""
    
    def __init__(self):
        self.rules: list[dict] = []
    
    def add_rule(self, name: str, pattern: str, action: str):
        self.rules.append({"name": name, "pattern": pattern, "action": action})
    
    def analyze(self, input_text: str) -> list[dict]:
        """Run analysis rules against input."""
        findings = []
        for rule in self.rules:
            if rule["pattern"] in input_text:
                findings.append({
                    "rule": rule["name"],
                    "action": rule["action"],
                    "location": input_text.find(rule["pattern"]),
                })
        return findings
```

#### Step 4: Create Data Models

```python
# apps/my_app/models.py
from dataclasses import dataclass, field
from typing import Any


@dataclass
class MyDomainInput:
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)
    source: str = "user"


@dataclass
class MyDomainResult:
    status: str
    findings: list[dict] = field(default_factory=list)
    confidence: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
```

#### Step 5: Register Skills

```yaml
# agents/skills.yaml — add your app's skills
skills:
  - id: "my-domain:analyze"
    name: "My Domain Analysis"
    pack: "my_app"
    description: "Analyze [domain] input for patterns and issues"
    pipeline: ["perception", "memory", "reasoning", "decision"]
    examples:
      - "Analyze this [domain] configuration"
      - "Check [domain] input for errors"
```

#### Step 6: Add Orchestration Integration

```python
# In backend/app/core/unified_orchestrator.py
# Extend _extract_skills() method:
def _extract_skills(self, task: str, context: dict) -> list[str]:
    skills = []
    # ... existing skills ...
    
    # Add your domain keywords
    if any(kw in task_lower for kw in ["my-keyword", "my-topic"]):
        skills.extend(["my-domain"])
    
    return skills
```

---

## 4. Adding Custom Cognitive Logic

### 4.1 Extending a Service

```python
# backend/app/core/cognitive/my_service.py
from typing import Any
from backend.app.core.cognitive_kernel import CognitiveService


class MyCustomService(CognitiveService):
    """Custom cognitive service for domain-specific processing."""
    
    async def process(self, context: dict[str, Any]) -> dict[str, Any]:
        input_data = context.get("input", "")
        perception = context.get("perception", {})
        
        # Custom logic
        result = self._process_domain(input_data, perception)
        
        return {"my_result": result}
    
    def _process_domain(self, input_data: str, perception: dict) -> dict:
        # Domain-specific implementation
        return {"processed": True, "entities": []}


# Register in CognitiveKernel.__init__():
# self.services["my_service"] = MyCustomService()
```

### 4.2 Creating a Custom Pipeline

```python
# In your app or orchestrator
from backend.app.core.cognitive_kernel import cognitive_kernel

CUSTOM_PIPELINE = [
    "perception",
    "memory", 
    "my_service",      # Your custom service
    "reasoning",
    "decision",
    "reflection",
]

async def execute_custom(task: str) -> dict:
    return await cognitive_kernel.execute_pipeline(
        CUSTOM_PIPELINE, 
        {"input": task}
    )
```

---

## 5. Registering API Routes

### 5.1 Create Router Module

```python
# backend/app/api/my_app.py
"""API routes for My App."""

from fastapi import APIRouter, HTTPException
from apps.my_app import get_app

router = APIRouter(prefix="/api/v1/my-app", tags=["My App"])


@router.post("/analyze")
async def analyze(input: str, context: dict | None = None):
    """Analyze input using My App."""
    app = get_app()
    try:
        result = await app.analyze(input, context)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health():
    """My App health check."""
    return {"status": "healthy", "app": "my_app"}


@router.post("/generate")
async def generate(spec: dict):
    """Generate artifact from specification."""
    app = get_app()
    result = await app.generate(spec)
    return result
```

### 5.2 Register in Main Router

```python
# backend/app/main.py
from backend.app.api.my_app import router as my_app_router

# Add to FastAPI app
app.include_router(my_app_router)
```

---

## 6. Using Memory

### 6.1 Basic Memory Operations

```python
from backend.app.core.memory_layer import memory_manager

# Store
await memory_manager.store(
    layer="working",
    key="my-key",
    value={"data": "important info"},
    session_id="session-123",
    project_id="proj-456",
)

# Retrieve
value = await memory_manager.retrieve(
    layer="working",
    key="my-key",
    session_id="session-123",
)

# Search
results = await memory_manager.search(
    layer="knowledge",
    query="important",
    limit=5,
)

# Delete
await memory_manager.delete(
    layer="working",
    key="my-key",
)
```

### 6.2 Memory Layer Selection Guide

| Use Case | Layer | TTL | Example |
|---|---|---|---|
| Short-term session state | `working` | 1 hour | Current analysis context |
| Chat history | `conversation` | 24 hours | User conversation |
| Domain knowledge | `knowledge` | ∞ | Vendor rules, patterns |
| Long-term patterns | `longterm` | ∞ | Consolidated learnings |
| Event timeline | `episodic` | ∞ | Task history |
| Conversation context | `session` | 24 hours | Multi-turn context |
| Project data | `project` | ∞ | Project configurations |

### 6.3 Cross-Session Search

```python
# Search across ALL memory layers
all_results = await memory_manager.cross_session_search(
    query="firewall rule",
    session_pattern="session-123",  # Optional filter
)
```

---

## 7. Publishing and Subscribing to Events

### 7.1 Publishing Events

```python
from backend.app.core.event_bus import event_bus
from backend.app.core.events import Event

async def report_progress(task_id: str, progress: float):
    await event_bus.publish(Event(
        event_type="my_app:progress",
        payload={
            "task_id": task_id,
            "progress": progress,
            "timestamp": datetime.utcnow().isoformat(),
        },
        source="my_app",
        target="*",
        correlation_id=task_id,
    ))
```

### 7.2 Subscribing to Events

```python
from backend.app.core.event_bus import event_bus
from backend.app.core.events import Event

async def handle_completion(event: Event):
    """Handle task completion events."""
    task_id = event.payload.get("task_id")
    result = event.payload.get("result")
    print(f"Task {task_id} completed: {result}")

# Subscribe at startup
event_bus.subscribe("task.completed", handle_completion)
```

### 7.3 Custom Event Types

```python
# Define your event types as constants
class MyAppEvents:
    ANALYSIS_STARTED = "my_app:analysis:started"
    ANALYSIS_COMPLETED = "my_app:analysis:completed"
    ANALYSIS_FAILED = "my_app:analysis:failed"
    PROGRESS_UPDATE = "my_app:progress"
```

---

## 8. Testing Your Application

### 8.1 Unit Test Template

```python
# tests/test_my_app.py
"""
Tests for My App capability pack.
"""
import pytest
from unittest.mock import AsyncMock, patch

from apps.my_app import get_app, MyApp


@pytest.fixture
def app():
    """Create app instance for testing."""
    return get_app()


@pytest.mark.asyncio
async def test_app_creation(app):
    """Verify app can be instantiated."""
    assert app is not None
    assert "my-domain:analyze" in app.capabilities


@pytest.mark.asyncio
async def test_analyze_basic(app):
    """Test basic analysis functionality."""
    result = await app.analyze("test input")
    assert result is not None
    assert "perception_result" in result


@pytest.mark.asyncio
async def test_generate(app):
    """Test generation functionality."""
    spec = {"type": "config", "params": {"key": "value"}}
    result = await app.generate(spec)
    assert result["status"] == "generated"


@pytest.mark.asyncio
@patch("backend.app.core.cognitive_kernel.cognitive_kernel.execute_pipeline")
async def test_analyze_with_mock(mock_pipeline, app):
    """Test with mocked cognitive kernel."""
    mock_pipeline.return_value = {"mock": "result"}
    
    result = await app.analyze("test")
    assert result["mock"] == "result"
    mock_pipeline.assert_called_once()
```

### 8.2 Integration Test Template

```python
# tests/test_my_app_integration.py
"""
Integration tests for My App (requires Redis).
"""

import pytest
from backend.app.core.event_bus import event_bus
from backend.app.core.events import Event
from backend.app.core.memory_layer import memory_manager


@pytest.mark.asyncio
@pytest.mark.integration
async def test_event_publish_subscribe():
    """Test event system integration."""
    received = []
    
    async def handler(event: Event):
        received.append(event)
    
    event_bus.subscribe("test:event", handler)
    await event_bus.publish(Event(
        event_type="test:event",
        payload={"msg": "hello"},
        source="test",
    ))
    
    assert len(received) == 1
    assert received[0].payload["msg"] == "hello"


@pytest.mark.asyncio
@pytest.mark.integration
async def test_memory_store_retrieve():
    """Test memory system integration."""
    test_key = "test-key-123"
    test_value = {"data": "test-value"}
    
    await memory_manager.store("working", test_key, test_value)
    retrieved = await memory_manager.retrieve("working", test_key)
    
    assert retrieved == test_value
    
    # Cleanup
    await memory_manager.delete("working", test_key)
```

---

## 9. Debugging and Observability

### 9.1 Logging

```python
import logging

logger = logging.getLogger(__name__)

# In your app code
logger.info("Analysis started", extra={"task_id": task_id, "input_length": len(input_data)})
logger.warning("Rule matched with low confidence", extra={"rule": rule_name, "confidence": 0.3})
logger.error("Analysis failed", exc_info=True)
```

### 9.2 Recording Execution Events

```python
from backend.app.core.observability import record_execution_event

await record_execution_event(
    event_type="analysis",
    status="completed",
    duration_ms=1500,
    metadata={
        "app": "my_app",
        "input_size": len(input_data),
        "findings_count": len(findings),
    },
)
```

### 9.3 Debugging Pipeline Execution

```python
from backend.app.core.cognitive_kernel import cognitive_kernel
import json

# Enable verbose debugging
cognitive_kernel._debug = True

# Execute with step-by-step logging
result = await cognitive_kernel.execute_pipeline(
    ["perception", "memory", "decision"],
    {"input": "test"},
)

# Inspect each stage
for stage in ["perception_result", "memory_result", "decision_result"]:
    if stage in result:
        print(f"{stage}: {json.dumps(result[stage], indent=2)}")
```

---

## 10. Deployment

### 10.1 Docker Deployment

```dockerfile
# Dockerfile for your app
FROM python:3.11-slim

WORKDIR /app

COPY backend/ /app/backend/
COPY apps/ /app/apps/
COPY pyproject.toml /app/

RUN pip install -e /app/backend/

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 10.2 Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379/0
      - DATABASE_URL=postgresql+asyncpg://enal:enal@db:5432/enal
    depends_on:
      - redis
      - db

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: enal
      POSTGRES_PASSWORD: enal
      POSTGRES_DB: enal
    ports:
      - "5432:5432"
```

### 10.3 Production Checklist

- [ ] Redis configured with persistence and replication
- [ ] PostgreSQL configured with connection pooling
- [ ] API keys/secrets in environment variables or secret manager
- [ ] CORS configured for frontend domains
- [ ] Rate limiting enabled
- [ ] Health check endpoints configured
- [ ] Logging to centralized destination (ELK, CloudWatch)
- [ ] Prometheus metrics exported
- [ ] TLS/SSL configured
- [ ] Backup strategy for memory persistence files

---

## 11. Checklist: Before Merge

### Code Quality

- [ ] `mypy apps/ backend/` — 0 errors
- [ ] `ruff check apps/ backend/` — 0 blockers
- [ ] No circular imports (`ruff check --select RUF011`)
- [ ] No new mutable defaults (`ruff check --select RUF012`)
- [ ] No `except Exception:` without justification

### Testing

- [ ] `pytest -v` — ≥95% pass
- [ ] New code has corresponding tests
- [ ] Integration tests pass (if applicable)

### Documentation

- [ ] Docstrings on all public functions/classes
- [ ] Capability Pack registered in `agents/skills.yaml`
- [ ] ADR filed if architectural change
- [ ] CHANGELOG.md updated

### Integration

- [ ] `python -c "from apps.my_app import get_app; app = get_app()"` — no import errors
- [ ] `python -c "from backend.app.api.my_app import router"` — no import errors
- [ ] `git checkout` in clean repo and verify

---

## 12. Troubleshooting

### 12.1 Common Issues

| Problem | Likely Cause | Solution |
|---|---|---|
| `ModuleNotFoundError` | Missing dependency | `pip install -e backend/` |
| `Redis connection error` | Redis not running | `docker start <redis-container>` |
| `Circular import` | Core module imports app | Move import inside function (lazy) |
| `MyPy errors` | Missing type hints | Add type annotations to all functions |
| `Tests failing` | Async test without `@pytest.mark.asyncio` | Add decorator |
| `Event not received` | Subscriber not registered | Check subscribe at module level or startup |
| `Memory not persisted` | Layer not flushed | Use `store()` for writes, not direct file access |

### 12.2 Debugging Commands

```bash
# Check import order
python -X importtime -c "from backend.app.main import app" 2>&1 | head -20

# Trace event flow
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from backend.app.core.event_bus import event_bus
"

# Test LLM connectivity
python -c "
from backend.app.core.model_router import model_router
response = model_router.complete(
    [{'role': 'user', 'content': 'Say hello'}],
    temperature=0
)
print(response.choices[0].message.content)
"
```

### 12.3 Getting Help

1. Check **AES Architecture** (`docs/AES_ARCHITECTURE.md`) — how the platform is built
2. Check **Reference Architecture** (`docs/REFERENCE_ARCHITECTURE.md`) — patterns and decisions
3. Check **ADR** (`docs/adr/`) — why architectural decisions were made
4. Check **Quality Gates** (`docs/quality/QUALITY_GATES.md`) — what's required for merge
5. Check **Existing Capability Packs** — learn from working examples in `apps/`

---

## Document Version History

| Version | Date | Changes |
|---|---|---|
| 1.0.0 | 2024 | Initial Application Development Guide |

---

*End of Application Development Guide*

