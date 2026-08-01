# RFC-0009: Data Engineer Capability Pack

| Field | Value |
|-------|-------|
| **RFC ID** | RFC-0009 |
| **Status** | Draft |
| **Version** | 0.1.0 |
| **Author** | Enal AI OS Core Team |
| **Target Release** | v1.2.0 (Capability Excellence phase) |
| **Capability Pack** | Data Engineer |
| **Capability ID** | `data-engineer` |
| **Category** | Data |
| **Quality Target** | A- (≥85) |
| **Maturity Target** | Level 3 — Production Ready |
| **Reference RFC** | RFC-0009 |

---

## Motivation

ECP's existing Capability Packs rely on high-quality data as input or produce data as output. Trading Analyst needs clean market data; Research Assistant needs validated datasets; Decision Intelligence needs reliable evidence. However, there is no dedicated data engineering layer that manages the entire data lifecycle—from ingestion to quality assurance.

Currently:

1. **Data quality is assumed, not verified** — packs trust that input data is clean, but often it is not.
2. **ETL/ELT is ad hoc per pack** — each pack builds its own data ingestion without standardized pipelines.
3. **Schema drift goes undetected** — data structure changes silently break downstream analysis.
4. **Data cleaning is manual** — missing values, duplicates, and outliers are not systematically handled.
5. **Feature engineering is pack-specific** — no reusable feature store or time-series utilities.
6. **No dataset validation framework** — datasets are consumed without quality gates.

The Data Engineer Capability Pack becomes the data foundation layer, providing ETL/ELT, data cleaning, dataset validation, schema evolution, feature engineering, and time-series handling for all downstream Capability Packs.

---

## Problem Statement

Without a dedicated Data Engineer Capability Pack:

- **No data quality framework** — bad data silently degrades output quality across Trading, Research, and Decision Intelligence.
- **ETL pipelines are fragmented** — each pack builds its own ingestion logic, creating inconsistency and duplication.
- **Schema drift is undetected** — structural changes in data sources break downstream consumers without warning.
- **Data cleaning is inconsistent** — missing values, duplicates, and outliers are handled differently (or not at all) across packs.
- **No feature engineering layer** — derived features are computed ad hoc, leading to inconsistency across models.
- **Time series gaps are not handled** — irregular or missing timestamps break time-series analysis in Trading and Research.
- **Dataset validation is manual** — large datasets are consumed without automated quality gates.

---

## Goals

1. **ETL/ELT Pipeline** — Extract, transform, and load data from heterogeneous sources into standardized formats.
2. **Data Cleaning** — Detect and remediate missing values, duplicates, outliers, and schema inconsistencies.
3. **Dataset Validation** — Validate dataset integrity, schema compliance, and quality before consumption.
4. **Schema Evolution** — Detect and manage schema changes across data source versions.
5. **Feature Engineering** — Generate and maintain derived features for downstream analysis.
6. **Time Series Handling** — Process, align, and interpolate time-series data.
7. **Data Quality Assurance** — Measure and report data quality metrics (completeness, accuracy, freshness, consistency).

### Success Criteria

| Metric | Target | Grade |
|--------|--------|-------|
| Data Cleaning Accuracy | ≥95% (all anomalies detected and remediated) | A |
| Dataset Validation Rate | ≥98% (all datasets validated before consumption) | A |
| Schema Drift Detection | ≥90% (all schema changes detected) | A- |
| Quality Coverage | ≥95% (all quality dimensions checked) | A |
| Time Series Integrity | ≥95% (gaps filled, alignment correct) | A |
| Feature Consistency | ≥95% (same feature computed identically across runs) | A |
| Explainability | ≥90% (data quality issues explained with remediation) | A- |
| Consistency | ≥95% (same input produces same output across runs) | A |

---

## Non-Goals

