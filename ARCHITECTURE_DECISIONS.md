<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary

Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `ARCHITECTURE_DECISIONS.md`
- Judul: Architecture Decisions
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Architecture Decision Records (ADR) and architecture governance
<!-- DOCUMENT_METADATA_END -->

# Architecture Decisions

This document records architecture decisions that are considered stable and must not be changed without formal review.
Each decision is identified by an Architecture Decision Record (ADR) and is treated as part of Enal Cognitive Platform's technical constitution.
> Terjemahan Indonesia: Ini dokumen records arsitektur decisions itu adalah considered stable dan must not menjadi changed without formal review. Each decision adalah identified oleh sebuah arsitektur Decision Record (ADR) dan adalah treated as part dari Enal kognitif platform's technical constitution.

Contributors must not bypass these decisions via shortcuts, new dependencies, or layer violations.
If a decision must change, the proposer must submit a new ADR with impact analysis and approval from the project's architecture authority.
> Terjemahan Indonesia: Contributors must not bypass these decisions via shortcuts, new dependencies, or layer violations. If sebuah decision must change, proposer must submit sebuah new ADR dengan impact analysis dan approval dari proyek's arsitektur authority.

---

## Governance Principle: Two Equal Architectures

Enal AI OS is governed by two architectures of equal importance:
> Terjemahan Indonesia: Enal AI OS adalah governed oleh two architectures dari equal importance:

1. **Technical Architecture** — represented by ADR-001 through ADR-008
2. **Experience Architecture** — represented by ADR-009 through ADR-012 and `docs/UX_DESIGN.md`

Both are frozen. Both are binding. Neither may be violated without an approved ADR.
> Terjemahan Indonesia: Both adalah frozen. Both adalah binding. Neither may menjadi violated without sebuah approved ADR.

Technical Architecture ensures the platform remains stable, maintainable, and extensible.
Experience Architecture ensures users interact with one AI through one conversation, without exposure to internal mechanisms.
> Terjemahan Indonesia: Technical arsitektur ensures platform remains stable, maintainable, dan extensible. Experience arsitektur ensures users interact dengan one AI through one conversation, without exposure untuk internal mechanisms.

A change that violates either architecture is a defect, regardless of its technical merit.
> Terjemahan Indonesia: Sebuah change itu violates either arsitektur adalah sebuah defect, regardless dari its technical merit.

---

## Feature Acceptance Rule

Every new feature must answer these three questions before implementation:
> Terjemahan Indonesia: Setiap fitur baru harus menjawab tiga pertanyaan berikut sebelum diterapkan:

1. Which Capability improves?
   - If no Capability improves: do not build.
> Terjemahan Indonesia: If no kapabilitas improves: do not membangun.

2. Which Journey becomes better?
   - If no Journey becomes better: do not build.
> Terjemahan Indonesia: If no journey becomes better: do not membangun.

3. Which Benchmark increases?
   - If no Benchmark increases: do not build.
> Terjemahan Indonesia: If no benchmark increases: do not membangun.

If all three answers are "yes", implementation may proceed.
This rule prevents feature creep and keeps development aligned with product value, not architectural novelty.
> Terjemahan Indonesia: If all three answers adalah "yes", implementation may proceed. ini rule prevents feature creep dan keeps development aligned dengan product value, not architectural novelty.

---

## ADR-001: Core Pipeline Freeze

**Status:** Frozen
**Effective:** 2026-07-10

The Core Pipeline must remain small, stable, and predictable.
> Terjemahan Indonesia: Core jalur must remain small, stable, dan predictable.

- Core must stay under 5,000 lines of code.
- Core must have zero external dependencies beyond stdlib + pydantic.
- Core contracts are versioned and backward-compatible within major versions.
- Breaking changes require a 2-release grace period with migration guides.

**Rationale:**
A growing Core becomes a maintenance bottleneck and reduces ECP's ability to evolve Capability Packs independently.
Freezing Core size and dependencies forces new work into Capability Packs, preserving Core stability.
> Terjemahan Indonesia: Sebuah growing Core becomes sebuah maintenance bottleneck dan reduces ECP's ability untuk evolve kapabilitas Packs independently. Freezing Core size dan dependencies forces new work into kapabilitas Packs, preserving Core stability.

