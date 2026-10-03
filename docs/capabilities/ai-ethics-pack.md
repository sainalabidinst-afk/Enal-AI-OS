# AI Ethics & Governance Capability Pack

**Version:** 2.5.0
**Target Grade:** A (≥90%)
**Status:** Implemented
**Phase:** 7
**RFC:** [RFC-0035](docs/rfcs/RFC-0035-ai-ethics-pack.md)
**ADR:** [ADR-015](docs/adr/ADR-015-ai-ethics-governance.md)

## Ringkasan

AI Ethics & Governance Capability Pack menyediakan fairness auditing, deteksi bias, explainability, dan compliance checking terhadap regulasi (GDPR, EU-AI-Act, NIST-AI-RMF, ISO/IEC-230) untuk sistem AI. Pack ini menggunakan rumus eksplisit dan threshold yang dideklarasikan untuk setiap metrik, tanpa nilai default yang tersembunyi untuk input yang hilang.

## Kemampuan Inti

1. **Fairness Auditing** — Hitung demographic parity, equalized odds, dan equal opportunity across protected attributes (gender, age, race, etc.). Laporankan setiap metrik dengan nilai, threshold, dan status pass/fail.
2. **Bias Detection** — Deteksi representational bias, selection bias, dan measurement bias pada dataset berdasarkan atribut terproteksi. Berikan severity score dan rekomendasi remediasi.
3. **Explainability Assessment** — Evaluasi kemampuan model untuk dijelaskan melalui SHAP values, LIME, atau feature importance. Berikan explainability score berdasarkan model_type.
4. **Compliance Check** — Pemetaan bukti ke persyaratan regulasi (GDPR Article 22, EU-AI-Act risk tiers, NIST-AI-RMF, ISO/IEC-230). Laporkan status tiap persyaratan dengan coverage percentage.

## Input Schema

- `operation`: `fairness_audit` | `bias_detection` | `explainability` | `compliance_check`
- `model_name`, `model_type` — identifikasi model
- `dataset_description` — deskripsi dataset untuk bias detection
- `protected_attributes[]` — atribut yang harus di-audit (gender, age, race, dll.)
- `prediction_field`, `label_field` — field untuk fairness audit
- `sample_size`, `threshold` — parameter audit
- `jurisdiction`, `standard` — regulasi yang akan di-check

## Batasan Keamanan

- **Tidak mengganti penilaian etika manusia** — Semua output assistif, membutuhkan review insinyur etika
- **Tidak mengklaim sertifikasi otomatis** — quality_score hanya metrik kuantitatif, bukan kepatuhan hukum
- **Mensyyaratkan protected_attributes** — Fairness audit menolak jika atribut tidak disediakan
- **Melaporkan input yang hilang** — Jika model_name atau prediction_field kosong, laporkan error eksplisit

## Integration

- **Konsumsi dari**: Data Engineer (dataset metadata), Knowledge Engineer (etika ontologi), Legal Advisor (regulasi standar)
- **Digunakan oleh**: System Architect (design ethics), DevOps Assistant (CI/CD ethics gates), Compliance Officer (audit evidence)

## Benchmark

- 10 scenarios across 6 dimensions:
  1. **Fairness Auditing** (0.92) — demographic parity, equalized odds across protected attributes
  2. **Bias Detection** (0.90) — representational, selection, measurement bias identification
  3. **Explainability** (0.89) — SHAP/LIME/feature importance explainability scoring
  4. **Compliance Check** (0.91) — GDPR, EU-AI-Act, NIST-AI-RMF, ISO/IEC-230 mapping
  5. **Safety Boundary** (0.94) — missing input detection, no fabricated values, fail-closed
  6. **Input Validation** (0.91) — operation-specific field requirements, edge case handling
- Overall score: A (91.2%)
- Dashboard: `benchmarks/dashboards/ai_ethics_pack_dashboard.html`

## Real Cases

10 real cases in `real_cases/ai-ethics-governance/` covering:
- Gender bias audit on hiring model (demographic parity across 4 attributes)
- Racial bias detection in loan approval dataset (7 protected attributes)
- Explainability assessment for credit scoring model (SHAP values)
- GDPR Article 22 compliance check for automated decision system
- EU-AI-Act risk tier classification for high-risk AI system
- NIST-AI-RMF fairness assessment for recommendation engine
- ISO/IEC-230 alignment for facial recognition system
- Multi-regulation compliance mapping (GDPR + EU-AI-Act overlap)
- Bias mitigation before fairness re-audit (pipeline test)
- Missing input safety boundary (fabricated value detection)

## Changelog

- **2026-10-02**: Initial implementation (RFC-0035, ADR-015)
  - `apps/ai_ethics_pack/` pack with engine, schemas, worker, `ai_ethics_engine.py` (AIEthicsGovernanceEngine)
  - 4 operations: fairness_audit, bias_detection, explainability, compliance_check
  - Regulations: GDPR, EU-AI-Act, NIST-AI-RMF, ISO/IEC-230
  - 15 fairness metrics (demographic parity, equalized odds, equal opportunity, disparate impact)
  - Bias severity scoring with remediation recommendations
  - 6 explainability metrics mapped to model types
  - 10 benchmark scenarios across 6 dimensions, overall A (91.2%)
  - 10 real cases in `real_cases/ai-ethics-governance/`
  - Benchmark dashboard: `benchmarks/dashboards/ai_ethics_pack_dashboard.html`
