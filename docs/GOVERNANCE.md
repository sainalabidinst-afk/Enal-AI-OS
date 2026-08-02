<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Aturan operasional, proses ADR, Aturan Kapabilitas Pertama, Pembekuan Arsitektur
<!-- DOCUMENT_METADATA_END -->

# Tata Kelola ECP — Aturan Operasional

**Versi:** 1.0.0
**Status:** Diratifikasi
**Berlaku:** 08-01-2026
**Otoritas:** Kepala Arsitek
**Induk:** `GOVERNANCE_CHARTER.md`
**Tujuan:** Aturan operasional yang harus dipenuhi oleh semua RFC, ADR, Capability Pack, dan rilis.

---

## 1. Aturan Pertama Kemampuan

> **Tidak ada perubahan Core yang diizinkan hanya untuk meningkatkan satu Capability Pack.**

- Jika satu Capability Pack membutuhkan perilaku yang berbeda, perubahan harus tetap berada di dalam Capability Pack tersebut.
- Jika 2 atau lebih Capability Pack membutuhkan perilaku yang sama, sebuah ADR dapat dikeluarkan dengan bukti dari kedua paket.
- Perubahan Core memerlukan persetujuan ADR dan bukti lintas-capability.

---

## 2. Tidak Ada Mesin Baru Tanpa Use Case

Setiap mesin, modul, atau abstraksi baru harus:

1. Dipilih setidaknya dua Capability Pack.
2. Memiliki Golden Test kasus.
3. Didokumentasikan dalam dokumentasi arsitektur.

Jika tidak ada Capability Pack yang membaik, tidak ada Benchmark yang meningkat, dan tidak ada perjalanan yang menjadi lebih baik — **jangan dibangun**.

---

## 3. Kebijakan Pembekuan Arsitektur

> **Core hanya dapat berubah jika semua hal berikut terpenuhi:**

| # |Kondisi|Bukti|
|---|-----------|----------|
|1|Digunakan oleh setidaknya dua Capability Pack|Dokumen bukti kemampuan lintas|
|2|Memiliki ADR yang disetujui|ADR di `docs/adr/` + entri di `ARCHITECTURE_DECISIONS.md`|
|3|Lulus Benchmark|Hasil Benchmark disimpan di `benchmarks/`|
|4|Uji regresi Lulus|Seluruh test suite hijau (CI/CD)|

**Proses perubahan Inti:**

1. Identifikasi perubahan Core yang dibutuhkan.
2. Dokumentasikan Capability Pack mana saja yang mendesak.
3. Jika kurang dari 2 paket yang mendesak → perubahan tersebut milik Capability Pack, bukan Core.
4. Jika 2+ paket memenuhi → ajukan RFC dengan test case dari kedua paket.
5. RFC diterima → ajukan ADR dengan analisis dampak.
6. ADR disetujui → diimplementasikan dengan bukti Benchmark + regresi.
7. Gabungkan hanya setelah kondisi keempat Architecture Freeze terpenuhi.

**Secara eksplisit dilarang tanpa proses di atas:**

- Menambahkan Runtime, Planner, Kernel, atau Layer arsitektur baru.
- Memodifikasi Core untuk meningkatkan satu Capability Pack.
- Melanggar kontrak Core tanpa masa tenggang 2 rilis dan panduan migrasi.

---

## 4. Stabilitas Kernel

Kernel (`backend/app/core/`) harus:

- Tetap di bawah 5.000 baris kode.
- Tidak memiliki ketergantungan eksternal selain stdlib + pydantic.
- Mempertahankan kontrak yang kompatibel ke belakang.
- Lulus semua tes pada setiap commit.

---

## 5. Kemerdekaan Capability Pack

Capability Pack **tidak boleh mengimpor mesin Capability Pack lain secara langsung.

Semua komunikasi lintas-pack mengalir melalui **Execution Runtime dan kontrak bersama saja**.

**Dilarang:**

```python
# DILARANG
from apps.trading_analyst import engine as trading_engine
trading_engine.analyze(...)
```

**Diizinkan:**

```python
# DIIZINKAN
task = {
    "domain": "research",
    "intent": "Analyze market sentiment for AAPL",
}
result = await execution_runtime.execute(task)
```

---

## 6. Catatan Keputusan Arsitektur (ADR)

- Semua keputusan arsitektur yang signifikan memerlukan ADR.
- ADR berada di `docs/adr/` dan dirangkum dalam `ARCHITECTURE_DECISIONS.md`.
- Perubahan pada ADR yang memerlukan:
  - Proses RFC dengan periode peninjauan yang diperpanjang
  - Rencana migrasi untuk semua komponen yang terdampak
  - Persetujuan oleh otoritas arsitektur proyek

### Apa yang Membutuhkan ADR

- Menambahkan Runtime baru
- Menambahkan Planner baru
- Menambahkan Kernel baru
- Menambahkan Layer arsitektur baru
- Memodifikasi Core untuk alasan apa pun

Semuanya memerlukan: bukti lintas-capability (≥2 pack), RFC dengan analisis dampak, dan persetujuan otoritas arsitektur.

---

## 7. Penegakan Tata Kelola di CI/CD

CI/CD harus memblokir penggabungan yang melanggar tata kelola:

|Pemeriksaan|Gagal Ketika|
|-------|------------|
|Tes Arsitektur|Batas paket (paket mengimpor paket mesin lain secara langsung)|
|Penjaga Perubahan Inti|Core dimodifikasi tanpa ADR yang disetujui dan dirujuk|
|Pemeriksaan Referensi ADR|Perubahan yang berdampak pada banyak paket yang tidak memiliki ADR|
|Benchmark Gerbang|Skor Benchmark di bawah ambang batas paket|
|Ujian Emas|Golden Test suite di bawah ambang lulus|

**Kebijakan Penggabungan:** Semua pemeriksaan harus lulus. Tanpa mengungkapkan.

---

## 8.Kemampuan Changelog

Setiap Capability Pack memelihara changelog-nya sendiri. Changelog mencatat penambahan pengetahuan, peningkatan Benchmark, dan peningkatan penalaran. Changelog **tidak** mencatat perubahan Core.

### Format

```markdown
## <Capability Pack> v<version>

### Added
- <knowledge/topic>

### Improved
- <aspek>

### Fixed
- <masalah>

### Benchmark
- <dimensi>: <sebelum> → <sesudah>
```

### Contoh

```markdown
## Network v1.1

### Added
- BGP path selection analysis
- MPLS forwarding rules
- IPv6 dual-stack patterns

### Improved
- Kedalaman penjelasan firewall
- Akurasi risk scoring: 85% → 92%

### Fixed
- VLAN false positive pada trunk interface

### Benchmark
- Accuracy: 89% → 92%
- Explainability: B → A-
```

---

## 9. Penanganan Pengecualian

Setiap aturan yang disampaikan dalam dokumen ini harus dikirimkan sebagai RFC, ditinjau, dan disetujui oleh otoritas arsitektur. Pengecualian dicatat dalam log ADR dan dokumen ini diperbarui sesuai.

---

## 10. Persetujuan

|Peran|Status|Tanggal|
|------|--------|------|
|Kepala Arsitek|Disetujui|01-08-2026|
