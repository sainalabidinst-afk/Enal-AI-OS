# Documentation Engineer — Spesifikasi Capability

**Versi:** 1.0.0
**Status:** Production Ready (RFC-0016)
**Target Kualitas:** A (≥90)

---

## 1. Tujuan

Documentation Engineer adalah **otoritas dokumentasi teknis** untuk ECP — Capability Pack yang menghasilkan dan memvalidasi OpenAPI specs, dokumentasi SDK, dokumentasi arsitektur, dan release notes dari implementasi kode dan metadata proyek.

Capability Pack ini memastikan dokumentasi selalu akurat, konsisten, dan lengkap — **tanpa memodifikasi Core**.

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- **OpenAPI Generation** — Menghasilkan spesifikasi OpenAPI dari implementasi kode
- **SDK Documentation** — Menghasilkan panduan SDK dengan contoh kode yang dapat dijalankan
- **Architecture Documentation** — Menghasilkan dokumen arsitektur dari ADR, RFC, dan struktur kode
- **Documentation Validation** — Memvalidasi kelengkapan, konsistensi, dan akurasi dokumentasi
- **Release Notes Generation** — Menghasilkan catatan rilis dari commit dan perubahan kode
- **Experience Memory** — Merekam hasil ke riwayat

### Di Luar Cakupan
- Penulisan dokumentasi manual sepenuhnya
- Desain visual dan tata letak
- Manajemen hosting dan deployment dokumentasi
- Modifikasi kontrak Core

---

## 3. Kontrak

### Input: DocumentationRequest
```json
{
  "request_id": "uuid",
  "operation": "openapi_generation | sdk_documentation | architecture_documentation | documentation_validation | release_notes_generation",
  "target": {
    "app_name": "string — e.g., devops-assistant",
    "version": "string — e.g., 2.0.0",
    "output_path": "string — e.g., docs/api/"
  },
  "options": {
    "include_examples": true,
    "validate_links": true,
    "generate_diagrams": true,
    "include_deprecated": false
  },
  "inputs": {
    "source_code_path": "string",
    "existing_docs_path": "string",
    "commit_range": "string — e.g., v1.0.0..v2.0.0",
    "architecture_artifacts": ["string"]
  }
}
```

### Output: DocumentationReport
```json
{
  "request_id": "uuid",
  "operation": "string",
  "generated_files": [
    {
      "path": "string",
      "type": "openapi | sdk | architecture | release_notes | validation_report",
      "size_bytes": 0,
      "status": "generated | validated | skipped | failed",
      "issues": [
        {
          "severity": "error | warning | info",
          "message": "string",
          "location": "string"
        }
      ]
    }
  ],
  "summary": {
    "total_files": 0,
    "generated": 0,
    "validated": 0,
    "errors": 0,
    "warnings": 0
  },
  "quality_metrics": {
    "completeness": 0.93,
    "accuracy": 0.95,
    "consistency": 0.90,
    "freshness": 0.95
  },
  "explanation": "string — human-readable summary"
}
```

---

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `openapi_generation` | Menghasilkan spesifikasi OpenAPI dari kode | source_code_path, app_name | OpenAPI YAML/JSON |
| `sdk_documentation` | Menghasilkan dokumentasi SDK dengan contoh | source_code_path, app_name | Dokumentasi Markdown |
| `architecture_documentation` | Menghasilkan dokumen arsitektur | ADR, RFC, source_code | Diagram dan deskripsi arsitektur |
| `documentation_validation` | Memvalidasi dokumentasi yang ada | existing_docs_path, source_code_path | Laporan validasi |
| `release_notes_generation` | Menghasilkan catatan rilis | commit_range, app_name | Catatan rilis terstruktur |

---

## 5. Modul Analyzer

| Modul | Tanggung Jawab |
|--------|----------------|
| `openapi_generator.py` | Menghasilkan spesifikasi OpenAPI dari kode dan skema |
| `sdk_docs_generator.py` | Menghasilkan dokumentasi SDK dengan contoh kode |
| `architecture_docs.py` | Menghasilkan dokumen arsitektur dari ADR, RFC, dan kode |
| `validator.py` | Memvalidasi kelengkapan, konsistensi, dan akurasi dokumentasi |

---

## 6. Dimensi Benchmark

| Dimensi | Target | Grade |
|-----------|--------|-------|
| OpenAPI Accuracy | ≥95% | A |
| SDK Documentation Quality | ≥90% | A |
| Architecture Docs Completeness | ≥90% | A |
| Validation Rate | ≥95% | A |
| Release Notes Completeness | ≥90% | A |
| Consistency | ≥90% | A |
| Freshness | ≥95% | A |
| Explainability | ≥90% | A |

---

## 7. Dependensi

- **apps/base.py** — Definisi model dasar
- **apps/documentation_engineer/schemas.py** — Kontrak publik
- **apps/documentation_engineer/engine.py** — Domain engine
- **apps/documentation_engineer/worker.py** — Adaptor tipis (ADR-003)

---

## 8. Contoh Penggunaan

```python
from apps.documentation_engineer.engine import DocumentationEngine
from apps.documentation_engineer.schemas import DocumentationRequest, OperationType

engine = DocumentationEngine()
request = DocumentationRequest(
    operation=OperationType.openapi_generation,
    target={"app_name": "devops-assistant", "version": "2.0.0", "output_path": "docs/api/"},
    inputs={"source_code_path": "apps/devops_assistant/", "existing_docs_path": "docs/"},
)
report = engine.generate(request)
print(f"Generated {len(report.generated_files)} files")
print(f"Quality score: {report.quality_metrics.accuracy:.0%}")
```
