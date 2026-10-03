# ADR-029: Visual Tool Builder Architecture

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Frontend Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-03
**Versi:** 1.0.0
**Status:** Accepted
**SSOT:** Arsitektur visual tool builder dengan step graph untuk ECP
<!-- DOCUMENT_METADATA_END -->

## Abstrak

ADR ini mendokumentasikan keputusan arsitektur untuk Visual Tool Builder, termasuk step graph UI, StepExecutor, dan ToolEngine.

## Konteks

Tool builder memerlukan step graph yang lebih kompleks dari agent builder, dengan branching, conditional logic, dan error handling.

## Keputusan

### 1. Step Graph UI

**Decision:** Gunakan ReactFlow dengan custom step nodes
**Rationale:**
- Reuse Visual Builder Foundation
- Visual step graph lebih intuitive
- Support untuk conditional branching

### 2. Step Executor Pattern

**Decision:** Strategy pattern dengan StepExecutor
**Rationale:**
- Setiap step type punya executor sendiri
- Easy to extend dengan step types baru
- Testable secara terisolasi

### 3. Configuration

**Decision:** JSON editor untuk step configuration
**Rationale:**
- Flexible untuk berbagai step types
- Power users bisa edit JSON langsung
- Simple untuk simple configurations

## Consequences

### Positive
- Visual step graph intuitif
- Extensible step types
- Flexible configuration

### Negative
- JSON editing bisa intimidating untuk non-technical users
- Step graph bisa jadi complex untuk large tools

### Neutral
- Uses existing Pipeline Engine untuk orchestration

## References

- RFC-0048: Visual Tool Builder
- RFC-0046: Visual Builder Foundation
