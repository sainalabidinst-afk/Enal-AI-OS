# Tinjauan Arsitektur ECP — Platform RC (2026-08-05)

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-05
**Versi:** 1.1.0
**Status:** Aktif
**SSOT:** Ikhtisar arsitektur sistem dan interaksi komponen
<!-- DOCUMENT_METADATA_END -->

## Filosofi Arsitektur

> **Core adalah platform yang stabil. Capability Pack adalah tempat terjadinya inovasi.**

Semua perluasan pengetahuan, pertumbuhan fitur, dan evolusi domain terjadi **di dalam Capability Pack**. Inti tetap tidak berubah.

## Arsitektur Sistem

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
│                      Core Platform Layer                      │
│  ┌─────────────┬─────────────┬─────────────┬──────────────┐ │
│  │  Runtime    │  Memory      │  Event Bus   │  Governance  │ │
│  │  Engine     │  (7 layers)  │  / TaskQueue │  / Security   │ │
│  └─────────────┴─────────────┴─────────────┴──────────────┘ │
│  ┌─────────────┬─────────────┬─────────────┬──────────────┐ │
│  │  Workspace   │  Artifact    │  Tool/MCP    │  Plugin      │ │
│  │  Service     │  Service     │  Registry     │  System       │ │
│  └─────────────┴─────────────┴─────────────┴──────────────┘ │
└───────────────────────────┬─────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Pluggable Capability Packs                       │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │ Trading      │ Network      │ Decision Intelligence     │ │
│  │ Analyst      │ Engineer     │ (shared reasoning)        │ │
│  └──────────────┴──────────────┴──────────────────────────┘ │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │ DevOps       │ Code         │ AI Engineer               │ │
│  │ Assistant    │ Engineer     │                           │ │
│  └──────────────┴──────────────┴──────────────────────────┘ │
│  ... (18+ Capability Packs, each independently evolving)      │
└───────────────────────────┬─────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      AI Workspace                              │
│  Narrative | Conversation | Tool Calling | Collaboration       │
└───────────────────────────────────┬─────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                       │
│  ┌──────────┬──────────┬──────────┬──────────┬────────────┐ │
│  │  Redis   │PostgreSQL│  Qdrant  │MinIO    │  Ollama    │ │
│  └──────────┴──────────┴──────────┴──────────┴────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Prinsip Inti

1. **Core Stabil**: `backend/app/core/` hanya berisi layanan umum: Runtime, Memory, EventBus, ToolRegistry, MCPRegistry, PluginSystem, Workspace, Artifact, Governance, Security.
2. **Inovasi di Capability Pack**: Semua domain knowledge, reasoning khusus, dan evolusi terjadi di `apps/<capability>/`.
3. **Decision Intelligence sebagai Shared Reasoning**: `apps/decision_intelligence/` menyediakan evidence gathering, alternative generation, risk analysis, trade-off analysis, confidence estimation, dan explainable decision untuk semua Capability Pack.
4. **AI Workspace sebagai Antarmoma Kolaborasi**: Menjelaskan keputusan kepada pengguna melalui narrative, conversation, dan tool calling.

## Alur Berpikir (Thinking Flow)

```
Capability Pack (misal: Trading)
        │
        ▼
Domain Analysis (Market Structure, Signal Engine, Evidence)
        │
        ▼
Decision Intelligence (Evidence → Alternative → Trade-off → Risk → Confidence → Recommendation)
        │
        ▼
AI Workspace (Narrative → Conversation → Tool Calling → User)
```

## Struktur Paket

