# Architecture Decisions

This document records architecture decisions that are considered stable and must not be changed without formal review.
Each decision is identified by an Architecture Decision Record (ADR) and is treated as part of Enal Cognitive Platform's technical constitution.

Contributors must not bypass these decisions via shortcuts, new dependencies, or layer violations.
If a decision must change, the proposer must submit a new ADR with impact analysis and approval from the project's architecture authority.

---

## Governance Principle: Two Equal Architectures

Enal AI OS is governed by two architectures of equal importance:

1. **Technical Architecture** — represented by ADR-001 through ADR-008
2. **Experience Architecture** — represented by ADR-009 through ADR-012 and `docs/UX_DESIGN.md`

Both are frozen. Both are binding. Neither may be violated without an approved ADR.

Technical Architecture ensures the platform remains stable, maintainable, and extensible.
Experience Architecture ensures users interact with one AI through one conversation, without exposure to internal mechanisms.

A change that violates either architecture is a defect, regardless of its technical merit.

---

## Feature Acceptance Rule

Every new feature must answer these three questions before implementation:

1. Which Capability improves?
   - If no Capability improves: do not build.

2. Which Journey becomes better?
   - If no Journey becomes better: do not build.

3. Which Benchmark increases?
   - If no Benchmark increases: do not build.

If all three answers are "yes", implementation may proceed.
This rule prevents feature creep and keeps development aligned with product value, not architectural novelty.

---

## ADR-001: Core Pipeline Freeze

**Status:** Frozen
**Effective:** 2026-07-10

The Core Pipeline must remain small, stable, and predictable.

- Core must stay under 5,000 lines of code.
- Core must have zero external dependencies beyond stdlib + pydantic.
- Core contracts are versioned and backward-compatible within major versions.
- Breaking changes require a 2-release grace period with migration guides.

**Rationale:**
A growing Core becomes a maintenance bottleneck and reduces ECP's ability to evolve Capability Packs independently.
Freezing Core size and dependencies forces new work into Capability Packs, preserving Core stability.

---

## ADR-002: Capability Pack Independence

**Status:** Frozen
**Effective:** 2026-07-10

Capability Packs must not import other Capability Packs directly.

Communication between Capability Packs must flow through:

1. Task / Intent definition
2. Execution Runtime
3. Shared contracts only

Example of forbidden pattern:

```python
# FORBIDDEN
from apps.trading_analyst import engine as trading_engine
trading_engine.analyze(...)
```

Example of allowed pattern:

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

---

## ADR-003: Worker = Adapter Only

**Status:** Frozen
**Effective:** 2026-07-10

A Worker is an adapter. A Worker does not own business logic.

Business logic belongs to the Domain Engine inside the Capability Pack.

Responsibilities:
- Worker: translates subtask into Capability Pack call, returns result
- Domain Engine: owns analysis, generation, validation, and domain-specific logic

Forbidden pattern:

```python
# FORBIDDEN - Worker owning business logic
class NetworkWorker:
    def analyze_firewall(self, config):
        # 200 lines of firewall analysis logic here
        ...
```

Required pattern:

```python
# ALLOWED - Worker delegates to Domain Engine
class NetworkWorker:
    async def execute(self, subtask, context):
        return await self._app.engine.analyze(config)
```

**Rationale:**
Keeping business logic in Domain Engines preserves testability, reusability, and separation of concerns.
Workers remain thin adapters that can be replaced or extended without changing domain logic.

---

## ADR-004: Domain Engine Owns Business Logic

**Status:** Frozen
**Effective:** 2026-07-10

All business logic for a Capability Pack resides in its Domain Engine.

- Domain Engine: analysis, generation, validation, simulation, recommendation
- Worker: adapter only (see ADR-003)
- Conversation Layer: context, history, streaming only

A Domain Engine may not:
- Import other Capability Pack engines directly
- Modify Core contracts
- Bypass Execution Runtime for cross-pack communication

**Rationale:**
Centralizing business logic in Domain Engines makes each Capability Pack self-contained and independently testable.
This is the architectural boundary that protects Core from domain-specific change.

---

## ADR-005: Human Approval Required

**Status:** Frozen
**Effective:** 2026-07-10

