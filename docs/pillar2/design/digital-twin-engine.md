# Digital Twin Engine

## Responsibility
Synchronize real-world state and execute what-if simulations.

## Components
- `DigitalTwinEngine`
- `StateSync`
- `MonteCarloRunner`
- `ScenarioSimulator`

## Flow
1. Ingest telemetry from IoT, DB, market feeds.
2. Build twin state snapshot.
3. Apply scenario parameters.
4. Run Monte Carlo iterations.
5. Aggregate results and generate recommendations.

## Data Contract
```json
{
  "simulation_id": "string",
  "scenario": "string",
  "parameters": {},
  "iterations": 1000,
  "time_warp_factor": 1.0,
  "status": "pending | running | completed | failed"
}
```

## VS Code Deliverables
- Add `apps/decision_intelligence/digital_twin_engine.py`
- Add `apps/decision_intelligence/state_sync.py`
- Add `apps/decision_intelligence/monte_carlo_runner.py`
