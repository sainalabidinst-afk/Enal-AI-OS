# ADR-002: Capability Pack Architecture

**Status:** ✅ Accepted  
**Date:** 2024  
**Deciders:** Chief Architect, Engineering Team

---

## Context

The platform needs to support multiple domain-specific capabilities (networking, coding, research, etc.) while maintaining a stable core. These capabilities must be:

- Independently developable
- Independently testable
- Plugable into the orchestration system
- Consistent in their interface contracts

---

## Decision

Organize domain-specific functionality into **Capability Packs** under `apps/`.

### Structure

```
apps/
├── __init__.py          # Dynamic loader
├── base.py              # BaseApp abstract class
├── code_engineer/
├── network_engineer/
├── research_assistant/
├── devops_assistant/
├── trading_analyst/
└── self_development/
```

### Capability Pack Contract

Each pack must expose:
1. A class inheriting from `BaseApp`
2. A module-level `get_app()` factory function
3. A `pipeline` list defining the cognitive pipeline stages
4. Required capabilities registered in `skills.yaml`

---

## Alternatives Considered

| Alternative | Reason Rejected |
|-------------|-----------------|
| Monolithic single app | Violates separation of concerns, hard to maintain |
| Microservices per capability | Premature — adds deployment complexity without proven need |
| Plugin system only | Plugins extend, capability packs are first-class citizens |

---

## Consequences

- **Positive:** Clear domain boundaries, independent testing
- **Positive:** Dynamic loading via `apps/__init__.py` for discovery
- **Positive:** Consistent interface via `BaseApp` abstract class
- **Negative:** Requires discipline to avoid cross-pack coupling
- **Negative:** Pack registration must be maintained in `skills.yaml`

---

## Compliance

All new domain capabilities MUST be implemented as a Capability Pack under `apps/`. No domain logic in core modules.

