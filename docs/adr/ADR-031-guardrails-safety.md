# ADR-031: Guardrails & Safety Architecture

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Safety & Governance
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-03
**Versi:** 1.0.0
**Status:** Accepted
**SSOT:** Arsitektur guardrails dan safety layer untuk ECP
<!-- DOCUMENT_METADATA_END -->

## Abstrak

ADR ini mendokumentasikan keputusan arsitektur untuk Guardrails & Safety layer, termasuk 8 validator types, corrective actions, dan integration points.

## Konteks

ECP memerlukan safety layer untuk mencegah output yang berbahaya, biased, atau tidak sesuai kebijakan.

## Keputusan

### 1. Validator Architecture

**Decision:** BaseGuardrail abstract class dengan concrete implementations
**Rationale:**
- Extensible untuk new validators
- Consistent interface
- Testable secara terisolasi

### 2. Corrective Actions

**Decision:** FIX, NOOP, EXCEPTION enum
**Rationale:**
- FIX: Auto-correct (PII redaction)
- NOOP: Allow but log
- EXCEPTION: Block and raise

### 3. Integration Points

**Decision:** Agent input/output, Tool step input/output, Voice agent
**Rationale:**
- Comprehensive coverage
- Layered safety
- Consistent across all interfaces

## Consequences

### Positive
- Comprehensive safety layer
- Extensible validator architecture
- Clear corrective actions

### Negative
- Performance overhead dari validation
- False positives possible

### Neutral
- Uses existing Consent Manager untuk UI

## References

- RFC-0050: Guardrails & Safety
- SimplAI Guardrails: https://simplai.ai/docs/guardrails/
