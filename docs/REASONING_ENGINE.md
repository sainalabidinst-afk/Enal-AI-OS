<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/REASONING_ENGINE.md`
- Judul: Reasoning Engine
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Reasoning Engine

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for REASONING_ENGINE
<!-- DOCUMENT_METADATA_END -->

## Overview

Reasoning Engine adalah symbolic/rule-based reasoning engine untuk multi-step reasoning, decision making, dan constraint validation. Engine menggunakan aturan deterministik (BUKAN LLM) untuk menghasilkan kesimpulan dan keputusan yang dapat dijelaskan.
> Terjemahan Indonesia: Reasoning Engine adalah mesin penalaran simbolik/berbasis aturan untuk penalaran multi-langkah, pengambilan keputusan, dan validasi batasan. Mesin menggunakan aturan deterministik (BUKAN LLM) untuk menghasilkan kesimpulan dan keputusan yang dapat dijelaskan.

## Methods

### 1. Forward Chaining
Mulai dari fakta yang diketahui, aplikasikan rules untuk mencapai kesimpulan.
> Terjemahan Indonesia: Mulai dari fakta yang diketahui, terapkan aturan untuk mencapai kesimpulan.

```
Known Facts â†’ Apply Rules â†’ New Facts â†’ Apply Rules â†’ ... â†’ Conclusions
```

**Use case**: Goal decomposition, capability identification

### 2. Backward Chaining
Mulai dari outcome yang diinginkan, cari prerequisites yang diperlukan.
> Terjemahan Indonesia: Mulai dari hasil yang diinginkan, cari prasyarat yang diperlukan.

```
Desired Outcome â† Find Prerequisites â† Find Sub-prerequisites â† ...
```

**Use case**: Finding what's needed to achieve a goal

### 3. Decision Tree
Evaluasi opsi-opsi terhadap kriteria yang ditentukan.
> Terjemahan Indonesia: Evaluasi opsi-opsi terhadap kriteria yang ditentukan.

```
Options Ã— Criteria â†’ Scoring â†’ Best Option Selected
```

**Use case**: Technology selection, resource allocation decisions

### 4. Constraint Propagation
Verifikasi bahwa semua constraint terpenuhi.
> Terjemahan Indonesia: Verifikasi bahwa semua kendala terpenuhi.

```
Variables Ã— Constraints â†’ Satisfied/Violated â†’ Proceed/Block
```

**Use case**: Budget validation, timeline checking

### 5. Causal Reasoning
Analisis cause-effect relationships.
> Terjemahan Indonesia: Analisis hubungan sebab-akibat.

```
Event â†’ Find Causes â†’ Identify Effects â†’ Generate Recommendations
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

1. **Goal Decomposition** (priority 1): Complex goals â†’ sub-goals
2. **Capability Requirement** (priority 2): Goal domain â†’ required capabilities
3. **Dependency Resolution** (priority 3): Steps â†’ ordered execution
4. **Constraint Validation** (priority 4): Constraints â†’ validated/blocked
5. **Resource Planning** (priority 5): Requirements â†’ resource allocation
6. **Risk Assessment** (priority 6): Complexity + dependencies â†’ risk level
7. **Quality Gate** (priority 7): Completed steps â†’ quality verification
