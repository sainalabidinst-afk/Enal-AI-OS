# RFC-0042: Document Processing Capability Pack

|Bidang|Nilai|
|-------|-------|
|**ID RFC**|RFC-0042|
|**Status**|Draft|
|**Versi**|0.1.0|
|**Penulis**|Tim Inti AI OS Akhir|
|**Target Rilis**|v3.0.0 (Platform Professional)|
|**Capability Pack**|Document Processing|
|**ID Kemampuan**|`document-processing`|
|**Kategori**|Proses Dokumen / Productivity|
|**Target Kualitas**|A (≥90)|
|**Target Kematangan**|Level 3 — Siap Produksi|
|**Referensi RFC**|RFC-0042|

---

## Motivasi

ECP saat ini menghasilkan dan menganalisis dokumen teknis, namun tidak ada Capability Pack yang fokus
untuk membaca, mengedit, dan memproduksi file Office (DOCX, XLSX, PPTX) serta PDF. Banyak workflow
domain — legal (kontrak), finance (laporan keuangan), technical (spesifikasi dokumen) — memerlukan
transformasi dokumen nyata: parsing, edit, konversi, dan generasi.

Saat ini:

1. **Tidak ada pipeline dokumen terpusat** — setiap pack yang membutuhkan proses dokumen harus
   mengimplementasikan sendiri parser Writer/PDF, menyebabkan duplikasi.
2. **Konversi format (Word → PDF, Excel → CSV) dilakukan secara manual** atau dengan alat eksternal
   yang tidak terintegrasi dengan ECP.
3. **Metadata dokumen (author, version, subject) tidak divalidasi** secara sistematis.
4. **Annotation (komentar, highlight) dan watermark tidak terstandardisasi** — setiap pack
   menggunakan pendekatan berbeda.
5. **Tidak ada batch processing adapter** untuk operasi dokumen massal.
6. **Tidak ada lazy-import strategy** untuk dependency opsional (python-docx, openpyxl, PyPDF2).

Capability Pack Document Processing menjadi lapisan dokumen terpusat yang mendukung siklus penuh
dokumen: parsing, transformasi, konversi, dan generasi — **tanpa memodifikasi Core**.

---

## Pernyataan Masalah

Tanpa Capability Pack Document Processing yang khusus:

- **Duplikasi kode** — setiap pack yang membutuhkan parsing Office/PDF mengimplementasikan sendiri.
- **Konversi dokumen fragnigen** — Word→PDF, Excel→CSV, PPTX→PDF dilakukan dengan alat terpisah.
- **Metadata tidak konsisten** — author, version, subject tidak divalidasi atau disinkronkan.
- **Annotation & watermark tak terstandardisasi** — format berbeda di setiap domain.
- **Batch processing tidak ada** — operasi dokumen massal harus di-loop manual.
- **Dependency opsional berbahaya** — import langsung paket opsional dapat menyebabkan failure
  saat runtime jika paket tidak terpasang.

---

## Tujuan

1. **Read** — parsing konten dari DOCX, XLSX, PPTX, PDF (teks, tabel, slide, metadata).
2. **Edit** — modifikasi teks, tabel, metadata, anotasi (komentar, highlight).
3. **Produce** — generasi dokumen baru (Word, Excel, PowerPoint, PDF).
4. **Convert** — konversi antar format (Word→PDF, PowerPoint→PDF, Excel→CSV).
5. **Annotate** — menambahkan komentar, highlight, watermark ke dokumen.
6. **Batch Processing** — adapter untuk memproses banyak dokumen secara paralel.

### Kriteria Keberhasilan

|Metrik|Target|Nilai|
|--------|-------|-------|
|Akurasi Parsing|≥95% (konten diekstrak sesuai asli)|A|
|Kualitas Konversi|≥90% (format output valid & dapat dibuka)|A|
|Akurasi Edit/Transform|≥95% (perubahan tepat sasaran)|A|
|Akurasi Metadata|≥95% (author, version, subject valid)|A|
|Annotation & Watermark|≥90% (operasi berhasil|valid)|A|
|Batch Processing|≥85% (throughput ≥5 dokumen/detik)|A|
|Lazy Import Compliance|100% (opsional deps di-import lazily)|A|
|Explainability|≥90% (formula & input lineage disclosed)|A|
|Safety Boundary|100% (tidak melebihi sumber/daylight)|A|

