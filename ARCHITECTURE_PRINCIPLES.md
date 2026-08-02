<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English


### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `ARCHITECTURE_PRINCIPLES.md`
- Judul: Architecture Principles
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# ECP Architecture Principles

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for ARCHITECTURE_PRINCIPLES
<!-- DOCUMENT_METADATA_END -->


These are the foundational principles that govern all design and implementation decisions in Enal Cognitive Platform (ECP).
> Terjemahan Indonesia: These adalah foundational principles itu govern all design dan implementation decisions dalam Enal kognitif platform (ECP).

## 1. Platform Exists to Serve Applications


> **Every change to Kernel, Runtime, SDK, Studio, or Marketplace must be justified by a real application need.**

- No engine, abstraction, or module is added unless a reference application requires it.
- If no app needs a feature, the feature does not exist.
- Applications are first-class citizens; platform components are infrastructure.

## 2. No Shortcuts in Integration


> **Reference applications must use the full platform stack.**

If a reference app bypasses SDK, Runtime, Contracts, Marketplace, or Studio, that is a platform defectâ€”not an app workaround.
> Terjemahan Indonesia: If sebuah reference app bypasses SDK, Runtime, Contracts, Marketplace, or Studio, itu adalah sebuah platform defectâ€”not sebuah app workaround.

- SDK Agent â†’ Adaptive Runtime â†’ Cognitive Pipeline â†’ Plugins â†’ Artifact System â†’ Studio Trace
- Every component must be exercised by at least one reference application.

## 3. Kernel Stability

> **The kernel must remain small, stable, and predictable.**

- Kernel must stay under 5,000 lines of code.
- Kernel must have zero external dependencies beyond stdlib + pydantic.
- Kernel contracts are versioned and backward-compatible within major versions.
- Breaking changes require a 2-release grace period with migration guides.

## 4. Contract-First Development


> **All public interfaces are contracts.**

- Every module boundary is defined by a typed contract.
- Contracts are registered, versioned, and tested for compatibility.
- SDK, plugins, and external tools depend on contracts, not implementation details.

## 5. Observable by Default


> **Every execution leaves a trace.**

- All cognitive pipelines emit trace spans.
- All decisions record reasoning, confidence, and cost.
- All artifacts are versioned and auditable.
- Studio provides replay, diff, and comparison of runs.

## 6. Security by Design

> **Plugins are untrusted by default.**

- Plugins declare required permissions explicitly.
- Privileged plugins require manual approval.
- Sandbox execution for restricted/privileged plugins.
- No plugin gets more access than it needs.

## 7. Developer Experience is Product


> **If a developer cannot build an app in under 1 hour, the platform is not ready.**

- SDK must be pip-installable with clear decorators.
- Documentation must include end-to-end examples.
- Error messages must be actionable.
- Debugging must be possible without reading platform source code.

## 8. Testing is Quality Gate


> **No PR merges without passing the full quality gate.**

Quality gate includes:
> Terjemahan Indonesia: Kualitas gate includes:
1. Lint & format
2. Type check
3. Unit tests
4. Architecture boundary tests
5. Performance benchmarks
6. SDK compatibility
7. Plugin compatibility
8. Golden test suite

Any failure blocks merge.
> Terjemahan Indonesia: Setiap blok kegagalan digabungkan.

## 9. Measure by Outcomes, Not Artifacts


> **Progress is measured by what users can accomplish, not by how many files exist.**

Bad metrics:
> Terjemahan Indonesia: Metrik yang buruk:
- Number of files
- Number of agents
- Number of plugins
- Number of commits

Good metrics:
> Terjemahan Indonesia: Metrik yang bagus:
- Reference apps that run end-to-end
- Golden test pass rate
- Developer onboarding time
- Production deployment success rate

## 10. Human Governance Principle


> **No code, configuration, or architecture changes may be applied without explicit user approval.**

- Autonomous capabilities may analyze, propose, and prepare changes.
- Execution of changes requires explicit user approval.
- All proposals, diffs, test results, and approval records are preserved as artifacts.
- The platform never modifies itself without a human decision in the loop.

## 11. Continuous Learning


> **The platform improves from every execution.**

- Every run produces lessons learned.
- Benchmarks run on every change.
- Regression is detected within minutes.
- Meta-cognition optimizes pipeline selection over time.

---

## Decision Filter

Use this filter for every significant decision:
> Terjemahan Indonesia: Use ini filter untuk every significant decision:

```
1. Does a reference application need this?
   â†’ No: reject.
   â†’ Yes: continue.

2. Does it require kernel changes?
   â†’ Yes: propose an RFC.
   â†’ No: implement in runtime/plugin/apps.

3. Does it break any existing contract?
   â†’ Yes: deprecate first, migrate, then remove.
   â†’ No: proceed.

4. Does it respect Human Governance Principle?
   â†’ No: reject.
   â†’ Yes: continue.

5. Is it testable?
   â†’ No: refine until it is.
   â†’ Yes: add to golden test suite.

6. Can a developer discover and use it in <1 hour?
   â†’ No: improve DX before merging.
   â†’ Yes: merge.
```
