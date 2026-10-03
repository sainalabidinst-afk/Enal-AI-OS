# Business Intelligence Capability Pack

**Version:** 2.8.0
**Target Grade:** A (≥90%)
**Status:** Implemented
**Phase:** 7
**RFC:** [RFC-0038](docs/rfcs/RFC-0038-business-intelligence.md)
**ADR:** [ADR-018](docs/adr/ADR-018-business-intelligence.md)

## Ringkasan

Business Intelligence Capability Pack menyediakan KPI tracking, dashboard generation, scenario planning, dan metric analysis untuk pengambilan keputusan strategis. Pack ini mengintegrasikan sumber data terdistribusi, menghitung variance dari target KPI, dan menghasilkan dashboard konfigurabel dengan forecast berbasis skenario.

## Kemampuan Inti

1. **KPI Tracking** — Hitung variance percentage dari current vs. target values untuk sekumpulan metrik. Kategorikan status (on-track, at-risk, off-track) berdasarkan threshold yang dikonfigurasi.
2. **Dashboard Generation** — Hasilkan konfigurasi dashboard dengan widget, layout grid, refresh interval, dan data source binding. Mendukung multi-department dan multi-timeframe.
3. **Scenario Planning** — Jalankan skenario what-if dengan variable change percentage, projected outcome, confidence interval, dan asumsi yang diekstrak. Berguna untuk foresight modeling.
4. **Metric Analysis** — Analisis historis metrik, tren (up/down/stable), dan identifikasi anomali berdasarkan pola historis.

## Input Schema

- `operation`: `kpi_tracking` | `dashboard_generation` | `scenario_planning` | `metric_analysis`
- `metrics[]` — daftar nama metrik yang akan dilacak
- `target_values` — target value per metrik
- `current_values` — nilai aktual per metrik
- `historical_data[]` — data historis untuk analisis tren
- `departments[]` — departemen yang terlibat
- `timeframe` — monthly, quarterly, yearly
- `scenario_name`, `variables[]`, `change_pct` — parameter skenario

## Output Schema

- `kpis[]` — KpiMetric: metric_name, current_value, target_value, variance_pct, status, trend
- `dashboard_configs[]` — DashboardConfig: dashboard_name, widgets, layout, refresh_interval, data_sources
- `scenarios[]` — ScenarioAnalysis: scenario_name, variable_name, change_pct, projected_outcome, confidence
- `recommendations[]` — actionable insight berdasarkan analisis

## Batasan Keamanan

- **Tidak memberikan rekomendasi investasi** — Semua output bersifat informatif dan analitis
- **Mensyyaratkan currency/unit labels** — Tolak input yang ambigu tentang satuan
- **Melaporkan denominator yang hilang** — Jangan hitung variance jika current atau target tidak ada

## Integration

- **Konsumsi dari**: Data Engineer (dataset, ETL output), Decision Intelligence (strategic metrics)
- **Digunakan oleh**: Product Manager (roadmap tracking), Finance Analyst (financial KPIs), Compliance Officer (regulatory reporting)

## Benchmark

- 10 scenarios across 6 dimensions:
  1. **KPI Tracking** (0.92) — variance calculation, status classification, trend detection
  2. **Dashboard Generation** (0.91) — widget layout, data source binding, config validity
  3. **Scenario Planning** (0.90) — what-if projection, confidence interval, assumption extraction
  4. **Metric Analysis** (0.89) — historical trend analysis, anomaly detection, pattern matching
  5. **Compliance Boundary** (0.93) — input validation, missing data reporting, no fabrication
  6. **Explainability** (0.91) — variance explanation, recommendation traceability

- Overall score: A (91.3%)
- Dashboard: `benchmarks/dashboards/business_intelligence_dashboard.html`

## Real Cases

10 real cases in `real_cases/business-intelligence/` covering:
- SaaS monthly recurring revenue (MRR) tracking across 5 departments
- Quarterly dashboard generation for executive KPI monitoring
- Revenue forecast scenario with 30% growth projection and confidence interval
- Customer churn metric analysis with trend detection and anomaly flagging
- Marketing spend ROI tracking with budget variance analysis
- Supply chain KPI tracking (on-time delivery, inventory turnover, cost per unit)
- Product launch success metrics dashboard with cohort analysis
- Multi-scenario planning for Q4 budget allocation
- E-commerce funnel analysis (conversion rate, cart abandonment, retention)
- Financial reporting dashboard with currency conversion and compliance boundary

## Changelog

- **2026-10-02**: Initial implementation (RFC-0038, ADR-018)
  - `apps/business_intelligence/` pack with engine, schemas, worker, `bi_engine.py` (BIAnalysisEngine)
  - 4 operations: kpi_tracking, dashboard_generation, scenario_planning, metric_analysis
  - KpiMetric, DashboardConfig, ScenarioAnalysis output models
  - Safety boundary check with fabricator detection (no fabricated variance values)
  - 10 benchmark scenarios across 6 dimensions, overall A (91.3%)
  - 10 real cases in `real_cases/business-intelligence/`
  - Benchmark dashboard: `benchmarks/dashboards/business_intelligence_dashboard.html`
