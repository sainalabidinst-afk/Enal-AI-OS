# Research Assistant — Spesifikasi Capability

**Versi:** 2.0.0
**Status:** Bersertifikat (RFC-0020)
**Target Kualitas:** A+ (≥95) — Level 4 — Pakar Domain

---

## 1. Tujuan

Research Assistant adalah **sistem penelitian otomatis** untuk ECP — Capability Pack yang mengumpulkan bukti, mendeteksi kontradiksi, menilai kualitas sitasi, menghitung kepercayaan, mensintesis temuan multi-sumber, dan menghasilkan laporan penelitian terstruktur.

Capability Pack ini mengintegrasikan 6 modul inti (Evidence Ranker, Contradiction Detector, Citation Assessor, Confidence Estimator, Synthesis Engine, Report Generator) melalui pipeline analisis terstruktur — **tanpa memodifikasi Core**.

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- **Evidence Gathering** — Pengumpulan bukti dari multi-sumber dengan perankingan kualitas
- **Contradiction Detection** — Deteksi konflik antar-sumber (faktual, metodologis, interpretatif, temporal)
- **Citation Quality Assessment** — Penilaian kualitas sitasi (APA, MLA, IEEE, Chicago)
- **Confidence Estimation** — Estimasi kepercayaan dengan kuantifikasi ketidakpastian
- **Synthesis** — Sintesis naratif multi-sumber dengan identifikasi consensus
- **Report Generation** — Generasi laporan markdown dengan sitasi terstruktur
- **Quality Tracking** — Pelacakan metrik kualitas penelitian
- **Bias Detection** — Deteksi publication bias, selection bias
- **Source Verification** — Verifikasi kredibilitas sumber

### Di Luar Cakupan
- Penelitian primer / eksperimen lapangan
- Integrasi database literatur berbayar
- Penilaian etik penelitian
- Penulisan ilmiah penuh (hanya asistensi)

---

## 3. Kontrak

### Input: ResearchRequest
```json
{
  "query": "string — pertanyaan penelitian atau topik",
  "operation": "literature_review | evidence_gathering | contradiction_analysis | citation_assessment | confidence_estimation | synthesis | report_generation",
  "sources": [
    {
      "id": "string",
      "title": "string",
      "content": "string — isi sumber",
      "source_type": "academic | industry | news | blog | government",
      "url": "string (opsional)",
      "published_at": "ISO-8601 (opsional)",
      "author": "string (opsional)"
    }
  ],
  "context": "string — konteks penelitian tambahan",
  "max_sources": 10,
  "citation_style": "apa | mla | ieee | chicago"
}
```

### Output: ResearchReport
```json
{
  "query": "string",
  "operation": "string",
  "findings": [
    {
      "id": "uuid",
      "title": "string",
      "summary": "string",
      "confidence": 0.85,
      "sources": ["source_id_1", "source_id_2"]
    }
  ],
  "evidence": [
    {
      "id": "uuid",
      "source_id": "string",
      "content": "string",
      "quality_score": 0.9,
      "relevance_score": 0.85
    }
  ],
  "synthesis": {
    "narrative": "string — sintesis naratif",
    "consensus_areas": ["area1", "area2"],
    "conflict_areas": ["area1"],
    "confidence": 0.8
  },
  "contradictions": [
    {
      "id": "uuid",
      "type": "factual | methodological | interpretative | temporal",
      "description": "string",
      "source_a": "source_id",
      "source_b": "source_id",
      "severity": "high | medium | low"
    }
  ],
  "citations": [
    {
      "id": "uuid",
      "source_id": "string",
      "style": "apa | mla | ieee | chicago",
      "text": "string — formatted citation",
      "confidence": 0.9
    }
  ],
  "quality": {
    "overall_score": 0.85,
    "source_quality_avg": 0.8,
    "citation_coverage": 0.9,
    "bias_risk": 0.1
  },
  "report_markdown": "string — laporan lengkap dalam markdown",
  "metadata": {
    "generated_at": "ISO-8601",
    "sources_analyzed": 10,
    "processing_time_ms": 150
  }
}
```

---

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `literature_review` | Review literatur dari query penelitian | query, sources, context | ResearchReport |
| `evidence_gathering` | Kumpulkan dan rank bukti dari sumber | query, sources, max_sources | ResearchReport |
| `contradiction_analysis` | Deteksi kontradiksi antar-sumber | sources, context | ResearchReport |
| `citation_assessment` | Evaluasi kualitas sitasi | sources, citation_style | ResearchReport |
| `confidence_estimation` | Estimasi kepercayaan temuan | findings, sources | ResearchReport |
| `synthesis` | Sintesis multi-sumber | findings, evidence, context | ResearchReport |
| `report_generation` | Generasi laporan lengkap | query, findings, synthesis, citations | ResearchReport |

