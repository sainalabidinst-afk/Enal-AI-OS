# Real Case: SIM-004 — Trading Analyst Integration: Price Path Simulation

**Scenario:** Monte Carlo price path simulation for BTC-USD
**Distribution:** Lognormal (geometric Brownian motion)
**Iterations:** 10000
**Seed:** 42

## Analysis

- Asset: BTC-USD
- Initial price: $50,000
- Volatility: 60% (0.60)
- Simulation time horizon: 30 days
- Final price distribution:
  - Mean: $52,300
  - P5: $28,450
  - P50 (median): $51,800
  - P95: $89,200
- Risk metrics:
  - Probability of 50% drawdown: 12.3%
  - Value at Risk (P5): -$21,550
  - Expected Shortfall (P5): -$28,300
- Confidence: 0.91 (lognormal model fit)

## Integration

```python
from apps.scenario_simulator.engine import ScenarioSimulatorEngine

engine = ScenarioSimulatorEngine()
result = engine.run_trading_analysis(
    asset="BTC-USD",
    initial_price=50000,
    volatility=0.6,
    iterations=10000,
    seed=42,
)
print(f"Mean price: {result.distribution.mean}")
print(f"P5: {result.distribution.p5}, P95: {result.distribution.p95}")
```

## Improvement
- Add multi-asset portfolio correlation simulation
- Integrate with real-time price feeds
