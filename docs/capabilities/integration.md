# Integration Capability

## Overview

Integration capability provides cross-capability workflow orchestration for ENAL AI OS. It coordinates capabilities through metadata-driven discovery, shared context, and sequential execution.

## Architecture

### Modules

- `orchestrator.py` — `IntegrationEngine` builds and runs cross-capability workflows
- `registry.py` — `CapabilityRegistry` for metadata-driven capability discovery
- `context.py` — `CapabilityContext` for shared mutable state across workflow steps
- `workflow.py` — `WorkflowEngine` for sequential step execution
- `evidence_adapter.py` — `EvidenceAdapter` for unified evidence across capabilities

## Workflow Execution

Workflows are defined as sequences of steps that share a `CapabilityContext`. Capability relationships are declared in the `CapabilityRegistry`, not hardcoded in orchestrator methods.

## Contracts

- Request: Workflow definition with steps and context
- Response: `WorkflowResult` with execution status and evidence

## Observability

Integration logs workflow execution, step timing, and capability interactions.

## Limitations

- Sequential execution model; parallel execution is not yet supported
- Context is shared mutable state; distributed context is not available