---

## ADR-002: Capability Pack Independence

**Status:** Frozen
**Effective:** 2026-07-10

Capability Packs must not import other Capability Packs directly.
> Terjemahan Indonesia: Kapabilitas Packs must not import other kapabilitas Packs directly.

Communication between Capability Packs must flow through:
> Terjemahan Indonesia: Communication between kapabilitas Packs must flow through:

1. Task / Intent definition
2. Execution Runtime
3. Shared contracts only

Example of forbidden pattern:
> Terjemahan Indonesia: Example dari forbidden pattern:

```python
# FORBIDDEN
from apps.trading_analyst import engine as trading_engine
trading_engine.analyze(...)
```

Example of allowed pattern:
> Terjemahan Indonesia: Example dari allowed pattern:

```python
# ALLOWED
task = {
    "domain": "research",
    "intent": "Analyze market sentiment for AAPL",
}
result = await execution_runtime.execute(task)
```

**Rationale:**
Direct imports create tight coupling, hidden dependencies, and circular import risks.
Independence allows Capability Packs to be developed, tested, and deployed without coordinating changes across packs.
> Terjemahan Indonesia: Direct imports membuat tight coupling, hidden dependencies, dan circular import risks. Independence memungkinkan kapabilitas Packs untuk menjadi developed, tested, dan deployed without coordinating changes across packs.

---

## ADR-003: Worker = Adapter Only

**Status:** Frozen
**Effective:** 2026-07-10

A Worker is an adapter. A Worker does not own business logic.
> Terjemahan Indonesia: Sebuah Worker adalah sebuah adapter. sebuah Worker does not own business logic.

Business logic belongs to the Domain Engine inside the Capability Pack.
> Terjemahan Indonesia: Business logic belongs untuk Domain Engine inside kapabilitas Pack.

Responsibilities:
> Terjemahan Indonesia: Tanggung jawab:
- Worker: translates subtask into Capability Pack call, returns result
- Domain Engine: owns analysis, generation, validation, and domain-specific logic

Forbidden pattern:
> Terjemahan Indonesia: Pola terlarang:

```python
# FORBIDDEN - Worker owning business logic
class NetworkWorker:
    def analyze_firewall(self, config):
        # 200 lines of firewall analysis logic here
        ...
```

Required pattern:
> Terjemahan Indonesia: Pola yang diperlukan:

```python
# ALLOWED - Worker delegates to Domain Engine
class NetworkWorker:
    async def execute(self, subtask, context):
        return await self._app.engine.analyze(config)
```

**Rationale:**
Keeping business logic in Domain Engines preserves testability, reusability, and separation of concerns.
Workers remain thin adapters that can be replaced or extended without changing domain logic.
> Terjemahan Indonesia: Keeping business logic dalam Domain Engines preserves testability, reusability, dan separation dari concerns. Workers remain thin adapters itu dapat menjadi replaced or extended without changing domain logic.

---

## ADR-004: Domain Engine Owns Business Logic

**Status:** Frozen
**Effective:** 2026-07-10

All business logic for a Capability Pack resides in its Domain Engine.
> Terjemahan Indonesia: All business logic untuk sebuah kapabilitas Pack resides dalam its Domain Engine.

- Domain Engine: analysis, generation, validation, simulation, recommendation
- Worker: adapter only (see ADR-003)
- Conversation Layer: context, history, streaming only

A Domain Engine may not:
> Terjemahan Indonesia: Sebuah Domain Engine may not:
- Import other Capability Pack engines directly
- Modify Core contracts
- Bypass Execution Runtime for cross-pack communication

**Rationale:**
Centralizing business logic in Domain Engines makes each Capability Pack self-contained and independently testable.
This is the architectural boundary that protects Core from domain-specific change.
> Terjemahan Indonesia: Centralizing business logic dalam Domain Engines makes each kapabilitas Pack self-contained dan independently testable. ini adalah architectural boundary itu protects Core dari domain-specific change.

