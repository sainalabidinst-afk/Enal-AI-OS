# Laporan Audit Dependency

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
<!-- DOCUMENT_METADATA_END -->

**Tanggal:** 2026-08-02
**Cakupan:** Packaging backend + konsistensi dependency + penyelarasan CI/Makefile/Dockerfile

---

## 1. Packaging Backend

| Item | Status |
|------|--------|
| `backend/pyproject.toml` | ✅ Dibuat |
| `backend/__init__.py` | ✅ Dibuat |
| Build backend | Pip |
| Dependency development | pytest, pytest-asyncio, ruff, black, mypy |
| Dependency runtime | FastAPI, uvicorn, sqlalchemy, qdrant-client, redis, pydantic, pydantic-settings, litellm, langchain-openai, langchain-core, httpx, pyyaml, aiohttp, python-multipart, psycopg2-binary |

---

## 2. Penggunaan Modul vs Deklarasi

| Modul | Status | Tindakan |
|--------|--------|--------|
| `fastapi` | ✅ Oke | Digunakan di `main.py`, `api/*` |
| `uvicorn` | ✅ Oke | Digunakan di Dockerfile, Makefile |
| `sqlalchemy` | ✅ Oke | Digunakan di `db/session.py` |
| `qdrant-client` | ✅ Oke | Digunakan di `core/vector_store.py` |
| `redis` | ✅ Oke | Digunakan di `core/memory.py`, `core/memory_layer.py`, `core/event_bus.py` |
| `pydantic` | ✅ Oke | Digunakan di `models/schemas.py` |
| `pydantic-settings` | ✅ Oke | Digunakan di `core/config.py` |
| `litellm` | ✅ Oke | Digunakan di `core/model_router.py` |
| `langchain-openai` | ✅ Oke | Digunakan di `agents/core/executor_agent.py` |
| `langchain-core` | ✅ Oke | Digunakan di `agents/core/*` |
| `httpx` | ✅ Oke | Digunakan di `core/benchmark/runner.py` |
| `pyyaml` | ✅ Oke | Digunakan di `core/skill_registry.py` |
| `python-multipart` | ⚠️ Tidak langsung | Diperlukan oleh FastAPI untuk `UploadFile`/`File`/`Form`; tidak ada `import multipart` langsung yang ditemukan |
| `aiohttp` | ⚠️ Belum terpakai | Dideklarasikan tetapi tidak ditemukan import langsung |
| `psycopg2-binary` | ⚠️ Belum terpakai | Dideklarasikan tetapi tidak ditemukan import langsung (driver abstrak SQLAlchemy) |

### Dependency yang Dideklarasikan Tidak Digunakan

| Dependency | Tindakan |
|------------|--------|
| `aiohttp` | Hapus dari `backend/pyproject.toml` |
| `psycopg2-binary` | Simpan atau hapus — SQLAlchemy tidak memerlukan import psycopg2 langsung, tetapi driver PostgreSQL tetap diperlukan di Runtime. Direkomendasikan: simpan untuk dukungan Postgres yang eksplisit. |

---

## 3. Pemeriksaan Import Circular

| Pola | Status |
|---------|--------|
| `cognitive/__init__.py` → `adaptive_runtime.py` → `cognitive_kernel.py` → `cognitive/world_model.py` | ✅ Rantai linier, bukan lingkaran |
| `meta_cognition.py` → `adaptive_runtime.py` → `cognitive_kernel.py` | ✅ Rantai linier, bukan lingkaran |
| `core/__init__.py` | ✅ Kosong — tidak ada efek samping import |
| Import `backend.app.*` tingkat atas | ✅ Tidak ada dependency circular yang terdeteksi |

**Kesimpulan:** Tidak ada import circular yang terdeteksi di antara import modul tingkat atas.

---

## 4. Struktur Paket

| Path | Status |
|------|--------|
| `backend/__init__.py` | ✅ Ada |
| `backend/app/__init__.py` | ✅ Ada |
| `backend/app/core/__init__.py` | ✅ Ada |
| `backend/app/api/__init__.py` | ✅ Ada |
| `backend/app/agents/__init__.py` | ✅ Ada |
| `backend/app/models/__init__.py` | ✅ Ada |
| `backend/app/db/__init__.py` | ✅ Ada |
| `backend/tests/__init__.py` | ✅ Ada |

---

## 5. Penyelarasan CI/Makefile/Dockerfile

| File | Masalah | Tindakan |
|------|-------|--------|
| `.github/workflows/ci.yml` | Hanya menginstal root `.[dev]` tetapi menjalankan test backend/mypy | ✅ Diperbaiki — ditambahkan `pip install -e backend/` |
| `Makefile` | Menggunakan `poetry install` tetapi backend tidak memiliki `pyproject.toml` | ✅ Diperbaiki — diganti dengan `pip install -e ".[dev]"` |
| `backend/Dockerfile` | Menggunakan `poetry install` dengan backend hatchling build | ✅ Diperbaiki — diganti dengan `pip install -e ".[dev]"` |
| `docker-compose.yml` | Tidak ada konteks `build` untuk service backend | ⚠️ Dapat diterima — service menjalankan image bawaan atau dev server lokal |
| Root `pyproject.toml` | Paket `enal-cognitive-platform` didefinisikan tanpa kode yang sebenarnya | ✅ Diperbaiki — diubah menjadi metadata khusus workspace |

---

## 6. Dependency Graph yang Dibersihkan

```
core
├── fastapi
├── uvicorn[standard]
├── pydantic
├── pydantic-settings
└── python-multipart

ai
├── litellm
├── langchain-openai
└── langchain-core

database
├── sqlalchemy
└── psycopg2-binary

queue
└── redis

vector
└── qdrant-client

telemetry
└── httpx

config
└── pyyaml

dev
├── pytest
├── pytest-asyncio
├── ruff
├── black
└── mypy
```

---

## 7. Tindakan yang Direkomendasikan

1. **Hapus `aiohttp` dari `backend/pyproject.toml`** — tidak ditemukan penggunaan langsung.
2. **Evaluasi ulang `psycopg2-binary`** — simpan jika akses driver PostgreSQL langsung direncanakan; jika tidak, hapus untuk mengurangi ukuran image.
3. **Jalankan `pip install -e backend/` di semua task CI yang mengimpor kode backend** — sudah diperbaiki.
4. **Verifikasi Docker build** — jalankan `docker build backend` setelah perubahan.
5. **Tambahkan verifikasi import langsung `python-multipart`** — pastikan endpoint upload file FastAPI tercakup dalam pengujian.

---

## 8. Sprint Berikutnya

Lanjutkan ke **Penyelesaian MVP Frontend** dengan dependency graph backend yang stabil dan telah diaudit.

