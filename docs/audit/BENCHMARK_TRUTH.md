# Benchmark Truth

Status: BLOCKED. No current benchmark score is valid.

## Execution Attempt

Command:

```text
python -m benchmarks.performance_benchmark
```

Result: process failed before measurement collection with:

```text
litellm.BadRequestError: LLM Provider NOT provided.
You passed model=claude-3-5-sonnet-20240620
```

The stack reaches `adaptive_runtime`, `cognitive_kernel`, `strategic_planner`, and `model_router.acomplete` before failing. Raw executions: 0. Latency, throughput, determinism and reliability measurements: none.

## Root Cause

- `backend/app/core/config.py` sets `DEFAULT_REASONING_MODEL` to `claude-3-5-sonnet-20240620`.
- `backend/app/core/model_router.py` passes that model to LiteLLM and adds an Anthropic key field, but does not add an explicit provider prefix.
- The local environment has no configured Anthropic, OpenAI or Google key.
- No credentials were created or injected during this audit.

Classification: ENVIRONMENT BLOCKER combined with an explicit model-routing configuration gap.

## Artifact Reconciliation

- 22 stored benchmark JSON files report the same `overallScore: 96.99`.
- The stored files also repeat identical latency, throughput, iteration and failure values.
- `docs/audit/BENCHMARK_EXECUTION_RESULT.md` records zero completed executions and no score.
- The stored 96.99 and platform scores are therefore STALE / UNVERIFIED, not fresh measurements.

## What Passed

`tests/test_performance_benchmark.py` passed 4 targeted regression tests for runtime output extraction and error handling in 14.35 seconds.

Those tests verify the adapter contract. They do not verify provider connectivity or produce benchmark measurements.

## Required Remediation

Configure an authorized model provider and an explicit provider-compatible model route, then rerun the benchmark without changing the scoring formula or supplying synthetic data. Do not update certification artifacts until raw executions are present.
