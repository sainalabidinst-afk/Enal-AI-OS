<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: isi utama dokumen disajikan dalam versi Indonesia di bawah konten asli.
- English: the main prose content is presented in an Indonesian bilingual section below the original content.

### Informasi Dokumen / Document Info
- File: `docs/capabilities/data-engineer.md`
- Judul: Data Engineer
- Status: bilingual content applied

<!-- BILINGUAL_DOCS_END -->

# Data Engineer Capability Specification

## Version: 1.0.0
## Status: Production Ready (RFC-0009)
## Quality Target: A- (≥85)

---

## 1. Purpose

Data Engineer adalah **otoritas rekayasa data** untuk ECP — Capability Pack yang
menangani ETL/ELT, pembersihan data, validasi, evolusi skema, rekayasa fitur,
penanganan deret waktu, dan jaminan kualitas data.
> Terjemahan Indonesia: Data Engineer adalah otoritas rekayasa data untuk ECP — kapabilitas Pack yang menangani ETL/ELT, pembersihan data, validasi, evolusi skema, rekayasa fitur, penanganan deret waktu, dan jaminan kualitas data.

Capability Pack ini mengekstrak data dari berbagai sumber, menerapkan transformasi,
memvalidasi kualitas, dan menghasilkan dataset yang siap konsumsi — **tanpa memodifikasi Core**.
> Terjemahan Indonesia: Kapabilitas Pack ini mengekstrak data dari berbagai sumber, menerapkan transformasi, memvalidasi kualitas, dan menghasilkan dataset yang siap konsumsi — tanpa memodifikasi Core.

---

## 2. Scope

### In Scope
- **ETL/ELT Pipeline** — Extract, Transform, Load dari berbagai sumber (CSV, JSON, API, DB)
- **Data Cleaning** — Deteksi dan perbaikan nilai hilang, duplikat, outlier, format issues
- **Dataset Validation** — Validasi schema, integritas, dan kualitas data
- **Schema Evolution** — Deteksi drift skema dan rencana migrasi
- **Feature Engineering** — Generasi fitur turunan dengan lineage
- **Time Series Handling** — Alignment, interpolasi, resampling data deret waktu
- **Data Quality Assurance** — Ukur metrik kelengkapan, keunikan, validitas, freshness, konsistensi
- **Experience Memory** — Perekaman hasil ke history

### Out of Scope
- Eksekusi pipeline di production
- Modifikasi Core contracts
- Direct import dari Capability Pack lain (ADR-002 compliance)

---

## 3. Contract

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

### Output: DataEngineeringReport
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

## 4. Operations

| Operation | Description | Inputs | Outputs |
|-----------|-------------|--------|---------|
| etl | Extract, Transform, Load pipeline | source, operations, target_schema | Cleaned dataset |
| elt | Extract, Load, Transform pipeline | source, operations | Transformed dataset |
| clean | Data cleaning and remediation | source, operations | Cleaned dataset + issues |
| validate | Dataset validation | source, schema, quality_rules | QualityReport |
| schema_evolve | Schema drift detection | source, old_schema, new_schema | SchemaDriftReport |
| feature_engineer | Feature engineering | source, feature_definitions | Generated features |
| time_series | Time series processing | source, time_series_config | TimeSeriesReport |

---

## 5. Analyzer Modules

| Module | Responsibility |
|--------|----------------|
| etl_pipeline.py | Extract from CSV/JSON/API/DB, transform, load |
| cleaner.py | Detect and remediate missing values, duplicates, outliers |
| validator.py | Validate dataset against schema and quality rules |
| schema_evolver.py | Detect schema drift and generate migration plans |
| feature_store.py | Generate derived features with lineage |
| time_series.py | Align, interpolate, resample time-series data |
| quality_assurance.py | Measure and report data quality metrics |

---

## 6. Benchmark Dimensions

| Dimension | Target | Grade |
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

## 7. Dependencies

- **apps/base.py** — Base model definitions
- **apps/data_engineer/schemas.py** — Public contracts
- **apps/data_engineer/engine.py** — Domain Engine
- **apps/data_engineer/worker.py** — Thin adapter (ADR-003)

---

## 8. Usage Example

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