---

## ADR-005: Human Approval Required

**Status:** Frozen
**Effective:** 2026-07-10

No code, configuration, or architecture changes may be applied without explicit user approval.
> Terjemahan Indonesia: No code, konfigurasi, or arsitektur changes may menjadi applied without explicit user approval.

- Autonomous capabilities may analyze, propose, and prepare changes.
- Execution of changes requires explicit user approval.
- All proposals, diffs, test results, and approval records are preserved as artifacts.
- The platform never modifies itself without a human decision in the loop.

Implementation rule:
> Terjemahan Indonesia: Aturan implementasi:
- Approval step must come before Apply step in any change workflow.
- Approval records must be immutable once created.

**Rationale:**
This principle is non-negotiable for user trust, auditability, and safe AI operation.
It is the governance mechanism that allows ECP to have autonomous capabilities without becoming autonomous in decision-making.
> Terjemahan Indonesia: Ini principle adalah non-negotiable untuk user trust, auditability, dan safe AI operation. It adalah tata kelola mechanism itu memungkinkan ECP untuk memiliki autonomous kapabilitas without becoming autonomous dalam decision-making.

---

## ADR-006: Capability Contract v1 Frozen

**Status:** Frozen
**Effective:** 2026-07-10

Capability Contract v1 is the stable schema for all Capability Packs.
> Terjemahan Indonesia: Kapabilitas Contract v1 adalah stable schema untuk all kapabilitas Packs.

Contract elements:
> Terjemahan Indonesia: Elemen kontrak:
- CapabilityNode: capability_id, name, description, required_skills, dependencies, estimated_complexity, tags
- SubtaskTemplate: subtask_id, name, description, required_skills, produces_artifact, estimated_duration_minutes, priority, can_parallelize
- Validation functions: validate_capability_node, validate_subtask_template, validate_capability_pack

Changes to Capability Contract require:
> Terjemahan Indonesia: Changes untuk kapabilitas Contract require:
- RFC process with 7-day review period
- Backward compatibility for all existing Capability Packs
- Migration guide for all affected templates
- Approval by project architecture authority

**Rationale:**
The Capability Contract is the interface between the platform and all Capability Packs.
Freezing it enables a marketplace of internal, community, and third-party packs to coexist without version conflicts.
> Terjemahan Indonesia: Kapabilitas Contract adalah interface between platform dan all kapabilitas Packs. Freezing it memungkinkan sebuah marketplace dari internal, community, dan third-party packs untuk coexist without versi conflicts.

---

## ADR-007: Conversation Boundary

**Status:** Frozen
**Effective:** 2026-07-10

Conversation Manager is responsible for:
> Terjemahan Indonesia: Conversation Manager adalah responsible untuk:
- Context management
- History tracking
- Streaming events
- Capability discovery responses

Conversation Manager must not:
> Terjemahan Indonesia: Manajer Percakapan tidak boleh:
- Perform planning
- Execute reasoning
- Schedule tasks
- Invoke Domain Engines directly

All task execution must flow through Society Runtime → Execution Runtime.
> Terjemahan Indonesia: Semua pelaksanaan tugas harus mengalir melalui Society Runtime → Execution Runtime.

**Rationale:**
Keeping Conversation Manager thin preserves the layer boundary between user interaction and task execution.
If Conversation Manager absorbs planning or execution logic, the system becomes harder to debug, test, and extend.
> Terjemahan Indonesia: Keeping Conversation Manager thin preserves layer boundary between user interaction dan task execution. If Conversation Manager absorbs planning or execution logic, sistem becomes harder untuk debug, test, dan extend.

---

## ADR-008: Core Change Requires Cross-Capability Proof

**Status:** Frozen
**Effective:** 2026-07-10

No change to Core may be made unless it is proven to be required by at least two Capability Packs.
> Terjemahan Indonesia: No change untuk Core may menjadi made unless it adalah proven untuk menjadi required oleh at least two kapabilitas Packs.

