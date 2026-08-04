# Dasar Teknik — garis dasar teknik v1.0.0

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 08-02-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dasar rekayasa, batasan arsitektur, dan aturan ketergantungan
<!-- DOCUMENT_METADATA_END -->

**Status:** 🟢 **Beku**
**Tag:** `v1.0.0-engineering-baseline`
**Tanggal:** 02-08-2026

---

## Tujuan

Dokumen ini mencatat keadaan engineering yang tepat dari Enal Cognitive Platform pada saat engineering baseline dibekukan. Setelah titik ini:

- **Tidak ada perubahan arsitektur baru atau refactor besar** tanpa kebutuhan lintas-domain yang terdokumentasi
- **Tidak ada desain ulang** pada komponen inti
- Fokus beralih ke:
  1. Dokumentasi keadaan kode aktual
  2. Pengembangan produk di atas fondasi yang stabil

---

## Kualifikasi Baseline

|Pemeriksaan|Hasil|Bukti|
|-------|--------|----------|
|Ketat MyPy|✅ **0 kesalahan**|Semua 27+ file diperbaiki di berbagai sprint|
|Pilance Keparahan 8|✅ **0**|Resolusi tipe bersih|
|Masalah Kode VS|✅ **0**|Tidak ada diagnostik yang tersisa|
|Rangkaian Tes|✅ **349 lulus**|Semua tes lulus|
|String-f Python 3.11|✅ **0 masalah dalam produksi**|Diverifikasi melalui pemindaian `compile()`|
|Kebersihan ruff|⚠️ Peringatan sisa|`ruff check --fix` dan `ruff format` menunggu (dapat diperbaiki secara otomatis)|
|Konsistensi arsitektur|✅ Tervalidasi|AR-001 hingga AR-017 lulus|
|Konsistensi kontrak API|✅ Tervalidasi|Semua tanda tangan cocok|
|Tanpa impor melingkar|✅ diatasi|pengetahuan, perencana_tugas, rapat|
|Tanpa default yang bisa diubah|✅ Diatasi|RUF012 diperbaiki di seluruh basis kode|
|Tanpa mengungkapkannya|⚠️ 45 lokasi|Hutang teknologi yang diterima — review per kasus di sprint mendatang|

---

## Struktur Repositori (Setelah Pengerasan)

```text
enal-ai-os/
├── apps/               # 13 Capability Packs (network, code, research, devops, trading, self, decision, system, security, data, database, qa, business)
├── backend/            # API, core, studio, models
├── benchmarks/         # Performance, capability, golden test benchmarks
├── docs/               # Architecture, API, quality gates, roadmap
│   ├── adr/            # Architecture Decision Records
│   └── quality/        # Quality Gate Policy
├── examples/           # Custom agent, custom workflow
├── frontend/           # Next.js frontend
├── golden/             # Cisco, Fortinet, MikroTik golden configs
├── plugins/            # MikroTik plugin
├── real_cases/         # Real-world test datasets
├── scripts/            # CI/CD, gate validation, release readiness
├── sdk/                # Python SDK
├── tests/              # Unit tests (349 passing)
├── tools/
│   └── audit/          # Utility scripts (hygiene, mypy fixing, f-string scanning)
└── workspace/          # Runtime workspace
```

---

## File yang Dimodifikasi Selama Pengerasan (27 core + utilitas)

### File Produksi Inti (27)

|Mengajukan|Perbaikan yang Diterapkan|
|------|-------------|
|`adaptive_runtime.py`|Ditulis ulang dengan tipe yang tepat|
|`reflection.py`|Tidak ada menunggu pada panggilan sinkron|
|`cognitive_kernel.py`|DecisionService mengembalikan dikte|
|`unified_orchestrator.py`|Perkiraan anggaran sinkron|
|`orchestrator_v2.py`|Menggunakan orkestrate_goal, bukan process_request|
|`code_engineer/__init__.py`|Perbaikan `str\|Tidak ada` Pembaca Arsitektur|
|`conversation_manager.py`|Menambahkan metode _persist_artifact|
|`reasoning_engine.py`|Tidak ada menunggu pada panggilan sinkron|
|`strategic_planner.py`|Tidak ada menunggu pada panggilan sinkron|
|`world_model.py`|Tidak ada menunggu pada panggilan sinkron|
|`decision_engine.py`|Mengembalikan dict, bukan DecisionResult|
|`vendor/models.py`|Menambahkan NATRule.in_interface, BridgeConfig.comment|
|`routeros_parser.py`|Menambahkan kolom dataclass yang hilang|
|`profiles.py`|Memperbaiki pemeriksaan model vendor|
|`enricher.py`|Memperbaiki pembentukan bukti|
|`attachments/pipeline.py`|Memperbaiki bidang InfrastrukturAST|
|`attachments/models.py`|Memperbaiki tipe kerusakan|
|`execution_session.py`|Memperbaiki parameter konstruktor|
|`memory_layer.py`|Memperbaiki masalah konstruktor|
|`workspace_service.py`|Memperbaiki tanda tangan create_workspace|
|`artifact_service.py`|Memperbaiki tanda tangan create_artifact|
|`config.py`|Memperbaiki pengaturan tipe|
|`event_bus.py`|Memperbaiki anotasi tipe Redis|
|`detector.py`|memperbaiki tipe `VendorFamily\|Tidak ada`|
|`voice_vision_agent.py`|Memperbaiki default Tidak ada|
|`execution.py`|Memperbaiki Artifact vs ExecutionArtifact|
|`society.py`|Memperbaiki tipe SubtaskResult|

