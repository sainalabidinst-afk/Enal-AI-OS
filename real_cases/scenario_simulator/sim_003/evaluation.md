# Real Case: SIM-003 — Monte Carlo Convergence Test

**Scenario:** Large-scale convergence validation
**Distribution:** Beta (probability of success), Lognormal (cost overrun)
**Iterations:** 5000
**Seed:** 12345

## Analysis

- 5000 iterations with beta distribution for success probability (alpha=8, beta=2)
- Lognormal distribution for cost overrun factor (mu=0.1, sigma=0.3)
- Convergence test: mean stabilizes after ~2000 iterations (within 1%)
- P5-P95 spread: 0.62 to 0.94 (success probability range)
- Histogram shows expected beta shape (skewed toward high success)
- Reproducibility: identical results across 3 runs with same seed
- Throughput: 3,200 iterations/second (parallel mode: 8,500 iter/sec)

## Improvement
- Add early termination when confidence interval is narrow enough
