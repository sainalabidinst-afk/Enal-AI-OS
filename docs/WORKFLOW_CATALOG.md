# Katalog Alur Kerja & Penyelesai Niat

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 02-08-2026
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

## Katalog

### Entri Katalog Alur Kerja

Setiap alur kerja dalam katalog memiliki atribut berikut:

|Bidang|Jenis|Diperlukan|Deskripsi|
|-------|------|----------|-------------|
|`workflow_id`|str|Ya|Pengidentifikasi unik untuk alur kerja|
|`display_name`|str|Ya|Nama yang dapat dibaca manusia|
|`description`|str|Tidak|Deskripsi alur kerja|
|`supported_intents`|daftar[str]|Ya|Daftar identifier maksud yang memicu alur kerja ini|
|`tags`|daftar[str]|Tidak|Tag untuk kategorisasi dan penemuan|
|`category`|str|Tidak|Kategori untuk pengelompokan (misalnya, "jaringan", "kode")|
|`metadata`|dikte|Tidak|Metadata tambahan (versi, penulis, dll.)|

### Operasi

|Metode|Deskripsi|
|--------|-------------|
|`register(entry)`|Mendaftarkan alur kerja entri (memvalidasi duplikat)|
|`register_from_dict(data)`|Mendaftarkan dari kamus|
|`register_from_json(json_str)`|Mendaftarkan dari string JSON|
|`register_from_file(filepath)`|Mendaftarkan dari file JSON|
|`unregister(workflow_id)`|Menghapus alur kerja beserta maksud-nya|
|`resolve(intent)`|Menemukan alur kerja yang cocok dengan niat|
|`resolve_or_raise(intent)`|Resolve atau memunculkan ResolveError|
|`get_entry(workflow_id)`|Mendapatkan entri berdasarkan workflow_id|
|`get_workflow_id(intent)`|Pencarian cepat: niat → workflow_id|
|`find_by_tag(tag)`|Menemukan semua entri dengan tag|
|`list_entries()`|Mendaftar semua entri (ringkasan)|
|`list_intents()`|Mendaftar semua maksud peta→alur kerja|
|`entry_count()`|Jumlah entri yang terdaftar|
|`intent_count()`|Jumlah niat yang terdaftar|
|`clear()`|Menghapus semua entri|

### Validasi

Katalog melakukan validasi saat registrasi:

- `workflow_id` wajib diisi
- Minimal satu `supported_intent`
- **Alur kerja duplikat**: Terdaftar secara independen (tidak ada duplikasi ID)
- **Niat duplikat**: Niat yang sama tidak boleh menjadi milik alur kerja yang berbeda

## Penyelesai

### Penyelesai Niat

Resolver menggunakan aturan deterministik untuk mencocokkan maksud ke alur kerja:

|Strategi|Hak lebih tinggi|Kepercayaan diri|Kriteria|
|----------|-----------|------------|----------|
|**Pencocokan Tepat**|1 (tertinggi)|1.0|Intent ID cocok bertahan dengan `supported_intents` di katalog|
|**Pertandingan Alias**|2|0,9|Intent cocok dengan alias yang terdaftar|
|**Nama Tugas Tepat**|3|1.0|Nama tugas cocok bertahan|
|**Awalan Nama Tugas**|4|0,8|Niat diawali dengan nama tugas yang terdaftar|
|**Tag Penggantian**|5 (terendah)|0,7|Intent cocok dengan tag workflow|

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

### Nama Tugas Registrasi

```python
resolver.register_task_name("run security audit on network", "audit-network")
resolver.register_task_names({
    "generate project documentation": "generate-docs",
})
```

## Kontrak Respons

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

## Alur Eksekusi

Alur end-to-end dari niat ke hasil eksekusi:

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

### Pembantu Integrasi

```python
# resolve_and_execute() menghubungkan seluruh alur:
response = await resolver.resolve_and_execute(
    intent_id="audit-network",
    executor=workflow_executor,
    input_data={"project": "my-project"},
)
```

## Peristiwa Telemetri

|Peristiwa|Saat|Data|
|-------|------|------|
|`IntentResolved`|Maksudnya berhasil di-resolve|`resolved`, `workflow_id`, `matched_intent`, `confidence`, `reason`|
|`IntentNotFound`|Niat tidak ditemukan|`resolved=false`, `intent_id`, `error`|
|`WorkflowSelected`|Alur kerja dipilih untuk eksekusi|`workflow_id`, `matched_intent`, `confidence`|
|`WorkflowExecutionStarted`|Alur kerja eksekusi dimulai|`workflow_id`, `matched_intent`, `has_input_data`|

Acara dikirim melalui `EventBus` dari `apps.organization.communication`.

## Contoh Penggunaan

### Pengaturan Dasar

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

### Eksekusi Penuh

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

### Kesalahan Penanganan

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

## File Lokasi

|Mengajukan|Deskripsi|
|------|-------------|
|`apps/organization/workflow_catalog.py`|Katalog Alur Kerja dan ResolveResult|
|`apps/organization/intent_resolver.py`|IntentResolver dengan resolusi alias, nama tugas, tag|
|`tests/test_workflow_catalog.py`|Tes integrasi ke katalog|
|`tests/test_intent_resolver.py`|Tes integrasi untuk penyelesai|