### Skrip Utilitas dipindahkan ke `tools/audit/`

```text
tools/audit/
├── __init__.py
├── audit_hygiene.py
├── find_fstring_backslash.py
├── fix_6_remaining.py
├── fix_all_remaining.py
├── fix_final_batch.py
├── fix_final_mypy.py
├── fix_mypy_errors.py
├── fix_remaining_4.py
├── fix_remaining_mypy.py
├── fix_self_verification.py
├── run_ruff.py
├── run_scans.py
├── run_scans_and_mypy.py
└── apply_mypy_fixes.py
```

---

## Kompatibilitas Python 3.11 — Detail Verifikasi

- **Metode:** `compile(content, path, 'exec', flags=0)` untuk setiap file `.py` di repositori
- **Hasil:** 0 masalah f-string backslash di `apps/`, `backend/`, `benchmarks/`, `tests/`
- **Satu peluncuran:** `_fix_final_mypy.py:93` — skrip utilitas, BUKAN kode produksi

Pola yang tidak berlaku:
```python
# ❌ Pola ini TIDAK ada di kode produksi:
f"{expr_with_backslash}"

# ✅ Semua f-string menggunakan variabel yang telah dihitung sebelumnya:
fixed = value.replace('\\n', '')
f"{fixed}"
```

---

## Lingkungan Membangun

|Komponen|Versi|
|-----------|---------|
|piton ular|3.11.9|
|Node.js|Tidak terpasang di lingkungan saat ini (didefinisikan di `frontend/package.json`: Next.js 14.2.0, React 18.2.0, TypeScript 5.3.0)|
|npm|Tidak terpasang di lingkungan saat ini|
|Docker|29.6.2|
|Git|2.55.0.windows.3|
|sistem operasi|jendela 11|

---

## Ketergantungan Cuplikan

### Bagian Belakang (`backend/pyproject.toml`)

|Ketergantungan|Persyaratan Versi|
|------------|-------------------|
|FastAPI|>=0.109.0|
|uvicorn[standar]|>=0.27.0|
|sqlalkimia|>=2.0.0|
|klien qdrant|>=1.7.0|
|redis|>=5.0.0|
|gila-gilaan|>=2.6.0|
|pengaturan pydantic|>=2.0.0|
|kecil|>=1.40.0|
|langchain-openai|>=0.1.0|
|inti rantailang|>=0.1.0|
|httpx|>=0.26.0|
|pyyaml|>=6.0|
|aiohttp|>=3.9.0|
|python-multipart|>=0,0,9|
|psycopg2-biner|>=2.9.0|

### Ketergantungan Pengembang Backend

|Ketergantungan|Persyaratan Versi|
|------------|-------------------|
|uji coba|>=8.0.0|
|pytest-asyncio|>=0.23.0|
|ruff|>=0.4.0|
|hitam|>=24.4.0|
|mypy|>=1.8.0|

### Bagian Depan (`frontend/package.json`)

|Ketergantungan|Versi|
|------------|---------|
|Selanjutnya|14.2.0|
|bereaksi|^18.2.0|
|reaksi-dom|^18.2.0|
|zustand|^5.0.14|
|reaksi jernih|^0.378.0|
|penarik angin (dev)|^3.4.0|
|naskah ketikan (pengembangan)|^5.3.0|

### SDK (`sdk/pyproject.toml`)

Lihat direktori `sdk/` untuk ketergantungan khusus SDK.

---

## Prinsip Dasar Rekayasa

Prinsip-prinsip ini membentuk rekayasa "konstitusi" untuk proyek ini. Setiap keputusan arsitektur, pengamatan kode, dan implementasi harus selaras dengan prinsip-prinsip ini.

| # |Prinsip|Deskripsi|
|---|-----------|-------------|
|1|**Pembekuan Arsitektur**|Tidak ada refactor skala besar, redesign, atau perubahan arsitektur baru tanpa perlu lintas-domain yang terdokumentasi dan divalidasi melalui ADR|
|2|**Kompatibilitas Mundur**|Semua API publik dan antarmuka harus mempertahankan kompatibilitas ke belakang. Perubahan yang memadukan kompatibilitas memerlukan ADR, periode izin, dan jalur migrasi|
|3|**Mengetik Kuat**|Semua kode harus lulus pemeriksaan MyPy strict. Tidak ada tipe `Any` di antarmuka publik. Gunakan `X \|Tidak ada`, bukan `Opsional[X]`|
|4|**Tidak Ada Ketergantungan Tertinggalnya**|Semua dependensi harus dideklarasikan secara eksplisit di `pyproject.toml` atau `package.json`. Tidak dapat mengandalkan paket transitif atau tingkat sistem|
|5|**Tes Dulu**|Setiap perubahan harus menyertakan atau memperbarui test. Baseline: 349 tes lulus. Tidak ada regresi di bawah tingkat kelulusan 95%|
|6|**Observabilitas Pertama**|Semua operasi Runtime harus mengeluarkan telemetri acara. Setiap jalur eksekusi harus dapat dilacak melalui `record_execution_event`|
|7|**Acara Didorong**|Komunikasi-lintasmodul harus menggunakan Event Bus. Tidak ada penggandengan langsung antara Capability Pack atau modul inti|
|8|**Plugin Pertama**|Perluas fungsionalitas melalui Plugin, bukan dengan memodifikasi inti. Plugin memerlukan manifestasi dan validasi keamanan|

