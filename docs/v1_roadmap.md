<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Strategic roadmap, Capability Pack lifecycle, and release timeline
<!-- DOCUMENT_METADATA_END -->

# ECP Governance Charter — v1.0.0-dev

> **Status:** This document has been restructured into focused strategic documents.
> It now serves as a landing page and index to the ECP documentation suite.

**Target Release:** Q3 2026
**Status:** In Development
**Goal:** ECP platform is complete. Next phase is Capability Excellence — making each Capability Pack genuinely expert in its domain.

---

## Core Philosophy

> **Core tidak lagi menjadi tempat berkembangnya fitur; Core menjadi platform yang stabil, sedangkan Capability Pack menjadi tempat inovasi.**

Prinsip ini adalah fondasi arsitektur ECP:

- **Core** dibekukan — stabil, backward-compatible, zero external dependencies selain stdlib + pydantic
- **Capability Pack** berevolusi — tempat inovasi, knowledge expansion, dan domain expertise
- **Governance** aktif — semua perubahan diatur oleh ADR, Capability First Rule, dan Architecture Freeze Policy

---

## Governance Charter

Dokumen ini adalah **dokumen konstitusi (governance charter)** proyek ECP. Artinya:

- Semua RFC harus konsisten dengan dokumen ini.
- Semua ADR harus merujuk dokumen ini.
- Semua Capability Pack harus memenuhi aturan di dokumen ini sebelum dianggap siap rilis.
- CI/CD dapat menambahkan pemeriksaan agar perubahan yang melanggar aturan governance (misalnya perubahan Core tanpa ADR) gagal sebelum merge.

---

## Document Index

Dokumen ini telah dipecah menjadi 5 dokumen strategis berikut:

| Document | Purpose | SSOT For |
|----------|---------|----------|
| `docs/GOVERNANCE_CHARTER.md` | Vision, philosophy, constitutional rules | Visi, filosofi, aturan konstitusional |
| `docs/GOVERNANCE.md` | Operational rules — ADR, Capability First, Architecture Freeze, enforcement | Aturan operasional |
| `docs/RELEASE_CRITERIA.md` | Release conditions, DoD, quality gates | Syarat rilis, DoD, quality gates |
| `docs/CAPABILITY_STRATEGY.md` | Capability Pack profiles, maturity, lifecycle | Profil, kematangan, siklus hidup Capability Pack |
| `docs/ROADMAP.md` | Timeline, release targets, long-term vision | Timeline, target rilis, visi jangka panjang |
| `docs/DOCUMENT_STRUCTURE.md` | Fungsi dan SSOT setiap dokumen strategis | Document mapping |

---

## Quick Reference

### Success Criteria (v1.0.0-dev)

1. ✅ **13 Capability Packs** exist and are registered in Capability Graph
2. ✅ **Golden Test Suite** passes with ≥80% pass rate
3. ✅ **CI/CD Pipeline** blocks merges on any failure
4. ✅ **Documentation** covers getting started, SDK, contracts, and Architecture
5. ✅ **No Framework Trap** — Core remains stable while Capability Packs evolve
6. ✅ **Architecture Governance** active: Core is frozen, Capability First Rule enforced, all changes require ADR when impacting multiple packs

### Capability Packs Overview

| Capability | Category | Quality Target |
|------------|----------|----------------|
| Network Engineer | Networking | A (≥90) |
| Code Engineer | Development | A- (≥85) |
| Research Assistant | Research | A- (≥85) |
| DevOps Assistant | DevOps | B+ (≥80) |
| Trading Analyst | Finance | B+ (≥80) — Certification Pending |
| Self Development | Platform | A (≥90) |
| Decision Intelligence | Platform — Shared Reasoning | A (91.25%) — RFC-0007 |
| System Architect | Architecture | A (≥90) — RFC-0011 |
| Security Engineer | Security | A- (≥85) — RFC-0008 |
| Data Engineer | Data | A- (≥85) — RFC-0009 |
| Database Engineer | Database | A- (≥85) — RFC-0010 |
| QA Engineer | Quality Assurance | A (≥90) — RFC-0012 |
| Business Analyst | Business Analysis | A- (≥85) — RFC-0013 |

### Capability Maturity Model

| Level | Label | Description |
|-------|-------|-------------|
| 1 | **Experimental** | Concept prototype, not production-ready |
| 2 | **Functional** | Works for basic scenarios, known limitations |
| 3 | **Production Ready** | Passes benchmarks, documented, stable |
| 4 | **Domain Expert** | Deep knowledge, multi-vendor, multi-domain |
| 5 | **Certified** | Audited, benchmarked, reference implementation |
| 6 | **Reference Capability** | Industry benchmark for the domain |

### Capability Lifecycle

```
Proposal → RFC → Prototype → Experimental → Stable → Certified → Maintenance → Deprecated
```

### Release Timeline

| Release | Target | Focus |
|---------|--------|-------|
| v1.0.0-dev | Q3 2026 | Platform complete, Architecture Governance active |
| v1.0.0 | Q4 2026 | Developer Preview: all packs certified |
| v1.1.0 | Q1 2027 | Capability Excellence: raise all packs one grade |
| v1.2.0 | Q2 2027 | Community Ecosystem: Marketplace |
| v1.3.0 | Q3 2027 | Enterprise: governance, multi-tenant, SLA |

---

## Related Documents

| Document | Location |
|----------|----------|
| Architecture Decisions (ADR) | `ARCHITECTURE_DECISIONS.md` |
| Product Contract | `docs/PRODUCT_CONTRACT.md` |
| Capability Guide (detailed specs) | `docs/CAPABILITY_GUIDE.md` |
| Quality Gate Status | `docs/QUALITY_GATE.md` |
| RFC Process | `docs/rfcs/README.md` |
| Architecture Overview | `docs/architecture.md` |
| Baseline Freeze | `docs/baseline_freeze.md` |