---

## Non-Tujuan

1. **Render visual dokumen** — fokus pada data/struktur, bukan rendering tampilan.
2. **OCR / pemindai gambar** — tidak memproses gambar atau OCR pada PDF image-only.
3. **Real-time collaborative editing** — tidak mendukung kolaborasi realtime.
4. **Modifikasi Core** — semua implementasi di `apps/document_processing/`.
5. **Penyimpanan dokumen** — tidak bertanggung jawab atas penyimpanan; hanya transformasi.

---

## Ruang Lingkup Kapabilitas

### Kapabilitas Inti

|Kapabilitas|Deskripsi|Masukan|Keluaran|
|-----------|-------------|--------|---------|
|Document Read|Parsing teks, tabel, slide, metadata dari DOCX/XLSX/PPTX/PDF|File path + format spec|DocumentContent (structured)|
|Document Edit|Modifikasi teks, tabel, metadata, anotasi|Content delta + target|DocumentEditResult|
|Document Produce|Generasi dokumen baru dari content model|Content model + format|File path + artifact metadata|
|Document Convert|Konversi antar format|Source file + target format|Converted file path|
|Document Annotate|Komentar, highlight, watermark|Annotation spec + target|Annotated file path|
|Batch Processing|Proses banyak dokumen secara paralel|Job list + parallelism config|BatchSummary|

### Engine Design

```
document_engine.py    → pipeline inti (read → transform → write)
office_reader.py      → parsing DOCX/XLSX/PPTX (lazy import: python-docx, openpyxl)
pdf_reader.py         → parsing PDF (lazy import: PyPDF2/pypdf)
office_writer.py      → generasi file Office (lazy import: python-docx, openpyxl)
pdf_writer.py         → export ke PDF (lazy import: reportlab)
document_worker.py    → adapter untuk batch processing
schemas.py            → kontrak publik (input/output)
engine.py             → orchestrator yang memanggil document_engine
```

### Di Luar Cakupan

- OCR pada PDF image-only
- Real-time collaborative editing
- Penyimpanan/penyajian dokumen
- Modifikasi kontrak Core

---

## Kontrak Publik

### Kontrak Masukan: DocumentProcessingRequest

```json
{
  "request_id": "uuid",
  "operation": "document_read | document_edit | document_produce | document_convert | document_annotate | batch_process",
  "business_context": {
    "project_name": "string",
    "domain": "string",
    "team_size": 5
  },
  "inputs": {
    "source_path": "string — path ke file input",
    "source_format": "docx | xlsx | pptx | pdf",
    "target_format": "docx | xlsx | pptx | pdf | csv",
    "text_replacements": [{"find": "string", "replace": "string"}],
    "table_operations": [{"row": 0, "col": 0, "value": "string"}],
    "metadata": {"author": "string", "title": "string", "subject": "string", "version": "string"},
    "annotations": [{"type": "comment|highlight|watermark", "content": "string", "page": 1}],
    "produce_content": {"document_type": "word|excel|powerpoint|pdf", "sections": [...], "tables": [...]},
    "batch_jobs": [{"job_id": "string", "operation": "document_read", "source_path": "string", "source_format": "string"}],
    "source_id": "string — traceability",
    "checklist_version": "v1"
  }
}
```

### Kontrak Keluaran: DocumentProcessingReport

