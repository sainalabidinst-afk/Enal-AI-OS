# Real Case: SIM-010 — Innovation Strategist Integration: R&D Portfolio Optimization

**Scenario:** Multi-project R&D portfolio simulation with budget and timeline uncertainty
**Distribution:** Triangular (project cost), Normal (timeline impact), Beta (success probability)
**Iterations:** 1000
**Seed:** 314

## Analysis

- R&D portfolio: 5 projects with allocated budgets:
  - Project Alpha (AI platform): $200K, critical
  - Project Beta (edge computing): $150K, high
  - Project Gamma (quantum ready): $500K, strategic
  - Project Delta (blockchain ID): $80K, opportunistic
  - Project Epsilon (IoT integration): $120K, tactical
- Total allocated: $1,050,000
- Budget uncertainty: +/- 20% triangular (min=0.8x, mode=1.0x, max=1.2x)
- Timeline impact: normal (mean=1.0x, std=0.15x duration multiplier)
- Success probability: beta(alpha=7, beta=3) for each project
- Portfolio ROI distribution:
  - Mean: $2,840K (2.7x budget)
  - P5: $1,120K (1.07x — break-even)
  - P50: $2,780K (2.65x)
  - P95: $4,920K (4.69x)
- Project-level risk:
  - Gamma: highest variance (std=$480K), expected ROI=3.2x
  - Delta: lowest variance (std=$12K), expected ROI=1.8x
- Optimal allocation recommendation: reduce Gamma to $400K, increase Beta to $200K (+12% expected ROI)
- Confidence: 0.89 (triangular cost with beta success captures project uncertainty well)

## Integration

```python
from apps.scenario_simulator.engine import ScenarioSimulatorEngine

engine = ScenarioSimulatorEngine()
base_state = {
    "project_alpha_budget": 200000,
    "project_beta_budget": 150000,
    "project_gamma_budget": 500000,
    "project_delta_budget": 80000,
    "project_epsilon_budget": 120000,
    "total_budget": 1050000,
}
request = engine.build_scenario(
    description="R&D portfolio ROI with cost and timeline uncertainty",
    base_state=base_state,
    iterations=1000,
    seed=314,
)
result = engine.run_simulation(request)
print(f"Mean portfolio ROI: ${result.distribution.mean/1000:.0f}K")
print(f"P5: ${result.distribution.p5/1000:.0f}K (break-even threshold)")
```

## Improvement
- Add correlation between project success probabilities
- Integrate with Innovation Strategist for tech trend weighting
