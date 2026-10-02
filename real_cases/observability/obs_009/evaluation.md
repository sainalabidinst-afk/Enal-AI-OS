# Evaluation

Scenario: obs-009 - Missing required metric name

## Analysis
- metrics_collect operation supplied without metric_name
- Validation reported missing metric_name instead of fabricating a value
- No metric_summary produced; quality_score reduced to 0.85
- Silent defaults not applied

## Improvement
- Return structured error codes for missing required fields
