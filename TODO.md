# TODO — Resolusi Temuan Audit (Menuju Skor 100%)

## Informasi yang Dikumpulkan
- Repo Enal Cognitive Platform (ECP) dengan 19-22 Capability Pack, Core frozen, ADR 1-14.
- Temuan audit: (1) duplikasi VERY_COMPLEX di adaptive_runtime.py, (2) 173 `except Exception`, (3) discrepansi test count, (4) duplikasi nomor apps/__init__.py, (5) BaseApp vs BaseReferenceApp, (6) test full_stack tipis, (7) contoh async/sync di docs, (8) real_cases kosong.

## Plan

### P0 — Bug Kode
- [x] Perbaiki duplikasi VERY_COMPLEX di `backend/app/core/adaptive_runtime.py`
- [x] Perbaiki ikon `BaseApp` vs `BaseReferenceApp` (rendering konsisten ke `BaseApp` dengan alias)

### P1 — Dokumentasi Sinkron dengan Aktual
- [ ] Perbaiki duplikasi nomor di `apps/__init__.py` docstring
- [ ] Perbaiki contoh penggunaan sync→async di `docs/capabilities/full-stack-engineer.md`
- [ ] Update `AUDIT_COMPREHENSIVE_FINAL.md` dengan status resolusi semua temuan
- [ ] Update README/CHANGELOG/VERSION_MATRIX agar konsisten

### P2 — Kualitas
- [ ] Perkuat `tests/test_full_stack_engineer.py` dengan test engine nyata
- [ ] Kurangi `except Exception` luas di titik kritikal

### Verifikasi
- [ ] Jalankan pytest untuk konfirmasi test count aktual
- [ ] Update skor ke 100% pada dokumen audit
