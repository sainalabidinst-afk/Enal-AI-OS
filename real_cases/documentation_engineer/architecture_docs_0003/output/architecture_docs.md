# Output

## Generated Architecture Documentation

### System Overview
ECP (Enal Capability Platform) adalah platform AI yang modular, dibangun di atas arsitektur Capability Pack.

### Key Decisions
- ADR-001: Event Bus Architecture
- ADR-002: Capability Pack Architecture
- ADR-003: Universal AST Design
- ADR-004: Debate Engine Architecture

### Component Diagram
```
apps/
├── base.py              # BaseReferenceApp abstract class
├── __init__.py          # Dynamic loader
├── business_analyst/    # Business analysis capability pack
├── devops_assistant/    # CI/CD and infrastructure automation
└── documentation_engineer/  # Documentation automation
```

### Data Flow
1. User Request → Execution Runtime
2. Execution Runtime → Capability Graph
3. Capability Graph → Task Planner
4. Task Planner → Subtasks
5. Subtasks → Execution Runtime → Worker → Engine → Result
