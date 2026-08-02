# Catatan Rilis v1.0.0-dev Product Intelligence

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi rilis
<!-- DOCUMENT_METADATA_END -->

**Tanggal Rilis:** 14-07-2026
**Tonggak Pencapaian:** Kecerdasan Produk
**Kode Nama:** Kemampuan Benchmark + Kecerdasan Berkualitas

## Ringkasnya

Rilis ini mengubah Enal AI OS dari platform analisis konfigurasi menjadi platform AI Quality Engineering. Sistem kini mengukur kualitas kemampuannya sendiri melalui telemetri, benchmarking, penilaian kemampuan, deteksi regresi, dan kalibrasi kepercayaan.

## Yang Berubah

### Bagian belakang

- **Kerangka Telemetri**: Kumpulan peristiwa berbasis JSONL untuk analisis peristiwa, dialog, parser, dan penalaran. Layanan agregasi KPI menghitung tingkat izin, cakupan bukti, cakupan, tingkat positif palsu, dan lainnya.
- **Benchmark Framework**: `BenchmarkRunner` async dengan koneksi pool `httpx.AsyncClient`, kontrol konkurensi `asyncio.Semaphore` (default 5), dan protokol `ProgressCallback` untuk kemajuan real-time.
- **Capability Scoring**: kemampuan perincian per kasus dalam 5 dimensi: parser, Reasoning, Evidence, Compliance, dan Executive Report. Setiap dimensi diberi skor 0-100, dirata-rata menjadi total skor kemampuan.
- **Hasil Emas yang Diharapkan**: Kasus Benchmark kini mendukung `expected.json` dengan temuan yang diharapkan yang terstruktur, ambang batas risiko/keyakinan, dan memenuhi target. Direktori kasus mengikuti pola `sample_hotspot/` dengan `config.rsc`, `expected.json`, `report.md`, dan `metadata.yaml`.
- **CCE API**: `POST /api/v1/benchmark/run` kini mengembalikan `capability_score` dan `capability_breakdown` per hasil. `GET /api/v1/benchmark/capability-scores` mengagregasi per vendor. `GET /api/v1/benchmark/cce/status` menampilkan status CCE terbaru dengan peringatan regresi dan kalibrasi data.

### Modul Baru

- `benchmarks/cce.py` — Pelari Evaluasi Kemampuan Berkelanjutan. Mengeksekusi rangkaian Benchmark lengkap, menghitung skor kemampuan, mendeteksi regresi terhadap run/baseline sebelumnya, menjalankan kalibrasi kepercayaan, menyimpan riwayat, dan menghasilkan laporan HTML.
- `benchmarks/trend_analyzer.py` — Analisis tren dan deteksi regresi. Menghitung arah tren per-vendor (`up`/`down`/`stable`) dan menandai regresi ketika skor kemampuan turun ≥5 poin.
- `benchmarks/calibration.py` — Penganalisis kalibrasi kepercayaan. Mengelompokkan hasil berdasarkan skor kepercayaan dan menghitung akurasi empiris per bin, mendeteksi overconfident dan underconfident.
- `benchmarks/report_generator.py` — Pembuat dasbor HTML. Menghasilkan laporan visual dengan tabel kemampuan kinerja, peringatan regresi, tabel kalibrasi keyakinan, dan indikator tren bergaya CSS.

### CI/CD

- `.github/workflows/cce.yml` — CCE otomatis pada setiap push/PR ke `main`. Membuat build gagal saat deteksi regresi. Mengunggah laporan HTML sebagai artefak. URL Keluaran GitHub Badge.

### Data

- `real_cases/mikrotik/sample_hotspot/` — Kasus nyata pertama dengan hasil yang diharapkan, laporan, dan metadata.
- `benchmarks/cce_history/` — Penyimpanan riwayat CCE yang dihasilkan saat Runtime (gitignored).

## Catatan Migrasi

- `BenchmarkRunner._load_expected()` kini mencari `expected.json` di dalam direktori kasus terlebih dahulu, lalu jatuh kembali ke format legacy `<filename>.expected.json`.
- `BenchmarkRunner._load_case_content()` mendukung jalur absolut dan jalur relatif `real_cases/<vendor>/<filename>`.
- `BenchmarkResult` kini termasuk `capability_score` dan `capability_breakdown`.
- `ExpectedResult.from_dict()` mendukung format penyimpanan `{"expected": {...}, "metadata": {...}}`.

## Validasi

- Semua modul Benchmark lolos serat `ruff`.
- Semua impor terverifikasi.
- Rangkaian tes yang ada: 74 lulus, 18 gagal (sudah ada sebelumnya, tidak terkait rilis ini).

## Langkah Berikutnya

- Kampanye Keunggulan Kapabilitas: menaikkan setiap skor kapabilitas ke target KPI.
- Evaluasi Kemampuan Berkelanjutan (CCE) masuk ke alur kerja pengembangan harian.
- Periode dogfooding 30 hari dengan kasus dunia nyata.
- Pratinjau Pengembang dengan gerbang kualitas CCE aktif.
