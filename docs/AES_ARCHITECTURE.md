# AES — Spesifikasi Teknik Arsitektur


**Versi Dokumen:** 1.0.0
**Tag Dasar:** `v1.0.0-engineering-baseline`
**Klasifikasi:** Internal — Referensi Teknik

---

## Daftar isi

1. [System Overview](#1-system-overview)
2. [Layer Architecture](#2-layer-architecture)
3. [Module Dependency Graph](#3-module-dependency-graph)
4. [Runtime Flow](#4-runtime-flow)
5. [Event Flow](#5-event-flow)
6. [Public API Contracts](#6-public-api-contracts)
7. [Memory Architecture](#7-memory-architecture)
8. [Cognitive Pipeline](#8-cognitive-pipeline)
9. [Capability Pack Architecture](#9-capability-pack-architecture)
10. [Quality Gates](#10-quality-gates)
11. [Testing Strategy](#11-testing-strategy)
12. [Coding Standards](#12-coding-standards)

---

## 1. Sistem Ikhtisar

ECP (Enal Cognitive Platform) adalah sistem operasi kognitif multi-agen yang mengatur paket kemampuan khusus domain melalui saluran kognitif terpadu. Arsitekturnya mengikuti desain berlapis yang digerakkan oleh peristiwa dengan aturan ketergantungan yang ketat.

### Prinsip Arsitektur


- **Isolasi berlapis:** Setiap lapisan hanya berkomunikasi dengan lapisan yang terdekat
- **Berbasis peristiwa:**Komunikasi modul lintas melalui Bus Peristiwa
- **Eksekusi alur:** Layanan kognitif dijalankan dalam alur berurutan yang ditentukan oleh kompleksitas tugas
- **Plugin-first:** Paket kemampuan perluasan fungsionalitas tanpa mengubah inti
- **Hierarki memori:** 7 lapisan memori dengan konsolidasi otomatis

### Diagram Arsitektur Tingkat Tinggi


```
┌──────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│  (REST API / WebSocket / CLI)                                    │
└────────────────────────────┬─────────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                     API LAYER (FastAPI)                          │
│  backend/app/api/ — 15 route modules                             │
│  - chat, execution, workspace, artifact, telemetry,              │
│    benchmark, model_gateway, capability_discovery, etc.          │
└────────────────────────────┬─────────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                  ORCHESTRATION LAYER                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│  │  AIOrchestrator  │  │ UnifiedOrch.     │  │ AdaptiveRuntime│ │
│  │(orchestrator_v2) │  │(unified_orch.)   │  │(adaptive_rt.)  │ │
│  └────────┬─────────┘  └────────┬─────────┘  └───────┬────────┘ │
└───────────┼──────────────────────┼──────────────────────┼────────┘
            │                      │                      │
┌───────────▼──────────────────────▼──────────────────────▼────────┐
│                   COGNITIVE KERNEL                               │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────────┐   │
│  │Perception│  Memory  │Reasoning │ Planning │   Decision    │   │
│  └──────────┴──────────┴──────────┴──────────┴──────────────┘   │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────────┐   │
│  │  Action  │Reflection│ Learning │  Debate  │  Simulation  │   │
│  └──────────┴──────────┴──────────┴──────────┴──────────────┘   │
└────────────────────────────┬─────────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                      RUNTIME LAYER                               │
│  ┌──────────────┬─────────────────┬──────────────────────────┐  │
│  │  Event Bus   │   Task Queue     │  Execution Integration  │  │
│  │ (Redis Pub/  │ (in-memory async)│  (scheduler + progress) │  │
│  │  Sub+Streams)│                  │                          │  │
│  └──────────────┴─────────────────┴──────────────────────────┘  │
│  ┌──────────────┬─────────────────┬──────────────────────────┐  │
│  │Model Router  │  Cost Optimizer │   State Recovery         │  │
│  │(LLM routing) │  (budget-aware) │   (checkpoint/restore)   │  │
│  └──────────────┴─────────────────┴──────────────────────────┘  │
└────────────────────────────┬─────────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                          │
│  ┌──────────┬──────────┬──────────┬──────────┬────────────────┐ │
│  │  Redis   │PostgreSQL│  Qdrant  │ File Sys │  External LLM  │ │
│  │(cache/   │(metadata)│(vectors) │(memory)  │  (LiteLLM)     │ │
│  │ events)  │          │          │          │                │ │
│  └──────────┴──────────┴──────────┴──────────┴────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Arsitektur Lapisan

### 2.1 API Lapisan — `backend/app/api/`


**Tujuan:** antarmuka HTTP/REST untuk konsumen eksternal. Tidak ada logika bisnis.

|Modul|Titik akhir|Penulis|
|--------|-----------|------|
|`chat.py`|`POST /chat`, WebSocket `/ws/chat`|Sesi token|
|`execution.py`|`POST /execute`, `GET /execute/{id}`, kemajuan WebSocket|Kunci API|
|`workspace.py`|MENTAH `/workspaces`|Kunci API|
|`artifact.py`|MENTAH `/artifacts`|Kunci API|
|`telemetry.py`|`GET /telemetry/metrics`, `GET /telemetry/traces`|Magang|
|`health.py`|`GET /health`|Tidak ada|
|`model_gateway.py`|`GET /models`, `POST /models/{id}/test`|Kunci API|
|`capability_discovery.py`|`GET /capabilities`|Kunci API|
|`benchmark.py`|`POST /benchmark/run`, `GET /benchmark/results`|Magang|
|`notifications.py`|WebSocket `/ws/notifications`|Sesi token|
|`orchestrator_v2.py`|`POST /orchestrate`|Kunci API|
|`attachments.py`|`POST /attachments/upload`|Kunci API|

### 2.2 Orkestrasi Lapisan


Ada tiga orkestrator dengan tanggung jawab yang berbeda:

|orkestra|Mengajukan|Tanggung jawab|
|---|---|---|
|**AIOrchestrator**|`agents/orchestrator_v2.py`|Tingkat atas: tujuan → persepsi → rencana → pelaksanaan. Titik masuk tunggal bagi konsumen eksternal|
|**Orkestrator Terpadu**|`core/unified_orchestrator.py`|Multi-mode: LANGSUNG, KOGNITIF, MULTI_AGENT, ALUR KERJA. Terbentuknya tim yang dinamis|
|**Waktu Proses Kognitif Adaptif**|`core/adaptive_runtime.py`|Berbasis saluran: memilih saluran kognitif berdasarkan kompleksitas tugas|

**Urutan resolusi:** AIOrchestrator → UnifiedOrchestrator → AdaptiveCognitiveRuntime → CognitiveKernel

### 2.3 Kernel Kognitif — `backend/app/core/cognitive_kernel.py`


8 layanan kognitif yang dijalankan dalam saluran yang dipesan:

|Melayani|Kelas|Tanggung jawab|
|---|---|---|
|Persepsi|`PerceptionService`|Pemrosesan masukan, esensi/niat, pengambilan memori|
|Ingatan|`MemoryService`|Pencarian memori yang relevan lintas lapisan|
|Pemikiran|`ReasoningService`|Pembuatan hipotesis, rantai penalaran, logika keputusan|
|Perencanaan|`PlanningService`|Pembuatan peta jalan strategis|
|Keputusan|`DecisionService`|Evaluasi dan seleksi multi-opsi|
|Tindakan|`ActionService`|Perumusan rencana aksi|
|Cerminan|`ReflectionService`|Tinjauan mandiri atas keputusan dan keluaran|
|Sedang belajar|`LearningService`|Penilaian kualitas, evaluasi sinyal|

### 2.4 Lapisan Runtime

|Komponen|Mengajukan|Teknologi|
|---|---|---|
|Acara Bus|`core/event_bus.py`|Redis Streams + pelanggan dalam memori|
|Antrian Tugas|`core/task_queue.py`|Antrian asyncio dalam memori|
|Integrasi Eksekusi|`core/execution_integration.py`|Penjadwalan khusus + kemajuan|
|Model Perute|`core/model_router.py`|Perutean berbasis LiteLLM|
|Pengoptimalan Biaya|`core/cost_optimizer.py`|Estimasi anggaran token|
|Pemulihan Negara|`core/state_recovery.py`|Pos pemeriksaan/pemulihan|

### 2.5 Lapisan Infrastruktur


|Komponen|Tujuan|Pola Akses|
|---|---|---|
|ulang|Aliran Bus Acara, cache, memori kerja|`redis.asyncio`|
|PostgreSQL|Sesi eksekusi, metadata artefak|SQLAlchemy asinkron|
|Qdrant|Pencarian vektor untuk memori pengetahuan|`qdrant-client`|
|Berkas Sistem|Kegigihan memori (pengetahuan, jangka panjang, episodik, sesi, proyek)|File JSON di `workspace/memory/`|
|Penyedia LLM|OpenAI, Antropik, Ollama, dll.|antarmuka terpadu LiteLLM|

---

## 3. Modul Grafik Ketergantungan


### 3.1 Aturan Ketergantungan (Diberlakukan)


```
apps/ ──────────► backend/app/core/ ──────────► infrastructure
   │                      │
   └──► backend/app/api/  └──► backend/app/agents/
```

**Peraturan ketat:**

1. `apps/*` → `backend.app.core.*` : Diizinkan (melalui impor)
2. `backend.app.api.*` → `backend.app.core.*` : Diizinkan
3. `backend.app.agents.*` → `backend.app.core.*` : Diizinkan
4. `backend.app.core.*` → `apps.*` : **DILARANG**
5. `backend.app.core.*` → `backend.app.api.*` : **DILARANG**
6. `apps/network_engineer` → `apps/code_engineer` : **DILARANG** (lintas kemampuan)
7. Semua komunikasi lintas modul: harus menggunakan Event Bus

### 3.2 Peta Ketergantungan Aktual


```
main.py
  ├── api/chat.py ────────────► core/cognitive_kernel.py
  │                              ├── core/memory_layer.py
  │                              ├── core/decision_engine.py
  │                              ├── core/cognitive/reasoning_engine.py
  │                              ├── core/cognitive/strategic_planner.py
  │                              ├── core/cognitive/world_model.py
  │                              ├── core/reflection.py
  │                              └── core/model_router.py
  ├── api/execution.py ───────► core/execution_integration.py
  │                              ├── core/execution_session.py
  │                              ├── core/artifact_service.py
  │                              ├── core/workspace_service.py
  │                              └── core/notification_service.py
  ├── api/workspace.py ───────► core/workspace_service.py
  ├── api/artifact.py ────────► core/artifact_service.py
  ├── agents/orchestrator_v2.py
  │    ├── core/perception_engine.py
  │    └── apps/organization/ai_planner.py
  ├── core/unified_orchestrator.py
  │    ├── core/cognitive_kernel.py
  │    ├── core/adaptive_runtime.py
  │    ├── core/organization.py
  │    ├── apps/organization/ai_planner.py
  │    └── apps/organization/multi_agent.py
  └── core/adaptive_runtime.py
       ├── core/cognitive_kernel.py
       ├── core/cognitive_budget.py
       ├── core/cost_optimizer.py
       └── core/model_router.py
```

### 3.3 Pola Singleton Malas


Untuk mencegah impor melingkar pada waktu buka modul, komponen inti menggunakan singleton yang malas:

```python
# Pattern used in: unified_orchestrator.py, event_bus.py
_unified_orchestrator = None

def get_unified_orchestrator() -> UnifiedOrchestrator:
    global _unified_orchestrator
    if _unified_orchestrator is None:
        _unified_orchestrator = UnifiedOrchestrator()
    return _unified_orchestrator
```

Komponen yang menggunakan pola ini:
- `UnifiedOrchestrator` (malas)
- `EventBus` (contoh tingkat modul)
- `CognitiveKernel` (tingkat modul `cognitive_kernel`)
- `MemoryManager` (tingkat modul `memory_manager`)
- `AdaptiveCognitiveRuntime` (tingkat modul `adaptive_runtime`)

---

## 4. Runtime Aliran

### 4.1 Siklus Hidup Pemulihan


```
1. HTTP Request ──► FastAPI Router
                         │
2.                      │
                  ┌──────▼──────┐
                  │ Parse input │  ← chat.py / execution.py
                  │ Validate    │
                  └──────┬──────┘
                         │
3.                      │
                  ┌──────▼──────────┐
                  │ Orchestration   │  ← AIOrchestrator
                  │ (goal → plan)   │     or UnifiedOrchestrator
                  └──────┬──────────┘
                         │
4.                      │
                  ┌──────▼────────────┐
                  │ Pipeline Selection│  ← AdaptiveCognitiveRuntime
                  │ (complexity-based)│     budget.estimate(task)
                  └──────┬────────────┘
                         │
5.                      │
                  ┌──────▼────────────┐
                  │ Cognitive Pipeline│  ← CognitiveKernel
                  │ 8 services in     │     execute_pipeline()
                  │ ordered sequence  │
                  └──────┬────────────┘
                         │
6.                      │
                  ┌──────▼────────────┐
                  │ Result Aggregation│
                  │ + Artifact         │  ← artifact_service
                  │ + Notification     │  ← notification_service
                  └──────┬────────────┘
                         │
7. HTTP Response ◄────────┘
```

### 4.2 Logika Pemilihan Saluran Pipa


```python
PIPELINE_PRESETS = {
    TRIVIAL:    ["perception", "memory", "decision", "action"],
    SIMPLE:     ["perception", "memory", "reasoning", "decision", "action"],
    MEDIUM:     ["perception", "memory", "planning", "reasoning",
                 "decision", "reflection", "action"],
    COMPLEX:    ["perception", "memory", "planning", "reasoning",
                 "debate", "simulation", "decision", "verification",
                 "reflection", "learning"],
    VERY_COMPLEX: ["perception", "memory", "planning", "reasoning",
                   "debate", "simulation", "decision", "verification",
                   "reflection", "learning"],
}
```

Setiap layanan saluran pipa menggunakan keluaran layanan sebelumnya (`context`) dan menghasilkan keluaran yang diperkaya. Rantainya adalah:

```
context = {"input": user_input}
→ perception (adds entities, intents, memories)
→ memory     (adds relevant_memories)
→ reasoning  (adds hypotheses, chain, decision)
→ planning   (adds roadmap)
→ decision   (adds selected_option, confidence)
→ action     (adds action plan)
→ reflection (adds review, score)
→ learning   (adds quality_score, suggestions)
```

### 4.3 Alur Sesi Eksekusi


```
POST /execute ──► ExecutionIntegration.execute()
                     │
               ┌─────▼─────┐
               │ Create     │  ← execution_session_manager
               │ Session    │
               └─────┬─────┘
                     │
               ┌─────▼─────┐
               │ Build      │  ← ExecutionGraph (DAG of tasks)
               │ Graph      │     understand → plan → execute → verify
               └─────┬─────┘
                     │
               ┌─────▼─────┐
               │ Submit     │  ← ExecutionScheduler
               │ Queue      │
               └─────┬─────┘
                     │
               ┌─────▼──────────┐
               │ × N tasks      │
               │  Each: run →   │
               │  complete/fail │
               └─────┬──────────┘
                     │
               ┌─────▼──────┐
               │ Create      │  ← artifact_service
               │ Artifact    │
               └─────┬──────┘
                     │
               ┌─────▼────────┐
               │ Notify       │  ← WebSocket / notification
               │ Complete     │
               └─────┬────────┘
                     │
               Return ExecutionSession ◄──
```

---

## 5. Alur Peristiwa

### 5.1 Arsitektur Sistem Acara


```
┌─────────────────────────────────────────────┐
│                 EventBus                      │
│  ┌──────────────────────────────────────┐   │
│  │         Redis Streams                 │   │
│  │  enal:events:task.created            │   │
│  │  enal:events:execution.progress      │   │
│  │  enal:events:memory.consolidated     │   │
│  │  enal:events:notification.sent       │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │      In-Memory Subscribers            │   │
│  │  {event_type: [handler_fn, ...]}     │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### 5.2 Model Data Peristiwa

```python
@dataclass
class Event:
    event_type: str           # e.g., "task.completed"
    payload: dict[str, Any]   # Event-specific data
    source: str               # Publisher component
    target: str = "*"         # Subscriber filter
    timestamp: datetime       # UTC
    correlation_id: str | None = None  # Trace ID
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class EventEnvelope:
    event: Event
    stream: str               # Redis stream name
    id: str | None = None     # Unique envelope ID
```

### 5.3 Jenis Peristiwa yang Diketahui


|Jenis Acara|Penerbit|Konsumen|Muatan|
|---|---|---|---|
|`task.created`|Penjadwalan Eksekusi|Layanan Pemberitahuan, Telemetri|`{task_id, name, session_id}`|
|`task.completed`|Penjadwalan Eksekusi|Layanan Pemberitahuan, Layanan Artefak|`{task_id, result}`|
|`task.failed`|Penjadwalan Eksekusi|Layanan Pemberitahuan, Pemulihan Negara|`{task_id, error}`|
|`memory.consolidated`|Manajer Memori|Layanan Pembelajaran|`{block_id, source_layer, summary}`|
|`execution.progress`|Integrasi Eksekusi|klien WebSocket|`{session_id, progress, status}`|
|`notification.sent`|Layanan Pemberitahuan|Telemetri|`{recipient, channel, message}`|

### 5.4 Pola Publikasi-Berlangganan


```python
# Publishing
await event_bus.publish(Event(
    event_type="task.completed",
    payload={"task_id": "task-1", "result": {...}},
    source="execution_scheduler",
    correlation_id=session.correlation_id,
))

# Subscribing
event_bus.subscribe("task.completed", my_handler)
```

---

## 6. Kontrak API Publik


### 6.1 REST API Titik Akhir


|Metode|Jalur|Memminta|Tanggapan|Status|
|---|---|---|---|---|
|`POST`|`/chat`|`{message, session_id, project_id?}`|`{reply, session_id, artifacts[]}`|✅ Stabil|
|`POST`|`/execute`|`{goal, workspace_id, conversation_id?}`|`{session_id, status}`|✅ Stabil|
|`GET`|`/execute/{id}`| — |`ExecutionSession`|✅ Stabil|
|`GET`|`/execute/{id}/stream`|Web Soket|Peristiwa Statistik (SSE)|✅ Stabil|
|`POST`|`/workspaces`|`{name, description?}`|`Workspace`|✅ Stabil|
|`GET`|`/workspaces`| — |`Workspace[]`|✅ Stabil|
|`GET`|`/workspaces/{id}`| — |`Workspace`|✅ Stabil|
|`POST`|`/artifacts`|`{workspace_id, name, type, content}`|`Artifact`|✅ Stabil|
|`GET`|`/artifacts/{id}`| — |`Artifact`|✅ Stabil|
|`GET`|`/capabilities`|`?query=`|`Capability[]`|✅ Stabil|
|`POST`|`/orchestrate`|`{goal, mode?, context?}`|`{session_id, plan_id, steps}`|✅ Stabil|
|`GET`|`/health`| — |`{status, version, uptime}`|✅ Stabil|
|`POST`|`/attachments/upload`|File multi-bagian|`{attachment_id, parsed?}`|✅ Stabil|
|`GET`|`/telemetry/metrics`|`?range=`|`Metrics`|⚠️ Dalaman|

### 6.2 Titik Akhir WebSocket


|Jalur|Arah|Format Pesan|
|---|---|---|
|`/ws/chat/{session_id}`|Dua arah|JSON `{type, content, metadata}`|
|`/ws/execution/{session_id}`|Server → Klien|JSON `{type, status, progress, data}`|
|`/ws/notifications/{user_id}`|Server → Klien|JSON `{type, message, timestamp, metadata}`|

### 6.3 Antarmuka Internal


|antarmuka|Penyedia|Konsumen|Metode|
|---|---|---|---|
|`CognitiveService.process(context)`|8 kelas layanan|`CognitiveKernel`|`async`|
|`MemoryLayer.store/retrieve/search/delete`|7 lapisan kenangan|`MemoryManager`|`async`|
|`EventBus.publish/subscribe/consume`|`EventBus`|Semua modul|`async`|
|`ModelRouter.complete/embed/generate`|`ModelRouter`|Semua layanan kognitif|`sync`|

---

## 7. Arsitektur Memori


### 7.1 Lapisan Memori

|Lapisan|Kelas|Bagian belakang|TTL|Tujuan|
|---|---|---|---|---|
|**Bekerja**|`WorkingMemory`|ulang|1 jam|Status sesi berumur pendek|
|**Percakapan**|`ConversationMemory`|ulang|24 jam|Riwayat percakapan|
|**Pengetahuan**|`KnowledgeMemory`|Berkas (JSON)| ∞ |Pengetahuan terstruktur|
|**Jangka panjang**|`LongTermMemory`|Berkas (JSON)| ∞ |Kenangan terkompresi|
|**Episodik**|`EpisodicMemory`|Berkas (JSON)| ∞ |Acara + garis waktu|
|**Sidang**|`SessionMemory`|Berkas (JSON)|24 jam|Konteks percakapan|
|**Proyek**|`ProjectMemory`|Berkas (JSON)| ∞ |Data yang fokus pada proyek|

### 7.2 Diagram Arsitektur Memori


```
                   MemoryManager
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼────┐    ┌─────▼─────┐    ┌────▼────┐
   │  Redis  │    │File System │    │ Qdrant  │
   │ Working │    │ Knowledge  │    │(planned)│
   │ Conv.   │    │ Long-term  │    │         │
   │         │    │ Episodic   │    │         │
   └─────────┘    │ Session    │    └─────────┘
                  │ Project    │
                  └────────────┘
```

### 7.3 Konsolidasi Memori


Ketika lapisan memori melebihi ambang batas (default: 50 entri), metode `MemoryManager.compress_memory()`:

1. Mengumpulkan entri dari lapisan sumber
2. Diperoleh ringkasan melalui LLM (`model_router.complete()`)
3. Membuat `ConsolidatedBlock` dengan ID sumber
4. Menyimpan blok terkompresi dalam memori jangka panjang
5. Menghapus entri asli

```python
async def compress_memory(self, layer: str, threshold: int = 50):
    keys = await self._layers[layer].list_keys()
    if len(keys) > threshold:
        block = await self.consolidate(layer, "", max_entries=threshold)
        if block:
            await self.store("longterm", block.block_id, block.consolidated_content)
            for k in block.source_ids:
                await self._layers[layer].delete(k)
```

---

## 8. Saluran Kognitif

### 8.1 Layanan Saluran Pipa


Setiap layanan kognitif mengimplementasikan:

```python
class CognitiveService(ABC):
    @abstractmethod
    async def process(self, context: dict[str, Any]) -> dict[str, Any]:
        """Process and return enriched context."""
```

### 8.2 Kontrak Input/Output Layanan


|Melayani|Masukan (dari konteks)|Output (ditambahkan ke konteks)|
|---|---|---|
|`perception`|`input`, `project_id`|`memories`, `world_entities`|
|`memory`|`perception`|`relevant_memories`, `working_memory`|
|`reasoning`|`perception`|`hypotheses[]`, `chain`, `decision`|
|`planning`|`perception`|`roadmap`|
|`decision`|`options[]`, `perception`|`selected_option_id`, `confidence`, `reasoning`|
|`action`|`decision`|`action`, `parameters`|
|`reflection`|`perception`, `decision`|`review`, `score`, `passed`|
|`learning`|`reflection`|`learned`, `quality_score`, `suggestions`|

### 8.3 Tingkat Kompleksitas Saluran Pipa


|Kompleksitas|Kriteria|Panjang Pipa|Perkiraan Durasi|
|---|---|---|---|
|**REMEH**|Pencarian fakta tunggal, tanya jawab sederhana|4 layanan|< 2 detik|
|**SEDERHANA**|Pola yang diketahui, ambiguitas rendah|5 layanan|2-5 detik|
|**SEDANG**|Analisis multi langkah dan moderat|7 layanan|5-15 detik|
|**KOMPLEK**|Masalah baru, taruhannya tinggi|10 layanan|15-60an|
|**SANGAT KOMPLEKS**|Strategi, lintas domain, wilayah tinggi|10 layanan|30-120an|

---

## 9. Capability Pack Arsitektur


### 9.1 Struktur Paket

```
apps/
├── __init__.py           # Dynamic loader — discovers and registers packs
├── base.py               # BaseApp abstract class
├── network_engineer/     # Network configuration analysis & generation
│   ├── __init__.py
│   ├── analyzer.py       # Configuration analysis
│   ├── compliance.py     # Compliance checking
│   ├── generator.py      # Configuration generation
│   ├── topology.py       # Network topology
│   ├── verification_engine.py  # Post-change verification
│   ├── ... (15 modules)
│   ├── mikrotik/         # Vendor-specific parser
│   └── nic/              # Network Intelligence Center
├── code_engineer/        # Code analysis & generation
│   ├── __init__.py
│   ├── analyzer.py
│   ├── architecture_reader.py
│   ├── refactoring_engine.py
│   └── ... (9 modules)
├── research_assistant/   # Research & analysis
├── devops_assistant/     # DevOps automation
├── trading_analyst/      # Trading analysis
└── self_development/     # Self-improvement
```

### 9.2 Kontrak Paket

Setiap paket harus menyediakan:

```python
# 1. Class inheriting from BaseApp
class NetworkEngineerApp(BaseApp):
    @property
    def capabilities(self) -> list[str]: [...]

# 2. Factory function
def get_app() -> BaseApp:
    return NetworkEngineerApp()
```

### 9.3 Pendaftaran Keterampilan


Paket mendaftarkan kemampuannya di `agents/skills.yaml`. `SkillRegistry` memuat ini di Runtime untuk mengaktifkan penemuan kemampuan.

---

## 10. Gerbang Kualitas

Lihat `docs/quality/QUALITY_GATES.md` untuk kebijakan lebih lanjut.

**Ringkasan:**

|Gerbang|Urutannya|Kerasnya|
|---|---|---|
|MyPy|0 kesalahan|🔴 PEMBLOKIRAN|
|Tes|≥95% lulus (dasar: 426)|🔴 PEMBLOKIRAN|
|API Kontrak|Kompatibel ke belakang|🔴 PEMBLOKIRAN|
|ADR|Diperlukan untuk mengubah arsitektur|🔴 PEMBLOKIRAN|
|Serat Ruff|Tidak ada pemblokiran|🟡 PERINGATAN|
|Format Ruff|0 file diformat ulang|🟡 PERINGATAN|
|Kompatibel dengan Python 3.11|Tidak ada garis miring terbalik f-string yang lolos dalam produksi|🔴 PEMBLOKIRAN|

---

## 11. Strategi Pengujian

### 11.1 Lapisan Uji

|Lapisan|Lokasi|Menghitung|Kerangka|
|---|---|---|---|
|Tes satuan|`tests/test_*.py`|426|pytest + pytest-asyncio|
|Integrasi|`backend/tests/`|Melalui unit tes|uji coba|
|Benchmark|`benchmarks/`|10+|Pelari Benchmark khusus|
|Kasus nyata|`real_cases/`|20+|Validasi berdasarkan kumpulan data|

### 11.2 Tes Cakupan Area


|Daerah|Tes|Status|
|---|---|---|
|Perencana AI|`test_ai_planner.py`| ✅ |
|Agen Peramban|`test_browser_agent.py`| ✅ |
|Kemampuan Eksekusi|`test_capability_execution_engine.py`| ✅ |
|Kapabilitas Saluran|`test_capability_pipeline.py`| ✅ |
|Penyelesai Niat|`test_intent_resolver.py`| ✅ |
|Lapisan Memori|`test_memory_layer.py`| ✅ |
|Multi-Agen|`test_multi_agent.py`, `test_multi_agent_coordination.py`| ✅ |
|Observabilitas|`test_observability_tracing.py`| ✅ |
|Plugin|`test_plugin_marketplace.py`| ✅ |
|Mesin Penalaran|`test_reasoning_engine.py`| ✅ |
|Cerminan|`test_reflection_agent.py`| ✅ |
|Keamanan|`test_security_audit.py`| ✅ |
|Orkestra Terpadu|`test_unified_orchestrator.py`| ✅ |
|Suara/Visi|`test_voice_vision_agent.py`| ✅ |

### 11.3 Perintah Uji

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=backend/app --cov=apps

# Run specific test
pytest tests/test_memory_layer.py -v
```

---

## 12. Standar Pengkodean

### 12.1 Standar Python


|Aturan|Standar|
|---|---|
|versi piton|3.11+|
|Ketik petunjuk|Diperlukan pada semua fungsi publik|
|Panjang garis|100 karakter|
|Impor|Dikelompokkan: stdlib → pihak ketiga → internal|
|asinkron|Gunakan `async def` untuk operasi ketergantungan I/O|
|Lajang|Inisialisasi yang lambat untuk menghindari impor melingkar|
|data kelas|Gunakan `@dataclass` untuk wadah data|
|enum|Gunakan `StrEnum` atau `Enum` untuk konstanta|

### 12.2 Konvensi Penamaan


|Elemen|Konvensi|Contoh|
|---|---|---|
|Mengajukan|`snake_case.py`|`memory_layer.py`|
|Kelas|`PascalCase`|`MemoryManager`|
|Fungsi|`snake_case`|`get_unified_orchestrator()`|
|Variabel|`snake_case`|`memory_manager`|
|Konstanta|`UPPER_CASE`|`PIPELINE_PRESETS`|
|Pribadi|`_prefix`|`_teams`|
|Ketik vars|`T`|`T = TypeVar('T')`|

### 12.3 Konfigurasi MyPy


```toml
[tool.mypy]
python_version = "3.11"
strict = false
ignore_missing_imports = true
explicit_package_bases = true
namespace_packages = true
```

### 12.4 Konfigurasi Ruff


```toml
[tool.ruff]
line-length = 100
target-version = "py311"
select = ["E", "F", "I", "N", "W", "UP"]
```

---

## Riwayat Dokumen Versi


|Versi|Tanggal|Perubahan|
|---|---|---|
|1.0.0|2024|Garis dasar awal pasca-rekayasa dokumen AES|

---

*Spesifikasi Arsitektur AES Akhir*
