# Rencana Komprehensif: Sinkronisasi Dokumentasi dengan Kondisi Aktual Proyek

## Informasi Terkumpul

Setelah membaca 50+ file proyek (dokumentasi, kode backend, frontend, konfigurasi, dan laporan), ditemukan **18+ ketidaksesuaian** antara dokumentasi dan kondisi aktual kode. Proyek telah melalui restrukturisasi monorepo, peningkatan test count, perubahan API, dan perubahan arsitektur yang belum tercermin dalam dokumentasi.

## Rencana Perbaikan

### Fase 1: Perbaikan Data Numerik & Statistik (KRITIS)

#### 1.1 Update Test Count di Semua Dokumen
- **Dokumen yang perlu diupdate:**
  - `README.md` — baris "368 tests passing" → "426 tests passing"
  - `docs/ENGINEERING_BASELINE.md` — baseline test count
  - `docs/quality/QUALITY_GATES.md` — Gate 4 baseline
  - `docs/AES_ARCHITECTURE.md` — test count references
  - `docs/architecture.md` — test count
  - `sdk/README.md` — "368 tests passing"
  - `docs/REFERENCE_ARCHITECTURE.md` — jika ada referensi
- **Aktual:** 426 test passing (diverifikasi dari `_test_output.txt`)

#### 1.2 Update Versi & Status Proyek
- **File:** `README.md`
- **Perubahan:** Status dari "Engineering Transformation: COMPLETE" → sesuaikan dengan status aktual RELEASE v1.0.0-rc1
- **Cek:** `VERSION`, `RELEASE/RELEASE_NOTES_v1.0.0-rc1.md`

### Fase 2: Perbaikan API Documentation (KRITIS)

#### 2.1 Sinkronisasi API Reference dengan Route Aktual
- **File:** `docs/api_reference.md`
- **Ketidaksesuaian ditemukan:**
  1. **Auth header**: Dokumen bilang `X-API-Key`, backend aktual pakai `Authorization: Bearer`
  2. **GET /chat** route tidak ada di backend (`main.py`) — hanya ada `POST /api/v1/chat`
  3. **Endpoint /conversations/{conversation_id}** tidak ada di backend
  4. **Endpoint /cognitive/process** ada di `phase3.py` prefix `/api/v1`, bukan `/cognitive/process`
  5. **Endpoint /organization** ada di `phase3.py` prefix `/api/v1`
  6. **Endpoint /marketplace/publish** dll ada di `ecosystem.py` prefix `/api/v1`
  7. **Endpoint /studio/traces** dll ada di `ecosystem.py` prefix `/api/v1`
  8. **Endpoint /cognitive/decide** ada di `phase3.py`
  9. **Endpoint /longtasks** ada di `phase3.py`
  10. **Endpoint /evaluation/benchmarks** ada di `phase3.py`
  11. **WebSocket endpoints** tidak diverifikasi keberadaannya
- **Tindakan:** Cocokkan setiap endpoint dengan kode aktual di `backend/app/api/` dan `main.py`

#### 2.2 Update Route Prefix Documentation
- **Base URL:** `docs/api_reference.md` bilang `/api/v1` — sudah benar
- **Tapi endpoint paths tidak konsisten:** beberapa pakai prefix `/api/v1` via FastAPI, beberapa tidak
- **Aktual:** Semua route terdaftar via `settings.API_V1_STR` = `/api/v1`

### Fase 3: Perbaikan Arsitektur & Infrastruktur (MODERAT)

#### 3.1 Update Infrastruktur Layer
- **File:** `docs/AES_ARCHITECTURE.md`, `docs/architecture.md`, `docker-compose.yml`
- **Ketidaksesuaian:**
  1. **MinIO** disebut di diagram arsitektur `docs/architecture.md` tapi **tidak ada** di `docker-compose.yml`
  2. **Qdrant** ada di docker-compose tapi tidak semua diagram menyertakannya
  3. Opsi: Hapus MinIO dari diagram arsitektur, atau tambahkan issue untuk implementasi MinIO

#### 3.2 Update Docker Configuration Docs
- **File:** `frontend/Dockerfile`
- **Temuan:** Ada workaround `network: host` untuk BuildKit sandbox — tidak didokumentasi
- **Tindakan:** Tambahkan komentar/penjelasan di dokumentasi deployment

