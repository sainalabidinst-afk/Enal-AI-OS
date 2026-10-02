# ADR-017: Data Scientist Engine Architecture

|Campo|Valor|
|-------|-------|
|**ID ADR**|ADR-017|
|**Status**|Accepted|
|**Date**|2026-10-02|
|**Decision Maker**|Platform Architecture Board|
|**Related RFC**|RFC-0037|

## Context

Data Scientist capability pack needs to provide advanced ML pipelines, feature engineering, and model evaluation for ECP users building predictive analytics solutions.

## Decision

1. **Feature Engineering**: Automated feature construction, encoding, and scaling using scikit-learn (lazy import); fallback to rule-based feature extraction.
2. **Model Evaluation**: Cross-validation, ROC/AUC, precision/recall metrics using scikit-learn; fallback to basic statistical measures.
3. **AutoML**: Grid search / random search hyperparameter tuning (lazy import of scikit-optimize); fallback to manual parameter grid.
4. **Pipeline Orchestration**: MLflow-style pipeline tracking using local JSON; fallback to basic file logging.
5. **Integration with Cognitive Pipeline**: Model outputs feed into Business Intelligence for reporting.

## Alternatives Considered

- **Cloud AutoML (AWS SageMaker, GCP Vertex)**: Rejected — external API dependency, vendor lock-in.
- **Custom model training**: Rejected — requires large compute resources, not suitable for edge deployment.

## Consequences

- Adds `ml_engine.py` to `apps/data_scientist/`
- Lightweight by default; heavy ML libraries are optional
- No external API dependencies

## Cross-Capability Proof

- Trading Analyst consumes model evaluation for trading signal models
- Research Assistant consumes statistical analysis for research papers
- Business Intelligence consumes ML model outputs for dashboards
