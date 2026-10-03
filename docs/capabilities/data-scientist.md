# Data Scientist Capability Pack

**Version:** 2.7.0
**Target Grade:** A (>=90%)
**Status:** Implemented
**Phase:** 7
**RFC:** [RFC-0037](docs/rfcs/RFC-0037-data-scientist.md)
**ADR:** [ADR-017](docs/adr/ADR-017-data-scientist.md)

## Ringkasan

Data Scientist Capability Pack menyediakan pipeline end-to-end untuk feature engineering, pelatihan model machine learning, dan evaluasi kualitas model. Pack ini mendukung data ingestion dari berbagai sumber, transformasi fitur otomatis, hyperparameter tuning, dan validasi silang (cross-validation) dengan metrik yang dapat dilacak.

## Kemampuan Inti

1. **Feature Engineering**
2. **Model Training**
3. **Model Evaluation**
4. **Pipeline Execution**

## Benchmark

- 10 scenarios across 6 dimensions
- Overall score: A (90.7%)
- Dashboard: `benchmarks/dashboards/data_scientist_dashboard.html`

## Real Cases

10 real cases in `real_cases/data-scientist/`

## Changelog

- **2026-10-02**: Initial implementation (RFC-0037, ADR-017)
