# Real Case: SIM-001 — Interest Rate Policy Impact

**Scenario:** What-if: "If suku bunga naik 1% dan kompetitor A turun harga 20%"
**Distribution:** Normal (interest rate), Uniform (competitor price)
**Iterations:** 100
**Seed:** 42

## Analysis

- Engine produces 100 iterations by default
- Same seed → same output (reproducibility verified)
- Variable changes reflect description parameters
- Assumptions extracted: ["Interest rate can be modeled as a continuous variable", "Competitor price responds proportionally"]
- Mean interest_rate: 0.0505, Mean competitor_price: 79.92
- Best case outcome: competitor_price = 60.2 (floor of uniform range)
- Worst case outcome: competitor_price = 99.85 (ceiling of uniform range)

## Improvement
- Add lognormal distribution for price variables (implemented)
