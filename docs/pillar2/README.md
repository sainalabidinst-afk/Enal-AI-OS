# Pilar 2 — VS Code Artifacts

## Scope
Design and contract artifacts for **Pilar 2: Advanced Decision Intelligence & Digital Twin Simulation**.

## What this folder contains
- `RFC-0057-decision-intelligence-simulation.md` — overarching RFC.
- `design/digital-twin-engine.md` — digital twin and Monte Carlo simulation.
- `design/red-team-agent.md` — adversarial testing and hardening loop.
- `design/causal-reasoner.md` — causal inference and counterfactual reasoning.

## Implementation Roadmap
1. Digital Twin Engine + State Sync
2. Scenario Simulator + Monte Carlo Runner
3. Red Team Agent + Hardening Loop
4. Causal Reasoner + Do-Calculus Engine
5. Benchmark and acceptance testing

## Acceptance Criteria
- Simulation latency per iteration < 100 ms
- Monte Carlo convergence within 10,000 iterations
- Causal query latency < 500 ms
- Adversarial test coverage >= 80% of decision paths
- Decision risk reduction >= 30% vs baseline
