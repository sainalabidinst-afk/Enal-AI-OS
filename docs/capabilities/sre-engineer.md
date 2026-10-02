# SRE Engineer Capability Pack

**Version:** 1.0.0  
**Target Grade:** A (≥90%)  
**Status:** Implemented  

## Ringkasan

SRE Engineer Capability Pack menyediakan keandalan sistem melalui observability setup, SLO design, incident response, dan capacity planning.

## Kemampuan Inti

1. **Observability Setup** — Prometheus, Grafana, OpenTelemetry, distributed tracing
2. **SLO Design** — error budgets, burn rate alerts, multi-window SLOs
3. **Incident Response** — runbooks, escalation, post-mortems
4. **Capacity Planning** — forecasting, right-sizing, autoscaling

## Monitoring Stacks

- Prometheus with federation, recording rules, Alertmanager
- Grafana with dashboards, templating, alerting
- OpenTelemetry agents, collectors, distributed tracing
- Datadog and New Relic integrations

## Supported SLIs

- Latency (p50, p95, p99)
- Availability (% uptime)
- Error Rate (% errors)
- Throughput (requests/second)

## Integration

- **Konsumsi dari**: Infrastructure Engineer (cluster designs), System Architect (SLO patterns)
- **Digunakan oleh**: DevOps Assistant, Application teams

## Benchmark

- 10 scenarios across 6 dimensions
- Overall score: A (≥90%)
- Scenarios: E-commerce observability, Fintech SLO design, Healthcare incident response, SaaS capacity planning, Multi-cloud monitoring, Critical SLO config, API gateway incident, Startup capacity, OTel migration, ML platform SRE

## Real Cases

10 real cases in `real_cases/sre_engineer/`

## Changelog

- **2026-10-02**: Initial implementation (RFC-0027, ADR-006)