1. **Live data streaming and real-time processing** — Data Engineer focuses on batch ETL/ELT; streaming is a future enhancement.
2. **Data storage infrastructure provisioning** — Data Engineer produces pipelines and quality reports; it does not provision databases or data lakes.
3. **Replacing dedicated data engineering tools** — dbt, Airflow, Spark remain valid; Data Engineer provides orchestration and quality assurance layer.
4. **Business intelligence / reporting** — Data Engineer does not produce dashboards or BI reports.
5. **Core modification** — All implementation resides within the Data Engineer Capability Pack.

---

## Capability Scope

### Core Capabilities

| Capability | Description | Inputs | Outputs |
|-----------|--------------|--------|---------|
| ETL Pipeline | Extract, transform, load from heterogeneous sources | Source data (CSV, JSON, API, DB, files) | Standardized dataset |
| ELT Pipeline | Extract, load, then transform within target | Raw data, schema definition, transform rules | Loaded + transformed dataset |
| Data Cleaning | Detect and remediate anomalies | Dirty data, quality rules | Cleaned data + quality report |
| Dataset Validation | Validate schema, integrity, quality | Dataset, schema, quality rules | Validation report with pass/fail |
| Schema Evolution | Detect and manage schema changes | Schema versions, diff | Schema drift report + migration plan |
| Feature Engineering | Generate derived features | Raw data, feature specs | Feature store entries |
| Time Series Handling | Align, interpolate, resample | Time-series data, frequency spec | Cleaned time-series dataset |
| Data Quality Assurance | Measure completeness, accuracy, freshness | Dataset, quality dimensions | Quality metrics report |

### Out of Scope

- Live streaming data processing (Apache Kafka, Flink)
- Data lake or warehouse provisioning
- Business intelligence dashboarding
- Machine learning model training (beyond feature engineering)
- Data governance policy definition
- Master data management

---

## Public Contracts

### Input Contract: Data Engineering Request

```json
{
  "job_id": "uuid",
  "job_type": "etl | elt | clean | validate | schema_evolve | feature_engineer | time_series",
  "source": {
    "type": "csv | json | api | database | file",
    "location": "string — file path, URL, or connection string",
    "schema": "object — expected schema definition"
  },
  "operations": [
    {
      "operation": "drop_duplicates | fill_missing | remove_outliers | normalize | encode | aggregate | interpolate",
      "parameters": {}
    }
  ],
  "quality_rules": [
    {
      "rule": "completeness | uniqueness | validity | freshness | consistency",
      "thresholds": {"min": 0.0, "max": 0.0}
    }
  ],
  "target_schema": "object — expected output schema",
  "time_series_config": {
    "frequency": "string — e.g., '1h', '1d'",
    "interpolation_method": "linear | forward_fill | nearest"
  },
  "feature_definitions": [
    {
      "name": "string",
      "expression": "string — transformation expression",
      "dependencies": ["string — input column names"]
    }
  ]
}
```

### Output Contract: Data Engineering Report

```json
{
  "job_id": "uuid",
  "job_type": "string",
  "status": "success | partial | failed",
  "dataset": {
    "row_count": 0,
    "column_count": 0,
    "schema": "object",
    "quality_score": 0.0
  },
  "quality_report": {
    "completeness": 0.0,
    "uniqueness": 0.0,
    "validity": 0.0,
    "freshness": 0.0,
    "consistency": 0.0,
    "overall_score": 0.0,
    "issues": [
      {
        "type": "missing_values | duplicate_rows | schema_drift | outlier | invalid_format",
        "column": "string",
        "severity": "critical | high | medium | low",
        "count": 0,
        "remediation": "string",
        "confidence": 0.0
      }
    ]
  },
  "schema_drift": {
    "detected": true,
    "changes": [
      {
        "column": "string",
        "change_type": "added | removed | type_changed | renamed",
        "old_type": "string",
        "new_type": "string"
      }
    ],
    "migration_required": true
  },
  "features": [
    {
      "name": "string",
      "type": "categorical | numerical | datetime",
      "description": "string",
      "created_at": "ISO 8601"
    }
  ],
  "time_series": {
    "frequency": "string",
    "missing_count": 0,
    "interpolated_count": 0,
    "alignment_complete": true
  },
  "lineage": {
    "source": "string",
    "transforms": ["string"],
    "target": "string"
  },
  "execution_time_ms": 0,
  "explanation": "string — summary of what was done and why"
}
```

