# Evaluation

Scenario: cs-006 - Incident severity classification

## Analysis

- Baseline of 4 events: [50.0, 52.0, 48.0, 51.0]
- Baseline average: 50.25
- Current event count: 120.0
- Deviation: +138.8% (above 30% threshold)
- Anomaly detected: true
- Alert severity: high (CPU usage alert)
- Alert confidence: 0.85
- Input lineage traced: baseline_events, current_event_count, alerts
- Source reference preserved: incident-2
- Quality score: 0.90

## Improvement

- Add alert suppression for known maintenance windows
- Include runbook auto-suggestion based on alert type and severity
