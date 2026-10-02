# Evaluation

Scenario: cs-010 - Source reference and formula traceability

## Analysis

- Operation: incident_detect with source_id = alert-42
- Baseline events: [100.0, 100.0, 100.0, 90.0], current = 300.0
- Baseline average: 97.5
- Deviation: +207.7% (above 50% threshold)
- Anomaly detected: true
- Source reference preserved: alert-42
- Formula disclosed: (current - baseline_avg) / baseline_avg * 100
- Input lineage traced: baseline_events, current_event_count, alerts, source_id
- Deviation percentage calculated and reported
- Incident detection claim: false (advisory only)
- Root cause attribution: false
- Quality score: 0.94

## Improvement

- Add correlation ID for cross-system incident tracking
- Include temporal context (first seen, last seen) in trace output
