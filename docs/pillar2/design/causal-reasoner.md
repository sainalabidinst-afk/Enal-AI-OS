# Causal Reasoner

## Responsibility
Perform causal inference and counterfactual reasoning on ECP knowledge graphs.

## Components
- `CausalReasoner`
- `CausalGraphBuilder`
- `DoCalculusEngine`
- `CounterfactualGenerator`

## Flow
1. Build DAG from Knowledge Graph.
2. Identify treatment and outcome variables.
3. Apply do-calculus to estimate causal effect.
4. Generate counterfactual scenarios.
5. Return structured result with confidence.

## Data Contract
```json
{
  "query_id": "string",
  "treatment": "string",
  "outcome": "string",
  "conditions": {},
  "result": {
    "causal_effect": 0.0,
    "confidence": 0.0,
    "counterfactual": "string"
  }
}
```

## VS Code Deliverables
- Add `apps/decision_intelligence/causal_reasoner.py`
- Add `apps/decision_intelligence/causal_graph_builder.py`
- Add `apps/decision_intelligence/do_calculus_engine.py`
- Update `backend/app/core/` to expose causal query endpoint.
