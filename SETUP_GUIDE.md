# ECP Environment Setup Guide

**Platform**: Windows 10/11  
**Python**: 3.11.9 ✓  
**Project**: Enal Cognitive Platform (ECP) v1.0.0-engineering-baseline

---

## Status Setup Saat Ini

✅ **Python 3.11.9** - Terdeteksi  
✅ **Virtual Environment** - Dibuat di `e:\Enal-AI-OS\.venv`  
⚠️ **PIP Install** - Timeout (mungkin karena network/koneksi lambat)  
❌ **Docker** - Tidak terinstall

---

## Langkah 1: Aktivasi Virtual Environment

### Windows (PowerShell)
```powershell
e:\Enal-AI-OS\.venv\Scripts\Activate.ps1
```

### Windows (CMD)
```cmd
e:\Enal-AI-OS\.venv\Scripts\activate.bat
```

**Verifikasi:**
```powershell
python --version  # Harus menampilkan Python 3.11.x
pip --version     # Harus menampilkan pip dari .venv
```

---

## Langkah 2: Install Dependencies

### Opsi A: Install Backend & SDK (Recommended)

```powershell
# Install Backend dengan dev dependencies
pip install -e "backend/[dev]"

# Install SDK
pip install -e sdk/
```

**Catatan:** Jika terjadi timeout, coba:
```powershell
# Dengan timeout lebih panjang
pip install --timeout 120 -e "backend/[dev]"
pip install --timeout 120 -e sdk/
```
### Opsi B: Install Manual (Jika Editable Install Gagal)

```powershell
# Install backend dependencies
pip install fastapi>=0.109.0 uvicorn[standard]>=0.27.0 sqlalchemy>=2.0.0
pip install qdrant-client>=1.7.0 redis>=5.0.0 pydantic>=2.6.0 pydantic-settings>=2.0.0
pip install litellm>=1.40.0 langchain-openai>=0.1.0 langchain-core>=0.1.0
pip install httpx>=0.26.0 pyyaml>=6.0 aiohttp>=3.9.0 python-multipart>=0.0.9
pip install psycopg2-binary>=2.9.0 PyJWT>=2.8.0

# Install dev tools
pip install pytest>=8.0.0 pytest-asyncio>=0.23.0 ruff>=0.4.0 black>=24.4.0 mypy>=1.8.0

# Install SDK
pip install pydantic>=2.6.0 aiohttp>=3.9.0 asyncio>=3.4.3
```

---

## Langkah 3: Setup Environment Variables

### Buat file `.env` dari template

```powershell
Copy-Item .env.example .env
```

### Edit file `.env` dan isi dengan nilai yang sesuai:

```env
# Database
POSTGRES_PASSWORD=your_secure_password_here
DATABASE_URL=postgresql://postgres:your_secure_password_here@localhost:5432/enal_ai_os

# Security (Generate dengan: python -c "import secrets; print(secrets.token_urlsafe(32))")
SECRET_KEY=your_generated_secret_key_here

# LLM Providers (Opsional - untuk testing)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
GEMINI_API_KEY=...

# Observability (Opsional)
---

## Langkah 5: Jalankan Services dengan Docker Compose

### Start Services
```powershell
docker compose up -d
```

### Verifikasi Services Running
```powershell
docker compose ps
```

**Expected Output:**
```
NAME                IMAGE                    STATUS
enal-ai-os-postgres-1   postgres:16-alpine    running
enal-ai-os-redis-1      redis:7-alpine        running
enal-ai-os-qdrant-1     qdrant/qdrant:v1.9.0 running
enal-ai-os-ollama-1     ollama/ollama:0.1.26 running
```

### Check Logs (jika ada error)
```powershell
docker compose logs -f
```

---

## Langkah 6: Verifikasi Environment (Quality Gates)

### 6.1 Type Safety Check (MyPy)
```powershell
mypy apps/ backend/
```
**Target:** 0 Error

### 6.2 Linter & Style Check (Ruff)
```powershell
ruff check apps/ backend/
```
**Target:** 0 Blocker

### 6.3 Run Test Suite
```powershell
pytest -v
```
**Target:** ≥95% Pass (166 tests)

---

## Troubleshooting

### Issue: pip install timeout
**Solusi:**
```powershell
# Gunakan timeout lebih panjang
pip install --timeout 300 -e backend/

# Atau install tanpa cache
pip install --no-cache-dir -e backend/

# Atau gunakan mirror (jika network lambat)
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -e backend/
```

### Issue: Docker tidak terdeteksi
**Solusi:**
1. Install Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Restart komputer setelah install
3. Pastikan Docker Desktop berjalan sebelum menjalankan `docker compose up`

### Issue: Port sudah dipakai
**Solusi:** Edit `docker-compose.yml` dan ganti port mapping:
```yaml
postgres:
  ports:
    - "5544:5432"  # Ganti dari 5543
redis:
  ports:
    - "6391:6379"  # Ganti dari 6390
```

### Issue: PostgreSQL connection refused
**Solusi:**
1. Tunggu 10-15 detik setelah `docker compose up -d`
2. Check health: `docker compose ps`
3. Pastikan postgres status adalah `healthy`
### 6.4 Pre-Merge Quality Gate
```powershell
python scripts/gate0_validate.py
```
**Target:** All gates PASSED

---

## Quick Start Checklist

- [ ] Python 3.11+ terinstall
- [ ] Virtual environment dibuat dan diaktifkan
- [ ] Backend & SDK terinstall (editable mode)
- [ ] File `.env` dibuat dan dikonfigurasi
- [ ] Docker Desktop terinstall dan berjalan
- [ ] `docker compose up -d` berhasil
- [ ] Semua services healthy
- [ ] `mypy apps/ backend/` = 0 error
- [ ] `ruff check apps/ backend/` = 0 blocker
- [ ] `pytest -v` ≥95% pass
- [ ] `python scripts/gate0_validate.py` all gates passed

---

## Next Steps

Setelah environment setup selesai:

1. **Buat branch baru** untuk fitur:
   ```powershell
   git checkout -b feat/nama-fitur-anda
   ```

2. **Baca dokumentasi inti:**
   - `README.md` - Ikhtisar ECP
   - `docs/ENGINEERING_BASELINE.md` - Aturan yang dibekukan
   - `docs/AES_ARCHITECTURE.md` - Arsitektur sistem
   - `docs/quality/QUALITY_GATES.md` - 12 syarat mutlak

3. **Mulai development** dengan mengikuti SOP onboarding

---

## Support

Jika mengalami kendala:
1. Check logs: `docker compose logs -f`
2. Verifikasi docker: `docker info`
3. Check network: `ping google.com`
4. Review dokumentasi di folder `docs/`

**Status Engineering Baseline:** 🟢 FROZEN - v1.0.0  
**Status Governance:** 🟢 ACTIVE  
**Approved For:** Product Development
### 6.5 Format Check
```powershell
ruff format --check .
```
LANGCHAIN_TRACING_V2=false
```

**Generate SECRET_KEY:**
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Langkah 4: Install Docker Desktop (Wajib)

### Download & Install
1. Kunjungi: https://www.docker.com/products/docker-desktop/
2. Download Docker Desktop untuk Windows
3. Install dan restart komputer
4. Jalankan Docker Desktop

### Verifikasi
```powershell
docker --version
docker compose --version
```