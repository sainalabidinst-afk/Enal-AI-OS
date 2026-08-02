# Enal AI OS — Catatan Rilis v1.0.0-rc1

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk RELEASE_NOTES_v1.0.0-rc1
<!-- DOCUMENT_METADATA_END -->

**Tanggal Rilis:** 2026-07-31
**Tag:** v1.0.0-rc1
**Commit:** 22f581c927454f4577a37af2f5be9beb93b04904
**Branch:** main

---

## Pengamanan Keamanan

### Perbaikan Kritis
- **Command Injection**: Mengganti `asyncio.create_subprocess_shell` dengan `create_subprocess_exec` + `shlex.split` di sandbox runtime
- **SSRF Protection**: Menambahkan validasi URL di browser agent untuk memblokir rentang IP privat/internal (127.0.0.1, 10.x, 192.168.x, 172.16-31.x, 169.254.169.254)
- **Hardcoded Secrets Removed**: Menghapus password database default dari config.py dan docker-compose.yml; kredensial sekarang diinjeksikan via environment variables
- **Authentication Framework**: Menambahkan middleware autentikasi dengan perilaku fail-closed ketika SECRET_KEY tidak diatur
- **Rate Limiting**: Menambahkan rate limiter per-IP (100 permintaan/60 detik)
- **Security Headers**: Menambahkan HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy

### Otorisasi
- Menerapkan injeksi dependensi RBAC (`backend/app/core/auth.py`)
- Menghubungkan `require_permission()` ke endpoint workspace dan eksekusi
- Operasi sensitif sekarang menerapkan izin READ/WRITE/EXECUTE

### Pencatatan Audit
- Menambahkan `AuditLoggingMiddleware` untuk jejak audit tingkat permintaan
- Log mencakup: method, path, kode status, durasi, identitas pengguna

---

## Peningkatan Arsitektur

### Penyelesaian Import Melingkar
- Memperbaiki ketergantungan melingkar: `cognitive/__init__.py` → `adaptive_runtime.py` → `cognitive_kernel.py` → `cognitive/__init__.py`
- Menunda impor tingkat modul ke metode `__init__` jika diperlukan

### Batas Backend/Apps
- Mengonversi impor `from apps.*` tingkat atas menjadi impor malas di router API (`chat.py`, `trading.py`, `capability_discovery.py`)
- Menghormati batasan arsitektur: backend tidak boleh mengimpor apps saat waktu muat modul

### Pewakilan Kapabilitas
- Mengisi `apps/organization/__init__.py` dengan ekspor yang tepat
- Menambahkan `self_development` ke registry kapabilitas
- Memperbaiki pengkabelan trading analyst ke paket `market_intelligence`
- Memperbaiki impor integration orchestrator

### Suite Pengujian
- Menghapus file pengujian duplikat (`test_integration_api.py`)
- Menambahkan `httpx2` ke dependensi dev
- Memperbaiki path API pengujian untuk mencocokkan registrasi rute aktual
- **Hasil: 426 pengujian berhasil, 0 gagal**

---

## Penguatan DevOps

### Keamanan Docker
- **Backend**: Build multi-stage, pengguna non-root (`appuser`), permukaan serangan minimal
- **Frontend**: Build multi-stage, pengguna non-root (`nextjs`), output standalone Next.js
- **docker-compose.yml**:
  - Filesystem baca-saja untuk semua layanan
  - `tmpfs` untuk `/tmp` jika berlaku
  - `cap_drop: [ALL]` + `no-new-privileges:true`
  - Batas sumber daya (memori, CPU) per layanan
  - Kondisi healthcheck untuk `depends_on`
  - Menghapus password database hardcoded; menggunakan `${POSTGRES_PASSWORD}`

### CI/CD
- Skrip gate validasi ditambahkan (`scripts/validate_*.py`)
- Gate 0-4 mencakup baseline, keamanan, arsitektur, kapabilitas, validasi kognitif

---

## Perubahan API

### Perubahan yang Melanggar Kompatibilitas
- **Authentication**: Endpoint non-publik sekarang memerlukan header `Authorization: Bearer <token>` ketika `SECRET_KEY` diatur
- **Public Endpoints** (tidak memerlukan autentikasi):
  - `GET /`
  - `GET /health`
  - `/docs`, `/openapi.json`, `/redoc`

### Catatan Migrasi
- Atur environment variable `SECRET_KEY` untuk mengaktifkan autentikasi
- Tanpa `SECRET_KEY`, semua endpoint non-publik mengembalikan 401
- Klien yang ada harus diperbarui untuk mengirim Bearer token

---

## Keterbatasan yang Diketahui

1. **Authentication**: Implementasi saat ini berbasis token tetapi tidak memvalidasi tanda tangan JWT. Dimaksudkan untuk penggunaan pengembangan/internal.
2. **Rate Limiter**: Implementasi dalam memori; tidak cocok untuk deployment multi-instance tanpa status bersama (Redis).
3. **Audit Logging**: Mencatat ke stream log aplikasi; untuk produksi, integrasikan dengan logging terpusat (ELK, Loki, dll.).
4. **Placeholder Capabilities**: `research_assistant`, `self_development`, `devops_assistant` tetap menjadi implementasi yang disimulasikan/dummy.

---

## Panduan Upgrade

### Dari Versi Sebelumnya
1. Atur environment variable yang diperlukan: `SECRET_KEY`, `DATABASE_URL`, `POSTGRES_PASSWORD`
2. Perbarui klien API untuk menyertakan header `Authorization: Bearer <token>`
3. Tinjau dan perbarui kebijakan RBAC sesuai kebutuhan
4. Deploy dengan gambar Docker baru (multi-stage, non-root)

### Rollback
- Kembalikan ke tag sebelumnya: `git checkout <previous-tag>`
- Redeploy gambar Docker sebelumnya
- Tidak ada perubahan skema database di rilis ini

---

## Hasil Validasi

| Gate | Status |
|------|--------|
| Gate 0 — Baseline Freeze | PASS |
| Gate 1 — Security Hardening | PASS |
| Gate 2 — Architecture Convergence | PASS |
| Gate 3 — Capability Wiring | PASS |
| Gate 4 — Cognitive Validation | PASS |

**Hasil Pengujian:** 426 berhasil, 0 gagal
**Status Build:** Siap untuk containerisasi
**Scan Keamanan:** Masalah P0 terselesaikan; masalah P1 didokumentasikan
