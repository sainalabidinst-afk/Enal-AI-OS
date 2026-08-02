# Tinjauan Arsitektur ECP — Platform RC (2026-08-02)

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Ikhtisar arsitektur sistem dan interaksi komponen
<!-- DOCUMENT_METADATA_END -->

## Arsitektur Sistem (Langsung)

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
└───────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                   Gateway API (FastAPI)                      │
└───────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              Adaptive Cognitive Runtime                        │
│  Meta-Cognition: Choose pipeline, optimize budget             │
└───────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    Cognitive Kernel (INTEGRATED)               │
│  ┌─────────┬─────────┬─────────┬─────────┬──────────────┐  │
│  │Perception│ Memory  │Reasoning│Planning │  Decision    │  │
│  └─────────┴─────────┴─────────┴─────────┴──────────────┘  │
│  ┌─────────┬─────────┬─────────┬─────────┬──────────────┐  │
│  │ Action  │Reflection│ Learning │ Debate │ Simulation  │  │
│  └─────────┴─────────┴─────────┴─────────┴──────────────┘  │
└────────────────────────────────────────────┬────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Runtime Layer                           │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │ Event Bus    │ Task Queue   │ Distributed Runtime      │ │
│  └──────────────┴──────────────┴──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                       │
│  ┌──────────┬──────────┬──────────┬──────────┬────────────┐ │
│  │  Redis   │PostgreSQL│  Qdrant  │MinIO    │  Ollama    │ │
│  └──────────┴──────────┴──────────┴──────────┴────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Saluran Kognitif (Aktif)

```
Input → Perception → Planner → Memory → Executor → Learning → Governance
```

Setiap lapisan yang diimplementasikan dan diuji:
- **Perception** (`backend/app/core/perception_engine.py`) — Pemrosesan masukan, ekstraksi entitas/intensi
- **Planner** (`apps/organization/ai_planner.py`) — Dekomposisi tujuan, estimasi biaya/risiko
- **Memory** (`backend/app/core/memory_layer.py`) — 7 lapisan memori dengan konsolidasi
- **Executor** (`apps/organization/workflow_executor.py`) — Eksekusi alur kerja, checkpoint, retry
- **Learning** (`backend/app/core/cognitive/continuous_learning.py`) — RL, masukan manusia
- **Governance** (`backend/app/core/governance.py`) — Alur kerja persetujuan, isolasi tenant

Diatur oleh `backend/app/agents/orchestrator_v2.py`.

---

## Aturan Arsitektur (2026-08-02)

> **Aturan Pemisahan Layanan Kognitif Inti:**
> Tidak ada Layanan Kognitif Inti yang dapat memanggil Layanan lain secara langsung tanpa melalui antarmuka layanan atau lapisan orkestrasi.

**Penerapan:** Memory ↔ Planner ↔ Executor ↔ Learning berkomunikasi melalui kontrak saja.

---

## Struktur Paket

```text
backend/
└── app/
    ├── main.py                 # FastAPI application entry point
    ├── api/                    # Route handlers (REST endpoints)
    │   ├── chat.py            # Chat + SSE streaming
    │   ├── execution.py       # Execution CRUD + progress
    │   ├── workspace.py       # Workspace CRUD + files
    │   ├── artifact.py        # Artifact CRUD + versions
    │   ├── model_gateway.py   # Model provider health/status
    │   ├── capability_discovery.py  # Capability registry lookup
    │   └── ...                 # Other route modules
    ├── core/                   # Canonical services (source of truth)
    │   ├── perception_engine.py # Input processing + NLP
    │   ├── memory_layer.py    # Memory layers (working, conversation, knowledge, long-term, session, project)
    │   ├── cognitive_kernel.py # Cognitive service orchestration
    │   ├── cognitive/        # Cognitive primitives
    │   │   ├── planner.py      # Plan creation + result review
    │   │   ├── reasoning_engine.py
    │   │   ├── debate_engine.py
    │   │   ├── self_verification.py
    │   │   ├── simulation_engine.py
    │   │   ├── world_model.py
    │   │   ├── strategic_planner.py
    │   │   └── continuous_learning.py
    │   ├── adaptive_runtime.py # Dynamic pipeline composition
    │   ├── evaluation.py       # QualityGate + benchmark framework
    │   ├── governance.py       # Approval + tenant isolation
    │   ├── security_model.py   # RBAC + audit logging
    │   └── ...                 # Other core services
    └── agents/                 # Agent implementations
        └── orchestrator_v2.py # Primary orchestrator (integrated pipeline)
apps/
    ├── organization/           # Organization runtime
    │   ├── ai_planner.py      # Planner with cost/risk estimation
    │   └── workflow_executor.py # Executor with checkpoint/resume/retry
    ├── society/               # Society runtime
    │   └── intent_router.py   # Intent routing + domain hints
    ├── network_engineer/      # Network reference app
    ├── code_engineer/         # Code reference app
    ├── research_assistant/    # Research reference app
    ├── devops_assistant/      # DevOps reference app
    ├── trading_analyst/       # Trading reference app
    ├── self_development/      # Self-development reference app
    ├── decision_intelligence/     # Decision Intelligence (RFC-0007)
    ├── system_architect/          # System Architect (RFC-0011)
    ├── security_engineer/         # Security Engineer (RFC-0008)
    ├── data_engineer/             # Data Engineer (RFC-0009)
    ├── database_engineer/         # Database Engineer (RFC-0010)
    ├── qa_engineer/               # QA Engineer (RFC-0012)
    └── business_analyst/          # Business Analyst (RFC-0013)
benchmarks/                   # Performance + quality benchmarks
```

---

## Status: Platform Kandidat Rilis (92/100)

| Lapisan | Status | Catatan |
|---------|--------|---------|
| Platform Inti | ✅ Lengkap | 90 |
| Layanan Kognitif | ✅ Terintegrasi | 91 |
| Capability Pack | ✅ Produksi Siap | 90 |
| Lapisan Operasional | ✅ Diimplementasikan | 90 |
| Keamanan | ✅ RBAC + Isolasi | 89 |
| Pengujian | ✅ 426 test lulus | 92 |

---

## Aturan Ketergantungan

```
apps → sdk → kernel
apps → runtime → kernel
studio → runtime → kernel
marketplace → runtime → kernel
plugins → kernel
```

**Dilarang:**
- kernel → Runtime, SDK, aplikasi, Capability Pack
- Runtime → aplikasi, SDK, Capability Pack

---

## Versi Kontrak

Semua kontrak memiliki versi dan kompatibel dengan versi utama.

```
Contract v1.x → Stable, backward-compatible
Contract v2.x → Breaking changes, migration guide provided
```

> **Perubahan Kebijakan (2026-08-02):** Semua kontrak publik API dihentikan. Perubahan internal diperbolehkan; perubahan tanda tangan publik memerlukan review.

---

## Sprint Berikutnya (Revisi Prioritas)

### Sprint A — Pengerasan Teknis
- 0 Keparahan Pylance 8
- 100% API Publik Diketik
- Konsistensi asinkron

### Sprint B — Dokumentasi AES
- Spesifikasi Arsitektur
- Spesifikasi Teknis
- Kontrak perilaku

### Sprint C — Refleksi + Evaluasi
```
Generate → Evaluate → Reflect → Improve → Verify
```

### Sprint D — Lapisan Bukti
```
Search → Retrieve → Extract → Normalize → Rank → Evidence → Citation
```

### Sprint E — Mesin Debat

