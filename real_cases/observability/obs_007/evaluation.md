# Evaluation

Scenario: obs-007 - Anomaly baseline deviation

## Analysis
- Metric `request_latency_p95`: baseline 100.0, current 400.0, deviation +300%
- Threshold 300.0 (above) breached; severity critical (>50% deviation)
- Finding derived from report with source_id alert-9 preserved
- Quality score: 0.90

## Improvement
- Add multi-dimension anomaly correlation (latency + error_rate)
