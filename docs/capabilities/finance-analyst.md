# Finance Analyst Capability Pack

**Version:** 1.0.0
**Target Grade:** A (≥90%)
**Status:** Implemented
**Category:** Vertical Industry

## Ringkasan

Finance Analyst Capability Pack menyediakan analisis keuangan, modeling skenario, risk assessment, dan kontrol kepatatuhan. Pack ini dirancang untuk mendukung keputusan keuangan dengan output yang dapat dilacak dan bebas saran investasi.

## Kemampuan Inti

1. **Financial Summary** — Hitung rasio keuangan (gross margin, current ratio) dari input yang lengkap
2. **Cash Flow Runway** — Estimasi runway dari kas dan burn rate bulanan
3. **Scenario Analysis** — Jalankan model sensitivitas untuk asumsi revenue
4. **Risk Modeling** — Bandingkan skenario downside dengan baseline
5. **Control Check** — Peta bukti kontrol ke checklist yang terversi

## Input Schema

- `operation`: financial_summary | cash_flow | scenario_analysis | risk_model | control_check
- `currency`: Kode mata uang (USD, EUR, dll)
- `revenue`, `cost_of_goods_sold`, `current_assets`, `current_liabilities`
- `cash_balance`, `monthly_net_burn`
- `baseline_revenue`, `margin`, `revenue_changes_pct[]`

## Batasan Keamanan

- **Tidak memberikan saran investasi individual** — Semua output harus bersifat informatif
- **Mensyaratkan unit/label mata uang yang jelas** — Tolak input ambigu
- **Melaporkan denominator yang hilang** — Jangan bagi dengan nol atau menemukan nilai
- **Certification claim = false** — Tidak boleh mendklaim kepatuhan dari bukti yang tidak cukup

## Integration

- **Konsumsi dari**: Infrastructure Engineer (biaya operasional), System Architect (budget planning)
- **Digunakan oleh**: Product Manager (pricing), Compliance Officer (evidence review)

## Benchmark

- 10 skenario dalam 6 dimensi
- Overall score: A (90.5%)
- Dimensi: financial_analysis, scenario_modeling, risk_modeling, control_check, compliance_boundary, explainability
- Dashboard: `benchmarks/dashboards/finance_analyst_dashboard.html`

## Real Cases

10 real cases di `real_cases/finance_analyst/`

## Changelog

- **2026-10-02**: Initial implementation (RFC-0030, ADR-010)