### Data Quality Record (Experience Memory)

```json
{
  "record_id": "uuid",
  "job_id": "uuid",
  "timestamp": "ISO 8601",
  "dataset_id": "string",
  "quality_score": 0.0,
  "issues_found": 0,
  "issues_resolved": 0,
  "schema_drift_detected": false,
  "features_created": 0,
  "time_series_gaps_filled": 0,
  "outcome": "success | partial | failed | revised"
}
```

---

## Integration Points (Capability Graph)

```
Consumer Capability Pack (Trading, Research, Decision Intelligence)
    │
    │  submits data for processing via task/intent
    ▼
Execution Runtime
    │
    │  routes to Data Engineer Domain Engine
    ▼
Data Engineer Engine
    │
    │  ┌──────────────────────────────────────────┐
    │  │ 1. ETL/ELT Pipeline                      │
    │  │ 2. Data Cleaning                         │
    │  │ 3. Dataset Validation                    │
    │  │ 4. Schema Evolution                      │
    │  │ 5. Feature Engineering                   │
    │  │ 6. Time Series Handling                  │
    │  │ 7. Data Quality Assurance → Experience   │
    │  │    Memory                                │
    │  └──────────────────────────────────────────┘
    │
    │  returns Data Engineering Report
    ▼
Consumer Capability Pack
    │
    │  receives clean dataset + quality report
    ▼
User / Human Approval Loop
```

### Task Template

| Task | Subtasks |
|------|----------|
| Process Dataset | Source analysis → ETL/ELT → Data cleaning → Schema validation → Feature engineering → Time series handling → Quality report → Lineage → Persistence |

---

## Consumer Capability Packs

| Consumer Capability Pack | Use Case |
|--------------------------|----------|
| **Trading Analyst** | Clean market data, align time-series, generate technical features |
| **Research Assistant** | Validate datasets, detect schema drift, clean source data |
| **Decision Intelligence** | Validate evidence datasets, clean input data, track data lineage |
| **System Architect** | Analyze data architecture, schema evolution impact on design |

---

## Dependencies

### Internal Dependencies (Shared Contracts)

1. **Execution Runtime** — Task routing and orchestration (per ADR-002)
2. **Experience Memory** — Data quality records persistence (per ADR-011)
3. **Shared Contracts** — Task/Intent definition and result schema (per ADR-006)

### External Libraries

1. **pandas** — DataFrame operations, ETL transformations
2. **polars** — High-performance DataFrame (optional, for large datasets)
3. **numpy** — Numerical computations
4. **pyarrow** — Schema definition and Parquet I/O

### No Core Changes Required

All implementation resides within the Data Engineer Capability Pack:

```
apps/
└── data_engineer/
    ├── engine.py            # Domain Engine (per ADR-004)
    ├── worker.py            # Thin adapter (per ADR-003)
    ├── schemas.py           # Public contracts
    ├── etl_pipeline.py      # ETL/ELT pipeline
    ├── cleaner.py           # Data cleaning
    ├── validator.py         # Dataset validation
    ├── schema_evolver.py    # Schema evolution
    ├── feature_store.py     # Feature engineering
    ├── time_series.py       # Time series handling
    └── quality_assurance.py # Data quality assurance
```

**ADR Impact:** None. No Core, Runtime, Kernel, or shared contract modification required.

---

## Benchmark Specification

### Benchmark Framework

