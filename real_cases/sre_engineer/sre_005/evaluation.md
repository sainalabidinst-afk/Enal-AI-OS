# Evaluation

Scenario: sre-005 - Multi-Cloud Monitoring

## Architecture Review
- Prometheus federation across cloud providers
- Grafana unified dashboards for all clusters
- Cross-cloud alerting with deduplication
- OpenTelemetry collectors with tail-based sampling

## Improvements
- Add cross-cloud trace correlation with trace IDs
- Implement global SLOs with per-region breakdowns
- Use Thanos for long-term metric storage and querying
- Set up multi-cloud status page for external visibility
