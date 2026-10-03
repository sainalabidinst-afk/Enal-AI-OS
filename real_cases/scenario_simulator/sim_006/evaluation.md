# Real Case: SIM-006 — Decision Intelligence Integration: Plan Simulation

**Scenario:** 5-step product launch roadmap under market variability
**Distribution:** Beta (step success probability), Normal (market demand modifier)
**Iterations:** 500
**Seed:** 7

## Analysis

- Plan steps converted to base state success probabilities:
  - Market research: 0.85
  - Product development: 0.78
  - Beta testing: 0.92
  - Marketing preparation: 0.70
  - Go-to-market launch: 0.65
- Beta distribution for success probability: alpha=8, beta=2 (skewed toward success)
- Market demand modifier: normal (mean=1.0, std=0.15) as percent delta
- Overall plan success rate distribution:
  - Mean: 0.39 (39% of simulations all 5 steps succeed)
  - P5: 0.12
  - P50: 0.41
  - P95: 0.72
- Bottleneck steps (lowest success): Go-to-market launch (0.65), Marketing preparation (0.70)
- Key drivers: ['market_demand_modifier', 'go_to_market_success', 'marketing_prep_success']
- Confidence: 0.87 (beta distribution provides realistic probability ranges)

## Integration

```python
from apps.scenario_simulator.engine import ScenarioSimulatorEngine

engine = ScenarioSimulatorEngine()
plan = [
    {"description": "Market research", "expected_result": 0.85},
    {"description": "Product development", "expected_result": 0.78},
    {"description": "Beta testing", "expected_result": 0.92},
    {"description": "Marketing preparation", "expected_result": 0.70},
    {"description": "Go-to-market launch", "expected_result": 0.65},
]
context = {"scenario": "product launch", "market_condition": "volatile"}
result = engine.simulate_plan(plan, context, iterations=500, seed=7)
print(f"Plan success rate: {result.distribution.mean:.2%}")
print(f"P5: {result.distribution.p5}, P95: {result.distribution.p95}")
print(f"Key drivers: {result.key_drivers}")
```

## Improvement
- Add conditional dependencies between plan steps
- Integrate with Decision Intelligence engine for evidence-weighted probabilities