---

## 5. Modul

| Modul | File | Tanggung Jawab |
|-------|------|----------------|
| Engine | `engine.py` | Orchestrator, 7 operasi, routing |
| Schemas | `schemas.py` | 12 Pydantic models (request/response) |
| Worker | `worker.py` | Thin adapter ke ECP Runtime |
| EvidenceRanker | `evidence_ranker.py` | Composite quality scoring |
| ContradictionDetector | `contradiction_detector.py` | Regex-based conflict detection |
| CitationAssessor | `citation_assessor.py` | Multi-style citation quality |
| ConfidenceEstimator | `confidence_estimator.py` | Weighted confidence + uncertainty |
| SynthesisEngine | `synthesis_engine.py` | Multi-source narrative synthesis |

---

## 6. Dimensi Benchmark

| Dimensi | Deskripsi | Target |
|---------|-----------|--------|
| accuracy | Ketepatan temuan penelitian | ≥95% |
| completeness | Kelengkapan cakupan topik | ≥95% |
| explainability | Kejelasan alur penalaran | ≥95% |
| safety | Keamanan konten (bias, kontradiksi) | ≥95% |
| efficiency | Kecepatan proses | ≥90% |
| consistency | Konsistensi lintas runs | ≥95% |

---

## 7. Audit Keamanan

### OWASP Top 10
- A03:2021 – Injection: Prompt injection dalam query penelitian
- A05:2021 – Security Misconfiguration: Default API keys untuk sumber
- A06:2021 – Vulnerable Components: Dependencies LLM yang outdated
- A08:2021 – Data Integrity Failures: Fabricated citations atau sources
- A09:2021 – Logging Failings: Missing audit trail untuk penelitian

### Deteksi Rahasia
- API keys dan tokens dalam input sources
- Credentials dalam URL sumber
- PII ( Personally Identifiable Information ) dalam konten sumber

### Pencegahan Injeksi
- Prompt injection dalam query penelitian
- Data injection melalui sources
- Citation injection (fake citations)

### Validasi Input
- Validasi query untuk panjang dan format
- Validasi sources untuk kredibilitas
- Validasi citation style

### Default Aman
- Source verification sebelum analisis
- Bias detection untuk setiap findings
- PII redaction dalam output

---

## 8. Optimasi Kinerja

### Strategi Caching
- Source analysis cache untuk sumber yang tidak berubah
- Citation formatting cache untuk style yang sama
- Benchmark result cache untuk skenario yang sama

### Peluang Paralelisme
- Parallel analysis untuk banyak sources
- Independent checks (quality, citation, contradiction) paralel
- Report generation paralel untuk bagian yang berbeda

### Optimasi Memori
- Streaming processing untuk banyak sources
- Lazy loading untuk source knowledge base
- Disk-based cache untuk large analysis results

### Efisiensi Token
- Context window management untuk large documents
- Chunking strategy untuk long sources
- Selective analysis berdasarkan relevance threshold

---

## 9. Dependensi Eksternal

| Package | Kegunaan |
|---------|----------|
| `pydantic` | Schema validation |
| `litellm` | LLM orchestration |
| `langchain-openai` | LLM provider |
| `aiohttp` | Async HTTP (fetch sources) |

---

## 10. Integrasi

| Capability Pack | Integrasi | Deskripsi |
|-----------------|-----------|-----------|
| Code Engineer | Ya | Review kode berbasis temuan penelitian |
| Security Engineer | Ya | Analisis kerentanan berbasis riset |
| Network Engineer | Ya | Best practice dari literatur jaringan |
| DevOps Assistant | Ya | Automate CI/CD berbasis riset |

---

## 11. Contoh Penggunaan

```python
from apps.research_assistant.engine import ResearchEngine
from apps.research_assistant.schemas import ResearchRequest, ResearchOperation

engine = ResearchEngine()
request = ResearchRequest(
    query="Impact of microservices on system reliability",
    operation=ResearchOperation.literature_review,
    max_sources=10,
)
report = engine.run(request)
print(f"Generated report with {len(report.findings)} findings")
print(f"Report markdown length: {len(report.report_markdown)} chars")
```

---

## 12. Riwayat Perubahan

| Versi | Tanggal | Perubahan |
|-------|---------|-----------|
| 2.0.0 | 2026-08-05 | Level 4 Domain Expert, A+ grade, 10 golden tests, security audit, performance optimization, RFC-0020 |
| 1.0.0 | 2026-08-04 | Production Ready, 150 real cases, 96.67% benchmark score, 19 golden tests |
