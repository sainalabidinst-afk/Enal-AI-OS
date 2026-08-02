# Data Engineer — Spesifikasi Capability

**Versi:** 1.0.0
**Status:** Production Ready (RFC-0009)
**Target Kualitas:** A- (≥85)

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

| Dimensi | Target | Grade |
|-----------|--------|-------|
| Data Cleaning Accuracy | ≥95% | A |
| Dataset Validation Rate | ≥98% | A |
| Schema Drift Detection | ≥90% | A |
| Feature Engineering Consistency | ≥90% | A |
| Time Series Integrity | ≥90% | A |
| Data Quality Coverage | ≥95% | A |
| Explainability | ≥90% | A |
| Consistency | ≥90% | A |

---

## 7. Dependensi

- **apps/base.py** — Definisi model dasar
- **apps/data_engineer/schemas.py** — Kontrak publik
- **apps/data_engineer/engine.py** — Domain engine
- **apps/data_engineer/worker.py** — Adaptor tipis (ADR-003)

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
)
report = engine.process(request)
print(f"Quality score: {report.quality_report.overall_score:.0%}")
```

