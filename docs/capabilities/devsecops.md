# DevSecOps Capability Pack

**Version:** 3.0.0
**Target Grade:** A (>=90%)
**Status:** Implemented
**Phase:** 7
**RFC:** [RFC-0040](docs/rfcs/RFC-0040-devsecops.md)
**ADR:** [ADR-020](docs/adr/ADR-020-devsecops.md)

## Ringkasan

DevSecOps Capability Pack mengintegrasikan keamanan ke dalam pipeline CI/CD dengan security gates yang otomatis, dependency vulnerability scanning, dan runtime policy enforcement. Pack ini memindai supply chain dependensi, memutuskan konsekuensi keamanan secara real-time, dan mencegah deployment yang tidak aman sebelum mencapai production environment.

## Kemampuan Inti

1. **Security Gate**
2. **Dependency Scan**
3. **Runtime Policy**
4. **Compliance As Code**

## Benchmark

- 10 scenarios across 6 dimensions
- Overall score: A (91.7%)
- Dashboard: `benchmarks/dashboards/devsecops_dashboard.html`

## Real Cases

10 real cases in `real_cases/devsecops/`

## Changelog

- **2026-10-02**: Initial implementation (RFC-0040, ADR-020)
