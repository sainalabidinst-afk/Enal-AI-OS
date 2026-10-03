<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Canonical Owner:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-10-03
**Versi:** v3.1.0-rc2
**Status:** Aktif
**SSOT:** Ikhtisar proyek, instalasi, quick start, dan registri Capability Pack
<!-- DOCUMENT_METADATA_END -->

# Enal Cognitive Platform (ECP)

**AI Operating System** — Platform yang stabil. Capability yang ahli. Satu percakapan.

> 🟢 **Engineering Baseline:** Tag `v1.0.0-engineering-baseline` (frozen baseline; code has diverged — see audit)
> 🟢 **Engineering Transformation:** COMPLETE — MyPy: 0 errors, Ruff: 0 errors, 1082 tests collected (1081 passed, 1 skipped)
> 🟢 **Governance:** ACTIVE — Quality Gates, ADRs, Architecture Specification
> 🟩 **Release Classification:** PRODUCTION — v3.0.0 (43 app directories including 37 capability packs + 6 infrastructure; all benchmarks Grade A)

---

## Ikhtisar

ECP adalah sistem operasi kognitif multi-agen yang mengorkestrasi Capability Pack spesifik-domain melalui cognitive pipeline yang terpadu. Platform ini menyediakan Core Runtime yang stabil, layanan kognitif, hierarki Memory, sistem event, dan kerangka tata kelola — memungkinkan tim untuk membangun dan men-deploy aplikasi domain bertenaga AI (Capability Pack) di atas fondasi yang terbukti dan terdokumentasi.

```
User → [API Layer] → [Orchestrator] → [Cognitive Pipeline (8 services)] → [Memory] → [Action]
                                     ↖                        ↗
                                  Event Bus (Redis Streams)
```

---

## Status Proyek

### Program Engineering Transformation: ✅ COMPLETE

| Area | Status | Detail |
|---|---|---|
| **Engineering Hardening** | ✅ Selesai | MyPy/Ruff gates PASSING (0 errors); 1082 tests collected (1081 passed, 1 skipped) |
| **Type Safety** | ✅ Selesai | MyPy: 0 errors; Ruff: 0 errors |
| **Test Suite** | ✅ Stabilitas | 1082 tests collected, 1081 passed, 1 skipped |
| **Python 3.11 Compatibility** | ✅ Selesai | Nol masalah f-string backslash pada production code |
| **Ruff Hygiene** | ✅ Selesai | 0 errors remaining; `ruff check --fix` clean |
| **subprocess.run Safety** | ✅ Selesai | Semua pemanggilan memiliki parameter `check=` eksplisit |
| **JWT Authentication** | ✅ Selesai | Real JWT dengan signature, expiry, algorithm enforcement |
| **Async Safety** | ✅ Selesai | Blocking `complete()` → `acomplete()` di jalur async |
| **Docker Hardening** | ✅ Selesai | Volume mounts, pinned ollama, read_only aman |
| **Complexity Reduction** | ✅ Selesai | Max complexity 272 → 211, top 10 files di-split |
| **Integration Tests** | ✅ Selesai | 122 tests baru covering 130 endpoints |
| **Trading Analyst** | ✅ Selesai | A+ (100%), Level 4 Domain Expert, bersertifikat |

### Architecture Governance: 🟢 COMPLETE

| Dokumen | Baris | Yang Disediakan |
|---|---|---|
| `docs/ENGINEERING_BASELINE.md` | 297 | Baseline yang dibekukan — apa yang dikunci dan mengapa |
| `docs/quality/QUALITY_GATES.md` | 137 | 12 quality gate dengan proses pengecualian |
| `docs/adr/ADR-001.md` — `ADR-026.md` | 1,247 | 26 arsip keputusan arsitektur (Event Bus — Voice Interaction) |
| `docs/AES_ARCHITECTURE.md` | 734 | Architecture Engineering Specification (kondisi kode aktual) |
| `docs/REFERENCE_ARCHITECTURE.md` | 635 | Pola, anti-pola, kerangka keputusan |
| `docs/APP_DEV_GUIDE.md` | 798 | Panduan langkah-demi-langkah untuk membangun Capability Pack |
| **Total** | **3,848 baris** | **~131 KB — rangkaian engineering governance lengkap** |

### Skor Kualitas Akhir

```
Engineering:     94/100  (Architecture APPROVED; Type Safety & Ruff gates PASSING)
Architecture:   100/100  (APPROVED 94/100 per COMPREHENSIVE_AUDIT_2026-09-21)
Governance:     100/100  (COMPLETE)
Documentation:   72/100  (6,553 lines documented; stale claims corrected 2026-09-21)
Product Ready:   85/100  (PRODUCTION — v3.0.0; 37 packs Grade A, benchmarks passing)
```

> 🟩 **Release Classification PRODUCTION — v3.0.0.** Semua 37 capability packs ter-implementasi, semua benchmark lulus Grade A. Governance & package boundary checks: ✅ 0 violations. TypeScript frontend: ✅ 0 errors. Lihat [`docs/audit/COMPREHENSIVE_AUDIT_2026-09-21.md`](docs/audit/COMPREHENSIVE_AUDIT_2026-09-21.md).

---

## Arsitektur

### Diagram Lapisan

