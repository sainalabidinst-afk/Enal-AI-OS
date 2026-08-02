<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `PRODUCT_VISION.md`
- Judul: Product Vision
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# ECP Product Vision

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for PRODUCT_VISION
<!-- DOCUMENT_METADATA_END -->

**Enal Cognitive Platform** is an AI Operating System. Users interact with a single conversational AI. Behind the scenes, ECP understands intent, selects the right Capability Pack, and orchestrates execution through a stable, frozen Core.

When given a goal, ECP breaks it into tasks, executes them through Workers, verifies results, and presents a single coherent outcomeâ€”all within one conversation. This is the execution model inspired by modern agentic AI systems such as Kimi: the user sees one AI, while internally the system coordinates many workers, tools, and capabilities to complete complex work.
> Terjemahan Indonesia: When given sebuah goal, ECP breaks it into tasks, executes them through Workers, verifies results, dan presents sebuah single coherent outcomeâ€”all within one conversation. ini adalah execution model inspired oleh modern agentic AI systems such as Kimi: user sees one AI, while internally sistem coordinates many workers, alat, dan kapabilitas untuk complete complex work.

**Motto: A stable core. Expert capabilities. One conversation.**

## Product Principles

- **One conversation, many experts.** The user sees one AI. Multiple domain experts work behind the same conversational interface.
- **Capability excellence over platform growth.** Success is measured by how well each Capability Pack solves real problems, not by how many architectural components exist.
- **Explainability over mystery.** Every decision, recommendation, and action must be traceable, auditable, and understandable.
- **Safety before automation.** The platform defaults to read-only analysis and explicit human approval before any irreversible action.
- **Extensibility without breaking compatibility.** Capability Packs integrate through stable contracts. No breaking changes without migration paths.
- **Stable Core, evolving Capability.** The Core is frozen. Capability Packs grow by gaining expertise, not by changing the platform.
- **Task execution is the product.** Users judge ECP by what it accomplishes, not by how many agents or workers it uses internally.

## What ECP Is

ECP is an **AI Operating System** that becomes an expert through Capability Packs. It is not a chatbot, not a wrapper, and not a framework that requires rebuilds for every new domain.
> Terjemahan Indonesia: ECP adalah sebuah AI sistem operasi itu becomes sebuah expert through kapabilitas Packs. It adalah not sebuah chatbot, not sebuah wrapper, dan not sebuah kerangka kerja itu requires rebuilds untuk every new domain.

It is designed for:
> Terjemahan Indonesia: It adalah dirancang untuk:
- **Users** who want one AI that understands multiple professional domains
- **Developers** who want to teach new expertise without rebuilding the platform
- **Organizations** that require auditable, explainable, and safe AI decisions

The Core is frozen. Capability Packs evolve.
> Terjemahan Indonesia: Core adalah frozen. kapabilitas Packs evolve.

## What ECP Is Not

- Not a chatbot framework
- Not a generic LLM wrapper
- Not a feature-complete platform built before anyone uses it
- Not a platform that keeps growing underneath the AI

ECP is built **through** Capability Packs, not **for** them.
> Terjemahan Indonesia: ECP adalah built through kapabilitas Packs, not untuk them.

## Execution Model

When a user gives a goal, ECP operates as:
> Terjemahan Indonesia: When sebuah user gives sebuah goal, ECP operates as:

```
One Conversation
      â†“
   One Goal
      â†“
  Many Tasks
      â†“
 Many Workers
      â†“
  One Result
```

The user never manages workers, selects capabilities, or configures execution.
The AI breaks the goal into tasks, executes them in parallel when possible, verifies results, and presents a single coherent outcome.
> Terjemahan Indonesia: User never manages workers, selects kapabilitas, or configures execution. AI breaks goal into tasks, executes them dalam parallel when possible, verifies results, dan presents sebuah single coherent outcome.

This is not "many agents." This is one AI that knows how to coordinate work internally.
> Terjemahan Indonesia: Ini adalah not "many agen." ini adalah one AI itu knows how untuk coordinate work internally.

---

## Capability Excellence Definition

Capability Excellence adalah kemampuan setiap Capability Pack untuk menyelesaikan masalah nyata secara konsisten, dapat dijelaskan, aman, dan terukur melalui benchmark sintetis maupun kasus nyata, tanpa memerlukan perubahan pada Core Platform.
> Terjemahan Indonesia: Kapabilitas Excellence adalah kemampuan setiap kapabilitas Pack untuk menyelesaikan masalah nyata secara konsisten, dapat dijelaskan, aman, dan terukur melalui benchmark sintetis maupun kasus nyata, tanpa memerlukan perubahan pada Core platform.

Semua peningkatan Capability harus lahir dari:
> Terjemahan Indonesia: Semua peningkatan kapabilitas harus lahir dari:
1. Penggunaan nyata yang terdokumentasi di `real_cases/`
2. Benchmark yang mengukur 6 dimensi: Accuracy, Completeness, Explainability, Safety, Efficiency, Consistency
3. Evaluasi yang objektif, bukan dugaan

## North Star Metric

> **How expert does each Capability Pack become in its domain?**

This is the only metric that matters for the next phase of ECP.
> Terjemahan Indonesia: Ini adalah only metric itu matters untuk next phase dari ECP.

## Capability Quality Metric

Quality is measured by benchmark performance, not checklist completion:
> Terjemahan Indonesia: Kualitas adalah measured oleh benchmark performance, not checklist completion:

| Capability Pack | Quality | Benchmark Target |
|-----------------|---------|------------------|
| Network Engineer | A | 100 real configs, â‰¥95% accuracy |
| Code Engineer | B+ | 100 repositories, â‰¥90% code quality |
| Research Assistant | B | 100 research questions, â‰¥85% citation accuracy |
| DevOps Assistant | B | 100 infrastructure scenarios, â‰¥85% correctness |
| Trading Analyst | Pending | 100 market scenarios, risk-adjusted returns |
| Self Development | A- | 10 real projects, â‰¥80% improvement acceptance |
