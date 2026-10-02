# Evaluation

Scenario: obs-002 - Threshold breach detection

## Analysis
- Metric `memory_usage` current value 92.5 with threshold 80.0 (above)
- Breach correctly flagged: breached=True
- Average/max/min computed and inputs traced to threshold direction
- Quality score: 0.85

## Improvement
- Add rolling-window breach cooldown to reduce alert flapping
