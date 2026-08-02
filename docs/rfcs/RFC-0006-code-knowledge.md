<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/rfcs/RFC-0006-code-knowledge.md`
- Judul: Rfc 0006 Code Knowledge
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# RFC: Code Knowledge Expansion

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** RFC for RFC-0006-code-knowledge
<!-- DOCUMENT_METADATA_END -->

**Status:** Planned
**Target:** Capability Excellence phase
**Capability Pack:** Code Engineer

## Summary

Expand Code Engineer knowledge depth across software design principles, architecture patterns, and secure coding practices.
> Terjemahan Indonesia: Expand Code Engineer knowledge depth across software design principles, arsitektur patterns, dan secure coding practices.

## Knowledge Domains

### Clean Architecture
- Layers: entities, use cases, interface adapters, frameworks
- Dependency rule
- Boundaries and interfaces
- Testing isolation through architecture
- When to apply vs over-engineering

### DDD (Domain-Driven Design)
- Bounded contexts
- Entities, Value Objects, Aggregates
- Domain events
- Repository and specification patterns
- Anti-corruption layers
- Ubiquitous language

### SOLID
- Single Responsibility
- Open/Closed
- Liskov Substitution
- Interface Segregation
- Dependency Inversion
- Practical examples in Python/TypeScript

### CQRS
- Command vs Query separation
- Write model and read model
- Event sourcing integration
- Consistency models
- When to use CQRS

### Event Sourcing
- Event store concepts
- Event schema design
- Replay and projection
- Snapshotting
- Integration with CQRS

### Secure Coding
- OWASP Top 10 mapping
- Injection prevention
- Authentication and authorization patterns
- Secrets management
- Secure dependency handling

## Implementation Approach

All knowledge is added to the Code Capability Pack domain engine. No Core changes are required.
> Terjemahan Indonesia: All knowledge adalah added untuk Code kapabilitas Pack domain engine. No Core changes adalah required.

## Success Criteria

- Each knowledge domain is represented in code generation, review, and refactoring logic
- Golden tests cover new patterns
- Benchmark scores for code quality and explainability improve

## References

- RFC-0006: Code Knowledge Base
- CAPABILITY_GUIDE.md â€” Code Engineer section