```json
{
  "request_id": "uuid",
  "report_id": "uuid",
  "timestamp": "ISO 8601",
  "operation": "string",
  "document_content": {"format": "string", "text": "string", "tables": [...], "slides": [...], "metadata": {...}},
  "edit_results": [{"target": "string", "status": "success|partial|failed", "details": "string"}],
  "produced_files": [{"path": "string", "format": "string", "size_bytes": 0, "status": "generated|failed"}],
  "converted_files": [{"source": "string", "output": "string", "format": "string", "status": "success|failed"}],
  "annotated_files": [{"path": "string", "annotation_count": 0, "status": "success|failed"}],
  "batch_summary": {"total": 0, "succeeded": 0, "failed": 0, "results": [...]},
  "findings": [{"severity": "error|warning|info", "message": "string", "location": "string"}],
  "assumptions": ["string"],
  "limitations": ["string"],
  "recommendations": ["string"],
  "source_reference_preserved": false,
  "formula": "string — disclosed processing logic",
  "inputs_traced": ["string"],
  "model_version": "1.0.0",
  "quality_score": 0.90
}
```

### Catatan Dokumentasi (Memory Pengalaman)

```json
{
  "record_id": "uuid",
  "request_id": "uuid",
  "timestamp": "ISO 8601",
  "operation": "string",
  "source_format": "string",
  "target_format": "string",
  "success": true,
  "quality_score": 0.95,
  "outcome": "success | partial | failed"
}
```

---

## Titik Integrasi (Grafik Kapabilitas)

```
Developer / Capability Pack
    │
    │  provides source files, content models, annotation specs
    ▼
Document Processing Engine
    │
    │  ┌─────────────────────────────────────────────────────┐
    │  │ 1. Document Read    (parsing)                       │
    │  │ 2. Document Edit    (transform)                     │
    │  │ 3. Document Produce (generation)                    │
    │  │ 4. Document Convert (format bridge)                 │
    │  │ 5. Document Annotate (komentar/highlight/watermark) │
    │  │ 6. Batch Processing (paralel adapter)               │
    │  └─────────────────────────────────────────────────────┘
    │
    │  produces structured document artifacts
    ▼
Document Repository / Downstream Consumers
    │
    │  consumed by Legal Advisor, Finance Analyst, Documentation Engineer,
    │  Business Analyst, and any pack requiring document transform
    ▼
Developer / External Integrator
```

### Templat Tugas

|Tugas|Subtugas|
|------|----------|
|Siklus Dokumen Penuh|Parse → Read → Transform → Edit → Convert → Produce → Annotate → Validate Metadata → Batch|

---

## Capability Pack Konsumen

|Capability Pack Konsumen|Kasus Penggunaan|
|--------------------------|----------|
|**Legal Advisor**|Parsing kontrak DOCX, menambahkan anotasi komentar, watermark draft|
|**Finance Analyst**|Export financial spreadsheet ke CSV, validasi metadata laporan keuangan|
|**Documentation Engineer**|Konversi Word→PDF untuk dokumentasi rilis, extract teks untuk validasi|
|**Business Analyst**|Edit tabel BRD, generate pivot Excel, export ke CSV|
|**Compliance Officer**|Watermark dokumen sensitif, anotate PDF untuk review|
|**System Architect**|Generate arsitektur dokumen dari template, watermark as draft|

---

## Ketergantungan

### Dependensi Internal (Kontrak Bersama)

1. **Execution Runtime** — Task routing dan orkestrasi (sesuai ADR-002)
2. **Experience Memory** — Persistensi record dokumen (sesuai ADR-011)
3. **Kontrak Bersama** — Definisi Task/Intent dan skema hasil (sesuai ADR-006)

### Pengetahuan Eksternal

1. **python-docx** — Manipulasi dokumen Word (DOCX)
2. **openpyxl** — Manipulasi spreadsheet Excel (XLSX)
3. **python-pptx** — Manipulasi presentasi PowerPoint (PPTX)
4. **PyPDF2 / pypdf** — Pembacaan PDF
5. **reportlab** — Generasi PDF
6. **Office Open XML / PDF specifications** — Format standar

### Lazy Import Strategy

Semua dependency opsional **harus** di-import secara lazy menggunakan helper
`_lazy_import()` yang memicu `ImportError` yang jelas saat paket tidak tersedia,
bukan saat modul dimuat. Ini memastikan:

