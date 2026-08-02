# RFC: Perluasan Pengetahuan Code

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Terakhir Diverifikasi:** 2026-08-02
**Versi:** 1.0.0
**Status:** Aktif
**SSOT:** RFC untuk RFC-0006-code-knowledge
<!-- DOCUMENT_METADATA_END -->

**Status:** Direncanakan
**Target:** Fase Capability Excellence
**Capability Pack:** Code Engineer

## Ringkasan

Memperluas kedalaman pengetahuan Code Engineer di seluruh prinsip desain perangkat lunak, pola arsitektur, dan praktik secure coding.

## Domain Pengetahuan

### Clean Architecture
- Layer: entities, use cases, interface adapters, frameworks
- Dependency rule
- Boundaries dan interfaces
- Isolasi testing melalui arsitektur
- Kapan diterapkan vs over-engineering

### DDD (Domain-Driven Design)
- Bounded contexts
- Entities, Value Objects, Aggregates
- Domain events
- Pola repository dan specification
- Anti-corruption layers
- Ubiquitous language

### SOLID
- Single Responsibility
- Open/Closed
- Liskov Substitution
- Interface Segregation
- Dependency Inversion
- Contoh praktis di Python/TypeScript

### CQRS
- Pemisahan Command vs Query
- Write model dan read model
- Integrasi event sourcing
- Model konsistensi
- Kapan menggunakan CQRS

### Event Sourcing
- Konsep event store
- Desain event schema
- Replay dan projection
- Snapshotting
- Integrasi dengan CQRS

### Secure Coding
- Pemetaan OWASP Top 10
- Pencegahan injection
- Pola authentication dan authorization
- Manajemen secrets
- Penanganan dependensi yang aman

## Pendekatan Implementasi

Semua pengetahuan ditambahkan ke domain engine Code Capability Pack. Tidak ada perubahan Core yang diperlukan.

## Kriteria Keberhasilan

- Setiap domain pengetahuan terwakili dalam logika generasi kode, review, dan refactoring
- Golden test mencakup pola baru
- Skor benchmark untuk kualitas kode dan explainability meningkat

## Referensi

- RFC-0006: Code Knowledge Base
- CAPABILITY_GUIDE.md — bagian Code Engineer

