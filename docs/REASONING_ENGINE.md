# Reasoning Engine

## Overview

Reasoning Engine adalah symbolic/rule-based reasoning engine untuk multi-step reasoning, decision making, dan constraint validation. Engine menggunakan aturan deterministik (BUKAN LLM) untuk menghasilkan kesimpulan dan keputusan yang dapat dijelaskan.

## Methods

### 1. Forward Chaining
Mulai dari fakta yang diketahui, aplikasikan rules untuk mencapai kesimpulan.

```
Known Facts → Apply Rules → New Facts → Apply Rules → ... → Conclusions
```

**Use case**: Goal decomposition, capability identification

### 2. Backward Chaining
Mulai dari outcome yang diinginkan, cari prerequisites yang diperlukan.

```
Desired Outcome ← Find Prerequisites ← Find Sub-prerequisites ← ...
```

**Use case**: Finding what's needed to achieve a goal

### 3. Decision Tree
Evaluasi opsi-opsi terhadap kriteria yang ditentukan.

```
Options × Criteria → Scoring → Best Option Selected
```

**Use case**: Technology selection, resource allocation decisions

### 4. Constraint Propagation
Verifikasi bahwa semua constraint terpenuhi.

```
Variables × Constraints → Satisfied/Violated → Proceed/Block
```

**Use case**: Budget validation, timeline checking

### 5. Causal Reasoning
Analisis cause-effect relationships.

```
Event → Find Causes → Identify Effects → Generate Recommendations
```

**Use case**: Failure analysis, impact assessment

## Data Structures

### Evidence
- `id`: Unique identifier
- `type`: FACT, RULE, CONSTRAINT, OBSERVATION, DERIVED
- `description`: Human-readable description
- `confidence`: 0.0 - 1.0
- `source`: Where this evidence came from

### ReasoningRule
- `rule_id`: Unique identifier
- `conditions[]`: Conditions that must be true
- `conclusions[]`: Conclusions when conditions are met
- `confidence`: Confidence when rule fires
- `priority`: For conflict resolution

### Decision
- `decision_id`: Unique identifier
- `options[]`: Available options
- `selected`: The chosen option
- `confidence`: Confidence in decision
- `reasoning`: Explanation of why
- `urgency`: LOW, MEDIUM, HIGH, CRITICAL

### Conclusion
- `conclusion_id`: Unique identifier
- `statement`: The conclusion
- `confidence`: Confidence level
- `evidence_ids[]`: Supporting evidence
- `derived`: Whether derived (vs direct)

### ReasoningResult
- `reasoning_id`: Unique session ID
- `method`: The reasoning method used
- `status`: COMPLETED, FAILED, INCONCLUSIVE
- `evidence[]`, `conclusions[]`, `decisions[]`
- `confidence`: Overall confidence
- `explanation`: Human-readable explanation
- `execution_time_ms`: Time taken

## Usage

```python
from apps.organization.reasoning_engine import (
    reasoning_engine,
    ReasoningMethod,
    Evidence, EvidenceType,
)

# Forward chaining
result = reasoning_engine.forward_chaining(
    "Complete a complex software project"
)

# Backward chaining
result = reasoning_engine.backward_chaining(
    "Deploy web app",
    "Application is running in production",
    context={"domain": "devops"}
)

# Decision tree
result = reasoning_engine.decision_tree(
    "Which framework?",
    options=[
        {"name": "FastAPI", "attributes": {"speed": 9, "cost": 3}},
        {"name": "Django", "attributes": {"speed": 6, "cost": 5}},
    ],
    criteria=["speed", "cost"]
)

# Constraint propagation
result = reasoning_engine.constraint_propagation(
    constraints=[
        {"name": "Budget limit", "variable": "budget", "operator": "lt", "value": 1000},
    ],
    variables={"budget": 500}
)

# Causal reasoning
engine.add_fact("Network was unstable", True)
result = engine.causal_reasoning("Pipeline execution failed")

# Knowledge base
engine.add_fact("System is ready", True, confidence=0.95)
evidence = engine.query_evidence("system")

# Rule management
from apps.organization.reasoning_engine import ReasoningRule
engine.register_rule(ReasoningRule(
    rule_id="my-rule",
    name="My Rule",
    description="Custom rule",
    conditions=["condition met"],
    conclusions=["conclusion reached"],
))
```

## Telemetry Events

- `ReasoningStarted`: When reasoning begins
- `ReasoningRuleApplied`: When a rule is fired
- `ReasoningCompleted`: When reasoning succeeds
- `ReasoningFailed`: When reasoning encounters an error
- `ReasoningDecisionMade`: When a decision is made

## Default Rules

1. **Goal Decomposition** (priority 1): Complex goals → sub-goals
2. **Capability Requirement** (priority 2): Goal domain → required capabilities
3. **Dependency Resolution** (priority 3): Steps → ordered execution
4. **Constraint Validation** (priority 4): Constraints → validated/blocked
5. **Resource Planning** (priority 5): Requirements → resource allocation
6. **Risk Assessment** (priority 6): Complexity + dependencies → risk level
7. **Quality Gate** (priority 7): Completed steps → quality verification

