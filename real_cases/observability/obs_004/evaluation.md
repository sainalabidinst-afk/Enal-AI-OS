# Evaluation

Scenario: obs-004 - Slow span and error-rate detection

## Analysis
- Trace trace-2002 across payment/card services, error_rate 0.12 (above 5% budget)
- Health status correctly marked unhealthy; charge span duration 1500ms dominant
- Spans grouped by status; slow span identifiable
- Quality score: 0.85

## Improvement
- Surface the slowest span as a focused recommendation
