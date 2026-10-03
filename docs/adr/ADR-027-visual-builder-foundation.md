# ADR-027: Visual Builder Foundation Architecture

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Frontend Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-03
**Versi:** 1.0.0
**Status:** Accepted
**SSOT:** Arsitektur fondasi visual builder untuk ECP
<!-- DOCUMENT_METADATA_END -->

## Abstrak

ADR ini mendokumentasikan keputusan arsitektur untuk fondasi visual builder ECP, termasuk penggunaan ReactFlow, schema blueprints, dan API persistensi.

## Konteks

ECP memerlukan visual builder untuk agent dan tool creation. Keputusan arsitektur harus mempertimbangkan maturity library, TypeScript support, dan skalabilitas.

## Keputusan

### 1. ReactFlow sebagai Canvas Engine

**Decision:** Gunakan `reactflow` library
**Rationale:**
- Mature library (11k+ stars)
- Built-in custom nodes/edges
- Excellent TypeScript support
- Optimized untuk 50-100 nodes

### 2. Blueprint Schema Design

**Decision:** Gunakan Pydantic models untuk schema
**Rationale:**
- Existing pattern di ECP (semua capability packs menggunakan Pydantic)
- Validasi bawaan
- Serialization/deserialization otomatis

### 3. Persistence Strategy

**Decision:** JSON file untuk development, PostgreSQL untuk production
**Rationale:**
- Simple untuk development
- Migration path yang jelas
- Existing database layer dapat digunakan

## Consequences

### Positive
- Rapid development dengan ReactFlow
- Type-safe schema dengan Pydantic
- Clear migration path ke production

### Negative
- ReactFlow menambah dependency
- JSON file persistence tidak cocok untuk production

### Neutral
- State management menggunakan React state + props untuk MVP

## References

- RFC-0046: Visual Builder Foundation
- ReactFlow Documentation: https://reactflow.dev/
