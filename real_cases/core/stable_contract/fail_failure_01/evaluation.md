# Evaluation: Pipeline Stage Crash (fail_failure_01)

- **Date:** 2026-10-02
- **Category:** failure_pipeline
- **Tags:** failure_isolation, resilience
- **Status:** PASS (failure isolated)

## Scenario



**Failure Isolation** — pack failure was contained and core remained operational.

Task intent: `code_engineer.generate`

## Execution Result

- **Status:** failure
- **Latency P95:** 50.0 ms
- **Events emitted:** 2
- **Trace ID propagated:** trace-fail_failure_01

## Expert Review

Pack failure was isolated. Core remained partially operational. Event Bus recorded error without crashing. 50ms recovery time.

## Lessons Learned

- Contract versioning allows graceful fallback to v1.0.0
- Event Bus Pydantic validation prevents malformed payloads
- Pipeline Engine records stage-level events for debugging