#### 3.3 Update Memory Layer Count
- **File:** `docs/architecture.md` bilang "6 memory layers"
- **File:** `docs/AES_ARCHITECTURE.md` bilang "7 memory layers" (termasuk Project)
- **Aktual:** `cognitive_kernel.py` panggil 7 layer via `memory_manager`
- **Tindakan:** Sinkronkan jumlah memory layer di semua dokumen

### Fase 4: Perbaikan Frontend Documentation (MODERAT)

#### 4.1 Update Component Library
- **File:** `docs/frontend/COMPONENT_LIBRARY.md`
- **Ketidaksesuaian:**
  1. **ProgressCard** — komponen ini tidak ditemukan di `frontend/components/`
  2. **WorkspaceSidebar** — tidak ditemukan, yang ada adalah `main-layout.tsx`
  3. **ChatWindow** — tidak ditemukan, yang ada adalah `chat-window.tsx`
  4. **LoadingIndicator** — tidak ditemukan, yang ada adalah `loading-skeleton.tsx`
  5. **NotificationToast** — tidak ditemukan, yang ada adalah `toast.tsx`
  6. **ApprovalDialog** — ada `approval-dialog.tsx` di `ui/`
- **Tindakan:** Update COMPONENT_LIBRARY.md sesuai komponen yang benar-benar ada

#### 4.2 Update UI Architecture
- **File:** `docs/frontend/UI_ARCHITECTURE.md`
- **Ketidaksesuaian:**
  1. Store slices: dokumen bilang conversationSlice, workspaceSlice, executionSlice, artifactSlice, notificationSlice, settingsSlice
  2. **Aktual:** Yang ditemukan di `frontend/store/` hanya `auth-store.ts`, `execution-store.ts`, `workspace-store.ts`
  3. Screen flow: dokumen bilang `/chat` route, tapi aktual root `/` redirect ke `/dashboard` atau `/login`
  4. **Route `/chat`** tidak ada di routing frontend — halaman utama adalah `/dashboard`
- **Tindakan:** Update UI_ARCHITECTURE.md dan SCREEN_FLOW.md sesuai routing aktual

#### 4.3 Update Screen Flow
- **File:** `docs/frontend/SCREEN_FLOW.md`
- **Ketidaksesuaian:**
  1. Routing table bilang `/` → Chat, tapi aktual `/` → redirect ke `/dashboard` atau `/login`
  2. Screen `/chat` tidak ada di routing aktual
  3. Screen `/executions/:executionId` — tidak ada di routing aktual (pakai query param `?selected=`)
  4. Screen `/artifact/:artifactId` — tidak ada di routing aktual
  5. Entry point "User clicks 'New Chat'" tidak relevan karena tidak ada route `/chat`
- **Tindakan:** Update SCREEN_FLOW.md sesuai routing aktual frontend

### Fase 5: Perbaikan Release & Capability Documentation (MINOR)

#### 5.1 Update RELEASE_MANIFEST.md
- **File:** `RELEASE_MANIFEST.md`
- **Ketidaksesuaian:**
  1. Hanya menyebut Network Engineer, padahal ada 6 capability packs
  2. Tidak menyebut frontend, SDK, benchmarks
  3. Versi perlu disinkronkan
- **Tindakan:** Update dengan semua capability packs, frontend, SDK

#### 5.2 Update Capability Pack Status
- **File:** `README.md`, `docs/v1_roadmap.md`
- **Ketidaksesuaian:**
  1. Dokumen bilang "5 reference applications" tapi `apps/__init__.py` punya 7 apps
  2. Status capability packs: Network Engineer disebut "Production Ready", Trading "Certification Pending"
  3. RELEASE_MANIFEST.md hanya menyebut Network Engineer dengan 30 cases
- **Tindakan:** Sinkronkan jumlah apps dan status capability packs

