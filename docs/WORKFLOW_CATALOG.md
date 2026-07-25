# Workflow Catalog & Intent Resolver

## Architecture

```
User Intent / Task Name
        │
        ▼
┌─────────────────────────────────────────────┐
│            Intent Resolver                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────────┐  │
│  │ Exact   │  │ Alias   │  │ Tag         │  │
│  │ Match   │─▶│ Match   │─▶│ Fallback    │  │
│  │(conf1.0)│  │(conf0.9)│  │(conf0.7)    │  │
│  └─────────┘  └─────────┘  └─────────────┘  │
│                    │                         │
│                    ▼                         │
│         ┌──────────────────┐                 │
│         │  WorkflowCatalog │                 │
│         │  (intent→workflow│                 │
│         │   mapping)       │                 │
│         └──────────────────┘                 │
└─────────────────────────────────────────────┘
                    │
                    ▼ workflow_id
┌─────────────────────────────────────────────┐
│           Workflow Executor                  │
│                    │                         │
│                    ▼                         │
│         ┌──────────────────┐                 │
│         │ CapabilityPipeline│                 │
│         │  (multi-step      │                 │
│         │   orchestration)  │                 │
│         └──────────────────┘                 │
│                    │                         │
│         ┌──────────────────┐                 │
│         │CapabilityExecEngine│               │
│         │  (single step)    │                 │
│         └──────────────────┘                 │
│                    │                         │
│         ┌──────────────────┐                 │
│         │ ExecutionRuntime  │                 │
│         │  (worker pool)    │                 │
│         └──────────────────┘                 │
└─────────────────────────────────────────────┘
                    │
                    ▼
            Execution Result
```

## Catalog

### WorkflowCatalogEntry

Setiap workflow dalam catalog memiliki atribut berikut:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `workflow_id` | str | Yes | Unique identifier for the workflow |
| `display_name` | str | Yes | Human-readable name |
| `description` | str | No | Description of the workflow |
| `supported_intents` | list[str] | Yes | List of intent identifiers that trigger this workflow |
| `tags` | list[str] | No | Tags for categorization and discovery |
| `category` | str | No | Category for grouping (e.g., "network", "code") |
| `metadata` | dict | No | Additional metadata (version, author, etc.) |

### Operations

| Method | Description |
|--------|-------------|
| `register(entry)` | Register a workflow entry (validates duplicates) |
| `register_from_dict(data)` | Register from dictionary |
| `register_from_json(json_str)` | Register from JSON string |
| `register_from_file(filepath)` | Register from JSON file |
| `unregister(workflow_id)` | Remove a workflow and its intents |
| `resolve(intent)` | Find workflow matching an intent |
| `resolve_or_raise(intent)` | Resolve or raise ResolveError |
| `get_entry(workflow_id)` | Get entry by workflow_id |
| `get_workflow_id(intent)` | Quick lookup: intent → workflow_id |
| `find_by_tag(tag)` | Find all entries with a tag |
| `list_entries()` | List all entries (summary) |
| `list_intents()` | List all intent→workflow mappings |
| `entry_count()` | Number of registered entries |
| `intent_count()` | Number of registered intents |
| `clear()` | Remove all entries |

### Validation

Catalog melakukan validasi saat registrasi:

- `workflow_id` wajib diisi
- Minimal satu `supported_intent`
- **Duplicate workflow**: Terdaftar secara independen (tidak ada duplikasi ID)
- **Duplicate intent**: Intent yang sama tidak boleh milik workflow berbeda

## Resolver

### IntentResolver

Resolver menggunakan aturan deterministik untuk mencocokkan intent ke workflow:

| Strategy | Precedence | Confidence | Criteria |
|----------|-----------|------------|----------|
| **Exact Match** | 1 (highest) | 1.0 | Intent ID cocok persis dengan `supported_intents` di catalog |
| **Alias Match** | 2 | 0.9 | Intent cocok dengan alias yang terdaftar |
| **Task Name Exact** | 3 | 1.0 | Task name cocok persis |
| **Task Name Prefix** | 4 | 0.8 | Intent diawali dengan task name yang terdaftar |
| **Tag Fallback** | 5 (lowest) | 0.7 | Intent cocok dengan tag workflow |

### Alias Management

```python
resolver.register_alias("audit", "audit-network")
resolver.register_aliases({
    "docs": "generate-docs",
    "review": "review-code",
})
resolver.unregister_alias("audit")
aliases = resolver.get_aliases()
aliases_for_intent = resolver.get_alias_for_intent("audit-network")
```

### Task Name Registration

```python
resolver.register_task_name("run security audit on network", "audit-network")
resolver.register_task_names({
    "generate project documentation": "generate-docs",
})
```

## Response Contract

### ResolveResult (Found)

