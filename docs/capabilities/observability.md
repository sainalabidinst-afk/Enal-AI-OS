# Observability Capability Pack

**Version:** 2.3.0
**Target Grade:** A (≥90%)
**Status:** Implemented
**Category:** Platform

## Ringkasan

Observability Capability Pack menyediakan pengumpulan metrik, analisis jejak terdistribusi (distributed tracing), analisis log, dan deteksi anomali untuk memantau kesehatan sistem. Semua output bersifat asistif dan tidak menggantikan investigasi insidental atau keputusan operasional manusia.

## Kemampuan Inti

1. **Metrics Collection** — Ringkasan metrik (avg/maks/min) dari sampel dan nilai historis, evaluasi pelanggaran threshold
2. **Trace Analysis** — Analisis kesehatan trase terdistribusi dari span, error rate, dan p95 latency
3. **Log Analysis** — Pengelompokan entri log ke pola berdasarkan level dan pola yang cocok
4. **Anomaly Detection** — Deteksi anomali dari deviasi baseline dengan severity yang dideklarasikan

## Input Schema

- `operation`: metrics_collect | trace_analyze | log_analyze | anomaly_detect
- `metric_name`, `metric_type` (gauge | counter | histogram), `aggregation`, `time_window`
- `threshold`, `threshold_direction` (above | below)
- `current_value`, `historical_values[]`, `metric_samples[]`
- `service_name`, `trace_id`, `spans[]`, `error_rate`, `p95_latency_ms`
- `log_entries[]`, `pattern`, `log_level`
- `baseline`, `data_points[]`, `source_id`

## Batasan Keamanan

- **Tidak mengeluarkan perintah operasional** — Deteksi tidak menggantikan response insiden
- **Tidak mengklaim sertifikasi** — anomaly_detection_claim = false, compliance_claim = false
- **Tidak menyatakan akar penyebab (root-cause)** — root_cause_attribution = false
- **Melaporkan input yang hilang** — Jangan menghitung metrik atau anomali jika nilai yang diperlukan tidak disediakan
- **Mensyaratkan source reference** — Setiap temuan dilacasi ke source_id atau alert penyebabnya

## Integration

- **Konsumsi dari**: System Architect (design metrics), SRE Engineer (runbook), Security Engineer (log threat hunting)
- **Digunakan oleh**: DevOps Assistant (CI/CD observability gates), SRE Engineer (incident triage), Product Manager (SLA dashboards)

## Benchmark

- 10 skenario dalam 6 dimensi
- Overall score: A (91%)
- Dimensi: metrics_collection, tracing_analysis, log_analysis, anomaly_detection, compliance_boundary, explainability
- Dashboard: `benchmarks/dashboards/observability_dashboard.html`

## Real Cases

10 real cases di `real_cases/observability/`

## Changelog

- **2026-10-02**: Initial implementation (RFC-0033, ADR-013) — Observability Capability Pack for ECP v2.3.0