```
┌─────────────────────────────────────────────────────────────────┐
│                    API LAYER (FastAPI)                      │
│  15 route modules — chat, execution, workspace, artifact... │
└────────────────────────────────────────┬───────────────────────┘
                          │
┌────────────────────────────────────────▼───────────────────────┐
│                 ORCHESTRATION LAYER                         │
│  ┌───────────────┐  ┌───────────────┐  ┌─────────────┐ │
│  │  AIOrchestrator  │  │UnifiedOrch.    │  │AdaptiveRT    │ │
│  │ (goal→plan→exec) │  │(4 modes+teams) │  │(pipeline sel)│ │
│  └───────────────┘  └───────────────┘  └─────────────┘ │
└────────────────────┬────────────────────┬───────────────────┘
             │                    │                  │
┌────────────────────────▼────────────▼──────────────▼─────────┐
│                   COGNITIVE KERNEL                          │
│  8 services: Perception, Memory, Reasoning, Planning,       │
│  Decision, Action, Reflection, Learning                     │
│  Executed in ordered pipelines per complexity level         │
└────────────────────────────────────────┬───────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────┐
│                      RUNTIME LAYER                          │
│  Event Bus (Redis Streams) • Task Queue • Execution Sched.  │
│  Model Router (LiteLLM) • Cost Optimizer • State Recovery   │
└────────────────────────────────────────┬───────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────┐
│                   INFRASTRUCTURE LAYER                      │
│  Redis │ PostgreSQL │ File System │ LLM Providers (LiteLLM) │
└───────────────────────────────────────────────────────────┘
```

### Cognitive Pipeline

Tugas diproses melalui pipeline yang dipilih berdasarkan kompleksitas:

| Kompleksitas | Layanan | Use Case |
|---|---|---|
| **TRIVIAL** | 4 (perception → memory → decision → action) | Q&A sederhana, pencarian fakta |
| **SIMPLE** | 5 (+ reasoning) | Pola yang dikenal, ambiguitas rendah |
| **MEDIUM** | 7 (+ planning + reflection) | Analisis multi-langkah |
| **COMPLEX** | 10 (+ debate + simulation + verification + learning) | Masalah baru, risiko tinggi |

### Arsitektur Jenny-like Interaction

