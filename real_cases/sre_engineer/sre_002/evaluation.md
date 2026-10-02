# Evaluation

Scenario: sre-002 - Fintech SLO Design

## Architecture Review
- SLOs with 99.99% availability target for payment service
- Error budget policy with automated actions
- Latency SLOs with 50ms p99 target
- Alerting with burn rate notifications

## Improvements
- Add SLO dashboard with error budget remaining
- Implement multi-window alerting for accurate detection
- Set up query performance insights with tracing
- Use recording rules for precomputed SLO burn rates
