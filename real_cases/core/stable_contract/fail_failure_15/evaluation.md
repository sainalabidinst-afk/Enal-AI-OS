# Evaluation: Trace Corruption (fail_failure_15)

- **Date:** 2026-10-02
- **Category:** failure_trace
- **Tags:** failure_isolation, resilience
- **Status:** PASS

## Scenario



**Failure Isolation** — pack failure was contained and core remained operational.

Task intent: `observability.trace.bad`

## Execution Result

- **Status:** success
- **Latency P95:** 50.0 ms
- **Events emitted:** 2
- **Trace ID propagated:** trace-fail_failure_15

## Expert Review

Pack failure was isolated. Core remained operational. Event Bus recorded error without crashing. 50ms recovery time.

## Lessons Learned

- Contract versioning allows graceful fallback to v1.0.0
- Event Bus Pydantic validation prevents malformed payloads
- Pipeline Engine records stage-level events for debugging