Process:
> Terjemahan Indonesia: Proses:
1. Identify the Core change needed
2. Document which Capability Packs require it
3. If fewer than 2 packs require it, the change belongs in the Capability Pack, not Core
4. If 2 or more packs require it, submit an RFC with test cases from both packs
5. RFC must be accepted before any Core modification

**Rationale:**
This prevents Core from growing based on single-use cases.
It ensures Core evolution is driven by cross-cutting concerns, not individual Capability Pack needs.
> Terjemahan Indonesia: Ini prevents Core dari growing based pada single-use cases. It ensures Core evolution adalah driven oleh cross-cutting concerns, not individual kapabilitas Pack needs.

---

## Process: Changing an Architecture Decision

1. Propose a new ADR or update an existing ADR
2. Document rationale and impact analysis
3. Submit to architecture review
4. If approved, update this document and notify all maintainers
5. Existing implementations must migrate according to the deprecation policy

Changes to frozen ADRs require:
> Terjemahan Indonesia: Changes untuk frozen ADRs require:
- RFC process with extended review period
- Migration plan for all affected components
- Approval by project architecture authority

---

## Definition of Architecture Complete

Enal AI OS architecture is considered complete when both conditions are satisfied:
> Terjemahan Indonesia: Enal AI OS arsitektur adalah considered complete when both conditions adalah satisfied:

1. A new Capability Pack can be added without any modification to Core.
2. Any change that impacts multiple Capability Packs requires an approved ADR with cross-capability proof.

Both conditions are satisfied as of 2026-07-10. Development focus shifts from platform construction to capability excellence.
> Terjemahan Indonesia: Both conditions adalah satisfied as dari 2026-07-10. Development focus shifts dari platform construction untuk kapabilitas excellence.

---

## Exception List: What Requires an ADR

The following changes are no longer routine. Any exception must be approved through the ADR process:
> Terjemahan Indonesia: Following changes adalah no longer routine. Any exception must menjadi approved through ADR process:

- Adding a new Runtime
- Adding a new Planner
- Adding a new Kernel
- Adding a new architectural Layer
- Modifying Core to improve a single Capability Pack

All of the above require:
> Terjemahan Indonesia: All dari above require:
1. Proof of cross-capability need (minimum 2 existing packs)
2. RFC with impact analysis
3. Approval by project architecture authority

---

## Architecture v1 Closure

**Effective:** 2026-07-11
**Status:** Closed

Architecture v1 is officially closed. The following conditions are met:
> Terjemahan Indonesia: Arsitektur v1 adalah officially closed. following conditions adalah met:
- Core Pipeline is frozen
- Capability Contract is frozen
- Worker API is stable
- Conversation Layer is stable
- Capability Discovery is stable
- Architecture Governance is active
- ADR process is established
- Capability Benchmark framework is active
- Real-world Benchmark is active
- Capability Excellence definition is formalized
- Documentation is synchronized

From this point forward, development focus shifts entirely from platform construction to Capability Excellence and Product Polish.
> Terjemahan Indonesia: Dari ini point forward, development focus shifts entirely dari platform construction untuk kapabilitas Excellence dan Product Polish.

New work must follow this cycle:
> Terjemahan Indonesia: New work must follow ini cycle:
> Real Usage → Measurement → Capability Improvement → Benchmark → Release

No further architecture changes are expected or permitted unless they satisfy the Exception List above.
> Terjemahan Indonesia: No further arsitektur changes adalah expected or permitted unless they satisfy Exception List above.

This document, together with ADR-001 through ADR-014, constitutes the Architecture Governance of Enal AI OS.
> Terjemahan Indonesia: Ini dokumen, together dengan ADR-001 through ADR-014, constitutes arsitektur tata kelola dari Enal AI OS.

---

## ADR-009: Single Conversation Interface

**Status:** Frozen
**Effective:** 2026-07-11

Users interact with Enal AI OS through a single conversational interface.
Users must not be required to select Capability Packs, configure Workers, choose Execution Runtimes, or understand any internal mechanism.
> Terjemahan Indonesia: Users interact dengan Enal AI OS through sebuah single conversational interface. Users must not menjadi required untuk select kapabilitas Packs, configure Workers, choose Execution Runtimes, or understand any internal mechanism.

