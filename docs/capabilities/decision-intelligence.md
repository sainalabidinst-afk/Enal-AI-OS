# Spesifikasi Capability Pack Decision Intelligence

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Spesifikasi Capability Pack untuk Decision Intelligence
<!-- DOCUMENT_METADATA_END -->

## Versi: 2.0.0
## Status: Production Ready (RFC-0007)
## Quality Target: A+ (≥95), Domain Expert (L4)
## Sertifikasi: Certified Lifecycle (RFC-0007)

---

## 1. Tujuan

Decision Intelligence adalah **lapisan penalaran bersama (shared reasoning layer)** untuk ECP — Capability Pack yang menyediakan pengambilan keputusan berbasis bukti, dapat dijelaskan, dan dapat diaudit untuk semua Capability Pack lainnya.

Bertindak sebagai layanan lintas-capability **tanpa memodifikasi Core**.

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- Pengumpulan bukti dari berbagai sumber (analisis, rekomendasi, data, Benchmark, riwayat)
- Generasi alternatif dengan pemfilteran constraint
- Analisis risiko (probabilitas × dampak)
- Analisis trade-off (skor tertimbang multi-objektif, batas Pareto)
- Skoring keputusan dan pemeringkatan
- Estimasi confidence (0–100%, lower bound, kalibrasi)
- Keputusan yang dapat dijelaskan (rantai lengkap: bukti → reasoning → alternatif → risiko → keputusan → rationale)
- Riwayat keputusan (pencatatan ke Experience Memory, audit trail)

### Di Luar Ruang Lingkup
- Eksekusi keputusan otomatis (hanya rekomendasi — memenuhi ADR-005)
- Modifikasi kontrak Core
- Impor langsung dari Capability Pack lain (kepatuhan ADR-002)

---

## 3. Kontrak

### Input: DecisionRequest
```json
{
  "decision_id": "uuid",
  "context": "string (natural-language decision context)",
  "evidence_sources": [
    {
      "source_id": "trading_analyst|network|code|research|devops|self-development",
      "evidence_type": "analysis|recommendation|data|benchmark|historical",
      "payload": {},
      "quality_score": 0.0-1.0,
      "weight": 0.0-2.0
    }
  ],
  "constraints": ["string hard constraints"],
  "objectives": [
    {"name": "Accuracy", "weight": 0.35, "goal": "maximize"}
  ],
  "risk_tolerance": "low|medium|high",
  "max_alternatives": 5,
  "include_explanation": true
}
```

### Output: DecisionResult
```json
{
  "decision_id": "uuid",
  "recommended_decision": "string",
  "alternatives": [
    {
      "description": "string",
      "score": 0.0-1.0,
      "risk_profile": {
        "overall_risk": 0.0-1.0,
        "probability": 0.0-1.0,
        "impact": 0.0-1.0,
        "risk_factors": []
      },
      "trade_offs": {}
    }
  ],
  "confidence_score": 0.0-1.0,
  "confidence_explanation": "string",
  "explanation": {
    "evidence_summary": "string",
    "reasoning_chain": ["string"],
    "simulation_results": {},
    "risk_assessment": "string",
    "final_rationale": "string"
  },
  "decision_history_ref": "uuid"
}
```

---

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `evaluate` | Evaluasi lengkap dengan evidence → alternatives → risk → trade-off → score → confidence → explanation | DecisionRequest | DecisionResult |
| `evaluate_quick` | Evaluasi cepat (tanpa alternatives lengkap) | DecisionRequest | DecisionResult |
| `score_alternatives` | Skoring alternatif berdasarkan objectives | alternatives, objectives | scored_alternatives |
| `analyze_risk` | Analisis risiko (probability × impact) untuk alternatif | alternative | risk_profile |
| `estimate_confidence` | Estimasi keyakinan (0–100%) dengan kalibrasi | evidence_sources, result | confidence_score + explanation |

## 5. Modul Analyzer

| Modul | Tanggung Jawab |
|--------|----------------|
| `evidence_collector.py` | Mengumpulkan, memvalidasi, dan menimbang bukti dari berbagai sumber |
| `alternative_generator.py` | Menghasilkan dan memfilter alternatif berdasarkan constraint |
| `risk_analyzer.py` | Menganalisis risiko (probability × impact) untuk setiap alternatif |
| `tradeoff_analyzer.py` | Analisis trade-off multi-objektif dan batas Pareto |
| `scoring_engine.py` | Menghitung skor komposit dan memeringkatkan alternatif |
| `confidence_estimator.py` | Menghasilkan estimasi confidence (0–100%) dengan kalibrasi |
| `explanation_generator.py` | Menghasilkan rantai penjelasan yang lengkap |
| `decision_history.py` | Mencatat keputusan ke Experience Memory |

## 6. Dimensi Benchmark

| Dimensi | Target | Grade |
|-----------|--------|-------|
| Decision Accuracy | ≥95% | A+ |
| Completeness | ≥95% | A+ |
| Explainability | 100% | A+ |
| Safety | ≥95% | A+ |
| Efficiency | ≥95% | A+ |
| Consistency | ≥95% | A+ |
| Confidence Calibration | ≥95% | A+ |
| Risk Detection | ≥95% | A+ |

---

## 7. Skenario Golden Test

