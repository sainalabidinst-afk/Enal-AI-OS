<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English


### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/adr/ADR-003-universal-ast-design.md`
- Judul: Adr 003 Universal Ast Design
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# ADR-003: Universal AST Design


**Status:** ✅ Accepted  
**Date:** 2024  
**Deciders:** Chief Architect, Engineering Team

---

## Context

Network configuration analysis must support multiple vendors (Cisco, MikroTik, Fortinet, Juniper, etc.). Each vendor has different configuration syntax, data models, and semantics.
> Terjemahan Indonesia: Network konfigurasi analysis must dukungan multiple vendors (Cisco, MikroTik, Fortinet, Juniper, etc.). Each vendor memiliki different konfigurasi syntax, data models, dan semantics.

Without a common representation, every analysis feature (validation, refactoring, security audit) must be implemented separately for each vendor.
> Terjemahan Indonesia: Without sebuah common representation, every analysis feature (validation, refactoring, keamanan audit) must menjadi implemented separately untuk each vendor.

---

## Decision

Design a **Universal AST (Abstract Syntax Tree)** that models network configuration in a vendor-agnostic way.
> Terjemahan Indonesia: Design sebuah Universal AST (Abstract Syntax Tree) itu models network konfigurasi dalam sebuah vendor-agnostic way.

### Key Components

- `UniversalFirewallRule` — Normalized firewall rule across vendors
- `UniversalNATRule` — Normalized NAT rule across vendors
- `UniversalBGP` — Normalized BGP configuration
- `UniversalInterface` — Normalized interface configuration
- Vendor-specific parsers in `apps/network_engineer/vendor/` map to Universal AST

### Design Principle

Each vendor parser translates vendor-specific syntax into Universal AST models. Downstream consumers (analyzer, enricher, security audit) operate only on Universal AST, never on vendor-specific formats.
> Terjemahan Indonesia: Each vendor parser translates vendor-specific syntax into Universal AST models. Downstream consumers (analyzer, enricher, keamanan audit) operate only pada Universal AST, never pada vendor-specific formats.

---

## Alternatives Considered


| Alternative | Reason Rejected |
|-------------|-----------------|
| Vendor-specific analysis per feature | N * M complexity (vendors × features), not scalable |
| Common intermediate format (JSON/YAML) | Loses type safety and structural validation |
| Abstract base class per feature | Still requires per-vendor implementation for each feature |

---

## Consequences

- **Positive:** Linear (N + M) complexity instead of (N × M)
- **Positive:** New vendor support adds N parser, M features work immediately
- **Positive:** Strong typing via dataclasses and Pydantic
- **Negative:** Universal models must be kept generic enough for all vendors
- **Negative:** Vendor-specific nuances may be lost in normalization
- **Negative:** Parser maintenance required for each vendor firmware update

---

## Compliance

All network configuration analysis MUST use Universal AST models. Direct access to vendor-specific structures by analysis code is prohibited.
> Terjemahan Indonesia: All network konfigurasi analysis MUST use Universal AST models. Direct access untuk vendor-specific structures oleh analysis code adalah prohibited.
