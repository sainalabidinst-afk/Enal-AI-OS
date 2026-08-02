# Workflow Catalog & Intent Resolver

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk WORKFLOW_CATALOG
<!-- DOCUMENT_METADATA_END -->

## Arsitektur

```
User Intent / Task Name
        |
        ▼
┌──────────────────────────────────────────┐
│            Intent Resolver               │
│  ┌─────────┐  ┌─────────┐  ┌──────────┐  │
│  │ Exact   │  │ Alias   │  │ Tag      │  │
│  │ Match   │─▶│ Match   │─▶│ Fallback   │
│  │(conf1.0)│  │(conf0.9)│  │(conf0.7) │  │
│  └─────────┘  └─────────┘  └──────────┘  │
│                    │                     │
│                    ▼                     │
│         ┌───────────────────┐            │
│         │  WorkflowCatalog  │            │
│         │  (intent→workflow │            │
│         │   mapping)        │            │
│         └───────────────────┘            │
└──────────────────────────────────────────┘
                    │
                    ▼ workflow_id
┌──────────────────────────────────────────┐
│           Workflow Executor                  │
│                    │                         │
│                    ▼                         │
│         ┌───────────────────┐                 │
│         │ CapabilityPipeline│                 │
│         │  (multi-step      │                 │
│         │   orchestration)  │                 │
│         └───────────────────┘                 │
│                    │                         │
│         ┌───────────────────┐                 │
│         │CapabilityExecEngine│               │
│         │  (single step)    │                 │
│         └───────────────────┘                 │
│                    │                         │
│         ┌───────────────────┐                 │
│         │ ExecutionRuntime  │                 │
│         │  (worker pool)    │                 │
│         └───────────────────┘                 │
└──────────────────────────────────────────┘
                    │
                    ▼
            Execution Result
```

## Catalog

### WorkflowCatalogEntry

Setiap workflow dalam catalog memiliki atribut berikut:

| Field | Type | Required | Deskripsi |
|-------|------|----------|-------------|
| `workflow_id` | str | Ya | Pengidentifikasi unik untuk workflow |
| `display_name` | str | Ya | Nama yang dapat dibaca manusia |
| `description` | str | Tidak | Deskripsi workflow |
| `supported_intents` | list[str] | Ya | Daftar identifier intent yang memicu workflow ini |
| `tags` | list[str] | Tidak | Tag untuk kategorisasi dan discovery |
| `category` | str | Tidak | Kategori untuk pengelompokan (misalnya, "network", "code") |
| `metadata` | dict | Tidak | Metadata tambahan (version, author, dll.) |

### Operasi

| Method | Deskripsi |
|--------|-------------|
| `register(entry)` | Mendaftarkan entri workflow (memvalidasi duplikat) |
| `register_from_dict(data)` | Mendaftarkan dari dictionary |
| `register_from_json(json_str)` | Mendaftarkan dari string JSON |
| `register_from_file(filepath)` | Mendaftarkan dari file JSON |
| `unregister(workflow_id)` | Menghapus workflow beserta intent-nya |
| `resolve(intent)` | Menemukan workflow yang cocok dengan intent |
| `resolve_or_raise(intent)` | Resolve atau memunculkan ResolveError |
| `get_entry(workflow_id)` | Mendapatkan entri berdasarkan workflow_id |
| `get_workflow_id(intent)` | Pencarian cepat: intent → workflow_id |
| `find_by_tag(tag)` | Menemukan semua entri dengan tag |
| `list_entries()` | Mendaftar semua entri (ringkasan) |
| `list_intents()` | Mendaftar semua pemetaan intent→workflow |
| `entry_count()` | Jumlah entri yang terdaftar |
| `intent_count()` | Jumlah intent yang terdaftar |
| `clear()` | Menghapus semua entri |

### Validasi

Catalog melakukan validasi saat registrasi:

- `workflow_id` wajib diisi
- Minimal satu `supported_intent`
- **Duplicate workflow**: Terdaftar secara independen (tidak ada duplikasi ID)
- **Duplicate intent**: Intent yang sama tidak boleh menjadi milik workflow berbeda

## Resolver

### IntentResolver

Resolver menggunakan aturan deterministik untuk mencocokkan intent ke workflow:

| Strategy | Precedence | Confidence | Kriteria |
|----------|-----------|------------|----------|
| **Exact Match** | 1 (tertinggi) | 1.0 | Intent ID cocok persis dengan `supported_intents` di catalog |
| **Alias Match** | 2 | 0.9 | Intent cocok dengan alias yang terdaftar |
| **Task Name Exact** | 3 | 1.0 | Task name cocok persis |
| **Task Name Prefix** | 4 | 0.8 | Intent diawali dengan task name yang terdaftar |
| **Tag Fallback** | 5 (terendah) | 0.7 | Intent cocok dengan tag workflow |

### Manajemen Alias

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

### Registrasi Task Name

```python
resolver.register_task_name("run security audit on network", "audit-network")
resolver.register_task_names({
    "generate project documentation": "generate-docs",
})
```

## Response Contract

### ResolveResult (Ditemukan)

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

### ResolveResult (Tidak Ditemukan)

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

Alur end-to-end dari intent ke hasil eksekusi:

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
# resolve_and_execute() menghubungkan seluruh alur:
response = await resolver.resolve_and_execute(
    intent_id="audit-network",
    executor=workflow_executor,
    input_data={"project": "my-project"},
)
```

## Telemetry Events

| Event | Saat | Data |
|-------|------|------|
| `IntentResolved` | Intent berhasil di-resolve | `resolved`, `workflow_id`, `matched_intent`, `confidence`, `reason` |
| `IntentNotFound` | Intent tidak ditemukan | `resolved=false`, `intent_id`, `error` |
| `WorkflowSelected` | Workflow dipilih untuk eksekusi | `workflow_id`, `matched_intent`, `confidence` |
| `WorkflowExecutionStarted` | Eksekusi workflow dimulai | `workflow_id`, `matched_intent`, `has_input_data` |

Event dikirim melalui `EventBus` dari `apps.organization.communication`.

## Contoh Penggunaan

### Basic Setup

```python
from apps.organization.workflow_catalog import (
    WorkflowCatalog, WorkflowCatalogEntry
)
from apps.organization.intent_resolver import IntentResolver

# Buat resolver
resolver = IntentResolver()

# Daftarkan workflow
resolver.get_catalog().register(WorkflowCatalogEntry(
    workflow_id="network-audit-flow",
    display_name="Network Security Audit",
    description="Run security audit",
    supported_intents=["audit-network", "check-security"],
    tags=["network", "security"],
    category="network",
))

# Daftarkan alias
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

# Daftarkan definisi workflow
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

# Resolve dan eksekusi
response = await resolver.resolve_and_execute(
    intent_id="audit",
    executor=executor,
    input_data={"project": "my-infra"},
)

print(response.status)  # ExecutionStatus.COMPLETED
print(response.summarize(response))
```

### Penanganan Error

```python
# Intent tidak dikenal
result = resolver.resolve("nonexistent")
if not result.found:
    print(f"Error: {result.error}")  # "No workflow found for intent: 'nonexistent'"

# resolve_or_raise
try:
    entry = resolver.resolve_or_raise("unknown")
except ResolveError as e:
    print(f"Resolution failed: {e}")
```

## Lokasi File

| File | Deskripsi |
|------|-------------|
| `apps/organization/workflow_catalog.py` | WorkflowCatalog dan ResolveResult |
| `apps/organization/intent_resolver.py` | IntentResolver dengan resolusi alias, task name, tag |
| `tests/test_workflow_catalog.py` | Integration test untuk catalog |
| `tests/test_intent_resolver.py` | Integration test untuk resolver |

