# Evaluation

Scenario: sre-009 - OpenTelemetry Migration

## Architecture Review
- OpenTelemetry agents on all application hosts
- Collector with tail-based sampling for traces
- Export to both Prometheus and trace backend
- Semantic conventions for consistent metrics naming

## Improvements
- Add automatic instrumentation for supported frameworks
- Implement trace-to-metrics correlation for deeper insights
- Set up metric pipelines with filtering and aggregation
- Create dashboard templates for common service patterns
