# Organization Capability

## Overview

Organization capability manages AI organization structures, agent registries, team building, task planning, and workflow execution within ENAL AI OS.

## Architecture

### Modules

- `capability_execution_engine.py` — Core execution engine for capability orchestration
- `capability_graph.py` — Capability dependency graph
- `capability_lifecycle.py` — Lifecycle management for capabilities
- `capability_pipeline.py` — Pipeline orchestration
- `registry.py` — `AgentRegistry` for agent metadata and discovery
- `task_planner.py` — Task planning and decomposition
- `team_builder.py` — Team composition and role assignment
- `workflow_catalog.py` — Workflow definitions
- `workflow_executor.py` — Workflow execution engine
- `meeting.py` — Meeting simulation and coordination
- `communication.py` — Inter-agent communication
- `economics.py` — Resource and cost modeling
- `learning.py` — Organizational learning
- `experience_memory.py` — Experience memory
- `collective_memory.py` — Collective memory
- `metrics.py` — Organizational metrics

## Contracts

- Agent registration and discovery
- Team creation and role assignment
- Task planning and delegation
- Workflow definition and execution

## Observability

Organization exposes metrics for agent activity, team performance, and workflow execution.

## Limitations

- Simulation-based organization; real-world deployment requires additional infrastructure
- Team dynamics are simplified compared to real organizational behavior
