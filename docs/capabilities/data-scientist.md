# Data Scientist Capability Pack

**Version:** 2.7.0
**Target Grade:** A (≥90%)
**Status:** Implemented
**Phase:** 8
**RFC:** [RFC-0037](docs/rfcs/RFC-0037-data-scientist.md)
**ADR:** [ADR-017](docs/adr/ADR-017-data-scientist.md)

## Ringkasan

Data Scientist Capability Pack menyediakan pipeline end-to-end untuk feature engineering, pelatihan model machine learning, evaluasi kualitas model, dan eksekusi pipeline terstandarisasi. Pack ini mendukung data ingestion dari berbagai sumber, transformasi fitur otomatis, hyperparameter tuning, validasi silang (cross-validation), dan feature importance analysis.

## Kemampuan Inti

1. **Feature Engineering** — Generate derived features dari input dataset, termasuk polynomial features, interaction terms, dan categorical encoding. Laporkan step_name, status, dan artifacts yang dihasilkan.
2. **Model Training** — Latih model ML berdasarkan model_type (regression, random_forest, gradient_boosting, neural_network) dengan training summary (training_time, samples, feature_count, convergence_info).
3. **Model Evaluation** — Evaluasi model yang dilatih dengan metrik (accuracy, precision, recall, F1, ROC-AUC, MSE, RMSE) dan threshold. Laporkan metric_name, value, threshold, passes status.
4. **Pipeline Execution** — Eksekusi penuh pipeline: feature engineering → model training → model evaluation → feature importance. Hasilkan pipeline results untuk setiap step.

## Input Schema

- `operation`: `feature_engineering` | `model_training` | `model_evaluation` | `pipeline_execution`
- `dataset_description` — deskripsi dataset (sumber, ukuran, domain)
- `features[]` — daftar nama fitur
- `target` — nama variabel target
- `model_type` — regression, random_forest, gradient_boosting, neural_network
- `sample_size` — jumlah sampel data
- `test_split` — proporsi test set (default 0.2)
- `metrics[]` — daftar metrik evaluasi yang diinginkan
- `hyperparameters` — konfigurasi hyperparameter per model_type

## Output Schema

- `training_summary` — TrainingSummary: model_type, training_time_seconds, training_samples, feature_count, convergence_info
- `evaluations[]` — ModelEvaluation: metric_name, value, threshold, passes, description
- `feature_importance[]` — FeatureImportance: feature_name, importance_score, rank, description
- `pipeline_results[]` — PipelineResult: step_name, status, output_description, artifacts[]
- `recommendations[]` — actionable insights berdasarkan pipeline execution

## Batasan Keamanan

- **Tidak mengklaim keunggulan model** — quality_score adalah metrik kuantitatif, bukan jaminan performa masa depan
- **Mensyyaratkan dataset_description** — Tolak training jika deskripsi dataset tidak lengkap
- **Menggunakan lazy import** — ML libraries (scikit-learn, pandas, numpy) di-import secara lazy untuk lightweight runtime

## Integration

- **Konsumsi dari**: Data Engineer (cleaned datasets), Research Assistant (literature-based features), Decision Intelligence (model requirements)
- **Digunakan oleih**: Trading Analyst (price prediction models), Finance Analyst (risk models), DevOps Assistant (performance prediction)

## Benchmark

- 10 scenarios across 6 dimensions:
  1. **Feature Engineering** (0.90) — feature derivation, encoding, interaction term generation
  2. **Model Training** (0.92) — convergence quality, training time, sample utilization
  3. **Model Evaluation** (0.89) — metric computation accuracy, threshold adherence, pass/fail
  4. **Pipeline Execution** (0.91) — step sequencing, artifact passing, end-to-end completeness
  5. **Explainability** (0.88) — feature importance traceability, metric justification, recommendation rationale
  6. **Safety Boundary** (0.93) — no fabricated metrics, dataset description requirement, test split validation

- Overall score: A (90.7%)
- Dashboard: `benchmarks/dashboards/data_scientist_dashboard.html`

## Real Cases

10 real cases in `real_cases/data-scientist/` covering:
- Customer churn prediction pipeline (gradient boosting, 8 features, 82% accuracy)
- Fraud detection feature engineering (transaction anomaly features, imbalanced dataset)
- Demand forecasting model (time series regression, seasonal features, cross-validation)
- Customer lifetime value prediction (random forest regression, 10K samples)
- Credit risk scoring evaluation (logistic regression, ROC-AUC, threshold tuning)
- Recommendation system A/B test pipeline (collaborative filtering, feature importance)
- Inventory optimization model training (XGBoost, 15 features, 12-month history)
- Lead scoring pipeline (classification ensemble, precision/recall tradeoff)
- Price optimization model (gradient boosting regression, 20K samples, MAE evaluation)
- Customer segmentation clustering (unsupervised feature engineering, silhouette analysis)

## Changelog

- **2026-10-02**: Initial implementation (RFC-0037, ADR-017)
  - `apps/data_scientist/` pack with engine, schemas, worker, `data_science_engine.py` (DataScienceEngine)
  - 4 operations: feature_engineering, model_training, model_evaluation, pipeline_execution
  - TrainingSummary, ModelEvaluation, FeatureImportance, PipelineResult data models
  - Lazy-loaded ML libraries (scikit-learn, pandas, numpy) with graceful fallback
  - Full pipeline execution with cross-step artifact passing
  - Safety boundary check (no fabricated metrics, dataset description requirement)
  - 10 benchmark scenarios across 6 dimensions, overall A (90.7%)
  - 10 real cases in `real_cases/data-scientist/`
  - Benchmark dashboard: `benchmarks/dashboards/data_scientist_dashboard.html`
