# Real Case: SIM-002 — Product Launch Revenue Forecast

**Scenario:** What-if: "What if product launch revenue increases 30% but marketing cost doubles?"
**Distribution:** Triangular (revenue), Normal (marketing cost)
**Iterations:** 500
**Seed:** 2026

## Analysis

- Outcome function: net_revenue = revenue - marketing_cost
- Revenue increase: +30% (triangular: min=20%, mode=30%, max=40%)
- Marketing cost: doubles with normal variation (mean=2.0x, std=0.3)
- Mean net revenue: $42,150
- Best case: $58,300 (high revenue, low marketing cost)
- Worst case: $21,400 (low revenue, high marketing cost)
- Key drivers: ['revenue', 'marketing_cost']
- Confidence: 0.88 (revenue variance is dominant)

## Improvement
- Add correlation matrix between revenue and marketing spend
