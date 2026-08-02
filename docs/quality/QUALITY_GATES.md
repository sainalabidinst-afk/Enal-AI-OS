# Kebijakan Quality Gate — Platform Kognitif Enal

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi kualitas untuk QUALITY_GATES
<!-- DOCUMENT_METADATA_END -->

**Status:** 🟢 **Aktif**
**Berlaku untuk:** Semua pull request yang menuju ke cabang `main` atau `release/*`
**Penegakan:** Pipeline CI/CD (lihat `scripts/gate0_validate.py`)

---

## Tujuan

Dokumen ini mendefinisikan **standar tujuan minimum** yang harus dipenuhi setiap perubahan sebelum digabungkan ke dalam dasar kode produksi. Gerbang ini bersifat non-negotiable dan ditegakkan oleh CI/CD.

Tujuannya bukan untuk mencegah perubahan, tetapi untuk memastikan setiap perubahan dipertahankan atau meningkatkan dasar rekayasa.

---

## Gerbang Tabel

| # |Gerbang|Urutannya|Kerasnya|Penegakan|
|---|------|-------------|----------|-------------|
|1|**PySaya**|`0 errors` pada `apps/ backend/ benchmarks/ tests/ sdk/`|🔴 PEMBLOKIRAN|`mypy apps/ backend/ benchmarks/ tests/`|
|2|**Serat Kasar**|`0 blockers`. Peringatan harus dijustifikasi di deskripsi PR|🟡 PERINGATAN|`ruff check apps/ backend/`|
|3|**Format Ruff**|`0 file yang akan diformat ulang`|🟡 PERINGATAN|`ruff format --check apps/ backend/`|
|4|**Tes**|`≥95% tingkat kelulusan` (baseline: 426 lulus)|🔴 PEMBLOKIRAN|`pytest --tb=short -q`|
|5|**Uji Stabilitas**|Tes tidak stabil = pemblokiran. `--reruns 3` tidak boleh menyembunyikan kegagalan|🔴 PEMBLOKIRAN|`pytest --reruns 3 -q`|
|6|**API Kontrak**|Semua tanda tangan API publik harus kompatibel ke belakang|🔴 PEMBLOKIRAN|Tinjau manual + pemeriksa tipe|
|7|**ADR**|Perubahan arsitektur memerlukan ADR yang disetujui sebelum implementasi|🔴 PEMBLOKIRAN|Panduan Tinjau|
|8|**Tidak Ada Impor Melingkar**|`0` import sirkular baru|🟡 PERINGATAN|`ruff check --select RUF011`|
|9|**Tidak Ada Default yang Dapat Diubah**|`0` pelanggaran RUF012 baru|🟡 PERINGATAN|`ruff check --select RUF012`|
|10|**Tidak Ada Pengecualian Buta**|`except Exception:` baru memerlukan justifikasi eksplisit|🟡 PERINGATAN|Tinjau manual + `ruff check --select BLE001`|
|11|**Kompatibel dengan Python 3.11**|Tidak ada f-string backslash escape di kode produksi|🔴 PEMBLOKIRAN|Pindai `compile()` (lihat `tools/audit/`)|
|12|**Jenis Keamanan**|Tanpa komentar `type: ignore` tanpa alasan terdokumentasi|🟡 PERINGATAN|Panduan Tinjau|

---

## Detil Gerbang

### Gerbang 1 — MyPy (🔴 BLOKER)

```bash
python -m mypy apps/ backend/ benchmarks/ tests/
```

Tidak ada kesalahan yang diperlukan. `type: ignore` hanya diizinkan dengan komentar inline yang menjelaskan alasan:

```python
# type: ignore[attr-defined] — Vendor model does not expose this field
```

### Gerbang 2 — Ruff Lint (🟡 PERINGATAN)

```bash
python -m ruff check apps/ backend/
```

Jika ada warning, masing-masing harus dijustifikasi di deskripsi PR. Contoh pembenaran:

> "BLE001 di baris 142 dimaksudkan: ini adalah penangan tingkat atas yang harus menangkap semua isinya untuk mencegah kerusakan."

### Gerbang 4 — Tes (🔴 BLOKER)

```bash
python -m pytest --tb=short -q --coverage
```

Spesifikasi:
- ≥95% dari tes baseline harus lulus (baseline: 426)
- Kode baru harus menyertakan tes yang sesuai
- Cakupan tes tidak boleh turun di bawah 80% (keseluruhan)

### Gerbang 7 — ADR (🔴 PEMBLOKIRAN)

Perubahan arsitektur mencakup:
- Menambahkan modul inti baru
- Mengubah antarmuka bus acara
- Memodifikasi kontrak Capability Pack
- Mengganti komponen infrastruktur (database, cache, dll.)
- Mengubah model eksekusi Runtime

Ini memerlukan:
1. ADR disampaikan di `docs/adr/` sebelum implementasi dimulai
2. Penentu pandangan minimal satu (Kepala Arsitek, Insinyur Senior)
3. Status ADR : ✅ Diterima

---

## Proses Pengecualian

Gerbang mana pun dapat dikirimkan melalui **Permintaan Pengecualian**:

1. Buat terbitan dengan label `quality-gate-override`
2. Sertakan:
   - Gerbang yang dilanggar
   - Alasannya
   - Rencana mitigasi
   - Tanggal kedaluwarsa (jika sementara)
3. Membutuhkan persetujuan dari 2 penentu

**Tidak ada yang menuangkan** yang permanen. Semua pembawa acara harus memiliki jalur menuju keikutsertaan.

---

## Eskalasi

Jika sebuah gerbang menghalangi perbaikan kritis:

1. **Pertama:** Perbaiki masalah (lebih disukai)
2. **Kedua:** Permintaan Pengecualian Ajukan (sementara)
3. **Ketiga:** Eskalasi ke Kepala Arsitek

Hotfix kritis produksi boleh melewati gerbang hanya dengan persetujuan eksplisit dari 2 keputusan DAN harus diperbaiki secara retroaktif dalam 24 jam.

---

## Penegakan di CI/CD

Lihat `scripts/gate0_validate.py` untuk implementasi CI/CD.

Skrip saat ini memvalidasi:
- MyPy: 0 kesalahan
- ruff: pindai
- Koleksi tes

Tabel gate lengkap harus diimplementasikan di CI/CD sebagai prioritas engineering berikutnya setelah baseline freeze.

---

## Hubungan dengan Engineering Baseline

Dokumen ini memperluas Engineering Baseline (`docs/ENGINEERING_BASELINE.md`).

Baseline mendefinisikan **state** dasar kode pada saat freeze.
Gerbang kualitas mendefinisikan **proses** untuk mempertahankan keadaan di depannya.

Keduanya diperlukan untuk rekayasa tata kelola.
