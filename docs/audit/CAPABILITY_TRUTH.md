# Capability Truth

Canonical registry: `apps/__init__.py`.

The probe below treats a capability as loadable only when its package imports and `get_app()` returns an application object. Package import alone is not enough because the registry loader calls `module.get_app()`.

| Capability | Registered | Package Exists | Importable | Executable | Tests | Certification | Frontend | Truth |
|---|---|---|---|---|---|---|---|---|
| trading-analyst | Yes | Yes | Yes | Yes | Collected | Unverified | Placeholder route | PARTIAL |
| network-engineer | Yes | Yes | Yes | Yes | Collected | Unverified | Workspace route | PARTIAL |
| devops-assistant | Yes | Yes | Yes | Yes | Collected | Unverified | Workspace route | PARTIAL |
| code-engineer | Yes | Yes | Yes | Yes | Collected | Unverified | Workspace route | PARTIAL |
| research-assistant | Yes | Yes | Yes | Yes | Collected | Unverified | Workspace route | PARTIAL |
| full-stack-engineer | Yes | Yes | Yes | Yes | Collected | Unverified | No dedicated route | PARTIAL |
| self-development | Yes | Yes | Yes | Yes | Collected | Unverified | Workspace route | PARTIAL |
| decision-intelligence | Yes | Yes | Yes | No | Collected | Unverified | Workspace route | UNLOADABLE |
| system-architect | Yes | Yes | Yes | No | Collected | Unverified | Workspace route | UNLOADABLE |
| security-engineer | Yes | Yes | Yes | No | Collected | Unverified | Workspace route | UNLOADABLE |
| data-engineer | Yes | Yes | Yes | No | Collected | Unverified | No dedicated route | UNLOADABLE |
| database-engineer | Yes | Yes | Yes | No | Collected | Unverified | Workspace route | UNLOADABLE |
| qa-engineer | Yes | Yes | Yes | No | Collected | Unverified | No dedicated route | UNLOADABLE |
| business-analyst | Yes | Yes | Yes | No | Collected | Unverified | Workspace route | UNLOADABLE |
| documentation-engineer | Yes | Yes | Yes | Yes | Collected | Unverified | No dedicated route | PARTIAL |
| product-manager | Yes | Yes | Yes | Yes | Collected | Unverified | No dedicated route | PARTIAL |
| infrastructure-engineer | Yes | Yes | Yes | No | Collected | Unverified | No dedicated route | UNLOADABLE |
| ai-engineer | Yes | Yes | Yes | No | Collected | Unverified | No dedicated route | UNLOADABLE |
| ui-ux-designer | Yes | Yes | Yes | No | Collected | Unverified | No dedicated route | UNLOADABLE |

## Loadability Probe

Result: 19 registered, 9 loadable, 10 not loadable.

All 19 package imports completed. The 10 failing registry entry points raised the same exact error:

```text
AttributeError: module 'apps.<package>' has no attribute 'get_app'
```

Affected packages: `decision_intelligence`, `system_architect`, `security_engineer`, `data_engineer`, `database_engineer`, `qa_engineer`, `business_analyst`, `infrastructure_engineer`, `ai_engineer`, and `ui_ux_designer`.

Classification: CODE DEFECT / ENTRYPOINT CONTRACT MISMATCH. These packages expose engines, workers and schemas from `__init__.py`, but not the `get_app()` function required by the canonical loader. This is not a missing dependency or environment-only failure.

## Execution Evidence

- Direct `trading-analyst` execution completed and returned the expected structured keys: `market`, `risk`, `portfolio`, and `strategy`.
- This proves one local capability entry point can execute; it does not certify the other 18 capabilities.
- No capability has fresh benchmark verification. The benchmark run completed zero executions.