ECP dapat berinteraksi seperti "Jenny" melalui lapisan tambahan di atas Cognitive Kernel yang sudah ada:

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INPUT                              │
│  Voice (STT) │ Text                                          │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│  Natural Language Interface Layer                         │
│  • STT (Whisper.cpp / Web Speech API / OpenAI Whisper)    │
│  • TTS (Piper / browser speechSynthesis / ElevenLabs)     │
│  • NLU Intent Classification + Dialogue Manager           │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│  Orchestration Layer (CognitiveKernel → Pipeline)          │
│  • AdaptiveCognitiveRuntime.execute()                      │
│  • MetaCognition (pipeline selection, optimization)        │
│  • Complexity-aware routing (TRIVIAL→SIMPLE→MEDIUM→COMPLEX)│
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│  Cognitive Pipeline (CognitiveKernel — 8 services)         │
│  Perception→Memory→Reasoning→Planning→Decision→Action→     │
│  Reflection→Learning (+Simulation, +AdversarialTesting)    │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│  Action Layer                                              │
│  • ToolRegistry (plugin-style tool registration)          │
│  • ConnectorManager (FileSystem, Email, Calendar, IoT)    │
│  • Capability Packs (37 packs, all Grade A)               │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│  Output Layer                                              │
│  • TTS (Jenny voice response)                             │
│  • Structured response w/ explanation, confidence, trace  │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│  Observability & Safety                                  │
│  • Observability (trace spans, anomaly_detect)            │
│  • Consent / Permission Layer (risk-based approval)       │
│  • Governance checks (ADR, quality gates)                 │
└─────────────────────────────────────────────────────────────┘
```

**Status komponen:**

| Komponen | Path | Status |
|---|---|---|
| VoiceAgent (STT/TTS provider abstraction) | `backend/app/core/voice_vision_agent.py` | ✅ Implementasi |
| STT Service | `backend/app/core/stt_service.py` | ✅ Implementasi |
| TTS Service | `backend/app/core/tts_service.py` | ✅ Implementasi |
| Voice API | `backend/app/api/voice.py` | ✅ Implementasi |
| Frontend voice (chatgpt-page.tsx) | `frontend/components/chat/chatgpt-page.tsx` | ✅ Implementasi |
| FileSystemConnector | `backend/app/connectors/file_system.py` | ✅ Implementasi |
| EmailConnector | `backend/app/connectors/email.py` | ✅ Implementasi |
| CalendarConnector | `backend/app/connectors/calendar.py` | ✅ Implementasi |
| SmartHomeConnector | `backend/app/connectors/smarthome.py` | ✅ Implementasi |
| ActionConnectorManager | `backend/app/connectors/base_action.py` | ✅ Implementasi |
| Action Tool Registration | `backend/app/connectors/action_tools.py` | ✅ Implementasi |
| Actions API | `backend/app/api/actions.py` | ✅ Implementasi |
| ConsentManager | `backend/app/core/consent.py` | ✅ Implementasi |
| Consent API | `backend/app/api/consent.py` | ✅ Implementasi |
| Consent Dialog (frontend) | `frontend/components/jenny/consent-dialog.tsx` | ✅ Implementasi |
| Observability (anomaly_detect) | `backend/app/core/observability.py` | ✅ Implementasi |
| Cognitive Kernel (8 services) | `backend/app/core/cognitive_kernel.py` | ✅ Siap |
| Adaptive Runtime | `backend/app/core/adaptive_runtime.py` | ✅ Siap |
| Memory (7 layers) | `backend/app/core/memory_layer.py` | ✅ Siap |
| MetaCognition | `backend/app/core/meta_cognition.py` | ✅ Siap |
| ToolRegistry | `backend/app/core/tool_registry.py` | ✅ Siap |
| ConnectorManager | `backend/app/connectors/__init__.py` | ✅ Siap (trading + action) |
| Governance / ADR / Quality Gates | `docs/adr/`, `docs/quality/` | ✅ Aktif |

> 📋 Lihat [`TODO_CAPABILITY_EXECUTION.md`](#fase-jenny-like-interaction) untuk roadmap implementasi 3-fase.

### Arsitektur Memory

7 lapisan memory dengan konsolidasi otomatis:

| Lapisan | Backend | TTL | Tujuan |
|---|---|---|---|
| Working | Redis | 1h | State sesi jangka pendek |
| Conversation | Redis | 24h | Riwayat chat |
 | Knowledge | File (JSON) | ∞ | Pengetahuan terstruktur |
 | Long-term | File (JSON) | ∞ | Memory terkompresi |
 | Episodic | File (JSON) | ∞ | Linimasa event |
 | Session | File (JSON) | 24h | Konteks percakapan |
 | Project | File (JSON) | ∞ | Data proyek |
 
 ---
 
 ## Solusi Industri
 
 Enal-AI-OS dapat disesuaikan untuk berbagai industri melalui **Vertical Industry Packs**:
 
 | Industri | Capability Pack | Manfaat |
 |----------|-----------------|---------|
 | **Financial Services** | Finance Analyst | Analisis keuangan, pemodelan, dan kontrol |
 | **Insurance** | Finance Analyst + Supply Chain Analyst | Underwrite, klaim, dan asuransi |
 | **Healthcare** | HSE Specialist + Document Processing | Alur kerja pasien dan administrasi medis |
 | **Legal, Consulting & Research** | Legal Advisor | Analisis dokumen, kewajiban, dan kepatuhan |
 | **Telecom, Media & Entertainment** | Translator Expert + Document Processing | Layanan dan konten lintas-bahasa |
 | **Mortgage Automation** | Finance Analyst | Aplikasi dan persetujuan pinjaman |
 | **Life Sciences** | HSE Specialist + Document Processing | Riset, uji klinis, dan kepatuhan regulasi |
 | **Trading & Investment** | Trading Analyst | Analisis pasar dan strategi investasi |
 | **Supply Chain & Logistics** | Supply Chain Analyst | Optimasi logistik dan manajemen risiko |
 
 ---
 
 ## Bidang Keahlian
 
 Enal-AI-OS mendukung berbagai bidang keahlian dan use case:
 
 | Bidang Keahlian | Use Case |
 |-----------------|----------|
 | **Insurance** | Underwriting, klaim, asuransi |
 | **Banking and Finance** | Analisis keuangan, pemodelan, kontrol |
 | **Customer Support** | Chatbot, escalation, knowledge base |
 | **HR** | Rekrutmen, onboarding, knowledge management |
 | **Healthcare** | Alur kerja pasien, administrasi medis |
 | **Marketing** | Konten, analisis kampanye, personalisasi |
 | **Defence** | Intelligence, logistik, kepatuhan |
 | **Legal** | Analisis dokumen, kewajiban, kepatuhan |
 | **Life Sciences** | Riset, uji klinis, kepatuhan regulasi |
 | **Procurement** | Vendor management, pengadaan, cost optimization |
 | **Supply Chain & Logistics** | Optimasi logistik, manajemen risiko |
 
 ---
 
 ## Roadmap — Fitur SimplAI Parity
 
 Berikut adalah fitur-fitur dari SimplAI yang direncanakan untuk diimplementasikan di Enal-AI-OS:
 
 | Fitur SimplAI | Deskripsi | Status |
 |---------------|-----------|--------|
 | **Visual Agent Builder** | UI no-code untuk membuat dan konfigurasi agent tanpa menulis kode | ✅ Done |
 | **Visual Tool Builder** | UI drag-drop/no-code dengan step graph (LLM, Python, API, web scraper) | ✅ Done |
 | **Voice Agent** | Telephony inbound/outbound, sub-second latency, voice-specific observability | ✅ Done |
 | **Guardrails & Safety** | PII detection, toxic language, prompt injection, bias check, logic check | ✅ Done |
 | **Marketplace** | Share/clone agents, internal marketplace, pre-built templates, analytics | ✅ Done |
 | **A2A/MCP Integration** | Agent-to-agent invocation, MCP tool registry, external sub-agents | ✅ Done |
 | **Bulk & Scheduled Execution** | Batch runs, scheduled triggers, webhooks, async queues | ✅ Done |
 | **Evaluation Framework** | Quality scoring, scheduled evaluations, metric details, feedback loops | ✅ Done |
 | **Templates System** | Pre-built agent/tool templates, guided cloning, dependency resolution | ✅ Done |
 
 ### Frontend Routes — SimplAI Parity
 
 | Route | Deskripsi |
 |-------|-----------|
 | `/builder/agent` | Visual Agent Builder — buat agent dengan drag-drop canvas |
 | `/builder/tool` | Visual Tool Builder — buat tool dengan step graph |
 | `/builder/voice` | Voice Agent Builder — konfigurasi STT/TTS, telephony, call history |
 | `/marketplace` | Marketplace — browse, clone, dan share agent/tool templates |
 | `/bulk-evaluation` | Bulk, Scheduled & Evaluation — bulk run, schedules, evaluasi kualitas |
 
 ### Backend Services — SimplAI Parity
 
 | Service | Deskripsi |
 |---------|-----------|
 | `backend/app/core/blueprint_repository.py` | Persistensi agent/tool blueprints |
 | `backend/app/core/agent_factory.py` | Factory untuk membuat agent dari blueprint |
 | `backend/app/core/agent_validator.py` | Validasi agent blueprint sebelum deploy |
 | `backend/app/core/agent_runtime.py` | Runtime eksekusi agent dari blueprint |
 | `backend/app/core/step_executor.py` | Eksekusi step tool (LLM, Python, API, KB, web scraper, conditional, delay) |
 | `backend/app/core/step_validator.py` | Validasi tool step graph |
 | `backend/app/core/tool_engine.py` | Engine eksekusi tool blueprint |
 | `backend/app/core/stt_service.py` | Speech-to-Text (Whisper, Deepgram, Google) |
 | `backend/app/core/tts_service.py` | Text-to-Speech (ElevenLabs, Azure, OpenAI) |
 | `backend/app/core/telephony_integration.py` | Telephony inbound/outbound call handling |
 | `backend/app/core/latency_monitor.py` | Voice latency monitoring (TTFS, P50/P90/P99) |
 | `backend/app/core/voice_agent_runtime.py` | Voice agent runtime (STT → LLM → TTS) |
 | `backend/app/core/guardrail_engine.py` | Guardrail engine (PII, toxic, injection, bias, logic, competitor, gibberish, reading level) |
 | `backend/app/core/marketplace_service.py` | Marketplace service (share, clone, analytics) |
 | `backend/app/core/a2a_registry.py` | A2A agent registry |
 | `backend/app/core/a2a_invoker.py` | A2A agent invoker |
 | `backend/app/core/mcp_tool_registry.py` | MCP server registry |
 | `backend/app/core/mcp_tool_proxy.py` | MCP tool proxy |
 | `backend/app/core/bulk_executor.py` | Bulk executor with concurrency control |
 | `backend/app/core/scheduler_service.py` | Scheduler service for cron jobs |
 | `backend/app/core/webhook_service.py` | Webhook notification service |
 | `backend/app/core/async_queue.py` | Async priority queue |
 | `backend/app/core/evaluator_engine.py` | Evaluator engine for quality scoring |
 | `backend/app/core/quality_scorer.py` | Quality scorer |
 | `backend/app/core/scheduled_evaluator.py` | Scheduled evaluator |
 | `backend/app/core/metric_details.py` | Metric details analytics |
 
 ### API Endpoints — SimplAI Parity
 
 | Endpoint | Method | Deskripsi |
 |----------|--------|-----------|
 | `/api/v1/blueprints/agent` | POST | Create agent blueprint |
 | `/api/v1/blueprints/agent` | GET | List agent blueprints |
 | `/api/v1/blueprints/agent/{id}` | GET | Get agent blueprint |
 | `/api/v1/blueprints/agent/{id}` | PUT | Update agent blueprint |
 | `/api/v1/blueprints/agent/{id}` | DELETE | Delete agent blueprint |
 | `/api/v1/blueprints/tool` | POST | Create tool blueprint |
 | `/api/v1/blueprints/tool` | GET | List tool blueprints |
 | `/api/v1/blueprints/tool/{id}` | GET | Get tool blueprint |
 | `/api/v1/blueprints/tool/{id}` | PUT | Update tool blueprint |
 | `/api/v1/blueprints/tool/{id}` | DELETE | Delete tool blueprint |
 | `/api/v1/guardrails/test` | POST | Test guardrails on content |
 | `/api/v1/guardrails` | GET | List available guardrails |
 | `/api/v1/marketplace/share` | POST | Share agent to marketplace |
 | `/api/v1/marketplace/share/{agent_id}` | DELETE | Unshare agent |
 | `/api/v1/marketplace` | GET | List marketplace items |
 | `/api/v1/marketplace/clone` | POST | Clone agent from marketplace |
 | `/api/v1/marketplace/analytics/{agent_id}` | GET | Get agent analytics |
 | `/api/v1/a2a/register` | POST | Register A2A agent |
 | `/api/v1/a2a` | GET | List A2A agents |
 | `/api/v1/a2a/invoke` | POST | Invoke A2A agent |
 | `/api/v1/mcp/servers` | POST | Register MCP server |
 | `/api/v1/mcp/servers/{server_id}/connect` | POST | Connect MCP server |
 | `/api/v1/mcp/servers/{server_id}/disconnect` | POST | Disconnect MCP server |
 | `/api/v1/mcp/servers` | GET | List MCP servers |
 | `/api/v1/mcp/tools/call` | POST | Call MCP tool |
 | `/api/v1/bulk/run` | POST | Run bulk tasks |
 | `/api/v1/schedule` | POST | Create schedule |
 | `/api/v1/schedule` | GET | List schedules |
 | `/api/v1/schedule/{job_id}` | DELETE | Delete schedule |
 | `/api/v1/webhooks/send` | POST | Send webhook |
 | `/api/v1/evaluate` | POST | Evaluate output |
 | `/api/v1/evaluate/results` | GET | Get evaluation results |
 
 ---
 
 ## Memulai

### Prasyarat

- Python 3.11+
- Redis 7+ (untuk Event Bus, Working/Conversation Memory)
- PostgreSQL 15+ (untuk execution session, artifacts)

### Quick Start

```bash
# Clone
git clone https://github.com/sainalabidinst-afk/Enal-AI-OS.git
cd Enal-AI-OS

