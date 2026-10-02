# ADR-022: Document Processing Pack Architecture

**ADR ID:** ADR-022
**RFC:** RFC-0042
**Tanggal:** 2026-10-02
**Status:** Accepted
**Topik:** Architecture Decision Record untuk Document Processing Capability Pack

## Konteks

Platform Enal-AI-OS (ECP) memiliki 35+ Capability Pack yang beroperasi di atas Core Runtime
yang dibekukan (Architecture Freeze Policy, ADR-001). Beberapa pack — terutama Legal Advisor,
Finance Analyst, dan Documentation Engineer — membutuhkan kemampuan membaca, mengedit,
dan memproduksi file Office (DOCX, XLSX, PPTX) serta PDF.

Saat ini, tidak ada Capability Pack yang menyediakan dokumen processing terpusat. Setiap pack
yang membutuhkan fungsionalitas ini harus mengimplementasikan sendiri, menyebabkan:

- Duplikasi kode parser/writer di setiap pack
- Inconsistensi dalam lazy import strategy untuk dependency opsional
- Risiko cross-capability import violations (Capability First Rule, ADR-002)

## Keputusan

Document Processing adalah Capability Pack baru yang **berada sepenuhnya di dalam `apps/document_processing/`**.
Tidak ada modifikasi pada Core, Runtime, Kernel, SDKs, atau kontrak bersama yang diperlukan.

### Arsitektur Modul

```
apps/document_processing/
├── __init__.py           # App registration (BaseReferenceApp)
├── schemas.py            # Public contracts (Pydantic models)
├── engine.py             # Orchestrator — memanggil DocumentEngine
├── document_engine.py    # Core pipeline: read → transform → write
├── office_reader.py      # Parser DOCX/XLSX/PPTX (lazy import)
├── pdf_reader.py         # Parser PDF (lazy import)
├── office_writer.py      # Generator Office files (lazy import)
├── pdf_writer.py         # Generator PDF (lazy import)
└── document_worker.py    # Thin adapter untuk Execution Runtime
```

### Lazy Import Strategy

Semua dependency opsional (python-docx, openpyxl, python-pptx, PyPDF2/pypdf, reportlab) harus
di-import menggunakan helper berikut yang didefinisikan di `document_engine.py`:

```python
def _lazy_import(module_name: str) -> Any:
    """Import optional dependency lazily, raising clear error if unavailable."""
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        raise ImportError(
            f"Optional dependency '{module_name}' is required for this operation. "
            f"Install with: pip install {module_name.replace('-', '_')}"
        ) from e
```

**Kebijatan ini karena:**

1. **Pack harus dapat di-import** tanpa dependency opsional terpasang (untuk registry loadability)
2. **Error hanya muncul** ketika operasi spesifik dipanggil, bukan pada import paket
3. **Governance checks** (boundary & cross-import) harus tetap passing

### Boundary Enforcement

- Document Processing **tidak meng-import** pack lain mana pun
- Document Processing **tidak meng-import** `backend.app.core` secara langsung
- Semua komunikasi lintas pack dilalui Execution Runtime (ADR-002)
- `document_worker.py` adalah thin adapter (ADR-003)

### Dokumen Engine Pipeline

Pipeline inti (`document_engine.py`):

```
Input (DocumentProcessingRequest)
  → validate_inputs
  → route_to_operation (read / edit / produce / convert / annotate / batch)
    → reader/writer sub-modules (lazy import)
  → build_report (DocumentProcessingReport)
Output (DocumentProcessingReport)
```

Semua operasi:
- Menggunakan formula yang disclosed
- Melacak input lineage
- Mengembalikan assumptions & limitations
- Menjaga safety boundary (tidak melebihi sumber daya yang diberikan)

## Implikasi

### Positif

- Satu source of truth untuk dokumen processing di seluruh ECP
- Reused oleh Legal Advisor, Finance Analyst, Documentation Engineer, Business Analyst, Compliance Officer
- Lazy import strategy konsisten dan testable
- Boundary checks otomatis di CI/CD (governance_checks.py)

### Negatif

- Tambahan satu pack baru ke registry (26 → 27 packs)
- Dependency opsional (python-docx, openpyxl, dll.) harus dikelola di environment tsbud

### Netral

- Tidak ada perubahan pada Core Runtime
- Semua komunikasi tetap melalui Execution Runtime dan kontrak bersama

## Referensi

- ADR-001: Core Pipeline Freeze
- ADR-002: Capability Pack Kemerdekaan
- ADR-003: Pekerja = Hanya Adaptor
- ADR-004: Logika Bisnis Milik Mesin Domain
- ADR-006: Capability Contract v1 Frozen
- RFC-0042: Document Processing Capability Pack
