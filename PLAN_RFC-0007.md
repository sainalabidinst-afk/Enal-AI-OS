# Plan: Implementasi RFC-0007 (Decision Intelligence)

## Informasi yang Dikumpulkan

RFC-0007 mendefinisikan **Decision Intelligence** — Capability Pack yang menjadi shared reasoning layer untuk semua Capability Pack lainnya. Ini adalah "otak" kedua setelah Core, tetapi tetap di level Capability Pack (tidak melanggar Core Freeze).

### Core Capabilities (8 sub-modul)
1. **Evidence Collection** — Kumpulkan evidence dari berbagai sumber
2. **Alternative Generation** — Generate alternatif keputusan
3. **Risk Analysis** — Analisis risiko (probability × impact)
4. **Trade-off Analysis** — Multi-objective optimization
5. **Decision Scoring** — Score dan ranking alternatif
6. **Confidence Estimation** — Quantifikasi uncertainty
7. **Explainable Decision** — Rantai explainability
8. **Decision History** — Record ke Experience Memory

### Target Quality: A (≥90)
- Decision Accuracy ≥90%
- Explainability ≥95%
- Consistency ≥90%
- Confidence Calibration ≥85%

### Prinsip Arsitektur
- **Zero Core changes** — semua di `apps/decision_intelligence/`
- **ADR-002 compliance** — komunikasi via Execution Runtime, bukan direct import
- **ADR-004 compliance** — Domain Engine owns business logic
- **ADR-005 compliance** — rekomendasi, bukan eksekusi otomatis

## Plan Implementasi

### Step 1: Buat package structure + schemas
- `apps/decision_intelligence/__init__.py`
- `apps/decision_intelligence/schemas.py` — DecisionRequest, DecisionResult, EvidenceItem, Alternative, RiskProfile, TradeOff, ConfidenceScore, DecisionRecord (Pydantic models)

### Step 2: Implementasi Evidence Collection
- `apps/decision_intelligence/evidence_collector.py`
- Support multiple source types: analysis, recommendation, data, benchmark, historical
- Quality scoring per evidence item
- Weighted evidence synthesis

### Step 3: Implementasi Alternative Generation
- `apps/decision_intelligence/alternative_generator.py`
- Generate ≥2 alternatif viable dari decision context
- Feasibility filtering berdasarkan constraints

### Step 4: Implementasi Risk Analysis
- `apps/decision_intelligence/risk_analyzer.py`
- Probability × impact scoring
- Multiple risk factor categories
- Risk tolerance parameter

### Step 5: Implementasi Trade-off Analysis
- `apps/decision_intelligence/tradeoff_analyzer.py`
- Weighted multi-objective scoring
- Pareto frontier identification
- Mendukung ≥3 simultaneous objectives

### Step 6: Implementasi Decision Scoring + Confidence
- `apps/decision_intelligence/scoring_engine.py` — Composite scoring, ranking
- `apps/decision_intelligence/confidence_estimator.py` — Confidence 0-100%, uncertainty bounds, calibration

### Step 7: Implementasi Explanation + History
- `apps/decision_intelligence/explanation_generator.py` — Full chain: evidence → reasoning → alternatives → risk → decision → rationale
- `apps/decision_intelligence/decision_history.py` — Record ke Experience Memory format

### Step 8: Implementasi Engine + Worker
- `apps/decision_intelligence/engine.py` — DecisionIntelligenceEngine orchestrator
- `apps/decision_intelligence/worker.py` — Thin adapter (per ADR-003)
- Integrasi semua sub-modul dalam pipeline

### Step 9: Benchmark
- `benchmarks/decision_intelligence_benchmark.py` — 100 decision scenarios
- Metrics: accuracy, completeness, explainability, safety, efficiency, consistency, confidence calibration, risk detection

### Step 10: Update dokumentasi
- `docs/CAPABILITY_STRATEGY.md` — tambah Decision Intelligence
- `docs/capabilities/` — profile Decision Intelligence
- `TODO.md` — update status

## Dependent Files
- `apps/decision_intelligence/` — seluruh package baru
- `benchmarks/decision_intelligence_benchmark.py` — benchmark baru
- `docs/CAPABILITY_STRATEGY.md` — update profil pack
- `docs/capabilities/` — file baru
- `TODO.md` — track progress

## Follow-up Steps
- Smoke test pipeline (import verification + sample decision scenario)
- Benchmark run (100 scenarios)
- Validasi integration points dengan Trading Analyst (first consumer)
- Update TODO.md

## Total Estimasi: 10 steps
