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

Dokumen `v1_roadmap.md` telah dipecah menjadi 5 dokumen strategis berikut:

| Document | Purpose | SSOT For |
|----------|---------|----------|
| `docs/GOVERNANCE_CHARTER.md` | Dokumen induk — visi, prinsip inti, filosofi, aturan konstitusional | Vision, philosophy, constitutional rules |
| `docs/GOVERNANCE.md` | Aturan operasional — ADR, Capability First, Architecture Freeze, enforcement | Operational rules |
| `docs/RELEASE_CRITERIA.md` | Syarat rilis — quality gates, Definition of Done, benchmark targets | Release conditions, DoD, quality gates |
| `docs/CAPABILITY_STRATEGY.md` | Strategi Capability Pack — maturity model, lifecycle, profil pack, knowledge expansion | Capability Pack profiles, maturity, lifecycle |
| `docs/ROADMAP.md` | Timeline dan target versi — jadwal rilis, 5-year roadmap, model strategy | Timeline, release targets, long-term vision |
| `docs/DOCUMENT_STRUCTURE.md` | Fungsi dan SSOT setiap dokumen strategis | Document mapping |

---

## Quick Reference

### Success Criteria (v1.0.0-dev)

1. ✅ **6 Capability Packs** exist and are registered in Capability Graph
2. ✅ **Golden Test Suite** passes with ≥80% pass rate
3. ✅ **CI/CD Pipeline** blocks merges on any failure
4. ✅ **Documentation** covers getting started, SDK, contracts, and architecture
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
