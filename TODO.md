# TODO — Pembersihan & Konsolidasi Dokumentasi

> Status: **In Progress** — Disetujui 2026-08-03

## Langkah

### 1. Konsolidasi ke `docs/audit/`
- [x] Merge 4 laporan audit → `docs/audit/AUDIT_REPORT.md`
- [x] Merge 3 laporan kualitas → `docs/audit/QUALITY_REPORTS.md`
- [x] Merge 3 laporan sprint → `docs/audit/SPRINT_REPORTS.md`
- [x] Merge 3 laporan konsistensi → `docs/audit/CONSISTENCY_REPORTS.md`

### 2. Hapus dokumen usang
- [x] Hapus `PLAN_DOKUMENTASI_CONSISTENCY.md`
- [x] Hapus `PLAN_RFC-0007.md`, `PLAN_RFC-0011.md`
- [x] Hapus `TODO_DOKUMENTASI_INDONESIA.md`
- [x] Hapus `RELEASE_MANIFEST.md`, `RELEASE_NOTES_v1.0.md`
- [x] Hapus `ENGINEERING_BASELINE.md` (root, duplikat)

### 3. Hapus kode debug/testing (root)
- [x] Hapus 24 file `_*.py` dan file output `_*.txt`
- [x] Hapus `scan_results.txt`, `docs_ci_report.txt`

### 4. Sinkronisasi dokumen
- [x] Update `VERSION_MATRIX.md` (test count 426, pack 13)
- [x] Update `README.md` (test count, status CI, audit script path)
- [x] Update `docs/audit/README.md` (indeks)

### 5. Validasi
- [ ] Jalankan import check / pytest collection
- [ ] Verifikasi tidak ada broken reference