```json
{
    "found": true,
    "workflow_id": "network-audit-flow",
    "entry": {
        "workflow_id": "network-audit-flow",
        "display_name": "Network Security Audit",
        "description": "Run security audit on network devices",
        "supported_intents": ["audit-network", "check-security", "network-scan"],
        "tags": ["network", "security", "audit"],
        "category": "network",
        "metadata": {"version": "1.0", "domain": "network"}
    },
    "error": null,
    "matched_intent": "audit-network",
    "confidence": 1.0,
    "reason": "Exact match for intent 'audit-network' → workflow 'network-audit-flow'"
}
```

### ResolveResult (Not Found)

```json
{
    "found": false,
    "workflow_id": null,
    "entry": null,
    "error": "No workflow found for intent: 'unknown-intent'",
    "matched_intent": null,
    "confidence": 0.0,
    "reason": "Intent 'unknown-intent' not found via any resolution strategy"
}
```

## Execution Flow

End-to-end flow dari intent ke hasil eksekusi:

```
1. Intent: "audit network security"
       │
2. IntentResolver.resolve("audit-network")
       │ Exact match → confidence 1.0
       ▼
3. ResolveResult(workflow_id="network-audit-flow")
       │
4. IntentResolver._emit_resolved()     → Telemetry: IntentResolved
       │
5. WorkflowExecutor.execute("network-audit-flow")
       │
6. IntentResolver._emit_workflow_selected() → Telemetry: WorkflowSelected
   IntentResolver._emit_execution_started() → Telemetry: WorkflowExecutionStarted
       │
7. CapabilityPipeline.execute(steps)
       │
8. CapabilityExecutionEngine.execute(step)
       │
9. ExecutionRuntime.execute(plan)
       │
10. WorkflowResponse(status="completed", steps=[...])
```

### Integration Helper

```python
# resolve_and_execute() connects the full flow:
response = await resolver.resolve_and_execute(
    intent_id="audit-network",
    executor=workflow_executor,
    input_data={"project": "my-project"},
)
```

## Telemetry Events

| Event | When | Data |
|-------|------|------|
| `IntentResolved` | Intent berhasil di-resolve | `resolved`, `workflow_id`, `matched_intent`, `confidence`, `reason` |
| `IntentNotFound` | Intent tidak ditemukan | `resolved=false`, `intent_id`, `error` |
| `WorkflowSelected` | Workflow dipilih untuk eksekusi | `workflow_id`, `matched_intent`, `confidence` |
| `WorkflowExecutionStarted` | Eksekusi workflow dimulai | `workflow_id`, `matched_intent`, `has_input_data` |

Events dikirim melalui `EventBus` dari `apps.organization.communication`.

## Contoh Penggunaan

### Basic Setup

```python
from apps.organization.workflow_catalog import (
    WorkflowCatalog, WorkflowCatalogEntry
)
from apps.organization.intent_resolver import IntentResolver

# Create resolver
resolver = IntentResolver()

# Register a workflow
resolver.get_catalog().register(WorkflowCatalogEntry(
    workflow_id="network-audit-flow",
    display_name="Network Security Audit",
    description="Run security audit",
    supported_intents=["audit-network", "check-security"],
    tags=["network", "security"],
    category="network",
))

# Register alias
resolver.register_alias("audit", "audit-network")

# Resolve
result = resolver.resolve("audit")
print(result.workflow_id)  # "network-audit-flow"
print(result.confidence)   # 0.9
```

### Full Execution

```python
from apps.organization.workflow_executor import (
    WorkflowExecutor, WorkflowDefinition, WorkflowStep
)
from apps.organization.capability_execution_engine import (
    CapabilityExecutionEngine
)
from apps.organization.capability_pipeline import CapabilityPipeline

# Setup execution stack
engine = CapabilityExecutionEngine()
pipeline = CapabilityPipeline(engine=engine)
executor = WorkflowExecutor(pipeline=pipeline)

# Register workflow definition
executor.register(WorkflowDefinition(
    workflow_id="network-audit-flow",
    name="Network Security Audit",
    ordered_steps=[
        WorkflowStep(
            capability_id="documentation",
            input_data={"skills": ["documentation"]},
            alias="Document",
        ),
    ],
))

# Resolve and execute
response = await resolver.resolve_and_execute(
    intent_id="audit",
    executor=executor,
    input_data={"project": "my-infra"},
)

print(response.status)  # ExecutionStatus.COMPLETED
print(response.summarize(response))
```

### Error Handling

```python
# Unknown intent
result = resolver.resolve("nonexistent")
if not result.found:
    print(f"Error: {result.error}")  # "No workflow found for intent: 'nonexistent'"

# resolve_or_raise
try:
    entry = resolver.resolve_or_raise("unknown")
except ResolveError as e:
    print(f"Resolution failed: {e}")
```

## File Locations

| File | Description |
|------|-------------|
| `apps/organization/workflow_catalog.py` | WorkflowCatalog and ResolveResult |
| `apps/organization/intent_resolver.py` | IntentResolver with alias, task name, tag resolution |
| `tests/test_workflow_catalog.py` | Integration tests for catalog |
| `tests/test_intent_resolver.py` | Integration tests for resolver |

