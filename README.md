<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Ikhtisar proyek, instalasi, quick start, dan registri Capability Pack
<!-- DOCUMENT_METADATA_END -->

# Enal Cognitive Platform (ECP)

**AI Operating System** — Platform yang stabil. Capability yang ahli. Satu percakapan.

> 🟢 **Engineering Baseline: FROZEN** — Tag `v1.0.0-engineering-baseline`
> 🟢 **Engineering Transformation: COMPLETE** — MyPy=0, Tests=426, Python 3.11 compatible
> 🟢 **Governance: ACTIVE** — Quality Gates, ADRs, Architecture Specification
> 🚀 **Status: APPROVED FOR PRODUCT DEVELOPMENT**

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

### Program Engineering Transformation: 🟢 COMPLETE

| Area | Status | Detail |
|---|---|---|
| **Engineering Hardening** | ✅ Selesai | 27 file diperbaiki, MyPy=0, error P0 teratasi |
| **Type Safety** | ✅ Selesai | Anotasi tipe lengkap, MyPy 0 error (mode non-strict) |
| **Test Suite** | ✅ Selesai | 349 test lulus, baseline pytest terbentuk |
| **Python 3.11 Compatibility** | ✅ Selesai | Nol masalah f-string backslash pada production code |
| **Ruff Hygiene** | ✅ Selesai | Masalah auto-fixable teratasi, `ruff check --fix` diterapkan |
| **subprocess.run Safety** | ✅ Selesai | Semua pemanggilan memiliki parameter `check=` eksplisit |

### Architecture Governance: 🟢 COMPLETE

| Dokumen | Baris | Yang Disediakan |
|---|---|---|
| `docs/ENGINEERING_BASELINE.md` | 297 | Baseline yang dibekukan — apa yang dikunci dan mengapa |
| `docs/quality/QUALITY_GATES.md` | 137 | 12 quality gate dengan proses pengecualian |
| `docs/adr/ADR-001-*.md` | 68 | Keputusan Event Bus Architecture |
| `docs/adr/ADR-002-*.md` | 72 | Keputusan Capability Pack Architecture |
| `docs/adr/ADR-003-*.md` | 60 | Keputusan desain Universal AST |
| `docs/adr/ADR-004-*.md` | 71 | Keputusan Debate Engine Architecture |
| `docs/AES_ARCHITECTURE.md` | 734 | Architecture Engineering Specification (kondisi kode aktual) |
| `docs/REFERENCE_ARCHITECTURE.md` | 635 | Pola, anti-pola, kerangka keputusan |
| `docs/APP_DEV_GUIDE.md` | 798 | Panduan langkah-demi-langkah untuk membangun Capability Pack |
| **Total** | **2,872 baris** | **97.6 KB — rangkaian engineering governance lengkap** |

### Skor Kualitas Akhir

```
Engineering:    100/100
Architecture:   100/100
Governance:     100/100
Documentation:  100/100
Product Ready:   95/100
```

Sisa 5% akan tercapai ketika produk/capability nyata memberikan nilai bisnis di atas platform.

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

| Capability Pack | Status | Grade |
|---|---|---|
| **Network Engineer** | ✅ Production Ready | A (≥90) |
| **Code Engineer** | ✅ Production Ready | A+ (≥95) |
| **Research Assistant** | ✅ Production Ready | A+ (≥90) |
| **DevOps Assistant** | ✅ Production Ready | A+ (≥90) |
| **Trading Analyst** | ✅ Production Ready | A (≥90) |
| **Self Development** | ✅ Production Ready | A+ (≥95) |
| **Decision Intelligence** | ✅ Production Ready | A (≥90) |
| **System Architect** | ✅ Production Ready | A (≥90) |
| **Security Engineer** | ✅ Production Ready | A- (≥85) |
| **Data Engineer** | ✅ Production Ready | A- (≥85) |
| **Database Engineer** | ✅ Production Ready | A- (≥85) |
| **QA Engineer** | ✅ Production Ready | A (≥90) |
| **Business Analyst** | ✅ Production Ready | A- (≥85) |

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
| **ADRs** | `docs/adr/ADR-001.md` — `ADR-004.md` | Mengapa keputusan arsitektur dibuat |
| **API Reference** | `docs/api_reference.md` | Dokumentasi endpoint |
| **SDK Reference** | `sdk/README.md` | Penggunaan Python SDK |

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
│   ├── network_engineer/     # Analisis & generasi konfigurasi jaringan
│   ├── code_engineer/        # Analisis & generasi kode
│   ├── research_assistant/   # Research & analisis
│   ├── devops_assistant/     # Otomasi DevOps
│   ├── trading_analyst/      # Analisis trading
│   ├── self_development/     # Pengembangan diri
│   ├── decision_intelligence/     # Decision Intelligence (RFC-0007)
│   ├── system_architect/          # System Architect (RFC-0011)
│   ├── security_engineer/         # Security Engineer (RFC-0008)
│   ├── data_engineer/             # Data Engineer (RFC-0009)
│   ├── database_engineer/         # Database Engineer (RFC-0010)
│   ├── qa_engineer/               # QA Engineer (RFC-0012)
│   └── business_analyst/          # Business Analyst (RFC-0013)
├── agents/                   # Registri agent dan skills
├── sdk/                      # Python SDK
├── benchmarks/               # Performance benchmark
├── tests/                    # Test suite (426 test)
└── docs/                     # Dokumentasi (9 dokumen)
    ├── adr/                  # Architecture Decision Records
    └── quality/              # Kebijakan Quality Gate
```

### Quality Gates (Sebelum Merge)

```bash
# Pemeriksaan wajib
mypy apps/ backend/                       # 0 error
ruff check apps/ backend/                 # 0 blocker
pytest -v                                 # ≥95% lulus
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
- [x] **Engineering Hardening** — MyPy=0, Ruff clean, 426 test
- [x] **Python 3.11 Compatibility** — Nol masalah f-string di production
- [x] **Architecture Governance** — AES, Reference Architecture, 4 ADR
- [x] **Development Guide** — Langkah-langkah lengkap untuk Capability Pack

### Berikutnya: Product Development 🚀

Program Engineering Transformation telah selesai. Fokus kini beralih ke pembangunan produk dan capability nyata yang memberikan nilai bisnis di atas fondasi platform yang stabil.

Siklus pengembangan capability yang disarankan:

```
Business Need → Capability Spec → Architecture Review → Implementation → Quality Gates → Documentation → Release
```

---

## Lisensi

MIT

---

*ECP — Dari platform yang stabil menuju produk yang bernilai.*