| Dimension | Definition | Measurement | Target |
|-----------|------------|-------------|--------|
| **Data Cleaning Accuracy** | % of anomalies correctly detected and remediated | % of ground truth anomalies found and fixed | ≥95% |
| **Dataset Validation Rate** | % of datasets passing validation before consumption | % of datasets with validation | ≥98% |
| **Schema Drift Detection** | % of schema changes correctly detected | % of schema changes identified | ≥90% |
| **Quality Coverage** | % of quality dimensions checked | Completeness × Uniqueness × Validity × Freshness × Consistency | ≥95% |
| **Time Series Integrity** | % of time series correctly aligned and gaps filled | % of time series with correct frequency and no gaps | ≥95% |
| **Feature Consistency** | % of features computed identically across runs | Variance across 10 runs < 5% | ≥95% |
| **Explainability** | Clarity of quality issues and remediation | Human evaluation score | ≥90% |
| **Efficiency** | Response time and resource usage | Latency P95 < 3000ms for 10K rows | within budget |

### Benchmark Dataset

- **100 dataset scenarios** covering:
  - Trading: market data (OHLCV, order books, volume)
  - Research: academic datasets (CSV, JSON, XML)
  - DevOps: log data, metrics, configuration data
  - Self-Development: code metrics, project data

### Benchmark Dimensions Detail

| Scenario Type | Description | Ground Truth |
|---------------|-------------|-------------|
| Missing Values | Rows/columns with null, NaN, empty strings | Manual annotation |
| Duplicate Data | Fully or partially duplicated rows | Ground truth dataset |
| Time Series Gap | Missing timestamps in regular intervals | Known gap insertions |
| Schema Drift | Column type changes, added/removed columns | Schema version diffs |
| Corrupted Dataset | Malformed rows, invalid formats, encoding issues | Ground truth corruption |

---

## Golden Test Specification

| # | Scenario | Expected Outcome | Acceptance Criteria |
|---|----------|-----------------|---------------------|
| 1 | Missing values in CSV dataset | Values detected and imputed | ≥95% detection, ≥90% imputation accuracy |
| 2 | Fully duplicated rows | Duplicates removed | ≥95% detection, 0 false removals |
| 3 | Time series with gaps | Gaps filled at correct frequency | ≥95% gap detection, correct interpolation |
| 4 | Schema drift (column type change) | Drift detected and migration planned | ≥90% detection, correct migration |
| 5 | Corrupted rows (malformed JSON) | Corrupted rows flagged/removed | ≥95% detection, ≥90% recovery |
| 6 | Categorical encoding | Categories encoded correctly | ≥95% correctness |
| 7 | Feature engineering (rolling mean) | Derived feature matches expected values | ≥95% accuracy |
| 8 | Outlier detection | Outliers identified and handled | ≥90% detection, <5% false positive |
| 9 | Uniqueness constraint violation | Violation detected | ≥98% detection |
| 10 | Data freshness check | Stale data flagged | ≥95% detection |

### Golden Test Acceptance Criteria

- All 10 golden test scenarios pass at ≥90% of acceptance criteria (100% pass)
- Overall Data Engineer golden test pass rate ≥95%
- Dataset validation rate ≥98%
- No data corruption introduced during cleaning

---

## Real Case Requirements

### Real Case Directory

`real_cases/data_engineer/` must contain:

| Requirement | Minimum Count |
|-------------|---------------|
| Real dataset processing cases from actual usage | 20 |
| Cases with missing values remediation | 5 |
| Cases with time series gap handling | 5 |
| Cases with schema drift detection | 5 |
| Cases with feature engineering | 10 |
| Cases with expert review/validation | 15 |

### Real Case Structure

```
real_cases/data_engineer/<case_id>/
├── input/
│   ├── source_data/          # Original dataset
│   ├── quality_rules.json     # Quality rules applied
│   └── schema.json           # Expected schema
├── output/
│   ├── report.json           # Full Data Engineering Report
│   ├── cleaned_dataset.csv   # Cleaned output
│   └── quality_explanation.md
└── evaluation.md             # Ground truth, expert review, lessons learned
```

