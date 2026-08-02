<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/GOVERNANCE_CHARTER.md`
- Judul: Governance Charter
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Project vision, principles, and constitutional rules
<!-- DOCUMENT_METADATA_END -->

# ECP Governance Charter

**Version:** 1.0.0
**Status:** Ratified
**Effective:** 2026-08-01
**Authority:** Chief Architect + Chief Product Officer
**Document Type:** Constitution / Governance Charter

---

## Preamble

This Charter is the supreme strategic and technical governance document of the Enal Cognitive Platform (ECP). It defines the product philosophy, the fundamental principles, and the decision-making rules that all RFCs, ADRs, Capability Packs, and release activities must follow.
> Terjemahan Indonesia: Ini Charter adalah supreme strategic dan technical tata kelola dokumen dari Enal kognitif platform (ECP). It defines product philosophy, fundamental principles, dan decision-making rules itu all RFCs, ADRs, kapabilitas Packs, dan rilis activities must follow.

Any document, RFC, ADR, implementation, or release that contradicts this Charter is invalid until amended through the prescribed amendment process.
> Terjemahan Indonesia: Any dokumen, RFC, ADR, implementation, or rilis itu contradicts ini Charter adalah invalid until amended through prescribed amendment process.

---

## 1. North Star Vision

> **Platform adalah enabler. Tujuan akhirnya adalah AI Trading yang membuat keputusan investasi cerdas secara otonom.**

ECP dibangun sebagai platform AI eksekusi yang stabil. **Trading Analyst** adalah Capability Pack utama yang menjadi tujuan akhir. Semua kemampuan lain â€” Network, Code, Research, DevOps, Self Development, Decision Intelligence, Security, Data, dan yang akan datang â€” adalah enabler yang memperkuat ekosistem menuju visi tersebut.
> Terjemahan Indonesia: ECP dibangun sebagai platform AI eksekusi yang stabil. Trading Analyst adalah kapabilitas Pack utama yang menjadi tujuan akhir. Semua kemampuan lain â€” Network, Code, Research, DevOps, Self Development, Decision Intelligence, keamanan, Data, dan yang akan datang â€” adalah enabler yang memperkuat ekosistem menuju visi tersebut.

Prinsip ini memandu setiap keputusan strategis:
> Terjemahan Indonesia: Prinsip ini memandu setiap keputusan strategi:
- Setiap Capability Pack baru harus dievaluasi: *"Apakah ini memperkuat Trading Analyst atau ekosistem yang mendukungnya?"*
- Kualitas Trading Analyst adalah prioritas tertinggi â€” pack ini harus menjadi yang paling matang, paling akurat, dan paling dapat diandalkan.
- Platform tidak akan melebar ke domain yang tidak relevan dengan visi ini.

---

## 2. Product Philosophy

> **Core is not the place where features grow. Core is the stable platform. Capability Packs are the place where innovation happens.**

This is the single most important architectural principle of ECP.
> Terjemahan Indonesia: Ini adalah single most important architectural principle dari ECP.

- **Core** is frozen, small, stable, and predictable. It provides contracts, execution, and governance.
- **Capability Packs** are the vehicle for all domain evolution, knowledge expansion, and feature growth.
- **No Core change** may be made to serve a single Capability Pack. Core evolves only when multiple packs prove a shared need.

### Why This Matters

- Keeps architecture stable and prevents feature-driven churn of the foundation.
- Enables a marketplace of internal, community, and third-party packs without version conflicts.
- Allows each Capability Pack to evolve, be tested, and be released independently.
- Shifts the development focus from platform construction to **Capability Excellence**.

---

## 3. Core Principles

| # | Principle | Meaning |
|---|-----------|---------|
| 1 | **Core Frozen** | Core contracts, Kernel, and Core Pipeline are stable. Changes require Architecture Freeze Policy approval (see `GOVERNANCE.md`). |
| 2 | **Capability First** | No Core change is allowed to improve a single Capability Pack. Changes must stay inside the pack. |
| 3 | **Cross-Capability Proof** | Core changes require proof from at least two Capability Packs and an approved ADR. |
| 4 | **Use Case Before Engine** | No new engine, module, or abstraction without at least two Capability Packs needing it, a golden test case, and architecture documentation. |
| 5 | **Human Approval** | No code, configuration, or architecture change may be applied without explicit user approval. (ADR-005) |
| 6 | **Outcome Over Mechanism** | Users request outcomes, not mechanisms. Internal machinery is never exposed. (ADR-009, ADR-013) |
| 7 | **Measure by Outcomes** | Progress is measured by benchmark scores, real-world case velocity, and user outcomes â€” not by artifact count. |
| 8 | **Continuous Learning** | Real cases â†’ Review â†’ Knowledge Update â†’ Benchmark. The platform improves from every execution. |

---

## 4. Documents Governed by This Charter

| Document | Purpose | Stability |
|----------|---------|-----------|
| `GOVERNANCE.md` | Operational rules: Capability First, No New Engines, Architecture Freeze Policy, Kernel Stability, ADR process, CI/CD enforcement, Capability Changelog | Stable, changes via amendment |
| `RELEASE_CRITERIA.md` | Release conditions, quality gates, Definition of Done, certification | Changes per release |
| `CAPABILITY_STRATEGY.md` | Capability Pack strategy, maturity model, quality grades, lifecycle, benchmarks, knowledge expansion | Evolves with pack development |
| `ROADMAP.md` | Release timeline, 12-month plan, 5-year free roadmap, model strategy | Changes as plans evolve |
| `DOCUMENT_STRUCTURE.md` | Role of each document, single source of truth (SSOT), who updates what | Stable |

---

## 5. Capability Maturity & Quality Grade

Maturity and quality are **two separate concepts**:
> Terjemahan Indonesia: Maturity dan kualitas adalah two separate concepts:

- **Capability Maturity Model** describes the lifecycle maturity of a Capability Pack (Level 1â€“6). See `CAPABILITY_STRATEGY.md`.
- **Quality Grades** (A, A-, B+, â€¦) describe the **current benchmark result** of a pack. They are outcomes of evaluation, not maturity levels.

A pack may be mature (Stable/Certified) but still working to raise its quality grade.
> Terjemahan Indonesia: Sebuah pack may menjadi mature (Stable/Certified) but still working untuk raise its kualitas grade.

---

## 6. Governance Obligations

Every RFC, ADR, Capability Pack, and release must:
> Terjemahan Indonesia: Every RFC, ADR, kapabilitas Pack, dan rilis must:

1. **Be consistent with this Charter.** Contradiction = rejection.
2. **Respect the Core Freeze.** Core changes require Architecture Freeze Policy approval.
3. **Provide cross-capability proof** for any Core or shared-layer change (minimum 2 packs).
4. **Define a benchmark** and a real-world case directory before being considered for release.
5. **Pass all governance checks in CI/CD.** Changes that violate governance (e.g., Core change without ADR) must fail before merge.

---

## 7. Amendment Process

This Charter is a constitution. Amendments are exceptional and require:
> Terjemahan Indonesia: Ini Charter adalah sebuah constitution. Amendments adalah exceptional dan require:

1. **Proposal** by Chief Architect or Chief Product Officer, with:
   - Rationale
   - Impact analysis
   - Migration plan (if applicable)
> Terjemahan Indonesia: Dasar Pemikiran Analisa dampak Rencana migrasi (jika ada)
2. **Review period** of at least 7 days for community/team feedback.
3. **Ratification** by:
   - Chief Architect approval
   - Chief Product Officer approval
> Terjemahan Indonesia: Persetujuan Kepala Arsitek Persetujuan Chief Product Officer
4. **Publication** â€” updated Charter version recorded, superseded version archived.

In case of conflict with any other document, **this Charter prevails**.
> Terjemahan Indonesia: Dalam case dari conflict dengan any other dokumen, ini Charter prevails.

---

## 8. Definition of Architecture Governance Active

Architecture Governance is considered **active** when all of the following are true:
> Terjemahan Indonesia: Arsitektur tata kelola adalah considered active when all dari following adalah true:

- [ ] Core is frozen and protected by the Architecture Freeze Policy.
- [ ] Capability First Rule is enforced in code review and CI/CD.
- [ ] Every Core change has an approved ADR with cross-capability proof.
- [ ] Every Capability Pack has a benchmark and a `real_cases/` directory.
- [ ] RFCs and ADRs reference this Charter.
- [ ] CI/CD blocks governance violations before merge.

---

## 9. Approval

| Role | Status | Date |
|------|--------|------|
| Chief Architect | Approved | 2026-08-01 |
| Chief Product Officer | Approved | 2026-08-01 |

**Next Review:** 2026-11-01 or upon any amendment.
