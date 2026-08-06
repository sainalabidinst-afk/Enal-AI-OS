# Data Engineer — Spesifikasi Capability

**Versi:** 2.0.0
**Status:** Production Ready (RFC-0009)
**Target Kualitas:** A (≥90), Domain Expert (L4)
**Sertifikasi:** Certified Lifecycle (RFC-0009)

---

## 1. Tujuan

Data Engineer adalah **otoritas rekayasa data** untuk ECP — Capability Pack yang menangani ETL/ELT, pembersihan data, validasi, schema evolution, feature engineering, penanganan time-series, dan data quality assurance.

Capability Pack ini mengekstrak data dari berbagai sumber, menerapkan transformasi, memvalidasi kualitas, dan menghasilkan dataset yang siap dikonsumsi — **tanpa memodifikasi Core**.

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- **ETL/ELT Pipeline** — Ekstraksi, transformasi, dan loading dari berbagai sumber (CSV, JSON, API, DB)
- **Data Cleaning** — Deteksi dan perbaikan nilai hilang, duplikat, outlier, masalah format
- **Dataset Validation** — Validasi skema, integritas, dan kualitas data
- **Schema Evolution** — Deteksi schema drift dan rencana migrasi
- **Feature Engineering** — Generasi fitur turunan dengan lineage
- **Time-series Handling** — Penyelarasan, interpolasi, dan resampling data dari waktu ke waktu
- **Data Quality Assurance** — Mengukur metrik completeness, uniqueness, validity, freshness, consistency
- **Experience Memory** — Merekam hasil ke riwayat

### Di Luar Cakupan
- Eksekusi pipeline di production
- Modifikasi kontrak Core
- Import langsung dari Capability Pack lain (kepatuhan ADR-002)

---

## 3. Kontrak

### Input: DataEngineeringRequest
```json
{
  "request_id": "uuid",
  "job_type": "etl | elt | clean | validate | schema_evolve | feature_engineer | time_series",
  "source": {
    "type": "csv | json | file | api | database",
    "location": "string — file path or URL",
    "schema_definition": {"column": "type"}
  },
  "operations": [
    {"operation": "fill_missing", "parameters": {"strategy": "mean"}},
    {"operation": "drop_duplicates", "parameters": {"subset": ["id"]}},
    {"operation": "normalize", "parameters": {"columns": ["salary"]}}
  ],
  "quality_rules": [
    {"rule": "completeness", "thresholds": {"min": 0.8}},
    {"rule": "uniqueness", "thresholds": {"min": 0.9}}
  ],
  "feature_definitions": [
    {"name": "salary_per_year", "type": "numerical", "dependencies": ["salary"], "expression": "salary * 12"}
  ],
  "time_series_config": {
    "frequency": "1h | 1d | 1w",
    "interpolation_method": "linear | forward_fill | nearest"
  }
}
```

### Output: Laporan Data Engineering
```json
{
  "request_id": "uuid",
  "job_type": "string",
  "status": "success | partial | failed",
  "dataset": {
    "row_count": 1000,
    "column_count": 5,
    "schema_definition": {"id": "string", "age": "integer"},
    "quality_score": 0.85
  },
  "quality_report": {
    "completeness": 0.95,
    "uniqueness": 0.98,
    "validity": 0.92,
    "freshness": 1.0,
    "consistency": 0.90,
    "overall_score": 0.93,
    "issues": [
      {"type": "missing_values", "column": "age", "severity": "medium", "count": 5}
    ]
  },
  "schema_drift": {
    "detected": true,
    "changes": [{"column": "email", "change_type": "added", "new_type": "string"}]
  },
  "features": [
    {"name": "salary_per_year", "type": "numerical", "description": "Annual salary"}
  ],
  "time_series": {
    "frequency": "1h",
    "missing_count": 3,
    "interpolated_count": 3,
    "alignment_complete": true
  },
  "lineage": {
    "source": "s3://bucket/data.csv",
    "transforms": ["fill_missing", "drop_duplicates"],
    "target": "output_abc123"
  },
  "explanation": "Processed etl job. Quality score: 93%. Issues: 3."
}
```

---

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `etl` | Pipeline Extract, Transform, Load | source, operations, target_schema | Dataset bersih |
| `elt` | Pipeline Extract, Load, Transform | source, operations | Dataset ter-transformasi |
| `clean` | Pembersihan dan remediasi data | source, operations | Dataset + issues bersih |
| `validate` | Validasi dataset | source, schema, quality_rules | Quality Report |
| `schema_evolve` | Deteksi schema drift | source, old_schema, new_schema | SchemaDrift Report |
| `feature_engineer` | Feature engineering | source, feature_definitions | Generated Features |
| `time_series` | Pemrosesan time-series | source, time_series_config | Time Series Report |

---

## 5. Modul Analyzer

| Modul | Tanggung Jawab |
|--------|----------------|
| `etl_pipeline.py` | Mengekstrak dari CSV/JSON/API/DB, transformasi, loading |
| `cleaner.py` | Mendeteksi dan memperbaiki nilai hilang, duplikat, outlier |
| `validator.py` | Memvalidasi dataset terhadap skema dan aturan kualitas |
| `schema_evolver.py` | Mendeteksi schema drift dan membuat rencana migrasi |
| `feature_store.py` | Menghasilkan fitur turunan dengan lineage |
| `time_series.py` | Menyelaraskan, menginterpolasi, me-resample data time-series |
| `quality_assurance.py` | Mengukur dan melaporkan metrik kualitas data |

