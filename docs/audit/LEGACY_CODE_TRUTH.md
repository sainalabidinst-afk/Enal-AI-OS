# Legacy Code Truth

No code was deleted during this audit.

| Area | Evidence | Decision |
|---|---|---|
| `apps/code_engineer` | Canonical underscore package, imported by tests, benchmarks and Full Stack Engineer | KEEP |
| `apps/trading_analyst` | Canonical underscore package, imported by tests, API and integration workflow | KEEP |
| `apps/devops_assistant` | Canonical underscore package, imported by tests and society worker | KEEP |
| Hyphenated `apps/code-engineer`, `apps/trading-analyst`, `apps/devops-assistant` directories | Not present in the repository structure | VERIFY no duplicate cleanup is required |
| `apps/integration` | Cross-capability workflow infrastructure | KEEP |
| `apps/organization` | Organization and cognitive support infrastructure | KEEP |
| `apps/society` | Society runtime and worker coordination infrastructure | KEEP |
| `agents/core` | README-only description of platform services | VERIFY; implementation lives under `backend/app/core` |
| `agents/specialized` | README-only future-agent scaffold | DEPRECATE or implement only under a separate approved scope |
| `sdk` | README, `pyproject.toml`, and `enal_ai.py` | VERIFY execution and consumer coverage |
| `plugins/mikrotik` | Plugin package exists under `plugins` | VERIFY through plugin tests and runtime loading |
| `tools/audit` | Audit utility scripts are present | KEEP |
| `tools/debug` | Debug utilities are present | KEEP but exclude from release claims |
| Frontend `TestComponent` and cognitive placeholder components | Explicit placeholder/test UI remains in product routes | DEPRECATE after a product decision; do not remove automatically |

The repository uses underscore package names consistently for the canonical applications. The prior concern about hyphenated duplicate directories is not reproduced by this audit.
