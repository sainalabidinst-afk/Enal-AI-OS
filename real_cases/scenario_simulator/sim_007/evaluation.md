# Real Case: SIM-007 — System Architect Integration: Architecture Risk Review

**Scenario:** Microservices architecture failure risk assessment
**Distribution:** Lognormal (failure cascade multiplier), Beta (component reliability)
**Iterations:** 2000
**Seed:** 42

## Analysis

- Architecture: 8 microservices with criticality scores:
  - auth-service: 0.95 (high — affects all other services)
  - payment-service: 0.90 (high — financial transactions)
  - order-service: 0.75 (medium-high — core business logic)
  - inventory-service: 0.60 (medium — can be cached)
  - notification-service: 0.40 (low — non-critical)
  - analytics-service: 0.35 (low — offline processing)
  - search-service: 0.55 (medium — user experience)
  - recommendation-service: 0.45 (medium — personalization)
- Budget: $125,000 for risk mitigation
- Risk tolerance: 0.15
- Lognormal distribution for failure cascade multiplier (mu=0.2, sigma=0.5)
- Risk distribution:
  - Mean system risk score: 3.42
  - P5: 1.18
  - P50: 3.21
  - P95: 6.87
- Budget adequacy: 73% of simulations stay within risk tolerance
- Highest-risk components: auth-service (0.95), payment-service (0.90)
- Mitigation recommendation: $45K for auth-service redundancy, $35K for payment-service failover
- Confidence: 0.91 (lognormal model captures tail risk effectively)

## Integration

```python
from apps.scenario_simulator.engine import ScenarioSimulatorEngine

engine = ScenarioSimulatorEngine()
result = engine.run_architecture_review(
    component_criticality={
        "auth-service": 0.95,
        "payment-service": 0.90,
        "order-service": 0.75,
        "inventory-service": 0.60,
        "notification-service": 0.40,
        "analytics-service": 0.35,
        "search-service": 0.55,
        "recommendation-service": 0.45,
    },
    budget=125000,
    risk_tolerance=0.15,
    iterations=2000,
    seed=42,
)
print(f"Mean risk score: {result.distribution.mean:.2f}")
print(f"Budget adequacy: {result.raw.get('budget_adequacy', 'N/A')}")
```

## Improvement
- Add network topology-aware failure propagation
- Integrate with Infrastructure Engineer for actual deployment data
