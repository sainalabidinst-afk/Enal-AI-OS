# ECP Architecture Principles

These are the foundational principles that govern all design and implementation decisions in Enal Cognitive Platform (ECP).

## 1. Platform Exists to Serve Applications

> **Every change to Kernel, Runtime, SDK, Studio, or Marketplace must be justified by a real application need.**

- No engine, abstraction, or module is added unless a reference application requires it.
- If no app needs a feature, the feature does not exist.
- Applications are first-class citizens; platform components are infrastructure.

## 2. No Shortcuts in Integration

> **Reference applications must use the full platform stack.**

If a reference app bypasses SDK, Runtime, Contracts, Marketplace, or Studio, that is a platform defect—not an app workaround.

- SDK Agent → Adaptive Runtime → Cognitive Pipeline → Plugins → Artifact System → Studio Trace
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
1. Lint & format
2. Type check
3. Unit tests
4. Architecture boundary tests
5. Performance benchmarks
6. SDK compatibility
7. Plugin compatibility
8. Golden test suite

Any failure blocks merge.

## 9. Measure by Outcomes, Not Artifacts

> **Progress is measured by what users can accomplish, not by how many files exist.**

Bad metrics:
- Number of files
- Number of agents
- Number of plugins
- Number of commits

Good metrics:
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

```
1. Does a reference application need this?
   → No: reject.
   → Yes: continue.

2. Does it require kernel changes?
   → Yes: propose an RFC.
   → No: implement in runtime/plugin/apps.

3. Does it break any existing contract?
   → Yes: deprecate first, migrate, then remove.
   → No: proceed.

4. Does it respect Human Governance Principle?
   → No: reject.
   → Yes: continue.

5. Is it testable?
   → No: refine until it is.
   → Yes: add to golden test suite.

6. Can a developer discover and use it in <1 hour?
   → No: improve DX before merging.
   → Yes: merge.
```