No code, configuration, or architecture changes may be applied without explicit user approval.

- Autonomous capabilities may analyze, propose, and prepare changes.
- Execution of changes requires explicit user approval.
- All proposals, diffs, test results, and approval records are preserved as artifacts.
- The platform never modifies itself without a human decision in the loop.

Implementation rule:
- Approval step must come before Apply step in any change workflow.
- Approval records must be immutable once created.

**Rationale:**
This principle is non-negotiable for user trust, auditability, and safe AI operation.
It is the governance mechanism that allows ECP to have autonomous capabilities without becoming autonomous in decision-making.

---

## ADR-006: Capability Contract v1 Frozen

**Status:** Frozen
**Effective:** 2026-07-10

Capability Contract v1 is the stable schema for all Capability Packs.

Contract elements:
- CapabilityNode: capability_id, name, description, required_skills, dependencies, estimated_complexity, tags
- SubtaskTemplate: subtask_id, name, description, required_skills, produces_artifact, estimated_duration_minutes, priority, can_parallelize
- Validation functions: validate_capability_node, validate_subtask_template, validate_capability_pack

Changes to Capability Contract require:
- RFC process with 7-day review period
- Backward compatibility for all existing Capability Packs
- Migration guide for all affected templates
- Approval by project architecture authority

**Rationale:**
The Capability Contract is the interface between the platform and all Capability Packs.
Freezing it enables a marketplace of internal, community, and third-party packs to coexist without version conflicts.

---

## ADR-007: Conversation Boundary

**Status:** Frozen
**Effective:** 2026-07-10

Conversation Manager is responsible for:
- Context management
- History tracking
- Streaming events
- Capability discovery responses

Conversation Manager must not:
- Perform planning
- Execute reasoning
- Schedule tasks
- Invoke Domain Engines directly

All task execution must flow through Society Runtime → Execution Runtime.

**Rationale:**
Keeping Conversation Manager thin preserves the layer boundary between user interaction and task execution.
If Conversation Manager absorbs planning or execution logic, the system becomes harder to debug, test, and extend.

---

## ADR-008: Core Change Requires Cross-Capability Proof

**Status:** Frozen
**Effective:** 2026-07-10

No change to Core may be made unless it is proven to be required by at least two Capability Packs.

Process:
1. Identify the Core change needed
2. Document which Capability Packs require it
3. If fewer than 2 packs require it, the change belongs in the Capability Pack, not Core
4. If 2 or more packs require it, submit an RFC with test cases from both packs
5. RFC must be accepted before any Core modification

**Rationale:**
This prevents Core from growing based on single-use cases.
It ensures Core evolution is driven by cross-cutting concerns, not individual Capability Pack needs.

---

## Process: Changing an Architecture Decision

1. Propose a new ADR or update an existing ADR
2. Document rationale and impact analysis
3. Submit to architecture review
4. If approved, update this document and notify all maintainers
5. Existing implementations must migrate according to the deprecation policy

Changes to frozen ADRs require:
- RFC process with extended review period
- Migration plan for all affected components
- Approval by project architecture authority

---

## Definition of Architecture Complete

Enal AI OS architecture is considered complete when both conditions are satisfied:

1. A new Capability Pack can be added without any modification to Core.
2. Any change that impacts multiple Capability Packs requires an approved ADR with cross-capability proof.

Both conditions are satisfied as of 2026-07-10. Development focus shifts from platform construction to capability excellence.

---

## Exception List: What Requires an ADR

The following changes are no longer routine. Any exception must be approved through the ADR process:

- Adding a new Runtime
- Adding a new Planner
- Adding a new Kernel
- Adding a new architectural Layer
- Modifying Core to improve a single Capability Pack

All of the above require:
1. Proof of cross-capability need (minimum 2 Capability Packs)
2. RFC with impact analysis
3. Approval by project architecture authority

---

## Architecture v1 Closure

**Effective:** 2026-07-11  
**Status:** Closed

Architecture v1 is officially closed. The following conditions are met:
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

New work must follow this cycle:
> Real Usage → Measurement → Capability Improvement → Benchmark → Release

No further architecture changes are expected or permitted unless they satisfy the Exception List above.

