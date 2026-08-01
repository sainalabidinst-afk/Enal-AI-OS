# Document Structure — ECP Strategic Documentation

**Purpose:** Maps the function, ownership, and stability level of each strategic document. Helps contributors know where to find information and where to make updates.

---

## Principles

1. **Single Source of Truth (SSOT)** — Each piece of information lives in exactly one document. Other documents may reference it but must not duplicate it.
2. **Stability Levels** — Documents are classified as `Frozen`, `Stable`, `Active`, or `Ephemeral` to indicate how frequently they change.
3. **Clear Ownership** — Each document has an owner responsible for keeping it accurate.

---

## Document Inventory

| Document | SSOT For | Stability | Owner | Update Frequency |
|----------|----------|-----------|-------|------------------|
| `GOVERNANCE_CHARTER.md` | Vision, philosophy, constitutional rules | **Frozen** | Chief Architect | Constitution-level amendments only |
| `GOVERNANCE.md` | Operational rules (ADR, Capability First, Architecture Freeze) | **Stable** | Chief Architect | When rules change (via ADR) |
| `RELEASE_CRITERIA.md` | Release conditions, Definition of Done, quality gates | **Stable** | Release Manager | Per release cycle |
| `CAPABILITY_STRATEGY.md` | Capability Pack profiles, maturity model, lifecycle, knowledge expansion | **Active** | Capability Lead | Per capability improvement cycle |
| `ROADMAP.md` | Timeline, release targets, long-term vision | **Active** | Chief Product Officer | Per quarter or when roadmap shifts |
| `DOCUMENT_STRUCTURE.md` | This table — document mapping | **Stable** | Chief Architect | When new strategic docs are added |
| `v1_roadmap.md` | (Legacy landing page) | **Frozen** | — | No longer updated; redirects to new docs |
| `ARCHITECTURE_DECISIONS.md` | ADR records | **Frozen** | Chief Architect | Only when new ADR is approved |
| `PRODUCT_CONTRACT.md` | Product definition, UI/API contracts | **Frozen** | Chief Product Officer | Product Change Request only |
| `CAPABILITY_GUIDE.md` | Detailed capability specs (complementary to CAPABILITY_STRATEGY) | **Active** | Capability Lead | Per pack improvement |
| `QUALITY_GATE.md` | Quality gate status | **Ephemeral** | QA Lead | Updated per build/validation run |

---

## Where to Find What

| If you need... | Go to... |
|----------------|----------|
| Project vision and philosophy | `GOVERNANCE_CHARTER.md` |
| Rules for making changes (ADR, governance) | `GOVERNANCE.md` |
| What "done" means for a release | `RELEASE_CRITERIA.md` |
| Capability Pack details, maturity, lifecycle | `CAPABILITY_STRATEGY.md` |
| Timeline and release schedule | `ROADMAP.md` |
| ADR decisions | `ARCHITECTURE_DECISIONS.md` |
| Product contract (frontend-backend) | `PRODUCT_CONTRACT.md` |
| Quality gate status | `QUALITY_GATE.md` |
| RFC process | `docs/rfcs/README.md` |

---

## Stability Level Definitions

| Level | Description | Can Change... |
|-------|-------------|---------------|
| **Frozen** | Cannot be changed without formal amendment process | Via ADR or constitutional amendment only |
| **Stable** | Seldom changes; changes require review | Via PR with architecture review |
| **Active** | Changes regularly as part of development cycle | Via normal PR process |
| **Ephemeral** | Snapshots of current state; may be regenerated | Any time, may be overwritten |
