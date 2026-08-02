<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary

Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/rfcs/README.md`
- Judul: RFC Process
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** RFC process, RFC index, and RFC lifecycle
<!-- DOCUMENT_METADATA_END -->

# RFC Process

This document describes the Request for Comments (RFC) process for ECP.
> Terjemahan Indonesia: Ini dokumen describes Request untuk Comments (RFC) process untuk ECP.

## Purpose

The RFC process ensures that significant changes to ECP are well-designed, reviewed, and documented before implementation.
> Terjemahan Indonesia: RFC process ensures itu significant changes untuk ECP adalah well-dirancang, reviewed, dan documented before implementation.

## When to Write an RFC

Write an RFC for:
> Terjemahan Indonesia: Write sebuah RFC untuk:
- New features or major functionality
- Changes to existing contracts/APIs
- Architectural changes
- Breaking changes
- New plugins or tools that affect Core behavior

## RFC Template

```markdown
# RFC-XXXX: Title

## Summary
One-paragraph summary of the proposal.

## Motivation
Why should we do this? What problem does it solve?

## Detailed Design
Technical details of the proposal.

## Alternatives Considered
What other approaches were considered?

## Compatibility
How does this affect backward compatibility?

## Security Considerations
Any security implications?

## Testing Strategy
How will this be tested?

## Timeline
Proposed timeline for implementation.

## References
Related RFCs, documentation, etc.
```

## RFC Process

1. **Draft:** Author creates RFC in `docs/rfcs/`
2. **Review:** Community reviews for 7 days
3. **Revision:** Author addresses feedback
4. **Acceptance:** Core team accepts or rejects
5. **Implementation:** Author implements with guidance
6. **Integration:** Merged into main branch

## Current RFCs

- RFC-0001: Stable Contracts (Accepted)
- RFC-0002: Plugin Manifest Format (Accepted)
- RFC-0003: SDK Decorators (Accepted)
- RFC-0004: Event Bus Protocol (Accepted)
- RFC-0005: Memory Interface (Accepted)
- RFC-0006: Capability Pack Registry (Accepted)
- RFC-0007: Decision Intelligence (Accepted)
- RFC-0008: Security Engineer (Implemented)
- RFC-0009: Data Engineer (Implemented)
- RFC-0010: Database Engineer (Implemented)
- RFC-0011: System Architect (Implemented)
- RFC-0012: QA Engineer (Implemented)
- RFC-0013: Business Analyst (Implemented)

## RFC Index

| RFC ID | Title | Status | Capability Pack |
|--------|-------|--------|-----------------|
| RFC-0001 | Stable Contracts | Accepted | Core |
| RFC-0002 | Plugin Manifest Format | Accepted | Core |
| RFC-0003 | SDK Decorators | Accepted | Core |
| RFC-0004 | Event Bus Protocol | Accepted | Core |
| RFC-0005 | Memory Interface | Accepted | Core |
| RFC-0006 | Capability Pack Registry | Accepted | Core |
| RFC-0007 | Decision Intelligence | Accepted | Decision Intelligence |
| RFC-0008 | Security Engineer | Implemented | Security Engineer |
| RFC-0009 | Data Engineer | Implemented | Data Engineer |
| RFC-0010 | Database Engineer | Implemented | Database Engineer |
| RFC-0011 | System Architect | Implemented | System Architect |
| RFC-0012 | QA Engineer | Implemented | QA Engineer |
| RFC-0013 | Business Analyst | Implemented | Business Analyst |
