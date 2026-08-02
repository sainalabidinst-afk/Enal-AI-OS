# Enal AI OS — Prosedur Rollback v1.0.0-rc1

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk ROLLBACK_PROCEDURE
<!-- DOCUMENT_METADATA_END -->

## Ringkasan

Dokumen ini mendefinisikan prosedur rollback yang telah diuji untuk Enal AI OS v1.0.0-rc1.
Jika terjadi kegagalan deployment atau masalah kritis, ikuti prosedur ini untuk memulihkan layanan ke versi stabil sebelumnya.

---

## Prasyarat

- Tag stabil sebelumnya tersedia (misalnya, `v0.9.0` atau commit hash sebelum `22f581c`)
- Gambar Docker untuk versi sebelumnya tersedia di registry
- Cadangan database dari sebelum deployment
- Load balancer / reverse proxy dikonfigurasi untuk pergantian tanpa downtime

---

## Opsi Rollback

### Opsi A: Rollback Cepat (Redeploy Container)

**Kapan digunakan:** Masalah tingkat aplikasi, tidak melibatkan migrasi data

**Langkah-langkah:**
1. Identifikasi tag stabil sebelumnya: `git tag -l "v*" | sort -V | tail -n 2`
2. Tarik gambar Docker sebelumnya:
   ```bash
   docker pull enal-ai-os-backend:<previous-tag>
   docker pull enal-ai-os-frontend:<previous-tag>
   ```
3. Perbarui tag gambar docker-compose.yml ke versi sebelumnya
4. Redeploy stack:
   ```bash
   docker compose up -d --force-recreate
   ```
5. Verifikasi kesehatan:
   ```bash
   curl -f http://localhost:8000/health
   curl -f http://localhost:3001/
   ```
6. Pantau log selama 5 menit:
   ```bash
   docker compose logs -f backend frontend
   ```

**Perkiraan Waktu:** 5-10 menit

---

### Opsi B: Rollback Penuh (Termasuk Database)

**Kapan digunakan:** Masalah migrasi database, kerusakan data, atau kegagalan sistem lengkap

**Langkah-langkah:**
1. Hentikan semua layanan:
   ```bash
   docker compose down
   ```
2. Pulihkan database dari cadangan:
   ```bash
   # Contoh menggunakan pg_restore
   pg_restore -U postgres -d enal_ai_os /backups/enal_ai_os_<date>.dump
   ```
3. Reset keadaan aplikasi (jika berlaku):
   ```bash
   # Kosongkan cache Redis jika diperlukan
   docker compose up -d redis
   docker compose exec redis redis-cli FLUSHALL
   ```
4. Deploy versi sebelumnya (lihat Langkah-langkah Opsi A 1-4)
5. Jalankan smoke tests:
   ```bash
   python scripts/validate_baseline.py
   ```
6. Verifikasi integritas data:
   - Periksa record kritis ada
   - Verifikasi sesi pengguna/workspace dapat diakses
   - Uji kapabilitas inti (chat, eksekusi, workspace)

**Perkiraan Waktu:** 15-30 menit

---

## Pohon Keputusan Rollback

```
Deployment Issue Detected
├── Health checks failing
│   ├── Backend unhealthy → Option A
│   └── Database unavailable → Option B
├── Application error rate > 5%
│   └── Option A
├── Data inconsistency detected
│   └── Option B
└── Security incident
    └── Option B + incident response
```

---

## Verifikasi Pasca-Rollback

Setelah rollback, verifikasi:
- [ ] Semua layanan sehat (`docker compose ps`)
- [ ] Endpoint kesehatan mengembalikan 200
- [ ] Tidak ada lonjakan error di log
- [ ] Konektivitas database terkonfirmasi
- [ ] Perjalanan pengguna inti berfungsi:
  - [ ] Chat/Conversation
  - [ ] Manajemen workspace
  - [ ] Eksekusi/Run Agen
  - [ ] Analisis trading (jika berlaku)
- [ ] Frontend dapat diakses dan komunikasi API berfungsi

---

## Komunikasi

Selama rollback:
1. Beri tahu pemangku kepentingan tentang insiden dan inisiasi rollback
2. Perbarui halaman status jika berlaku
3. Dokumentasi timeline insiden
4. Setelah stabilisasi, lakukan post-mortem

---

## Versi Sebelumnya

| Tag | Commit | Tanggal | Catatan |
|-----|--------|---------|---------|
| v1.0.0-rc1 | 22f581c | 2026-07-31 | Release candidate saat ini |
| v0.9.0 | (sebelumnya) | - | Versi stabil produksi terakhir |

---

## Kontak

- **On-Call Engineer:** (definisi di runbook Anda)
- **DevOps Lead:** (definisi di runbook Anda)
- **Security Contact:** (definisi di runbook Anda)
