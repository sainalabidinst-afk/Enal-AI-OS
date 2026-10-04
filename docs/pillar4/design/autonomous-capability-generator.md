# Autonomous Capability Generator (Self-Synthesis)

## Responsibility
Detect capability gaps and synthesize new Capability Packs autonomously without manual engineering.

## Components
- `CapabilityGapDetector`
- `PackSynthesizer`
- `GovernanceSandbox`
- `PackRegistrar`

## Flow
1. Monitor user queries and execution failures.
2. Detect unsupported domain or recurring gap.
3. Generate pack scaffold: schemas, engine, worker, tests.
4. Run Governance Sandbox: type check, lint, benchmark.
5. If Quality Gates pass -> register to `apps/`.
6. If fail -> reject and log feedback for improvement.

## Data Contract
```json
{
  "pack_id": "string",
  "domain": "string",
  "status": "draft | testing | approved | rejected",
  "coverage": 0.0,
  "benchmark_score": 0.0,
  "tests_passed": 0,
  "tests_total": 0
}
```

## VS Code Deliverables
- Add `apps/self_development/gap_detector.py`
- Add `apps/self_development/pack_synthesizer.py`
- Add `apps/self_development/governance_sandbox.py`
- Update `backend/app/core/contract_validator.py` to support auto-registration.
