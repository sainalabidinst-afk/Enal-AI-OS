# Evaluation

Scenario: obs-006 - Warning pattern detection

## Analysis
- Log entries grouped by level: warning (search) and error (search)
- Pattern `level:warning` and `level:error` produced with service attribution
- Severity mapped appropriately per level
- Quality score: 0.85

## Improvement
- Correlate grouped warnings with downstream error spikes
