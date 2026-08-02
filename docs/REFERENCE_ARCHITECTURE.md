# Arsitektur Referensi - Platform Kognitif Enal (ECP)

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 02-08-2026
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Dokumentasi untuk REFERENCE_ARCHITECTURE
<!-- DOCUMENT_METADATA_END -->

**Versi:** 1.0.0
**Berbasis pada:** `docs/AES_ARCHITECTURE.md`
**Status:** 🟢 Aktif

---

## Daftar Isi

1. [Tujuan](#1-tujuan)
2. [Apa itu Reference Architecture](#2-apa-itu-reference-architecture)
3. [Building Blocks Arsitektur](#3-architecture-building-blocks)
4. [Tipe Aplikasi di ECP](#4-application-types-on-ecp)
5. [Membangun Aplikasi di ECP](#5-building-an-application-on-ecp)
6. [Kerangka Keputusan Arsitektur](#6-architecture-decision-framework)
7. [Katalog Pola](#7-patterns-catalog)
8. [Anti-Pola](#8-anti-patterns)
9. [Atribut Kualitas](#9-quality-attributes)
10. [Evolusi Arsitektur](#10-architecture-evolution)
11. [Dokumen Terkait](#11-related-documents)

---

## 1. Tujuan

Referensi Arsitektur ini memperluas AES (Spesifikasi Teknik Arsitektur) dengan menyediakan:

- **Pola yang dapat digunakan ulang (pola yang dapat digunakan kembali)** untuk membangun aplikasi di ECP
- **Kerangka keputusan** bagi arsitek yang membangun Capability Pack atau aplikasi baru
- **Tradeoff atribut kualitas** dan cara memutarnya
- **Panduan berevolusi** untuk menumbuhkan platform tanpa merusak baseline

**Audiens:** Arsitek solusi, insinyur senior, dan tim platform yang membangun di atas ECP.

---

## 2. Arsitektur Referensi Apa itu

Arsitektur Referensi adalah **template arsitektur** yang:

1. Mengidentifikasi **building block arsitektur** utama
2. Mendefinisikan **cara blok berinteraksi** (kontrak, protokol, alur data)
3. Mendokumentasikan **pola terbukti** dan **anti-pola** yang dikenal
4. Menyediakan **kriteria keputusan** untuk memilih pendekatan

Ia BUKAN cetak biru yang kaku. Ia adalah **titik awal** yang disesuaikan oleh tim aplikasi sesuai kebutuhan domain spesifik mereka sambil tetap menjaga kompatibilitas platform.

### Hubungan dengan Dokumen Lain

```
Engineering Baseline (apa yang dibekukan)
        │
        ▼
AES Architecture (bagaimana platform dibangun)
        │
        ▼
Reference Architecture (bagaimana membangun DI ATAS platform) ← ANDA DISINI
        │
        ▼
Application Development Guide (langkah demi langkah untuk tim aplikasi)
```

---

## 3. Arsitektur Blok Bangunan

ECP menyediakan blok bangunan yang dapat digunakan ulang untuk aplikasi apa pun:

### 3.1 Blok Inti (Platform yang Disediakan)

|Blok|Komponen|Cara Menggunakan|
|---|---|---|
|**Persepsi**|`CognitiveKernel.perception`|Masukkan masukan pengguna, dapatkan entitas/niat yang dikumpulkan|
|**Ingatan**|`MemoryManager` (7 lapisan)|Simpan/ambil/cari di hirarki memory|
|**Pemikiran**|`ReasoningEngine`|Hasilkan hipotesis, rantai langkah penalaran|
|**Perencanaan**|`StrategicPlanner` / `AIPlanner`|Uraikan tujuan menjadi rencana yang dapat dilaksanakan|
|**Keputusan**|`DecisionEngine`|Evaluasi opsi, pilih dengan percaya diri|
|**Cerminan**|`ReflectionService`|Tinjau ulang keluaran untuk kualitas|
|**Sedang belajar**|`ContinuousLearning`|Ekstrak sinyal pembelajaran dari hasil|
|**Perdebatan**|`DebateEngine`|Verifikasi keluaran multiperspektif|
|**Simulasi**|`SimulationEngine`|Analisis bagaimana-jika sebelum eksekusi|
|**Verifikasi**|`SelfVerification`|Pemeriksaan kebenaran pasca-eksekusi|

### 3.2 Blok Infrastruktur (Platform Disediakan)

|Blok|Komponen|Abstraksi|
|---|---|---|
|**Bus Acara**|`EventBus`|Redis Streams — pub/sub + bertahan|
|**Antrian Tugas**|`TaskQueue`|Antrean asinkron dalam memori|
|**Eksekusi**|`ExecutionIntegration`|Sesi + penjadwal + kemajuan|
|**Model Router**|`ModelRouter`|LiteLLM — akses multi-penyedia LLM|
|**Pemulihan Negara**|`StateRecovery`|Pos pemeriksaan/pemulihan untuk tugas panjang|
|**Tata Kelola**|`Governance`|Alur kerja persetujuan, isolasi penyewa|
|**Keamanan**|`SecurityModel`|RBAC, audit pencatatan|

### 3.3 Titik Ekstensi (Untuk Tim Aplikasi)

|Titik Ekstensi|Yang Diimplementasikan|Contoh|
|---|---|---|
|**Capability Pack**|Subkelas `BaseApp` + pabrik `get_app()`|`NetworkEngineerApp`|
|**Pengurai Vendor**|Parsing konfigurasi → model Universal AST|`mikrotik.py` → `UniversalFirewallRule`|
|**Pekerja Kustom**|Pengendali tugas untuk masyarakat Runtime|`network_worker.py`|
|**Plugin**|Plugin manifes + pengendali|MikroTik Plugin|
|**API Rute**|Modul router FastAPI|`api/chat.py`|
|** Pengendali Peristiwa **|Tipe acara berlangganan|`task.completed` → notifikasi|

---

## 4. Tipe Aplikasi di ECP

Berdasarkan ability packs yang ada, ECP mendukung archetype aplikasi berikut:

### 4.1 Aplikasi Analisis (Aplikasi Analisis)

**Deskripsi:** Menganalisis masukan data, menghasilkan wawasan dan rekomendasi.

**Contoh:** Network Engineer (analisis konfigurasi), Code Engineer (peninjauan kode)

**Jalur umum:**
```
Perception → Memory → Reasoning → Decision → Reflection
```

**Blok Kunci:** Persepsi, Memori, Penalaran, Knowledge Graph

### 4.2 Aplikasi Generasi (Aplikasi Generasi)

**Deskripsi:** Menghasilkan artefak (config, kode, dokumen) dari spesifikasi.

**Contoh:** Network Engineer (generasi konfigurasi), Code Engineer (generasi patch)

**Jalur umum:**
```
Perception → Planning → Reasoning → Decision → Action → Reflection
```

**Blok Kunci:** Perencanaan, Aksi, Verifikasi, Debat

### 4.3 Aplikasi Asisten (Aplikasi Asisten)

**Deskripsi:** Asisten interaktif berbasis chat dengan memori dan konteks.

**Contoh:** Asisten Peneliti, Asisten DevOps, Pengembangan Diri

**Jalur umum:**
```
Perception → Memory → Reasoning → Decision → Reflection → Learning
```

**Blok Kunci:** Memori (percakapan + sesi), Pembelajaran Berkelanjutan

### 4.4 Aplikasi Otomasi (Aplikasi Otomasi)

**Deskripsi:** Mengeksekusi alur kerja multi-langkah dengan pemantauan dan pemulihan.

**Contoh:** DevOps (orkestrasi CI/CD), Trading (eksekusi strategi)

**Jalur umum:**
```
Perception → Planning → Execution → Verification → Reflection
```

**Blok Kunci:** Integrasi Eksekusi, Pemulihan Negara, Tata Kelola

---

## 5. Membangun Aplikasi di ECP

### 5.1 Proses Langkah-demi-Langkah

```
Langkah 1: Tentukan Domain Scope
        │
        ▼
Langkah 2: Identifikasi Building Blocks yang Diperlukan
        │
        ▼
Langkah 3: Implementasikan Capability Pack
        │
        ▼
Langkah 4: Daftarkan Skills
        │
        ▼
Langkah 5: Implementasikan Logika Kustom
        │
        ▼
Langkah 6: Tambahkan Test
        │
        ▼
Langkah 7: Daftarkan API Routes (jika perlu)
        │
        ▼
Langkah 8: Integrasikan dengan Orchestration
```

### 5.2 Detil Langkah

#### Langkah 1: Tentukan Cakupan Domain

```markdown
Domain: Network Engineering
Scope: Analisis konfigurasi, generasi, pemeriksaan kepatuhan
Boundary: Mulai dari teks config, berakhir pada konfigurasi tervalidasi
Exclusions: Network monitoring real-time, traffic analysis
```

#### Langkah 2: Identifikasi Building Block yang diperlukan

```python
required_blocks = [
    "perception",    # Parse teks konfigurasi
    "memory",        # Panggil kembali pengetahuan vendor
    "reasoning",     # Analisis pola konfigurasi
    "decision",      # Pilih perbaikan
    "reflection",    # Verifikasi kualitas output
]
```

#### Langkah 3: Implementasikan Capability Pack

```python
# apps/my_app/__init__.py
from apps.base import BaseApp

class MyApp(BaseApp):
    @property
    def capabilities(self) -> list[str]:
        return ["my-domain:analyze", "my-domain:generate"]

    @property
    def pipeline(self) -> list[str]:
        return ["perception", "memory", "reasoning", "decision"]

def get_app() -> BaseApp:
    return MyApp()
```

#### Langkah 4: Daftarkan Keterampilan

```yaml
# agents/skills.yaml
skills:
  - id: "my-domain:analyze"
    name: "My Domain Analysis"
    pack: "my_app"
    description: "Analyze domain-specific input"
    pipeline: ["perception", "memory", "reasoning", "decision"]
```

#### Langkah 5: Implementasi Logika Kustom

letakkan logika khusus domain di modul aplikasi. Jaga layanan kognitif core tetap generik.

```
apps/my_app/
├── __init__.py           # Class App + factory
├── analyzer.py           # Logika analisis domain
├── generator.py          # Generasi output
└── models.py             # Model data domain
```

#### Langkah 6: Tambahkan Tes

```python
# tests/test_my_app.py
import pytest
from apps.my_app import get_app

@pytest.mark.asyncio
async def test_my_app_analyze():
    app = get_app()
    result = await app.analyze("test input")
    assert result["status"] == "success"
```

#### Langkah 7: Daftarkan API Rute

```python
# backend/app/api/my_app.py
from fastapi import APIRouter
from apps.my_app import get_app

router = APIRouter(prefix="/my-app")

@router.post("/analyze")
async def analyze(input: str):
    app = get_app()
    return await app.analyze(input)
```

#### Langkah 8: Integrasikan dengan Orkestrasi

```python
# Daftarkan di unified_orchestrator._extract_skills()
if "my-keyword" in task_lower:
    skills.append("my-domain")
```

---

## 6. Kerangka Keputusan Arsitektur

### 6.1 Kategori Keputusan

|Kategori|Kapan Digunakan|Membutuhkan ADR|
|---|---|---|
|**Perubahan Inti Platform**|Memodifikasi Event Bus, Memory Manager, Cognitive Kernel|✅ Ya|
|**Capability Pack Baru**|Menambahkan aplikasi domain baru|❌ Tidak (kecuali melanggar kontrak yang ada)|
|**Infrastruktur Baru**|Menambahkan PostgreSQL, penyedia LLM baru, antrian baru|✅ Ya (jika mengubah alur data)|
|**Perubahan Kontrak API**|Memodifikasi tanda tangan endpoint publik|✅ Ya (kompatibilitas mundur diperlukan)|
|**Memfaktorkan Ulang Internal**|Restrukturisasi di dalam modul|❌ Tidak|
|**Pola Baru**|Penggunaan pertama pola arsitektur baru|✅ Ya|

### 6.2 Diagram Alur Keputusan

```
Perlu mengubah ECP?
        │
        ├── Modifikasi core (Event Bus, Kernel, Memory)?
        │   └── ✅ ADR diperlukan + tinjauan Baseline freeze
        │
        ├── Tambah capability pack baru?
        │   └── ❌ Tidak perlu ADR. Ikuti Reference Architecture
        │
        ├── Ubah API publik?
        │   ├── Backward compatible? → ❌ Tidak perlu ADR
        │   └── Breaking change? → ✅ ADR + periode deprecation
        │
        └── Ubah infrastruktur?
            ├── Aditif (fitur baru)? → ❌ Tidak perlu ADR
            └── Mengganti (swap komponen)? → ✅ ADR diperlukan
```

### 6.3 Pengorbanan Evaluasi Templat

```markdown
## Keputusan: [Judul]

### Opsi yang Dipertimbangkan
1. Opsi A: [deskripsi]
2. Opsi B: [deskripsi]

### Kriteria Evaluasi
| Kriteria | Bobot | Opsi A | Opsi B |
|---|---|---|---|
| Development effort | 30% | 8/10 | 5/10 |
| Runtime performance | 25% | 7/10 | 9/10 |
| Maintainability | 25% | 9/10 | 6/10 |
| Platform alignment | 20% | 8/10 | 7/10 |

### Rekomendasi
Opsi A: [rasional]

### Konsekuensi
- Positif: [manfaat]
- Negatif: [tradeoff]
- Mitigasi: [cara mengatasi sisi negatif]
```

---

## 7. Katalog Pola

### Pola 1: Lajang Malas

**Konteks:** Menghindari impor melingkar saat memuat modul.

**Solusi:**

```python
# Alih-alih instansiasi level modul:
event_bus = EventBus()  # ❌ Dapat menyebabkan circular imports

# Gunakan inisialisasi lazy:
_event_bus = None

def get_event_bus() -> EventBus:
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus
```

**Digunakan di:** `unified_orchestrator.py`, `event_bus.py`

---

### Pola 2: Eksekusi Saluran Pipa

**Konteks:** Mengeksekusi urutan layanan kognitif di mana setiap layanan memperkaya konteks bersama.

**Solusi:**

```python
async def execute_pipeline(pipeline: list[str], context: dict) -> dict:
    result = context
    for service_name in pipeline:
        service = services[service_name]
        result = await service.process(result)
        result[f"{service_name}_result"] = result
    return result
```

**Digunakan di:** `cognitive_kernel.py`, `adaptive_runtime.py`

---

### Pola 3: AST Universal

**Konteks:** Mendukung banyak format vendor tanpa kerumitan N×M.

**Solusi:**

```
vendor_config → [Vendor Parser] → UniversalAST → [Analisis/Generasi]
                                      │
                                      ├── UniversalFirewallRule
                                      ├── UniversalNATRule
                                      ├── UniversalBGP
                                      └── UniversalInterface
```

**Digunakan di:** `apps/network_engineer/`, `attachments/parsers/network/`

---

### Pola 4: Pemisahan Berbasis Peristiwa

**Konteks:** Modul harus berkomunikasi tanpa kopling langsung.

**Solusi:**

```python
# Publisher: Tidak tahu subscriber
await event_bus.publish(Event(
    event_type="task.completed",
    payload={"task_id": task.id, "result": result},
    source="execution_scheduler",
))

# Subscriber: Tidak tahu publisher
event_bus.subscribe("task.completed", handle_task_completed)
```

**Digunakan di:** `event_bus.py` — komunikasi lintas-modul

---

### Pola 5: Konsolidasi Memori

**Konteks:** Membantu pertumbuhan memori tak terbatas sambil mempertahankan informasi penting.

**Solusi:**

```
threshold terlampaui → kumpulkan entri → ringkasan LLM → konsolidasi → simpan di long-term → hapus asli
```

**Pemicu:** Otomatis saat lapisan memori mana pun melebihi 50 entri.

**Digunakan di:** `memory_layer.py`

---

### Pola 6: Pemilihan Saluran Kognitif

**Konteks:** Kompleksitas tugas yang berbeda memerlukan kedalaman pemrosesan kognitif yang berbeda.

**Solusi:**

```python
complexity = cognitive_budget.estimate(task)
pipeline = PIPELINE_PRESETS[complexity]
# TRIVIAL → 4 layanan (cepat, murah)
# COMPLEX → 10 layanan (menyeluruh, mahal)
```

**Digunakan di:** `adaptive_runtime.py`

---

## 8. Anti Pola

### Anti-Pola 1: Panggilan Langsung Lintas-Modul

```python
# ❌ ANTI-POLAR: Import langsung antar capability packs
from apps.code_engineer import CodeEngineerApp
network_app = NetworkEngineerApp()
network_app._code_engineer = CodeEngineerApp()  # Tight coupling!

# ✅ BENAR: Gunakan Event Bus
await event_bus.publish(Event(
    event_type="code:analyze",
    payload={"code": config_script},
    source="network_engineer",
    target="code_engineer",
))
```

### Anti-Pola 2: Aplikasi Inti Mengimpor

```python
# ❌ ANTI-POLAR: Modul core mengimpor app
from apps.network_engineer import NetworkEngineerApp
# Ini membuat circular dependency: apps → core → apps

# ✅ BENAR: Apps mengimpor core, bukan sebaliknya
from backend.app.core.adaptive_runtime import adaptive_runtime
```

### Anti-Pola 3: Akses Infrastruktur Langsung dari Apps

```python
# ❌ ANTI-POLAR: App mengakses infrastruktur langsung
import redis.asyncio as aioredis
redis = aioredis.from_url("redis://localhost")

# ✅ BENAR: Gunakan abstraksi platform
from backend.app.core.memory_layer import memory_manager
await memory_manager.store("working", key, value)
```

### Anti-Pola 4: Pipa Melewati

```python
# ❌ ANTI-POLAR: Panggilan layanan langsung melewati pipeline
from backend.app.core.decision_engine import decision_engine
result = await decision_engine.decide(options, context)
# Melewati perception, memory, reasoning, planning

# ✅ BENAR: Gunakan pipeline
from backend.app.core.cognitive_kernel import cognitive_kernel
result = await cognitive_kernel.execute_pipeline(
    ["perception", "memory", "reasoning", "decision"],
    {"input": task}
)
```

### Anti-Pola 5: Pertumbuhan Memori Tak Terbatas

```python
# ❌ ANTI-POLAR: Simpan tanpa rencana konsolidasi
await memory_manager.store("episodic", key, value)
# Tidak pernah dipanggil: await memory_manager.compress_memory("episodic")

# ✅ BENAR: Konsolidasi otomatis via threshold
# MemoryManager menegakkan compression pada threshold=50
```

---

## 9. Atribut Kualitas

### 9.1 Tradeoff Atribut Kualitas

|Atribut|Cara ECP Mengatasinya|Pengorbanan|
|---|---|---|
|**Pertunjukan**|Pemilihan saluran pipa meminimalkan layanan yang tidak perlu|Kurang menyeluruh untuk tugas kompleks jika salah klasifikasi|
|**Skalabilitas**|Bus Acara memungkinkan penskalaan horizontal; konsolidasi memori membatasi pertumbuhan|Ketergantungan Redis menambah kerumitan operasional|
|**Keandalan**|Pemulihan Negara untuk tugas panjang; persistensi Event Bus|Penyimpanan tambahan untuk pos pemeriksaan data|
|**Keamanan**|RBAC melalui SecurityModel; isolasi penyewa melalui Tata Kelola|Latensi tambahan pada pemeriksaan autentikasi|
|**Kemampuan Pemeliharaan**|Kopling longgar melalui Bus Acara; aturan ketergantungan jelas|Alur acara implisit — membutuhkan dokumentasi|
|**Kemampuan untuk diuji**|426 unit uji; lapisan memori dapat di-mock|Tes integrasi membutuhkan Redis/PostgreSQL|
|**Kemungkinan diperpanjang**|Pola Capability Pack; sistem Plugin|Paket baru harus mengimplementasikan kontrak BaseApp|
|**Kemampuan observasi**|Telemetri peristiwa di semua operasi|Bus acara lalu lintas tambahan|

### 9.2 Mengukur Kualitas Atribut

|Atribut|Metrik|Target|pengukuran|
|---|---|---|---|
|Pertunjukan|Waktu respons P95|< 30 detik untuk saluran pipa MEDIUM|Benchmark pelari|
|Keandalan|Tingkat keberhasilan tugas|> 99%|Log sesi eksekusi|
|Kualitas Kode|Kesalahan MyPy|0|`mypy apps/ backend/`|
|Kualitas Tes|Tingkat kelulusan tes|> 95%|`pytest`|
|Cakupan|Cakupan garis|> 80%|`pytest --cov`|
|Ingatan|Ukuran lapisan memori|< 50 entri sebelum konsolidasi|`memory_manager.count()`|

---

## 10. Evolusi Arsitektur

### 10.1 Prinsip Evolusi

1. **Pertahankan baseline:** Jangan pernah merusak kontrak yang dibekukan tanpa ADR
2. **Tambahkan, jangan ganti:** Fungsionalitas baru harus aditif, bukan pengganti
3. **Abstraksikan, jangan konkritkan:** Jaga pola umum di inti; domain spesifik di aplikasi
4. **Dokumentasikan dulu:** ADR sebelum implementasi untuk perubahan arsitektur

### 10.2 Jalur Evolusi yang diharapkan

|Evolusi|Pemicu|Pendekatan|
|---|---|---|
|**Penyedia LLM baru**|Model lebih baik tersedia|Tambahkan ke `ModelRouter`, tanpa perubahan arsitektur|
|**Memori backend baru**|Pencarian Qdrant/vektor untuk pengetahuan|Tambahkan subkelas `MemoryLayer` baru, daftarkan di `MemoryManager`|
|**Penerapan multi-wilayah**|Skala produksi|Bus Acara → kompatibel Kafka/RabbitMQ|
|**Capability Pack baru**|Aplikasi domain baru|Ikuti Arsitektur Referensi, tanpa perubahan core|
|**Ekosistem Plugin**|Ekstensi pihak ketiga|Perluas `PluginManifest`, tambahkan marketplace|
|**Kolaborasi real-time**|Kebutuhan multi-pengguna|Tambahkan WebSocket ke Event Bus, resolusi konflik|

### 10.3 Penghentian Kebijakan

1. Tandai sebagai tidak digunakan lagi di CHANGELOG.md + komentar dokumen
2. Mempertahankan kompatibilitas mundur selama 2 versi minor
3. Hapus di versi mayor berikutnya
4. Panduan migrasi sediakan

---

## 11. Dokumen Terkait

|Dokumen|Lokasi|Tujuan|
|---|---|---|
|Dasar Teknik|`docs/ENGINEERING_BASELINE.md`|Apa yang membekukan|
|Arsitektur AES|`docs/AES_ARCHITECTURE.md`|Bagaimana platform dibangun|
|Kebijakan Gerbang Mutu|`docs/quality/QUALITY_GATES.md`|Aturannya bergabung|
|Keputusan Arsitektur|`docs/adr/ADR-*.md`|Mengapa keputusan dibuat|
|Panduan Pengembangan Aplikasi|`docs/APP_DEV_GUIDE.md`|Langkah demi langkah untuk tim aplikasi|
|Ringkasan Pengerasan Sprint|`SPRINT_HARDENING_SUMMARY.md`|Apa yang diperbaiki|
|API Referensi|`docs/api_reference.md`|Titik akhir dokumentasi API|

---

## Riwayat Dokumen Versi

|Versi|Tanggal|Perubahan|
|---|---|---|
|1.0.0|2024|Dokumen Referensi Arsitektur awal|

---

*Akhir dari Arsitektur Referensi*
