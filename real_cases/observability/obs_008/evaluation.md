# Evaluation

Scenario: obs-008 - Critical threshold breach

## Analysis
- Metric `error_rate`: baseline 0.5, current 12.0, deviation +2300%
- Threshold 5.0 (above) breached; severity critical
- Detection surfaced as advisory only, no operational control
- Quality score: 0.85

## Improvement
- Add burn-rate alerting integration for SLO-style metrics