This document, together with ADR-001 through ADR-014, constitutes the Architecture Governance of Enal AI OS.

---

## ADR-009: Single Conversation Interface

**Status:** Frozen
**Effective:** 2026-07-11

Users interact with Enal AI OS through a single conversational interface.
Users must not be required to select Capability Packs, configure Workers, choose Execution Runtimes, or understand any internal mechanism.

All of the following must remain internal:
- Capability Pack selection
- Worker routing
- Execution Runtime selection
- Task Planning details
- Internal data structures

Users see one AI. Internally, ECP routes to the appropriate Capability Pack, plans tasks, and executes through Workers.

Violation of this principle is a UX defect, not a feature.

**Rationale:**
Enal AI OS competes with ChatGPT, Claude, and Kimi on user experience, not on architectural complexity.
The value proposition is "one AI that understands multiple professional domains through one conversation."
Exposing internal mechanisms breaks this promise and creates cognitive load for users.

---

## ADR-010: Workspace Isolation

**Status:** Frozen
**Effective:** 2026-07-11

Each project or work context is isolated in a Workspace.
Workspace contains: History, Artifacts, and Memory.
Memory is scoped per Workspace. Cross-Workspace memory sharing requires explicit user action.

**Rationale:**
Users work on multiple projects simultaneously.
Mixing memory and artifacts between projects creates confusion and privacy risks.
Workspace isolation keeps contexts clean and predictable.

---

## ADR-011: Artifact Persistence

**Status:** Frozen
**Effective:** 2026-07-11

All significant outputs from Capability Packs must be persisted as Artifacts.
Artifacts are versioned and scoped per Workspace.
Users can retrieve, compare, and restore previous artifact versions.

Artifact types include, but are not limited to:
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

---

## ADR-012: Progress Transparency

**Status:** Frozen
**Effective:** 2026-07-11

During long-running tasks, the system must show progress to the user.
Progress indication must be coarse-grained and human-readable.
Users should never see a silent spinner with no information.

Acceptable progress patterns:
- "Analyzing configuration..."
- "Generating documentation..."
- "Running tests..."

Not acceptable:
- Generic "Loading..." with no context
- Internal step names like "Stage 3: Execute Subtask 7"

**Rationale:**
Progress indication builds trust and reduces perceived wait time.
It also helps users understand what the AI is doing, which is part of explainability.

---

## ADR-013: Outcome First Rule

**Status:** Frozen
**Effective:** 2026-07-11

Users request outcomes, not mechanisms.

A user never says:
- "Use Capability Network."
- "Call Worker NetworkWorker."
- "Run Execution Runtime."

A user says:
- "Audit jaringan kantor saya."
- "Analisa BTCUSDT."
- "Bangun aplikasi Inventory."

All internal mechanisms—Capability Packs, Workers, Execution Graph, Scheduler, Model Gateway—are means to an end. The end is the user's outcome.

Any feature, UI element, or API that exposes internal mechanisms to the user is a defect, not a feature.

**Rationale:**
Enal AI OS competes on outcomes, not on architectural transparency. Users do not need to know how the AI works; they need to know that it works. Exposing internal concepts like Capability Packs, Workers, or Execution Graphs violates the single-conversation promise and creates unnecessary cognitive load. The product is judged by what it delivers, not by how it delivers it.

---

## ADR-014: Operational Product Layer

**Status:** Frozen
**Effective:** 2026-07-11

The Operational Product Layer consists of services that make ECP feel like a real product rather than an AI framework. These services are built on top of the stable Core and are required for production use.

Required services:
- Execution Service: manages full lifecycle of execution sessions
- Workspace Service: isolates projects with conversation, files, memory, artifacts, timeline
- Artifact Service: versioned storage with compare, restore, export
- Model Gateway: unified routing to OpenAI, Anthropic, Gemini, Qwen, DeepSeek, Llama, Ollama
- Notification Service: real-time progress and completion notifications

These services must not modify Core. They are part of the product layer, not the platform layer.

**Rationale:**
Users judge ECP by daily usability, not by internal architecture. The Operational Product Layer is what transforms a powerful AI runtime into a product that users can rely on for real work. Without these services, ECP remains a framework. With them, it becomes an AI Execution Platform.