| # | Skenario | Input | Output yang Diharapkan |
|---|----------|-------|------------------------|
| 1 | Pemilihan Cloud Provider | context: pilih AWS/GCP/Azure | DecisionResult dengan 3 alternatif, confidence ≥ 0.75 |
| 2 | Build vs Buy: Sistem Autentikasi | context: build vs buy auth | DecisionResult dengan rekomendasi dan TCO analysis |
| 3 | Microservices vs Monolith | context: startup 10 engineer | DecisionResult dengan migration criteria |
| 4 | Framework Selection: API Gateway | context: 10K RPS | DecisionResult dengan 3 framework alternatives |
| 5 | Hiring: Staff vs Konsultan | context: budget < 200K/th | DecisionResult dengan cost-benefit analysis |
| 6 | Data Storage: RDBMS vs Data Lake | context: e-commerce | DecisionResult dengan hybrid recommendation |
| 7 | Caching Strategy | context: P99 latency 500ms | DecisionResult dengan multi-layer strategy |
| 8 | Product Roadmap Priority | context: Q3 feature selection | DecisionResult dengan timeline roadmap |
| 9 | Vendor Negotiation | context: SaaS contract renewal | DecisionResult dengan negotiation leverage |
| 10 | Security Compliance Path | context: SOC 2 vs ISO 27001 | DecisionResult dengan dual certification strategy |

Golden Tests: `golden_tests/decision_intelligence/`

---

## 8. Audit Keamanan

| Aspek | Status | Catatan |
|--------|--------|---------|
| Input Validation | ✅ | Semua input divalidasi via Pydantic schema |
| Output Sanitization | ✅ | Tidak ada data sensitif dalam output DecisionResult |
| Evidence Source Trust | ✅ | Quality score (0–1) untuk setiap bukti; source validation diperlukan |
| Constraint Enforcement | ✅ | Hard constraints memfilter alternatif sebelum skoring |
| Explainability | ✅ | Full chain: bukti → reasoning → alternatif → risiko → keputusan |
| Audit Trail | ✅ | Setiap keputusan dicatat ke Experience Memory |
| No Auto-Execution | ✅ | Hanya rekomendasi — memenuhi ADR-005 |

**Catatan Keamanan:**
- Decision Intelligence tidak mengeksekusi keputusan secara otomatis (ADR-005 compliance).
- Confidence score merepresentasikan ketidakpastian — tidak boleh dianggap sebagai kepastian.
- Evidence source harus divalidasi untuk mencegah poisoning decision dengan data yang tidak terpercaya.

---

## 9. Optimasi Kinerja

| Aspek | Rekomendasi | Dampak |
|--------|-------------|--------|
| Evidence Collection | Batch collect dari semua sumber secara paralel | Mengurangi latency pengumpulan bukti |
| Alternative Generation | Early termination saat constraint filter menyisakan < 2 alternatif | Mengurangi waktu komputasi |
| Risk Analysis | Pre-compute risk model untuk skenario umum | Cache hasil analisis risiko |
| Scoring Engine | Vectorized scoring untuk objectives yang independen | 2–3x peningkatan kinerja |
| Confidence Estimation | Calibrated model dengan pre-computed bounds | Konsisten < 50ms |
| Explanation Generation | Template-based explanation dengan slot filling | Mengurangi LLM call |
| Decision History | Async write ke Experience Memory (fire-and-forget) | Tidak memblokir response |
| Cache | Cache DecisionResult untuk konteks yang identik (hash-based) | Response time untuk repeat requests |

**Target Latensi:**
- Evaluate (quick): < 200ms
- Evaluate (full): < 1 detik
- Score alternatives: < 100ms

---

## 10. Integrasi Konsumen (Pertama: Trading Analyst)

Decision Intelligence menerima bukti dari:
- **Trading Analyst** — analisis pasar, bias, confidence, penilaian risiko
- **Network Engineer** — analisis konfigurasi, risk score, rekomendasi
- **Code Engineer** — analisis arsitektur, kualitas kode, security findings
- **Research Assistant** — kualitas bukti, confidence kutipan
- **DevOps Assistant** — risiko deployment, hasil verifikasi
- **Self Development** — dampak perubahan, penilaian risiko

`DecisionIntelligenceWorker` adalah adaptor tipis (ADR-003) yang merutekan tugas yang ditentukan ke `DecisionIntelligenceEngine.evaluate()`.

---

## 11. Kepatuhan Arsitektur

| Prinsip | Kepatuhan |
|-----------|------------|
| ADR-001 Core Pipeline Freeze | ✅ Zero Core Change |
| ADR-002 Capability Pack Independence | ✅ Tidak ada impor langsung |
| ADR-003 Worker = Hanya Adaptor | ✅ Worker mendelegasikan ke Engine |
| ADR-004 Domain Engine Memiliki Business Logic | ✅ Engine memiliki pipeline |
| ADR-005 Persetujuan Manusia Diperlukan | ✅ Rekomendasi saja, tanpa eksekusi otomatis |
| Kernel Stability | ✅ Tidak di Core |

---

## 12. File

| File | Tujuan |
|------|---------|
| `apps/decision_intelligence/schemas.py` | Model Pydantic |
| `apps/decision_intelligence/evidence_collector.py` | Pengumpulan bukti |
| `apps/decision_intelligence/alternative_generator.py` | Generasi alternatif |
| `apps/decision_intelligence/risk_analyzer.py` | Analisis risiko |
| `apps/decision_intelligence/tradeoff_analyzer.py` | Analisis trade-off |
| `apps/decision_intelligence/scoring_engine.py` | Skoring keputusan |
| `apps/decision_intelligence/confidence_estimator.py` | Estimasi confidence |
| `apps/decision_intelligence/explanation_generator.py` | Generasi penjelasan |
| `apps/decision_intelligence/decision_history.py` | Riwayat keputusan |
| `apps/decision_intelligence/engine.py` | Orchestrator domain engine |
| `apps/decision_intelligence/worker.py` | Adaptor worker tipis |
| `benchmarks/decision_intelligence_benchmark.py` | Benchmark (8 dimensi) |