### Real Case Targets

| Metric | Target |
|--------|--------|
| Real cases logged | ≥20 (Level 3) → ≥100 (Level 4) |
| Real case quality score (expert review) | ≥90% |
| Data quality improvement (before → after) | ≥85% average improvement |

---

## Definition of Done

```text
Definition of Done — Data Engineer Capability Pack

Functional
- [ ] ETL Pipeline extracts from CSV, JSON, API, and database sources
- [ ] ELT Pipeline supports transform-after-load patterns
- [ ] Data Cleaning handles missing values, duplicates, outliers, and invalid formats
- [ ] Dataset Validation checks completeness, uniqueness, validity, freshness, consistency
- [ ] Schema Evolution detects column type changes, additions, removals
- [ ] Feature Engineering generates derived features from raw data
- [ ] Time Series Handling aligns, interpolates, and resamples time-series data
- [ ] Data Quality Assurance produces measurable quality metrics

Benchmark
- [ ] Data Cleaning Accuracy ≥ 95% (grade A)
- [ ] Dataset Validation Rate ≥ 98%
- [ ] Schema Drift Detection ≥ 90%
- [ ] Quality Coverage ≥ 95%
- [ ] Time Series Integrity ≥ 95%
- [ ] Feature Consistency ≥ 95%
- [ ] Explainability ≥ 90%
- [ ] Efficiency: P95 < 3000ms for 10K rows

Golden Tests
- [ ] All 10 pack golden test scenarios pass at ≥90% of acceptance criteria (100% pass)

Real Cases
- [ ] ≥ 20 real cases logged in real_cases/data_engineer/
- [ ] Evaluation notes recorded for each case
- [ ] ≥ 5 cases with missing values remediation
- [ ] ≥ 5 cases with time series gap handling
- [ ] ≥ 5 cases with schema drift detection
- [ ] ≥ 10 cases with feature engineering

Documentation
- [ ] Capability Guide updated (CAPABILITY_GUIDE.md — Data Engineer section)
- [ ] API reference / contract updated (this RFC + schemas.py)
- [ ] Real case evaluation summary published

SDK
- [ ] Pack accessible via SDK without Core changes
- [ ] Data Engineer callable via Execution Runtime task routing

Performance
- [ ] Latency P95 < 3000ms for 10K row datasets
- [ ] Latency P95 < 10000ms for 100K row datasets

Security
- [ ] No known P0/P1 security issues
- [ ] Data processing does not persist sensitive data beyond workspace scope

Regression
- [ ] No regression in existing Capability Pack benchmark dimensions
- [ ] Benchmark reproducible (documented command + persisted result)

Release Notes
- [ ] Capability Changelog updated
```

---

## Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Data cleaning removes valid data | High — information loss | Medium | Conservative cleaning with explainability; user review for destructive ops |
| Schema drift detection misses silent changes | High — downstream breakage | Medium | Multi-layer validation (schema + content-level checks) |
| Time series imputation introduces bias | Medium — skewed analysis | Medium | Multiple interpolation methods; user-selectable |
| Performance bottleneck on large datasets | Medium — blocks workflows | High | Lazy evaluation; chunked processing; parallelism |
| Feature engineering creates inconsistency | Medium — model drift | Medium | Feature store with versioning; lineage tracking |
| Data quality metrics are noisy | Low — false alerts | High | Statistical smoothing; threshold tuning per domain |
| External dependency (pandas, polars) version conflicts | Low — compatibility issues | Medium | Pinned versions; compatibility tests |

---

## ADR Impact

**Does this require Core changes?** No.

Data Engineer is a **new Capability Pack** that follows the established patterns:

