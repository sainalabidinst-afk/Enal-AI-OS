# Spesifikasi Capability Pack Decision Intelligence

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** Spesifikasi Capability Pack untuk Decision Intelligence
<!-- DOCUMENT_METADATA_END -->

## Versi: 1.0.0
## Status: Production Ready (RFC-0007)
## Quality Target: A (≥90)

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

## 4. Pipeline

```
DecisionRequest
    ↓
EvidenceCollection (collect, validate, weight)
    ↓
AlternativeGeneration (enumerate, filter constraints)
    ↓
RiskAnalysis (probability × impact)
    ↓
TradeoffAnalysis (multi-objective, weighted, Pareto)
    ↓
DecisionScoring (composite score, rank)
    ↓
ConfidenceEstimation (0-100%, calibration)
    ↓
ExplanationGeneration (full explainability chain)
    ↓
DecisionHistory (Experience Memory, audit trail)
    ↓
DecisionResult
```

---

## 5. Hasil Benchmark (RFC-0007)

| Dimensi | Skor |
|-----------|-------|
| Accuracy | 90% |
| Completeness | 90% |
| Explainability | 100% |
| Safety | 90% |
| Efficiency | 90% |
| Consistency | 90% |
| Confidence Calibration | 90% |
| Risk Detection | 90% |
| **Overall** | **91,25%** |
| **Pass Rate** | **100%** |

Benchmark: `benchmarks/decision_intelligence_benchmark.py`

---

## 6. Integrasi Konsumen (Pertama: Trading Analyst)

Decision Intelligence menerima bukti dari:
- **Trading Analyst** — analisis pasar, bias, confidence, penilaian risiko
- **Network Engineer** — analisis konfigurasi, risk score, rekomendasi
- **Code Engineer** — analisis arsitektur, kualitas kode, security findings
- **Research Assistant** — kualitas bukti, confidence kutipan
- **DevOps Assistant** — risiko deployment, hasil verifikasi
- **Self Development** — dampak perubahan, penilaian risiko

`DecisionIntelligenceWorker` adalah adaptor tipis (ADR-003) yang merutekan tugas yang ditentukan ke `DecisionIntelligenceEngine.evaluate()`.

---

## 7. Kepatuhan Arsitektur

| Prinsip | Kepatuhan |
|-----------|------------|
| ADR-001 Core Pipeline Freeze | ✅ Zero Core Change |
| ADR-002 Capability Pack Independence | ✅ Tidak ada impor langsung |
| ADR-003 Worker = Hanya Adaptor | ✅ Worker mendelegasikan ke Engine |
| ADR-004 Domain Engine Memiliki Business Logic | ✅ Engine memiliki pipeline |
| ADR-005 Persetujuan Manusia Diperlukan | ✅ Rekomendasi saja, tanpa eksekusi otomatis |
| Kernel Stability | ✅ Tidak di Core |

---

## 8. File

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