---

## 6. Dimensi Benchmark

**Hasil Terverifikasi:**
- Overall: 90.00%
- Pass rate: 100%
- Status: PASS (A Certified)


| Dimensi | Target | Grade |
|-----------|--------|-------|
| Data Cleaning Accuracy | ≥90% | A |
| Dataset Validation Rate | ≥95% | A |
| Schema Drift Detection | ≥90% | A |
| Feature Engineering Consistency | ≥90% | A |
| Time Series Integrity | ≥90% | A |
| Data Quality Coverage | ≥90% | A |
| Explainability | ≥90% | A |
| Consistency | ≥90% | A |

---

## 7. Dependensi

- **apps/base.py** — Definisi model dasar
- **apps/data_engineer/schemas.py** — Kontrak publik
- **apps/data_engineer/etl_pipeline.py** — Pipeline ETL/ELT
- **apps/data_engineer/cleaner.py** — Pembersihan data
- **apps/data_engineer/validator.py** — Validasi dataset
- **apps/data_engineer/schema_evolver.py** — Deteksi schema drift
- **apps/data_engineer/feature_store.py** — Feature engineering
- **apps/data_engineer/time_series.py** — Pemrosesan time-series
- **apps/data_engineer/quality_assurance.py** — Metrik kualitas data
- **apps/data_engineer/engine.py** — Orchestrator domain engine
- **apps/data_engineer/worker.py** — Adaptor worker tipis (ADR-003)

---

## 8. Contoh Penggunaan

```python
from apps.data_engineer.engine import DataEngineerEngine
from apps.data_engineer.schemas import DataEngineeringRequest, DataSource, SourceType

engine = DataEngineerEngine()
request = DataEngineeringRequest(
    job_type="etl",
    source=DataSource(type=SourceType.file, location="data.csv"),
    operations=[{"operation": "fill_missing", "parameters": {"strategy": "mean"}}],
    quality_rules=[{"rule": "completeness", "thresholds": {"min": 0.9}}],
)
report = engine.process(request)
print(f"Quality score: {report.quality_report.overall_score:.0%}")
print(f"Rows processed: {report.dataset.row_count}")
```

---

## 9. Audit Keamanan

| Aspek | Status | Catatan |
|--------|--------|---------|
| Input Validation | ✅ | Source data divalidasi untuk tipe dan format |
| PII Handling | ✅ | Anonymization workflow tersedia untuk data sensitif |
| Output Sanitization | ✅ | Metadata tidak mengekspos data sensitif |
| Access Control | ✅ | Hanya membaca source data — tidak menulis tanpa eksplisit |
| Audit Trail | ✅ | Lineage tracking untuk semua transformasi |

**Catatan Keamanan:**
- Data Engineer dapat diakses untuk data sensitif — anonymization diperlukan untuk PII.
- Lineage tracking membantu audit data access untuk compliance (GDPR Article 30).
- Output tidak menyimpan data sensitif dalam log kecuali di-redact.

---

## 10. Optimasi Kinerja

| Aspek | Rekomendasi | Dampak |
|--------|-------------|--------|
| ETL Pipeline | Chunked processing untuk large files (>1GB) | Memory efficient |
| Data Cleaning | Vectorized operations (pandas/numpy) | 10x faster cleaning |
| Validation | Schema validation dengan batch mode | Reduced overhead |
| Feature Engineering | Feature lineage caching | Avoid recomputation |
| Time Series | Pre-computed alignment untuk regular frequency | Faster resampling |
| Quality Assurance | Parallel metric computation | Multi-core utilization |
| Schema Evolution | Incremental drift detection | Only check changed columns |

**Target Throughput:**
- ETL (1M rows): < 30 detik
- Validation (1M rows): < 10 detik
- Feature engineering (100 features): < 5 detik
- Time series resampling (1M points): < 15 detik

---

## 11. Skenario Golden Test

| # | Skenario | Input | Output yang Diharapkan |
|---|----------|-------|------------------------|
| 1 | Desain Pipeline ETL | CSV sales data + operations | Dataset bersih, quality score ≥ 0.9 |
| 2 | Validasi Dataset | Customer CSV + quality rules | Validation report dengan 5D metrics |
| 3 | Deteksi Schema Drift | Orders v1 → v2 schema | Schema drift report + migration plan |
| 4 | Feature Engineering | Customer data + feature defs | 3+ fitur turunan dengan lineage |
| 5 | Time Series Sensor Data | Sensor CSV, config 1h | Aligned data, interpolation count |
| 6 | Pipeline ELT Data Lake | API source + operations | ELT complete, lineage traced |
| 7 | Pembersihan Data | Messy CSV + outlier ops | Outlier count, missing filled count |
| 8 | Lineage Tracking | DB source + transforms | Full lineage: source → transforms → target |
| 9 | Kualitas Data Metrics | Customer CSV + 5D rules | All 5D metrics, issues report |
| 10 | Streaming ETL Kafka | Kafka source + window ops | Stream processed, watermark handled |

Golden Tests: `golden_tests/data_engineer/`