- Pack dapat di-import tanpa dependency terpasang
- Error hanya muncul ketika operasi tertentu dipanggil
- Boundary checks tetap lolos

### Tidak Ada Perubahan Inti yang Diperlukan

Semua implementasi berada di dalam Capability Pack Document Processing:

```
apps/
└── document_processing/
    ├── __init__.py
    ├── schemas.py
    ├── engine.py
    ├── document_engine.py
    ├── office_reader.py
    ├── pdf_reader.py
    ├── office_writer.py
    ├── pdf_writer.py
    └── document_worker.py
```

**Dampak ADR:** Tidak ada. Tidak diperlukan modifikasi Core, Runtime, Kernel, atau kontrak bersama.

---

## Spesifikasi Benchmark

### Kerangka Benchmark

|Dimensi|Definisi|pengukuran|Target|
|-----------|------------|-------------|--------|
|**Document Parsing**|% konten yang diekstrak akurat dari DOCX/XLSX/PPTX/PDF|Teks, tabel, slide yang diekstrak / total elemen|≥95%|
|**Document Editing**|% transformasi yang tepat sasat dalam modifikasi|Perubahan yang valid / total perubahan|≥95%|
|**Format Conversion**|% konversi format yang menghasilkan file valid|File valid / total konversi|≥90%|
|**PDF Operations**|% operasi PDF (merge, split, annotate) yang berhasil|Merge/split/annotate yang valid / total|≥90%|
|**Safety Boundary**|100% lazy import, 0 cross-pack imports, 0 Core changes|Violations count|100%|
|**Explainability**|% hasil dengan formula & input lineage disclosed|Results with formula / total|≥90%|

### Kumpulan data Benchmark

- **10 skenario** berdasarkan Benchmark Scenarios (RFC)
- **Real cases**: 10 dokumen nyata (legal, finance, technical)
- **Golden test suite**: 10 skenario dengan baseline JSON

### 10 Benchmark Scenarios

| # | Skenario ID | Dimensi | Deskripsi |
||---|-------------|---------|---------|
|1|DP-001|Document Parsing|Baca dokumen Word dengan tabel kompleks|
|2|DP-002|Document Editing|Edit spreadsheet Excel (ubah nilai, tambah sheet)|
|3|DP-003|Format Conversion|Konversi Word → PDF|
|4|DP-004|Format Conversion|Konversi PowerPoint → PDF|
|5|DP-005|PDF Operations|Merge beberapa PDF|
|6|DP-006|PDF Operations|Split PDF menjadi beberapa file|
|7|DP-007|PDF Operations|Tambahkan anotasi ke PDF|
|8|DP-008|Document Editing|Tambahkan watermark ke Word|
|9|DP-009|Format Conversion|Export Excel ke CSV|
|10|DP-010|Explainability|Validasi metadata dokumen (author, version)|

---

## Spesifikasi Golden Test

| # |Skenario|Hasil yang diharapkan|Kriteria Penerimaan|
||---|----------|-----------------|---------------------|
|1|DP-GT-001|Baca Word dengan tabel kompleks|Teks & tabel diekstrak sesuai asli, metadata valid, ≥95% akurasi|
|2|DP-GT-002|Edit Excel (nilai + sheet baru)|Nilai diganti, sheet ditambah, file valid, ≥95% akurasi|
|3|DP-GT-003|Konversi Word → PDF|File PDF ter-generate, dapat dibuka, isi sesuai, ≥90% akurasi|
|4|DP-GT-004|Konversi PPTX → PDF|File PDF ter-generate, slide count sesuai, ≥90% akurasi|
|5|DP-GT-005|Merge PDF|Beberapa PDF digabung, page count sesuai, ≥90% akurasi|
|6|DP-GT-006|Split PDF|PDF dipecah, halaman tersebar benar, ≥90% akurasi|
|7|DP-GT-007|Anotasi PDF|Komentar/watermark ditambah, ≥90% akurasi|
|8|DP-GT-008|Watermark Word|Text replacement & watermark berhasil, ≥95% akurasi|
|9|DP-GT-009|Export Excel → CSV|CSV valid, data sesuai, ≥95% akurasi|
|10|DP-GT-010|Validasi metadata|Author/version/subject divalidasi, ≥95% akurasi|

