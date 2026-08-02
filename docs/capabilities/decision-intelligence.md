<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/capabilities/decision-intelligence.md`
- Judul: Decision Intelligence
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Decision Intelligence Capability Specification

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Capability Pack specification for decision-intelligence
<!-- DOCUMENT_METADATA_END -->

## Version: 1.0.0
## Status: Production Ready (RFC-0007)
## Quality Target: A (â‰¥90)

---

## 1. Purpose

Decision Intelligence adalah **shared reasoning layer** untuk ECP â€” Capability Pack
yang menyediakan pengambilan keputusan berbasis bukti (evidence-based), explainable,
dan auditable untuk semua Capability Pack lain.
> Terjemahan Indonesia: Decision Intelligence adalah shared reasoning layer untuk ECP â€” kapabilitas Pack yang menyediakan pengambilan keputusan berbasis bukti (evidence-based), explainable, dan auditable untuk semua kapabilitas Pack lain.

Acting as a cross-cutting cognitive service **tanpa memodifikasi Core**.
> Terjemahan Indonesia: Acting as sebuah cross-cutting kognitif layanan tanpa memodifikasi Core.

---

## 2. Scope

### In Scope
- Evidence collection dari multiple sources (analysis, recommendation, data, benchmark, historical)
- Alternative generation dengan constraint filtering
- Risk analysis (probability Ã— impact)
- Trade-off analysis (multi-objective weighted scoring, Pareto frontier)
- Decision scoring dan ranking
- Confidence estimation (0â€“100%, uncertainty bounds, calibration)
- Explainable decision (full chain: evidence â†’ reasoning â†’ alternatives â†’ risk â†’ decision â†’ rationale)
- Decision history (record ke Experience Memory, audit trail)

### Out of Scope
- Eksekusi keputusan otomatis (rekomendasi saja â€” ADR-005 compliance)
- Modifikasi Core contracts
- Direct import dari Capability Pack lain (ADR-002 compliance)

---

## 3. Contract

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
    â†“
EvidenceCollection (collect, validate, weight)
    â†“
AlternativeGeneration (enumerate, filter constraints)
    â†“
RiskAnalysis (probability Ã— impact)
    â†“
TradeoffAnalysis (multi-objective, weighted, Pareto)
    â†“
DecisionScoring (composite score, rank)
    â†“
ConfidenceEstimation (0-100%, calibration)
    â†“
ExplanationGeneration (full explainability chain)
    â†“
DecisionHistory (Experience Memory, audit trail)
    â†“
DecisionResult
```

---

## 5. Benchmark Results (RFC-0007)

| Dimension | Score |
|-----------|-------|
| Accuracy | 90% |
| Completeness | 90% |
| Explainability | 100% |
| Safety | 90% |
| Efficiency | 90% |
| Consistency | 90% |
| Confidence Calibration | 90% |
| Risk Detection | 90% |
| **Overall** | **91.25%** |
| **Pass Rate** | **100%** |

Benchmark: `benchmarks/decision_intelligence_benchmark.py`
> Terjemahan Indonesia: Tolok ukur: benchmarks/decision_intelligence_benchmark.py

---

## 6. Consumer Integration (First: Trading Analyst)

Decision Intelligence menerima evidence dari:
> Terjemahan Indonesia: Decision Intelligence menerima bukti dari:
- **Trading Analyst** â€” market analysis, bias, confidence, risk assessment
- **Network Engineer** â€” config analysis, risk score, recommendations
- **Code Engineer** â€” architecture analysis, code quality, security findings
- **Research Assistant** â€” evidence quality, citation confidence
- **DevOps Assistant** â€” deployment risk, verification results
- **Self Development** â€” change impact, risk assessment

The `DecisionIntelligenceWorker` is a thin adapter (ADR-003) that routes
task dicts to `DecisionIntelligenceEngine.evaluate()`.
> Terjemahan Indonesia: DecisionIntelligenceWorker adalah sebuah thin adapter (ADR-003) itu routes task dicts untuk DecisionIntelligenceEngine.evaluate().

---

## 7. Architecture Compliance

| Principle | Compliance |
|-----------|------------|
| ADR-001 Core Pipeline Freeze | âœ… Zero Core changes |
| ADR-002 Capability Pack Independence | âœ… No direct imports |
| ADR-003 Worker = Adapter Only | âœ… Worker delegates to Engine |
| ADR-004 Domain Engine Owns Business Logic | âœ… Engine owns pipeline |
| ADR-005 Human Approval Required | âœ… Recommend only, no auto-execute |
| Kernel Stability | âœ… Not in Core |

---

## 8. Files

| File | Purpose |
|------|---------|
| `apps/decision_intelligence/schemas.py` | Pydantic models |
| `apps/decision_intelligence/evidence_collector.py` | Evidence collection |
| `apps/decision_intelligence/alternative_generator.py` | Alternative generation |
| `apps/decision_intelligence/risk_analyzer.py` | Risk analysis |
| `apps/decision_intelligence/tradeoff_analyzer.py` | Trade-off analysis |
| `apps/decision_intelligence/scoring_engine.py` | Decision scoring |
| `apps/decision_intelligence/confidence_estimator.py` | Confidence estimation |
| `apps/decision_intelligence/explanation_generator.py` | Explainability |
| `apps/decision_intelligence/decision_history.py` | Decision history |
| `apps/decision_intelligence/engine.py` | Domain engine orchestrator |
| `apps/decision_intelligence/worker.py` | Thin worker adapter |
| `benchmarks/decision_intelligence_benchmark.py` | Benchmark (8 dimensions) |