---

## Catatan Keputusan Arsitektur (ADR)

ADR disimpan di `docs/adr/`. Setiap ADR mencatat keputusan arsitektur yang signifikan, konteksnya, alternatif yang dipertimbangkan, dan alasan pendekatan yang dipilih.

|ADR|Judul|Deskripsi|
|-----|-------|-------------|
|ADR-001|Arsitektur Bus Acara|Mengapa Event Bus dipilih untuk lintas komunikasi-modul|
|ADR-002|Capability Pack Arsitektur|Mengapa Capability Pack adalah unit ekstensi|
|ADR-003|Desain AST Universal|Mengapa Universal AST dipilih untuk konfigurasi jaringan multi-vendor|
|ADR-004|Arsitektur Mesin Debat|Mengapa penalaran berdasarkan perdebatan dipilih untuk verifikasi diri|

Lihat `docs/adr/` untuk catatan keputusan lengkap.

---

## Kebijakan Gerbang Mutu

Lihat `docs/quality/QUALITY_GATES.md` untuk Kebijakan Gerbang Kualitas lengkap.

Setiap pull request yang menargetkan `main` atau `release/*` harus lulus:

|Gerbang|Urutannya|Kerasnya|
|------|-------------|----------|
|MyPy|0 kesalahan|🔴 PEMBLOKIRAN|
|Tes|≥95% lulus (dasar: 349)|🔴 PEMBLOKIRAN|
|API Kontrak|Kompatibel ke belakang|🔴 PEMBLOKIRAN|
|ADR|Diperlukan untuk mengubah arsitektur|🔴 PEMBLOKIRAN|
|Serat Ruff|Tidak ada pemblokiran|🟡 PERINGATAN|
|Format Ruff|0 file yang diformat ulang|🟡 PERINGATAN|
|Tidak Ada Pengecualian Buta|Yang baru harus dibenarkan|🟡 PERINGATAN|

Pengecualian memerlukan persetujuan yang terdokumentasi. Lihat kebijakan lengkap untuk proses pengunduhan.

---

## Tech Debt yang Diterima dan Diketahui

|Masalah|Jumlah|Kerasnya|Keputusan|
|-------|-------|----------|----------|
|Buta `except Exception:`|45|Rendah|Diterima untuk saat ini. Tinjau per kasus di sprint mendatang|
|`subprocess.run` tanpa `check=False`|5|Rendah|Semua yang ada di skrip utilitas. Perbaiki saat aktif memelihara pemeliharaan|
|`ruff check --fix` tertunda|~50 dapat diperbaiki secara otomatis|Rendah|Jalankan saat melakukan perubahan commit berikutnya|
|`ruff format` tertunda|~10 berkas|Rendah|Jalankan saat melakukan perubahan commit berikutnya|

---

## Langkah Berikutnya

1. **Fase 2: Dokumentasi AES** — Dokumentasikan keadaan kode aktual:
   - Ikhtisar arsitektur
   - Modul ketergantungan grafik
   - Alur Runtime
   - acara Alur
   - API publik
   - Gerbang berkualitas
   - Strategi pengujian
   - Standar Pengkodean

2. **Fase 3: Arsitektur Referensi** — Naikkan AES menjadi referensi arsitektur untuk semua aplikasi yang dibangun di atas ECP
3. **Tahap 4: Panduan Pengembangan Aplikasi** — Pengkodean standar, panduan pengembangan Capability Pack
4. **Fase 5: Pengembangan Produk** — Pengembangan fitur di atas fondasi yang stabil

---

## Inventarisasi Dokumen

|Dokumen|Jalur|
|----------|------|
|Dasar Teknik|`docs/ENGINEERING_BASELINE.md`|
|Kebijakan Gerbang Mutu|`docs/quality/QUALITY_GATES.md`|
|ADR-001: Bus Acara|`docs/adr/ADR-001-event-bus-architecture.md`|
|ADR-002: Capability Pack|`docs/adr/ADR-002-capability-pack-architecture.md`|
|ADR-003: AST Universal|`docs/adr/ADR-003-universal-ast-design.md`|
|ADR-004: Debat Mesin|`docs/adr/ADR-004-debate-engine-architecture.md`|
|Ikhtisar Arsitektur|`docs/architecture.md`|
|Gerbang Kualitas|`docs/QUALITY_GATE.md`|
|Ringkasan Pengerasan Sprint|`SPRINT_HARDENING_SUMMARY.md`|