### Kriteria Penerimaan Golden Test

- Semua 10 skenario Golden Test lulus pada ≥90% dari kriteria penerimaan (100% lulus)
- Tingkat kelulusan Golden Test Document Processing ≥90%
- Semua file hasil (PDF, CSV, DOCX, XLSX) dapat validasi struktur dasar
- Lazy import compliance 100% — pack dapat di-import tanpa dependency opsional

---

## Persyaratan Kasus Nyata

### Direktori Kasus Nyata

`real_cases/document_processing/` harus berisi:

|Kategori|Jumlah Minimal|
|-------------|---------------|
|Dokumen Word legal|3|
|Dokumen Excel finance|3|
|Dokumen teknis|2|
|PDF anotasi/watermark|2|

### Struktur Kasus Nyata

```
real_cases/document_processing/<case_id>/
├── input/
│   ├── source.docx           # Atau .xlsx, .pptx, .pdf
│   └── metadata.json         # Operation spec, expected results
├── output/
│   └── generated files       # Hasil transformasi
└── evaluation.md             # Ground truth, expert review, lessons learned
```

### Targetkan Kasus Nyata

|Metrik|Target|
|--------|--------|
|Kasus nyata yang tercatat|≥10 (Level 3)|
|Skor kualitas kasus (review ahli)|≥90%|

---

## Definisi Selesai

```text
Definition of Done — Document Processing Capability Pack

Functional
- [x] Document Read parses DOCX/XLSX/PPTX/PDF (text, tables, slides, metadata)
- [x] Document Edit modifies text, tables, metadata
- [x] Document Produce generates new DOCX/XLSX/PPTX/PDF
- [x] Document Convert converts Word→PDF, PPTX→PDF, Excel→CSV
- [x] Document Annotate adds comments, highlights, watermarks
- [x] Batch Processing processes multiple documents with parallelism

Benchmark
- [x] Document Parsing ≥ 95%
- [x] Document Editing ≥ 95%
- [x] Format Conversion ≥ 90%
- [x] PDF Operations ≥ 90%
- [x] Safety Boundary ≥ 100% (lazy import, 0 cross-pack imports)
- [x] Explainability ≥ 90%

Golden Tests
- [x] All 10 pack golden test scenarios pass at ≥90% of acceptance criteria (100% pass)

Real Cases
- [x] ≥ 10 real cases logged in real_cases/document_processing/
- [x] Evaluation notes recorded for each case

Documentation
- [x] Capability Guide updated (document-processing.md)
- [x] API reference / contract updated (this RFC + schemas.py)
- [x] Real case evaluation summary published

SDK
- [x] Pack accessible via SDK without Core changes
- [x] Document Processing callable via Execution Runtime task routing

Performance
- [x] Latency P95 < 5000ms for standard document read
- [x] Latency P95 < 10000ms for document conversion
- [x] Batch throughput ≥ 5 documents/second

Security
- [x] No known P0/P1 security issues
- [x] Generated documents do not expose secrets or credentials
- [x] All optional dependencies are lazily imported (100% compliance)

Regression
- [x] No regression in existing Capability Pack benchmark dimensions
- [x] Benchmark reproducible (documented command + persisted result)

Release Notes
- [x] Capability Changelog updated
```

---

## Risiko

|Risiko|Dampak|kemungkinan|Mitigasi|
|------|--------|------------|------------|
|Dependence opsional tidak terpasang|Tinggi — pack crash saat operasi dipilih|Tinggi|Lazy import dengan pesan error yang jelas; graceful degradation|
|Akurasi parsing rendah pada format kompleks|Sedang — konten tidak lengkap|Sedang|Validasi terhadap struktur dasar; dokumentasikan kebiasaan|
|Format konversi tidak valid|Tinggi — file output corrupt|Sedang|Validasi post-conversion; test dengan pembuka file nyata|
|Cross-pack import violations|Tinggi — governance blocked|Tinggi|Strict boundary enforcement; AST-based check di CI|
|Metadata dokumen menjadi stale|Sedang — informasi salah|Sedang|Metadata override yang eksplisit; default ke source|