#### 5.3 Update CI/CD Documentation
- **File:** `docs/quality/QUALITY_GATES.md`, `docs/v1_roadmap.md`
- **Ketidaksesuaian:**
  1. Dokumen klaim CI/CD pipeline aktif, tapi tidak ada konfigurasi CI/CD ditemukan (no `.github/`, no `.gitlab-ci.yml`)
  2. `scripts/gate0_validate.py` ada tapi hanya untuk validasi pre-merge lokal
  3. Quality Gates bilang enforcement di CI/CD tapi CI/CD tidak ada
- **Tindakan:** Klarifikasi bahwa quality gates adalah pre-merge manual, bukan CI/CD otomatis

### Fase 6: Perbaikan Dokumentasi Getting Started

#### 6.1 Update Getting Started Guide
- **File:** `docs/getting_started.md`
- **Ketidaksesuaian:**
  1. Contoh kode `pip install -e .` tidak akan work karena `pyproject.toml` ada di `backend/`
  2. Command untuk backend: `pip install -e backend/`
  3. Contoh agen `enal_ai` — SDK mungkin tidak terinstal dengan cara itu
  4. Path impor `backend.app.agents.orchestrator_v2` — perlu diverifikasi
- **Tindakan:** Update contoh kode sesuai struktur monorepo aktual

#### 6.2 Update Agent Guide
- **File:** `docs/agent_guide.md`
- **Perlu dibaca** untuk verifikasi konsistensi dengan SDK aktual

### Fase 7: Perbaikan Dokumentasi SDK

#### 7.1 Update SDK README
- **File:** `sdk/README.md`
- **Ketidaksesuaian:**
  1. Bilang "368 tests passing" → perlu update ke 426
  2. Contoh kode pakai `enal_ai` — perlu diverifikasi apakah SDK benar-benar punya `Agent`, `EnalAI`, `Tool`, `Workflow`
  3. "Platform RC (2026-07-27)" — tanggal perlu diverifikasi
- **Tindakan:** Update test count dan verifikasi contoh kode

### Fase 8: Validasi & Testing

#### 8.1 Validasi Akhir
- Jalankan ulang validasi impor untuk memastikan semua path yang disebut di dokumentasi valid
- Pastikan tidak ada broken link internal di dokumentasi
- Verifikasi bahwa endpoint yang didokumentasikan benar-benar ada di kode

#### 8.2 Update Inventaris Dokumentasi
- Update `docs/ENGINEERING_BASELINE.md` "Document Inventory" section
- Update `README.md` "Documentation Suite" table

## File yang Perlu Diubah

### Prioritas Tinggi (KRITIS):
1. `README.md` — test count, status, capability packs
2. `docs/api_reference.md` — auth, routes, endpoints
3. `docs/ENGINEERING_BASELINE.md` — test count, status
4. `docs/quality/QUALITY_GATES.md` — test baseline, CI/CD clarification
5. `docs/AES_ARCHITECTURE.md` — test count, infrastructure
6. `docs/architecture.md` — infrastructure layer, memory layers

### Prioritas Sedang (MODERAT):
7. `docs/frontend/COMPONENT_LIBRARY.md` — actual components
8. `docs/frontend/UI_ARCHITECTURE.md` — actual store slices, routes
9. `docs/frontend/SCREEN_FLOW.md` — actual routing
10. `sdk/README.md` — test count
11. `docs/getting_started.md` — installation commands, code examples

### Prioritas Rendah (MINOR):
12. `RELEASE_MANIFEST.md` — complete capability packs
13. `docs/v1_roadmap.md` — app count, status
14. `docs/v1_sprint_plan.md` — status updates
15. `docs/baseline_freeze.md` — status verification

## Langkah Tindak Lanjut

1. ✅ Setujui rencana ini
2. Implementasi Fase 1 (data numerik) — perubahan langsung
3. Implementasi Fase 2 (API docs) — perubahan langsung
4. Implementasi Fase 3-5 (arsitektur, frontend, release) — perubahan langsung
5. Implementasi Fase 6-7 (getting started, SDK) — perubahan langsung
6. Validasi akhir — jalankan pengecekan

## Catatan

- Semua perubahan harus backward compatible dengan dokumentasi
- Tidak ada perubahan kode yang diperlukan — hanya perubahan dokumentasi
- Setiap perubahan harus mencerminkan kondisi aktual kode saat ini
- Gunakan prinsip "document what exists, not what was planned"
