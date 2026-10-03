# ADR-028: Visual Agent Builder Architecture

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Frontend Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-03
**Versi:** 1.0.0
**Status:** Accepted
**SSOT:** Arsitektur visual agent builder untuk ECP
<!-- DOCUMENT_METADATA_END -->

## Abstrak

ADR ini mendokumentasikan keputusan arsitektur untuk Visual Agent Builder, termasuk layout UI, backend integration dengan AgentFactory/Validator/Runtime, dan API endpoints.

## Konteks

Setelah Visual Builder Foundation (ADR-027), Agent Builder diperlukan untuk memungkinkan user membuat agent tanpa menulis kode.

## Keputusan

### 1. Layout UI

**Decision:** Canvas kiri + Config Panel kanan (384px)
**Rationale:**
- Pattern yang familiar dari Figma/Excalidraw
- Config panel tetap terlihat saat scroll canvas
- Responsive untuk laptop/desktop

### 2. Backend Integration

**Decision:** AgentFactory + AgentValidator + AgentRuntime
**Rationale:**
- Separation of concerns
- Reusable dari blueprint execution
- Testable secara terisolasi

### 3. Configuration Tabs

**Decision:** General/Model/Tools/Knowledge tabs
**Rationale:**
- Group related settings
- Reduce cognitive load
- Extensible untuk future tabs

## Consequences

### Positive
- Clean separation UI/backend
- Reusable factory pattern
- Testable components

### Negative
- Multiple tabs bisa confusing untuk new users
- Config panel width fixed (384px)

### Neutral
- Uses existing Decorator SDK untuk middleware

## References

- RFC-0047: Visual Agent Builder
- RFC-0046: Visual Builder Foundation