All of the following must remain internal:
> Terjemahan Indonesia: All dari following must remain internal:
- Capability Pack selection
- Worker routing
- Execution Runtime selection
- Task Planning details
- Internal data structures

Users see one AI. Internally, ECP routes to the appropriate Capability Pack, plans tasks, and executes through Workers.
> Terjemahan Indonesia: Users see one AI. Internally, ECP routes untuk appropriate kapabilitas Pack, plans tasks, dan executes through Workers.

Violation of this principle is a UX defect, not a feature.
> Terjemahan Indonesia: Violation dari ini principle adalah sebuah UX defect, not sebuah feature.

**Rationale:**
Enal AI OS competes with ChatGPT, Claude, and Kimi on user experience, not on architectural complexity.
The value proposition is "one AI that understands multiple professional domains through one conversation."
Exposing internal mechanisms breaks this promise and creates cognitive load for users.
> Terjemahan Indonesia: Enal AI OS competes dengan ChatGPT, Claude, dan Kimi pada user experience, not pada architectural complexity. value proposition adalah "one AI itu understands multiple professional domains through one conversation." Exposing internal mechanisms breaks ini promise dan membuat kognitif load untuk users.

---

## ADR-010: Workspace Isolation

**Status:** Frozen
**Effective:** 2026-07-11

Each project or work context is isolated in a Workspace.
Workspace contains: History, Artifacts, and Memory.
Memory is scoped per Workspace. Cross-Workspace memory sharing requires explicit user action.
> Terjemahan Indonesia: Each proyek or work context adalah isolated dalam sebuah Workspace. Workspace contains: History, Artifacts, dan Memory. Memory adalah scoped per Workspace. Cross-Workspace memory sharing requires explicit user action.

**Rationale:**
Users work on multiple projects simultaneously.
Mixing memory and artifacts between projects creates confusion and privacy risks.
Workspace isolation keeps contexts clean and predictable.
> Terjemahan Indonesia: Users work pada multiple projects simultaneously. Mixing memory dan artifacts between projects membuat confusion dan privacy risks. Workspace isolation keeps contexts clean dan predictable.

---

## ADR-011: Artifact Persistence

**Status:** Frozen
**Effective:** 2026-07-11

All significant outputs from Capability Packs must be persisted as Artifacts.
Artifacts are versioned and scoped per Workspace.
Users can retrieve, compare, and restore previous artifact versions.
> Terjemahan Indonesia: All significant outputs dari kapabilitas Packs must menjadi persisted as Artifacts. Artifacts adalah versioned dan scoped per Workspace. Users dapat retrieve, compare, dan restore previous artifact versions.

Artifact types include, but are not limited to:
> Terjemahan Indonesia: Artifact types include, but adalah not limited untuk:
- Analysis reports
- Recommendations
- Patches and diffs
- Test reports
- Deployment plans
- Documentation

**Rationale:**
AI outputs are valuable and should not be ephemeral.
Persistent, versioned artifacts enable auditability, comparison, and rollback.
This is especially important for Self Development and controlled deployment workflows.
> Terjemahan Indonesia: AI outputs adalah valuable dan should not menjadi ephemeral. Persistent, versioned artifacts memungkinkan auditability, comparison, dan rollback. ini adalah especially important untuk Self Development dan controlled penyebaran workflows.

---

## ADR-012: Progress Transparency

**Status:** Frozen
**Effective:** 2026-07-11

During long-running tasks, the system must show progress to the user.
Progress indication must be coarse-grained and human-readable.
Users should never see a silent spinner with no information.
> Terjemahan Indonesia: During long-running tasks, sistem must show progress untuk user. Progress indication must menjadi coarse-grained dan human-readable. Users should never see sebuah silent spinner dengan no information.

Acceptable progress patterns:
> Terjemahan Indonesia: Pola kemajuan yang dapat diterima:
- "Analyzing configuration..."
- "Generating documentation..."
- "Running tests..."

