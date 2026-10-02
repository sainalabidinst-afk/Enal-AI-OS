# Evaluation

Scenario: cs-005 - Incident anomaly detection from baseline

## Analysis

- Baseline of 5 events: [100.0, 110.0, 95.0, 105.0, 98.0]
- Baseline average: 101.6
- Current event count: 500.0
- Deviation: +392.1% (well above 50% threshold)
- Anomaly detected: true
- Formula disclosed: (current - baseline_avg) / baseline_avg * 100
- Input lineage traced: baseline_events, current_event_count, threshold
- Source reference preserved: incident-1
- Quality score: 0.92

## Improvement

- Add seasonal baseline adjustment for recurring traffic patterns
- Include multi-metric correlation to reduce false positives
