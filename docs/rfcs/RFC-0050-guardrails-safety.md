# RFC-0050: Guardrails & Safety

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Safety & Governance
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-03
**Versi:** 1.0.0
**Status:** Draft → Proposed
**SSOT:** Rancangan guardrails dan safety layer untuk ECP: PII detection, toxic language, prompt injection, bias check, logic check, competitor check, gibberish detection, reading level validation
<!-- DOCUMENT_METADATA_END -->

## Abstrak

RFC ini mendefinisikan Guardrails & Safety layer untuk ECP, yang menyediakan validasi input/output agent dan tool melalui 8 validator types. Guardrails ini mencegah output yang berbahaya, biased, atau tidak sesuai kebijakan.

## Konteks

ECP memerlukan safety layer untuk:
1. Mencegah PII (email, phone, SSN, credit card) bocor
2. Mendeteksi toxic language
3. Mencegah prompt injection attacks
4. Mendeteksi bias dalam output
5. Validate logical consistency
6. Mendeteksi competitor mentions
7. Mendeteksi gibberish output
8. Validate reading level complexity

## Keputusan

### 1. Guardrail Engine Architecture

**Core Components:**
- `GuardrailEngine` — Orchestrator untuk menjalankan guardrails
- `BaseGuardrail` — Abstract base class
- `GuardrailResult` — Result object dengan triggered, action, details, modified_content
- `CorrectiveAction` — Enum: FIX, NOOP, EXCEPTION

### 2. Validators

| Validator | Name | Action | Description |
|-----------|------|--------|-------------|
| PIIValidator | `pii` | FIX | Detect email, phone, SSN, credit card |
| ToxicLanguageValidator | `toxic_language` | NOOP | Detect profanity and harmful content |
| PromptInjectionValidator | `prompt_injection` | EXCEPTION | Detect injection attacks |
| BiasCheckValidator | `bias_check` | NOOP | Detect biased output |
| LogicCheckValidator | `logic_check` | NOOP | Validate logical consistency |
| CompetitorCheckValidator | `competitor_check` | NOOP | Detect competitor mentions |
| GibberishValidator | `gibberish` | NOOP | Detect nonsense output |
| ReadingLevelValidator | `reading_level` | NOOP | Validate reading complexity |

### 3. Corrective Actions

- **FIX** — Auto-correct content (PII redaction)
- **NOOP** — Allow but log
- **EXCEPTION** — Block and raise error

### 4. Integration Points

- Agent input/output
- Tool step input/output
- Voice agent input/output

### 5. Frontend Components

- `GuardrailConfig.tsx` — Configure guardrails
- `GuardrailTest.tsx` — Test guardrails on sample input
- `GuardrailDashboard.tsx` — View guardrail triggers

### 6. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/guardrails/test` | Test guardrails on content |
| GET | `/api/v1/guardrails` | List available guardrails |

## Implementasi

### Frontend Components

- `GuardrailConfig.tsx` — Guardrail configuration panel
- `GuardrailTest.tsx` — Test guardrails on sample input
- `GuardrailDashboard.tsx` — View guardrail triggers

### Backend Modules

- `backend/app/core/guardrail_engine.py` — GuardrailEngine + 8 validators
- `backend/app/api/guardrails.py` — API endpoints

## Dependencies

- RFC-0046: Visual Builder Foundation

## Testing

- TypeScript: 0 errors
- Ruff: 0 errors
- Mypy: 0 errors

## References

- SimplAI Guardrails: https://simplai.ai/docs/guardrails/
