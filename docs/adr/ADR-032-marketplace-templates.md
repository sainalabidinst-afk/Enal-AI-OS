# ADR-032: Marketplace & Templates Architecture

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Frontend Platform
**Canonical Owner:** Lead Platform Engineer
**Terakhir Diverifikasi:** 2026-10-03
**Versi:** 1.0.0
**Status:** Accepted
**SSOT:** Arsitektur marketplace untuk berbagi dan menemukan agent/tool templates
<!-- DOCUMENT_METADATA_END -->

## Abstrak

ADR ini mendokumentasikan keputusan arsitektur untuk Marketplace & Templates, termasuk visibility model, sharing flow, cloning flow, dan analytics.

## Konteks

ECP memerlukan cara untuk share, discover, dan clone agent/tool templates.

## Keputusan

### 1. Visibility Model

**Decision:** Private/Internal/Public
**Rationale:**
- Simple dan clear
- Support berbagai use cases
- Easy to implement

### 2. Sharing Flow

**Decision:** Share dialog dengan visibility + roles + clone permission
**Rationale:**
- Flexible sharing controls
- Clear permissions
- Easy to understand

### 3. Cloning Flow

**Decision:** Dependency resolution during clone
**Rationale:**
- Ensure cloned templates work
- Handle dependencies automatically
- Better user experience

## Consequences

### Positive
- Flexible sharing model
- Dependency resolution
- Analytics tracking

### Negative
- Complexity dari visibility model
- Dependency resolution bisa lambat

### Neutral
- Uses existing BlueprintRepository untuk storage

## References

- RFC-0051: Marketplace & Templates
- SimplAI Marketplace: https://simplai.ai/docs/templates-and-marketplace/