Not acceptable:
> Terjemahan Indonesia: Tidak dapat diterima:
- Generic "Loading..." with no context
- Internal step names like "Stage 3: Execute Subtask 7"

**Rationale:**
Progress indication builds trust and reduces perceived wait time.
It also helps users understand what the AI is doing, which is part of explainability.
> Terjemahan Indonesia: Progress indication membangun trust dan reduces perceived wait time. It also helps users understand what AI adalah doing, which adalah part dari explainability.

---

## ADR-013: Outcome First Rule

**Status:** Frozen
**Effective:** 2026-07-11

Users request outcomes, not mechanisms.
> Terjemahan Indonesia: Pengguna meminta hasil, bukan mekanisme.

A user never says:
> Terjemahan Indonesia: Sebuah user never says:
- "Use Capability Network."
- "Call Worker NetworkWorker."
- "Run Execution Runtime."

A user says:
> Terjemahan Indonesia: Sebuah user says:
- "Audit jaringan kantor saya."
- "Analisa BTCUSDT."
- "Bangun aplikasi Inventory."

All internal mechanisms—Capability Packs, Workers, Execution Graph, Scheduler, Model Gateway—are means to an end. The end is the user's outcome.
> Terjemahan Indonesia: All internal mechanisms—kapabilitas Packs, Workers, Execution Graph, Scheduler, Model Gateway—adalah means untuk sebuah end. end adalah user's outcome.

Any feature, UI element, or API that exposes internal mechanisms to the user is a defect, not a feature.
> Terjemahan Indonesia: Any feature, UI element, or API itu exposes internal mechanisms untuk user adalah sebuah defect, not sebuah feature.

**Rationale:**
Enal AI OS competes on outcomes, not on architectural transparency. Users do not need to know how the AI works; they need to know that it works. Exposing internal concepts like Capability Packs, Workers, or Execution Graphs violates the single-conversation promise and creates unnecessary cognitive load. The product is judged by what it delivers, not by how it delivers it.
> Terjemahan Indonesia: Enal AI OS competes pada outcomes, not pada architectural transparency. Users do not need untuk know how AI works; they need untuk know itu it works. Exposing internal concepts like kapabilitas Packs, Workers, or Execution Graphs violates single-conversation promise dan membuat unnecessary kognitif load. product adalah judged oleh what it delivers, not oleh how it delivers it.

---

## ADR-014: Operational Product Layer

**Status:** Frozen
**Effective:** 2026-07-11

The Operational Product Layer consists of services that make ECP feel like a real product rather than an AI framework. These services are built on top of the stable Core and are required for production use.
> Terjemahan Indonesia: Operational Product Layer consists dari services itu make ECP feel like sebuah real product rather than sebuah AI kerangka kerja. These services adalah built pada top dari stable Core dan adalah required untuk production use.

Required services:
> Terjemahan Indonesia: Layanan yang dibutuhkan:
- Execution Service: manages full lifecycle of execution sessions
- Workspace Service: isolates projects with conversation, files, memory, artifacts, timeline
- Artifact Service: versioned storage with compare, restore, export
- Model Gateway: unified routing to OpenAI, Anthropic, Gemini, Qwen, DeepSeek, Llama, Ollama
- Notification Service: real-time progress and completion notifications

These services must not modify Core. They are part of the product layer, not the platform layer.
> Terjemahan Indonesia: These services must not modify Core. They adalah part dari product layer, not platform layer.

**Rationale:**
Users judge ECP by daily usability, not by internal architecture. The Operational Product Layer is what transforms a powerful AI runtime into a product that users can rely on for real work. Without these services, ECP remains a framework. With them, it becomes an AI Execution Platform.
> Terjemahan Indonesia: Users judge ECP oleh daily usability, not oleh internal arsitektur. Operational Product Layer adalah what transforms sebuah powerful AI runtime into sebuah product itu users dapat rely pada untuk real work. Without these services, ECP remains sebuah kerangka kerja. dengan them, it becomes sebuah AI Execution platform.