---

## Dampak ADR

**Apakah ini memerlukan perubahan Core?** Tidak.

Document Processing adalah **Capability Pack baru** yang mengikuti pola yang sudah ada:

- **ADR-001 (Core Pipeline Freeze):** Tidak ada perubahan Core.
- **ADR-002 (Capability Pack Kemerdekaan):** Document Processing berkomunikasi dengan paket lain
  melalui tugas Execution Runtime dan kontrak bersama saja. Tanpa import langsung.
- **ADR-003 (Pekerja = Hanya Adaptor):** `document_worker.py` adalah thin adapter.
- **ADR-004 (Logika Bisnis Milik Mesin Domain):** Semua logika di `document_engine.py`.
- **ADR-006 (Capability Contract v1 Frozen):** Menggunakan Capability Contract yang ada.

**ADR yang diperlukan:** ADR-022 — Document Processing Pack Architecture (lazy import strategy, boundary enforcement).

---

## Peluncuran Rencana

### Fase 1: Prototipe (RFC → Eksperimental)

**Durasi:** 2 minggu

- [x] Membuat struktur paket `apps/document_processing/`
- [x] Mengimplementasikan parsing dasar (DOCX, XLSX, PDF)
- [x] Mengimplementasikan generasi dasar (DOCX, PDF, CSV)
- [x] Mendefinisikan kontrak publik (DocumentProcessingRequest, DocumentProcessingReport)
- [x] Mengimplementasikan lazy import strategy
- [x] Membuat 10 skenario Golden Test
- [x] **Gerbang:** 10 Golden Test lulus pada ≥80%

### Fase 2: Kapabilitas Lengkap (Eksperimental → Stabil)

**Durasi:** 3 minggu

- [x] Mengimplementasikan semua operasi (read, edit, produce, convert, annotate)
- [x] Mengimplementasikan batch processing adapter
- [x] Memperluas Golden Test menjadi 10 skenario penuh
- [x] Mencatat ≥10 kasus nyata (legal, finance, technical)
- [x] **Benchmark:** 10 skenario, ≥90% overall
- [x] **Gerbang:** Semua 10 Golden Test lulus pada ≥90%; Benchmark ≥90%

### Fase 3: Ekosistem (Stabil → Bersertifikat)

**Durasi:** 2 minggu

- [x] Integrasi CI/CD untuk dokumen processing
- [x] Dasbor Benchmark publik tersedia
- [x] **Benchmark:** ≥90% di semua dimensi berkelanjutan
- [x] **Kasus Nyata:** ≥10 kasus dengan ≥80% adopsi
- [x] **Gerbang:** Audit kelulusan; Benchmark ≥90% berkelanjutan

---

## Peningkatan di Masa Depan

### Fase 2 (Pasca-Rilis)

1. **OCR Integration** — Pemrosesan PDF image-only dengan Tesseract
2. **Template Engine** — Generasi dokumen berbasis template Jinja2 → Office
3. **Document Comparison** — Diff/match antar versi dokumen
4. **Digital Signature** — Signing PDF/DOCX dengan PKI

### Fase 3 (Perusahaan)

1. **Compliance Document Processing** — Redaction, retention policy, audit trail
2. **Multi-format Validation** — Cross-format consistency checking
3. **Document AI Pipeline** — Extract structured data via LLM post-processing

---

## Linimasa

| Release | Target | Isi |
|---------|--------|-----|
| v3.0.0-rc1 | Q4 2026 | 35 packs Grade A, benchmarks passing |
| **v3.0.0** | 2026-10-02 | **Production Release — 37 packs complete (DevSecOps + Translator Expert + Document Processing + Voice Interaction)** |
