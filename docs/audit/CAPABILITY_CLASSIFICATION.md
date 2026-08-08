# Capability Classification

The canonical user-facing capability registry is `apps/__init__.py`. The packages below are imported by API and orchestration code but are not registered in that registry.

| Package | User Capability | Infrastructure | Evidence | Decision |
|---|---|---|---|---|
| `apps/integration` | No | Yes | API integration routes and workflow orchestration; absent from `apps.APPS` | Keep as platform integration infrastructure |
| `apps/organization` | No | Yes | Capability graph, agent registry, reasoning and lifecycle services; imported by backend APIs | Keep as organization/runtime infrastructure |
| `apps/society` | No | Yes | Society runtime, conversation manager and worker coordination; imported by chat/orchestration paths | Keep as society/runtime infrastructure |

This classification is architectural, not a certification exclusion. These packages remain in scope for platform testing and runtime verification, but they must not be counted as additional user-facing capabilities without a canonical registry change.
