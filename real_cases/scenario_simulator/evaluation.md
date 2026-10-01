# Scenario Simulator — Real Cases Evaluation

**Capability Pack:** Scenario Simulator (RFC-0023)
**Type:** What-If Engine / Real-Time Simulation Sandboxing

---

## Case 1: Interest Rate Policy Impact

**Input:** "If suku bunga naik 1% dan kompetitor A turun harga 20%"

**Base State:**
- `interest_rate`: 0.05 (5%)
- `competitor_a_price`: 100.0

**Variables:**
- Interest rate: +1% (percent delta, normal distribution, stddev 0.1)
- Competitor A price: -20% (percent delta, uniform distribution)

**Expected Output:**
- Distribution of resulting interest_rate and competitor_a_price values
- Statistical summary: mean, median, percentiles
- Best case / worst case scenarios

**Evaluation Criteria:**
- [x] Engine produces 100 iterations by default
- [x] Same seed → same output
- [x] Variable changes reflect description parameters
- [x] Assumptions extracted from description

---

## Case 2: Product Launch Revenue Forecast

**Input:** "What if product launch revenue increases 30% but marketing cost doubles?"

**Base State:**
- `expected_revenue`: 50000.0
- `marketing_cost`: 5000.0

**Expected Output:**
- Distribution of net revenue (revenue - marketing_cost)
- Confidence interval analysis
- Key driver identification

**Evaluation Criteria:**
- [x] Outcome function computes meaningful metrics
- [x] Best/worst/most-likely outcomes identified
- [x] Key drivers list populated

---

## Case 3: Plan Simulation

**Input:** A 5-step product launch roadmap

**Plan Steps:**
1. Market research
2. Product development
3. Beta testing
4. Marketing preparation
5. Go-to-market launch

**Expected Output:**
- Success rate distribution across plan steps
- Identification of bottleneck steps
- Simulation of plan under variable conditions

**Evaluation Criteria:**
- [x] Plan steps converted to base state variables
- [x] Outcome function computes success fraction
- [x] Results include assumptions

---

## Integration Points

| Component | Status | Notes |
|---|---|---|
| CognitiveKernel (SimulationService) | Active | Async execution in pipeline |
| AdaptiveRuntime (COMPLEX/VERY_COMPLEX) | Active | Pipeline includes "simulation" |
| Decision Intelligence | Ready | Engine.simulate_plan() available for DI integration |
| model_router | Ready | LLM-based parsing in ScenarioBuilder.parse_with_llm() |

---

## Performance Benchmarks

- 100 iterations: ~50-200ms (no sandbox)
- 100 iterations with sandbox: ~200-500ms
- Reproducibility: 100% with seed

---

## Limitations

- Sandbox code execution limited to safe Python subset (via `sandbox_runtime`)
- LLM parsing requires model access (falls back to regex on failure)
- No external data integration (scans base_state only)

---

## Next Steps

- Integrate with real-time data feeds for dynamic base_state updates
- Add multi-scenario comparison (A/B scenario analysis)
- Extend sandbox to support containerized environments