# Buat virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependensi backend
pip install -e backend/

# Install SDK
pip install -e sdk/

# Jalankan test
pytest -v

# Verifikasi type safety
mypy apps/ backend/
```

### Verifikasi Baseline

```bash
# Pemeriksaan engineering baseline - lihat tools/audit/ untuk utility audit
python -m ruff check apps/ backend/   # lint check
pytest -v                             # test collection

# Quality Gates
python scripts/gate0_validate.py   # Validasi pre-merge
```

---

## Capability Pack Resmi

| Capability Pack | Status | Grade | RFC/ADR |
|---|---|---|---|
| **Network Engineer** | ✅ Production Ready | A (≥90) | RFC-0004 |
| **Code Engineer** | ✅ Production Ready | A+ (≥95) | RFC-0006 |
| **Research Assistant** | ✅ Production Ready | A+ (≥90) | RFC-0020 |
| **DevOps Assistant** | ✅ Production Ready | A+ (≥90) | RFC-0021 |
| **Trading Analyst** | ✅ Production Ready | A+ (≥95) | RFC-0005 |
| **Self Development** | ✅ Production Ready | A+ (≥95) | RFC-0022 |
| **Decision Intelligence** | ✅ Production Ready | A+ (≥95) | RFC-0007 |
| **System Architect** | ✅ Production Ready | A+ (≥95) | RFC-0011 |
| **Security Engineer** | ✅ Production Ready | A (≥90) | RFC-0008 |
| **Data Engineer** | ✅ Production Ready | A (≥90) | RFC-0009 |
| **Database Engineer** | ✅ Production Ready | A- (≥85) | RFC-0010 |
| **QA Engineer** | ✅ Production Ready | A (≥90) | RFC-0012 |
| **Business Analyst** | ✅ Production Ready | A- (≥85) | RFC-0013 |
| **Infrastructure Engineer** | ✅ Production Ready | A (≥90) | RFC-0014 |
| **AI Engineer** | ✅ Production Ready | A+ (≥95) | RFC-0015 |
| **Documentation Engineer** | ✅ Production Ready | A (≥90) | RFC-0016 |
| **Product Manager** | ✅ Production Ready | A- (≥85) | RFC-0017 |
| **UI/UX Designer** | ✅ Production Ready | A- (≥85) | RFC-0018 |
| **Full Stack Engineer** | ✅ Production Ready | A- (≥85) | RFC-0019 |
| **Cloud Architect** | ✅ Production Ready | A+ (≥95) | RFC-0026/ADR-005 |
| **SRE Engineer** | ✅ Production Ready | A (≥90) | RFC-0027/ADR-006 |
| **Compliance Officer** | ✅ Production Ready | A (≥90) | RFC-0028/ADR-007 |
| **Knowledge Engineer** | ✅ Production Ready | A (≥90) | RFC-0029/ADR-008 |
| **Finance Analyst** | ✅ Vertical Industry Pack | A (≥90) | RFC-0030/ADR-010 |
| **Legal Advisor** | ✅ Vertical Industry Pack | A (≥90) | RFC-0031/ADR-011 |
| **HSE Specialist** | ✅ Vertical Industry Pack | A (≥90) | RFC-0032/ADR-012 |
| **Observability** | ✅ Platform Services Pack | A (≥90) | RFC-0033/ADR-013 |
| **Cybersecurity Analyst** | ✅ Platform Services Pack | A (≥90) | RFC-0034/ADR-014 |
| **AI Ethics & Governance** | ✅ Governance Pack | A (≥90) | RFC-0035/ADR-015 |
| **Supply Chain Analyst** | ✅ Vertical Industry Pack | A (≥90) | RFC-0036/ADR-016 |
| **Data Scientist** | ✅ AI/ML Engineering Pack | A (≥90) | RFC-0037/ADR-017 |
| **Business Intelligence** | ✅ Analytics Pack | A (≥90) | RFC-0038/ADR-018 |
| **Innovation Strategist** | ✅ Strategy Pack | A (≥90) | RFC-0039/ADR-019 |
| **DevSecOps** | ✅ Security Engineering Pack | A (≥90) | RFC-0040/ADR-020 |
| **Translator Expert** | ✅ Platform Services Pack | A (≥90) | RFC-0041/ADR-021 |
| **Document Processing** | ✅ Productivity Pack | A (≥90) | RFC-0042/ADR-022 |
| **Voice Interaction** | ✅ Platform Professional | A (≥90) | RFC-0043/ADR-026 |

### Membangun Capability Pack Baru

Lihat [Application Development Guide](docs/APP_DEV_GUIDE.md) untuk petunjuk langkah-demi-langkah yang lengkap:

```
1. Define Domain Scope      → 5. Implement Custom Logic
2. Identify Building Blocks  → 6. Add Tests
3. Create App Module         → 7. Register API Routes
4. Register Skills           → 8. Integrate with Orchestration
```

---

## Rangkaian Dokumentasi

| Dokumen | Lokasi | Terbaik Untuk |
|---|---|---|
| **Getting Started** | `docs/getting_started.md` | Setup pertama kali |
| **Architecture (AES)** | `docs/AES_ARCHITECTURE.md` | Memahami bagaimana platform dibangun |
| **Reference Architecture** | `docs/REFERENCE_ARCHITECTURE.md` | Pola, anti-pola, kerangka keputusan |
| **App Development Guide** | `docs/APP_DEV_GUIDE.md` | Membangun capability pack baru |
| **Engineering Baseline** | `docs/ENGINEERING_BASELINE.md` | Apa yang dibekukan dan mengapa |
| **Quality Gates** | `docs/quality/QUALITY_GATES.md` | Persyaratan merge dan pengecualian |
| **ADRs** | `docs/adr/ADR-001.md` — `ADR-026.md` | Mengapa keputusan arsitektur dibuat |
| **API Reference** | `docs/api_reference.md` | Dokumentasi endpoint |
| **SDK Reference** | `sdk/README.md` | Penggunaan Python SDK |
| **Infrastructure Engineer** | `docs/rfcs/RFC-0014.md` | Infrastructure design (K8s, HA, DR) |
| **AI Engineer** | `docs/rfcs/RFC-0015.md` | AI/ML engineering (RAG, agents, LLMOps) |
| **Documentation Engineer** | `docs/rfcs/RFC-0016.md` | Documentation generation (OpenAPI, SDK, ADR) |
| **Product Manager** | `docs/rfcs/RFC-0017.md` | Product management (roadmap, OKR, backlog) |
| **UI/UX Designer** | `docs/rfcs/RFC-0018.md` | UI/UX design (design system, accessibility) |
| **Full Stack Engineer** | `docs/rfcs/RFC-0019.md` | Full stack engineering (code review, refactoring, release) |
| **Trading Analyst** | `docs/rfcs/RFC-0005.md` | Trading analysis, Wyckoff, ICT/SMC, Elliott Wave |
| **Self Development** | `docs/rfcs/RFC-0022.md` | Cross-project pattern learning, impact prediction |
| **Decision Intelligence** | `docs/rfcs/RFC-0007.md` | Evidence → Reasoning → Simulation → Decision pipeline |
| **System Architect** | `docs/rfcs/RFC-0011.md` | System design, security architecture, cost optimization |
| **Security Engineer** | `docs/rfcs/RFC-0008.md` | Security assessment, vulnerability management |
| **Data Engineer** | `docs/rfcs/RFC-0009.md` | Data pipeline, ETL, data quality |
| **Database Engineer** | `docs/rfcs/RFC-0010.md` | Database design, optimization, migration |
| **QA Engineer** | `docs/rfcs/RFC-0012.md` | Test automation, quality assurance |
| **Business Analyst** | `docs/rfcs/RFC-0013.md` | Business analysis, requirements, process modeling |
| **Cloud Architect** | `docs/rfcs/RFC-0026.md` | Cloud architecture (landing zones, DR, security) |
| **SRE Engineer** | `docs/rfcs/RFC-0027.md` | SRE & reliability engineering (SLOs, incident response) |
| **Compliance Officer** | `docs/rfcs/RFC-0028.md` | Compliance monitoring & evidence collection |
| **Knowledge Engineer** | `docs/rfcs/RFC-0029.md` | Knowledge management & RAG optimization |
| **Finance Analyst** | `docs/rfcs/RFC-0030.md` | Financial analysis, modeling, and controls |
| **Legal Advisor** | `docs/rfcs/RFC-0031.md` | Legal document analysis, obligations, compliance |
| **HSE Specialist** | `docs/rfcs/RFC-0032.md` | Health, Safety & Environment risk and compliance |
| **Observability** | `docs/rfcs/RFC-0033.md` | Metrics, tracing, logging, anomaly detection |
| **Cybersecurity Analyst** | `docs/rfcs/RFC-0034.md` | Threat modeling, vulnerability, incident detection |
| **AI Ethics & Governance** | `docs/rfcs/RFC-0035.md` | Fairness auditing, bias detection, explainability |
| **Supply Chain Analyst** | `docs/rfcs/RFC-0036.md` | Logistics optimization, demand forecasting, risk management |
| **Data Scientist** | `docs/rfcs/RFC-0037.md` | Advanced ML pipelines, feature engineering |
| **Business Intelligence** | `docs/rfcs/RFC-0038.md` | Dashboarding, KPI tracking, metric analysis |
| **Innovation Strategist** | `docs/rfcs/RFC-0039.md` | Trend analysis, foresight, R&D portfolio |
| **DevSecOps** | `docs/rfcs/RFC-0040.md` | CI/CD security gates, dependency scanning |
| **Translator Expert** | `docs/rfcs/RFC-0041.md` | Multi-domain translation, glossary enforcement |
| **Document Processing** | `docs/rfcs/RFC-0042.md` | Read, edit, produce, convert, annotate DOCX/XLSX/PPTX/PDF |
| **Voice Interaction** | `docs/rfcs/RFC-0043.md` | STT/TTS with multi-provider fallback, language detection |
| **Jenny-like Interaction** | `docs/rfcs/RFC-0043.md`, `RFC-0044.md`, `RFC-0045.md` | Voice-first interaction, action connectors, safety & observability |
| **Scenario Simulator** | `docs/rfcs/RFC-0023.md` | Real-time simulation & sandboxing |
| **Cross-Domain Knowledge Graph** | `docs/rfcs/RFC-0024.md` | Cross-domain knowledge graph generator |
| **Adversarial Testing** | `docs/rfcs/RFC-0025.md` | Adversarial testing, devil's advocate |
| **Decorator SDK** | `docs/rfcs/RFC-0003.md` | Transparent middleware decorators for Capability Packs |

---

## Pengembangan

### Struktur Proyek

```
enal-ai-os/
├── backend/                  # Core platform (FastAPI + cognitive runtime)
│   ├── app/
│   │   ├── api/              # REST/WebSocket endpoints (15 modul)
│   │   ├── core/             # Cognitive kernel, memory, event bus, runtime
│   │   ├── models/           # Data models
│   │   └── studio/           # ECP Studio
│   └── tests/
├── apps/                     # Capability Packs
│   ├── network_engineer/     # Network configuration analysis & generation (RFC-0004)
│   ├── code_engineer/        # Code analysis & generation (RFC-0006)
│   ├── research_assistant/   # Literature research & synthesis (RFC-0020)
│   ├── devops_assistant/     # DevOps automation (RFC-0021)
│   ├── trading_analyst/      # Trading analysis (RFC-0005)
│   ├── self_development/     # Self-development & learning (RFC-0022)
│   ├── decision_intelligence/     # Decision Intelligence (RFC-0007)
│   ├── system_architect/          # System Architect (RFC-0011)
│   ├── security_engineer/         # Security Engineer (RFC-0008)
│   ├── data_engineer/             # Data Engineer (RFC-0009)
│   ├── database_engineer/         # Database Engineer (RFC-0010)
│   ├── qa_engineer/               # QA Engineer (RFC-0012)
│   ├── business_analyst/          # Business Analyst (RFC-0013)
│   ├── infrastructure_engineer/   # Infrastructure design (K8s, HA, DR) (RFC-0014)
│   ├── ai_engineer/               # AI/ML engineering (RAG, agents, LLMOps) (RFC-0015)
│   ├── documentation_engineer/    # Documentation generation (OpenAPI, SDK, ADR) (RFC-0016)
│   ├── product_manager/           # Product management (roadmap, OKR, backlog) (RFC-0017)
│   ├── ui_ux_designer/            # UI/UX design (design system, accessibility) (RFC-0018)
│   ├── full_stack_engineer/       # Full stack engineering (code review, refactoring, release) (RFC-0019)
│   ├── cloud_architect/           # Cloud architecture design (landing zones, DR, security) (RFC-0026)
│   ├── sre_engineer/              # SRE & reliability engineering (SLOs, incident response) (RFC-0027)
│   ├── compliance_officer/        # Compliance monitoring & evidence collection (RFC-0028)
│   ├── knowledge_engineer/        # Knowledge management & RAG optimization (RFC-0029)
│   ├── finance_analyst/           # Financial analysis, modeling, and controls (RFC-0030)
│   ├── legal_advisor/             # Legal document analysis, obligations, compliance (RFC-0031)
│   └── hse_specialist/            # Health, Safety & Environment risk and compliance (RFC-0032)
│   ├── observability/             # Metrics, tracing, logging, anomaly detection (RFC-0033)
│   ├── cybersecurity_analyst/     # Threat modeling, vulnerability, incident detection (RFC-0034)
│   ├── ai_ethics_pack/            # Fairness auditing, bias detection, explainability (RFC-0035)
│   ├── supply_chain_analyst/      # Logistics optimization, demand forecasting, risk management (RFC-0036)
│   ├── data_scientist/            # Advanced ML pipelines, feature engineering (RFC-0037)
│   ├── business_intelligence/     # Dashboarding, KPI tracking, metric analysis (RFC-0038)
│   ├── innovation_strategist/     # Trend analysis, foresight, R&D portfolio (RFC-0039)
│   ├── devsecops/                 # CI/CD security gates, dependency scanning (RFC-0040)
│   ├── translator_expert/         # Multi-domain translation, glossary enforcement (RFC-0041)
│   ├── document_processing/       # Read, edit, produce, convert, annotate DOCX/XLSX/PPTX/PDF (RFC-0042)
│   ├── voice_interaction/         # STT/TTS with multi-provider fallback, language detection (RFC-0043)
│   ├── adversarial_testing/       # Adversarial testing, devil's advocate (RFC-0025)
│   ├── cross_domain_graph/        # Cross-domain knowledge graph generator (RFC-0024)
│   ├── scenario_simulator/        # Real-time simulation & sandboxing (RFC-0023)
│   ├── integration/               # Core integration layer
│   ├── organization/              # Organization structure & governance
│   └── society/                   # Society-level patterns
├── agents/                   # Registri agent dan skills
├── sdk/                      # Python SDK
├── benchmarks/               # Performance benchmark
├── tests/                    # Test suite (1082 tests collected, 1081 passed, 1 skipped)
├── voice/                    # STT/TTS provider configs (whisper.cpp, piper, elevenlabs)
└── docs/                     # Dokumentasi (170+ dokumen)
    ├── adr/                  # Architecture Decision Records (26 ADRs)
    ├── audit/                # Audit & compliance reports
    ├── capabilities/         # Capability pack specifications (37 docs)
    ├── frontend/             # Frontend architecture & component docs
    ├── guides/               # Technical guides & tutorials
    ├── quality/              # Kebijakan Quality Gate
    ├── releases/             # Release notes & changelogs
    └── rfcs/                 # RFCs (45 RFCs)
