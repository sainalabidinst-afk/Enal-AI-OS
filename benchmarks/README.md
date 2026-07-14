# ECP Benchmark Suite

This directory contains benchmarks for measuring ECP performance and quality.

## Running Benchmarks

```bash
# Run all benchmarks
python -m benchmarks.performance_benchmark

# Run specific benchmark
python -m benchmarks.agent_quality
```

## Benchmark Categories

### Performance Benchmarks

- `performance_benchmark.py` — Latency, token efficiency, determinism, success rate
- `package_boundaries.py` — Package dependency enforcement

### Quality Benchmarks

- `agent_quality.py` — Agent response quality
- `capability_benchmark.py` — Capability Pack quality across 6 dimensions: Accuracy, Completeness, Explainability, Safety, Efficiency, Consistency
- Real-world cases from `real_cases/<capability_id>/` feed into capability benchmarks

## Benchmark Types

### Synthetic Benchmark

Structured scenarios with known expected outputs, defined in `benchmarks/`.

### Real-world Benchmark

Cases from actual usage stored in `real_cases/<capability_id>/`.
Each case contains input, output, and evaluation.
Real-world cases are the primary source of Capability Pack improvement.
Synthetic benchmarks validate improvements; real-world cases drive them.

## Adding New Benchmarks

1. Create a new Python file in this directory
2. Use the `Benchmark` class from `backend.app.core.evaluation`
3. Run with `python -m benchmarks.your_benchmark`

## CI Integration

Benchmarks run automatically on every PR:
- Performance benchmarks must not degrade > 10%
- Quality benchmarks must maintain > 80% pass rate
- Package boundaries must have zero violations