```text
backend/
└── app/
    ├── main.py                 # FastAPI application entry point
    ├── api/                    # Generic route handlers
    │   ├── capability_execution.py  # Generic capability execution
    │   ├── chat.py             # Chat + SSE streaming
    │   ├── execution.py        # Execution CRUD + progress
    │   ├── workspace.py        # Workspace CRUD + files
    │   ├── artifact.py         # Artifact CRUD + versions
    │   └── ...                 # Other route modules
    └── core/                   # Stable platform services ONLY
        ├── runtime/            # Runtime engine, adaptive pipeline
        ├── memory/             # Memory layers (7 layers)
        ├── event_bus.py        # Event-driven communication
        ├── task_queue.py       # Async task management
        ├── tool_registry.py    # Tool registration + schemas
        ├── mcp_registry.py     # MCP plugin registry
        ├── plugin_manifest.py  # Plugin validation + compatibility
        ├── workspace_service.py # Workspace CRUD
        ├── artifact_service.py # Artifact versioning
        ├── governance.py       # Approval workflows + tenant isolation
        ├── security_model.py   # RBAC + audit logging
        ├── contracts.py        # Stable interface contracts
        └── ...

apps/
    ├── trading_analyst/        # Trading Capability Pack
    │   ├── engine.py           # TradingEngine (domain analysis)
    │   ├── market_intelligence/ # Wyckoff, SMC, Elliott, Volume, Psychology, Macro
    │   └── knowledge/          # Trading-specific knowledge seeding
    ├── infrastructure_engineer/ # Infrastructure Capability Pack
    │   ├── engine.py
    │   ├── attachments/        # Config parsers, compliance, reasoning
    │   └── ...
    ├── decision_intelligence/  # Shared reasoning layer (RFC-0007)
    │   ├── engine.py
    │   ├── evidence_collector.py
    │   ├── alternative_generator.py
    │   ├── risk_analyzer.py
    │   ├── tradeoff_analyzer.py
    │   ├── scoring_engine.py
    │   ├── confidence_estimator.py
    │   ├── explanation_generator.py
    │   └── decision_history.py
    ├── network_engineer/       # Network Capability Pack
    ├── code_engineer/          # Code Capability Pack
    ├── research_assistant/     # Research Capability Pack
    ├── devops_assistant/       # DevOps Capability Pack
    ├── self_development/       # Self Development Capability Pack
    ├── system_architect/       # System Architect Capability Pack
    ├── security_engineer/      # Security Engineer Capability Pack
    ├── data_engineer/          # Data Engineer Capability Pack
    ├── database_engineer/      # Database Engineer Capability Pack
    ├── qa_engineer/            # QA Engineer Capability Pack
    ├── business_analyst/       # Business Analyst Capability Pack
    ├── documentation_engineer/ # Documentation Engineer Capability Pack
    ├── product_manager/        # Product Manager Capability Pack
    ├── ui_ux_designer/         # UI/UX Designer Capability Pack
    ├── full_stack_engineer/    # Full Stack Engineer Capability Pack
    ├── ai_engineer/            # AI Engineer Capability Pack
    ├── organization/           # Organization runtime
    └── society/                # Society runtime

frontend/
└── components/
    └── workspace/
        ├── engine/             # Core workspace layout, panels, resize
        ├── decision-intelligence/ # Shared reasoning UI components
        ├── apps/               # Capability-specific workspace apps
        │   ├── trading/        # Trading workspace panels
        │   ├── network/        # Network workspace panels
        │   └── ...
        └── ai/                 # AI Workspace (narrative, conversation)
```

## Aturan Ketergantungan

```
apps → core (platform services only)
apps → decision_intelligence (shared reasoning)
frontend workspace apps → decision-intelligence components
capability packs → tidak boleh mengimpor dari capability packs lain
```

**Dilarang:**
- Core mengimpor dari Capability Pack
- Capability Pack mengimpor dari Capability Pack lain
- Core memuat domain knowledge (trend, RSI, Wyckoff, MikroTik, Kubernetes, SQL)

## Capability Execution Flow

```
User Request
    ↓
Generic API: POST /api/v1/capabilities/{capability_id}/execute
    ↓
Capability Adapter (loads capability pack)
    ↓
Capability Pack Engine (domain analysis)
    ↓
Decision Intelligence (optional, cross-cutting)
    ↓
AI Workspace (narrative + explanation)
    ↓
Response
```

## Status: Platform Kandidat Rilis (92/100)

| Lapisan | Status | Catatan |
|---------|--------|---------|
| Core Platform | ✅ Stabil | 90 |
| Capability Packs | ✅ Produksi Siap | 90 |
| Decision Intelligence | ✅ Shared Reasoning | 91 |
| AI Workspace | ✅ Kolaborasi | 88 |
| Keamanan | ✅ RBAC + Isolasi | 89 |
| Pengujian | ✅ 426 test lulus | 92 |