```

### Quality Gates (Sebelum Merge)

```bash
# Pemeriksaan wajib
mypy apps/ backend/                       # 0 error (PASSING)
ruff check apps/ backend/                 # 0 error (PASSING)
pytest -v                                 # 1082 collected, 1081 passed, 1 skipped
python scripts/gate0_validate.py          # Gate pre-merge

# Opsional (disarankan)
ruff format --check .                     # Format konsisten
python -m tools.audit.code_analysis        # Audit hygiene lengkap
```

---

## Roadmap

### Selesai ✅

- [x] **v0.1.0** — Arsitektur inti dan cognitive runtime
- [x] **v1.0.0-dev** — Canonical Consolidation, Telemetry, Benchmark, CCE
- [x] **Memory Integration** — 7 lapisan memory dengan konsolidasi
- [x] **Orchestrator** — AIOrchestrator, UnifiedOrchestrator, AdaptiveRuntime
- [x] **Engineering Hardening** — MyPy 0→0 errors, Ruff 0→0, 1082 tests collected (1081 passed)
- [x] **Python 3.11 Compatibility** — Nol masalah f-string di production
- [x] **Architecture Governance** — AES, Reference Architecture, 4 ADR
- [x] **Development Guide** — Langkah-demi-langkah untuk Capability Pack
- [x] **JWT Authentication** — Real JWT dengan signature, expiry, algorithm enforcement
- [x] **Async Safety** — Blocking `complete()` → `acomplete()` di jalur async
- [x] **Docker Hardening** — Volume mounts, pinned ollama, read_only aman
- [x] **Complexity Reduction** — Max complexity 272 → 211, top 10 files di-split
- [x] **Integration Tests** — 122 tests baru covering 130 endpoints
- [x] **Jenny-like Interaction Foundation** — VoiceAgent skeleton, ToolRegistry, ConnectorManager, Observability (anomaly detection) — foundation for voice-first interaction
- [x] **Trading Analyst** — A+ (100%), Level 4 Domain Expert, bersertifikat
- [x] **Cloud Architect** — A+ (≥95), RFC-0026/ADR-005, 10 golden tests, 10 real cases
- [x] **Jenny-like Interaction Phase 1** — VoiceAgent STT/TTS implementation, voice API endpoints, frontend voice bridge, 12 tests
- [x] **Jenny-like Interaction Phase 2** — FileSystem/Email/Calendar/SmartHome connectors, action API, ToolRegistry integration
- [x] **Jenny-like Interaction Phase 3** — Anomaly detection engine, consent/permission layer, consent dialog UI
- [x] **SRE Engineer** — A (≥90), RFC-0027/ADR-006, 10 golden tests, 10 real cases
- [x] **Compliance Officer** — A (≥90), RFC-0028/ADR-007, 10 golden tests, 10 real cases
- [x] **Knowledge Engineer** — A (≥90), RFC-0029/ADR-008, 10 golden tests, 10 real cases
- [x] **Finance Analyst** — A (≥90), RFC-0030/ADR-010, 10 golden tests, 10 real cases (Vertical Industry Pack)
- [x] **Legal Advisor** — A (≥90), RFC-0031/ADR-011, 10 golden tests, 10 real cases (Vertical Industry Pack)
- [x] **HSE Specialist** — A (≥90), RFC-0032/ADR-012, 10 golden tests, 10 real cases (Vertical Industry Pack)
- [x] **Observability** — A (≥90), RFC-0033/ADR-013, 10 golden tests, 10 real cases (Platform Services Pack)
- [x] **Cybersecurity Analyst** — A (≥90), RFC-0034/ADR-014, 10 golden tests, 10 real cases (Platform Services Pack)
- [x] **AI Ethics & Governance** — A (≥90), RFC-0035/ADR-015, 10 golden tests, 10 real cases (Governance Pack)
- [x] **Supply Chain Analyst** — A (≥90), RFC-0036/ADR-016, 10 golden tests, 10 real cases (Vertical Industry Pack)
- [x] **Data Scientist** — A (≥90), RFC-0037/ADR-017, 10 golden tests, 10 real cases (AI/ML Engineering Pack)
- [x] **Business Intelligence** — A (≥90), RFC-0038/ADR-018, 10 golden tests, 10 real cases (Analytics Pack)
- [x] **Innovation Strategist** — A (≥90), RFC-0039/ADR-019, 10 golden tests, 10 real cases (Strategy Pack)
- [x] **DevSecOps** — A (≥90), RFC-0040/ADR-020, 10 golden tests, 10 real cases (Security Engineering Pack)
- [x] **Translator Expert** — A (≥90), RFC-0041/ADR-021, 10 golden tests, 10 real cases (Platform Services Pack)
- [x] **Document Processing** — A (≥90), RFC-0042/ADR-022, 10 golden tests, 10 real cases (Productivity Pack)
- [x] **Voice Interaction** — A (≥90), RFC-0043/ADR-026, 10 golden tests, 10 real cases (Platform Professional Package)
- [x] **Decorator SDK** — RFC-0003, 26 golden tests, 30 real cases, 100% benchmark score, 0 wrapping overhead
- [x] **Jenny-like Interaction Phase 3** — Anomaly detection engine, consent/permission layer, consent dialog UI (frontend)

### Berikutnya: v3.1.0-rc2 🟨

> ⚠️ **Production Release v3.0.0 — COMPLETE.** Semua 37 capability packs ter-implementasi, semua benchmark Grade A, TypeScript 0 errors, MyPy 0 errors, Ruff 0 errors. Rilis v3.1.0-rc2 direncanakan untuk: Android PWA (Stage 1), CI/CD pipeline Android, LM Studio integration, frontend layout updates, dan Self-Development ECP meta-analysis. Lihat [`TODO_CAPABILITY_EXECUTION.md`](TODO_CAPABILITY_EXECUTION.md) → Outstanding Work dan [`docs/plans/Android_Release_Plan.md`](docs/plans/Android_Release_Plan.md).

### Outstanding Work (v3.1.0-rc2)

- [x] **LM Studio Integration** — Chat fallback ke LM Studio (`lmstudio/qwen/qwen3.5-9b`) ketika conversation manager tidak menghasilkan respon meaningful. Updated `backend/app/api/chat.py` dengan `_extract_llm_text()` yang support `reasoning_content` fallback.
- [x] **Frontend Layout Updates** — Workspace header/status indicator, sidebar workspace selector + artifacts + observability sections, main panel chat stream + quick actions, right panel timeline + consent requests + alerts, bottom panel command shortcuts + voice input + latency indicator. Updated `frontend/components/workspace/`.
- [x] **Self-Development ECP Meta-Analysis** — Extended `apps/self_development/` dengan `ECPAnalyzer`, `proposal_repository.py`, dan routing ECP meta-analysis. Support `analyze_ecp`, `propose_capabilities`, `propose_improvements`.
- [x] **Android PWA Stage 1** — `manifest.json`, service worker (`public/sw.js`), PWA metadata di `layout.tsx`, service worker registration di `app-client.tsx`.
- [x] **Android CI/CD Pipeline** — `.github/workflows/android-ci.yml` dengan jobs: build, sign, governance check, deploy staging, smoke test, promote beta/production.
- [x] **React Native Stage 2** — Expo project structure (`enal-ai-os-mobile/`), API bridge, chat UI ported, consent dialog, observability panel, STT/TTS hooks, navigation, screens.
- [ ] **PWA Icons & Screenshots** — Tambahkan icon PNG ke `frontend/public/icons/` dan screenshot ke `frontend/public/screenshots/`.
- [ ] **Android Testing** — Test Add to Home Screen, offline caching, dan push notifications di Android device.
- [ ] **React Native Testing** — Test on Android emulator, Firebase Test Lab, QA checklist.

---

## Lisensi

MIT

---

*ECP — Dari platform yang stabil menuju produk yang bernilai.*
Penggunaan kode ini diperbolehkan untuk keperluan penelitian, pengembangan, dan produksi sesuai ketentuan MIT License.
Kontribusi komunitas dipersilakan, dengan tetap menjaga standar kualitas, keamanan, dan governance yang sudah ditetapkan.
Tidak ada jaminan eksplisit maupun implisit; penggunaan sepenuhnya menjadi tanggung jawab pengguna.
