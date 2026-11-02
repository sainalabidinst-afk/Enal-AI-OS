<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Canonical Owner:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-11-02
**Versi:** v3.1.0-rc1
**Status:** Aktif
**SSOT:** Ikhtisar proyek, setup pengembangan, dan navigasi dokumentasi
<!-- DOCUMENT_METADATA_END -->

# Enal AI OS

Enal AI OS (Enal Cognitive Platform/ECP) adalah platform modular untuk
membangun dan menjalankan aplikasi AI berbasis capability pack. Repositori ini
mencakup backend API, layanan runtime dan orkestrasi, aplikasi domain, web
frontend, SDK, serta klien mobile.

> **Versi repositori:** `v3.1.0-rc1`. Status rilis dan kesiapan deployment dapat
> berubah; jalankan pemeriksaan pada branch dan environment yang akan digunakan.

## Gambaran arsitektur

```text
Web / mobile clients
        │
        ▼
FastAPI backend ── API, auth, chat, execution, workspace
        │
        ▼
Core runtime ───── orchestration, memory, events, tools
        │
        ▼
Capability packs ─ domain-specific application logic
        │
        ▼
Database, cache, vector store, and model providers
```

Komponen dapat dijalankan bersama melalui Docker Compose atau dikembangkan
secara terpisah. Integrasi yang dibutuhkan bergantung pada fitur yang dijalankan;
misalnya database, Redis, vector store, dan penyedia model mungkin memerlukan
konfigurasi tersendiri.

## Struktur repositori

| Direktori / file | Isi |
|---|---|
| `backend/app/` | FastAPI application, API routes, core runtime, dan konfigurasi |
| `apps/` | Capability packs dan logika aplikasi domain |
| `frontend/` | Web frontend |
| `enal-ai-os-mobile/` | Klien mobile berbasis React Native |
| `enal-ai-os-android/` | Klien Android native |
| `sdk/` | Python SDK |
| `tests/`, `backend/tests/` | Test suite |
| `docs/` | Panduan, referensi API, arsitektur, dan catatan audit |
| `docker-compose.yml` | Definisi layanan lokal berbasis Docker Compose |
| `pyproject.toml` | Metadata paket Python, dependensi, pytest, Ruff, dan MyPy |

## Persyaratan

- Python 3.11 atau lebih baru.
- Node.js dan npm untuk menjalankan web frontend secara terpisah.
- Docker Desktop dengan Docker Compose untuk menjalankan stack lengkap.
- Kredensial atau layanan eksternal hanya untuk fitur yang memerlukannya.

## Menjalankan aplikasi

### Opsi 1: Docker Compose

Salin konfigurasi contoh, lalu sesuaikan nilainya sebelum menjalankan layanan.
Jangan gunakan kredensial contoh untuk deployment dan jangan commit file `.env`.
Sebelum menjalankan backend, isi `SECRET_KEY` dengan nilai acak minimal 32
karakter dan konfigurasi akun operator. Hash password dibuat dengan prompt
tersembunyi:

```powershell
Copy-Item .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(48))"
python .\backend\app\core\passwords.py
docker compose up --build
```

Masukkan hash yang dicetak ke `AUTH_ACCOUNT` dalam `.env`, misalnya:

```text
AUTH_ACCOUNT={"username":"admin","password_hash":"<hash>","roles":["admin"],"permissions":["model:read","read","execute","capabilities:execute"]}
```

Tidak ada akun/password bawaan. Berikan hanya permission yang diperlukan.

Alamat default:

- Web frontend: <http://localhost:3001>
- Dokumentasi API: <http://localhost:8000/docs>

Gunakan `docker compose ps` untuk memeriksa layanan yang berjalan dan
`docker compose logs -f <nama-layanan>` untuk melihat log layanan tertentu.

### Opsi 2: Backend lokal

Buat environment Python, pasang dependensi proyek, lalu jalankan API:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Untuk Linux atau macOS, aktifkan environment dengan:

```bash
source .venv/bin/activate
```

Pastikan layanan eksternal yang diperlukan oleh konfigurasi aktif tersedia
sebelum menguji endpoint yang menggunakannya.

### Web frontend secara terpisah

```powershell
Set-Location frontend
npm install
npm run dev
```

Secara default, frontend mengirim request ke `/api` pada origin yang sama.
Next.js meneruskan request tersebut ke `http://localhost:8000`; Docker Compose
mengatur target internal `http://backend:8000`. Untuk target lain, atur
`NEXT_API_PROXY_URL` saat build. `NEXT_PUBLIC_API_URL` dapat diisi saat build
bila frontend memang perlu mengakses API secara langsung; nilai publik Next.js
ditanam ke bundle ketika dibangun.

## Pemeriksaan dan test

Jalankan perintah dari root repositori:

```bash
# Seluruh test yang dikonfigurasi untuk pytest
python -m pytest tests/ backend/tests/ -q

# Test kontrak stabil
python -m pytest tests/test_stable_contract_*.py -v

# Lint dan pemeriksaan tipe
python -m ruff check apps/ backend/
python -m mypy apps/ backend/
```

Test yang memerlukan service eksternal mungkin membutuhkan environment lokal
yang sudah dikonfigurasi. Tinjau output test dan jangan menganggap hasil audit
atau log lama sebagai status terbaru.

## Dokumentasi

- [Panduan memulai](docs/getting_started.md)
- [Panduan setup](SETUP_GUIDE.md)
- [Arsitektur](docs/AES_ARCHITECTURE.md)
- [Panduan pengembangan capability pack](docs/APP_DEV_GUIDE.md)
- [Referensi API](docs/api_reference.md)
- [Audit menyeluruh](docs/audit/COMPREHENSIVE_AUDIT.md)
- [Panduan kontribusi](CONTRIBUTING.md)
- [Kebijakan keamanan](SECURITY.md)
- [Dokumentasi SDK](sdk/README.md)

## Kontribusi

Sebelum mengirim perubahan:

1. Ikuti panduan di [CONTRIBUTING.md](CONTRIBUTING.md).
2. Tambahkan atau perbarui test untuk perilaku yang berubah.
3. Jalankan lint dan test yang relevan.
4. Perbarui dokumentasi yang terdampak.

## Lisensi

Proyek ini menggunakan lisensi MIT sebagaimana dinyatakan di `pyproject.toml`.