- **ADR-001 (Core Pipeline Freeze):** No Core changes. All logic in `apps/data_engineer/`.
- **ADR-002 (Capability Pack Independence):** Data Engineer communicates with other packs via Execution Runtime tasks and shared contracts only. No direct imports.
- **ADR-003 (Worker = Adapter Only):** A thin Worker routes tasks to the Domain Engine.
- **ADR-004 (Domain Engine Owns Business Logic):** All data engineering logic resides in `apps/data_engineer/engine.py`.
- **ADR-005 (Human Approval Required):** Data transformations are recommendations; execution requires explicit user approval.
- **ADR-006 (Capability Contract v1 Frozen):** Uses the existing Capability Contract for node and subtask template registration. No contract changes.
- **ADR-007 (Conversation Boundary):** Data Engineer is invoked through Execution Runtime, not directly by Conversation Manager.
- **ADR-008 (Core Change Requires Cross-Capability Proof):** Not applicable — no Core changes.

**ADR Required:** None. This is a new Capability Pack, not a Core modification.

---

## Rollout Plan

### Phase 1: Prototype (RFC → Experimental)

**Duration:** 5 weeks

- [ ] Create `apps/data_engineer/` package structure
- [ ] Implement basic ETL pipeline (CSV/JSON ingestion)
- [ ] Implement data cleaning (missing values, duplicates)
- [ ] Implement dataset validation (completeness, uniqueness)
- [ ] Define public contracts (Data Engineering Request, Report)
- [ ] Implement thin Worker adapter
- [ ] Create 10 golden test scenarios
- [ ] Integration: Trading Analyst → Data Engineer (market data cleaning)
- [ ] Integration: Research Assistant → Data Engineer (dataset validation)
- **Gate:** 10 golden tests pass at ≥80%

### Phase 2: Full Capabilities (Experimental → Stable)

**Duration:** 7 weeks

- [ ] Implement full ETL/ELT with API and database sources
- [ ] Implement schema evolution detection
- [ ] Implement feature engineering
- [ ] Implement time series handling with multiple interpolation methods
- [ ] Implement full data quality assurance (5 dimensions)
- [ ] Expand golden tests to 10 full scenarios
- [ ] Log ≥20 real cases from Trading and Research usage
- [ ] **Benchmark:** 100 scenarios, ≥95% cleaning accuracy, ≥98% validation
- [ ] **Integration:** Decision Intelligence starts using Data Engineer for evidence validation
- **Gate:** All 10 golden tests pass at ≥90%; benchmark ≥95% cleaning, ≥98% validation

### Phase 3: Ecosystem (Stable → Certified)

**Duration:** 6 weeks

- [ ] All 4 consumer packs integrated
- [ ] Feature store with versioning and lineage
- [ ] Time series handling validated on real market data
- [ ] Independent audit of data quality and schema drift detection
- [ ] Public benchmark dashboard available
- [ ] **Benchmark:** ≥95% across all dimensions sustained
- [ ] **Real Cases:** ≥100 cases with ≥80% expert validation
- **Gate:** Independent audit passed; benchmark ≥95% sustained

---

## Future Enhancements

### Fase 2 (Post-v1.0.0 Release)

1. **Streaming ETL** — Real-time data ingestion and transformation (Kafka, Kinesis)
2. **Data Catalog** — Metadata management, data discovery, and lineage visualization
3. **Anomaly Detection** — Statistical and ML-based anomaly detection in data streams
4. **Data Observability** — Automated monitoring of data quality metrics in production

### Fase 3 (Enterprise)

1. **Data Governance** — Data ownership, access control, and retention policy enforcement
2. **Master Data Management** — Golden record creation and conflict resolution
3. **Cross-Workspace Data Sharing** — Secure data sharing between workspaces with lineage
4. **Data Cost Optimization** — Storage tiering and query optimization recommendations

### Long-term

1. **Automated Data Pipeline Generation** — End-to-end pipeline generation from requirements
2. **Causal Data Inference** — Beyond correlation to causal relationships in data
3. **Data Mesh Architecture** — Domain-oriented data ownership and distributed architecture
4. **AI-Powered Data Quality** — Predictive data quality management with auto-remediation
