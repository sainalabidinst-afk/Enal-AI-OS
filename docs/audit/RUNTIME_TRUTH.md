# Runtime Truth

| Component | Status | Evidence |
|---|---|---|
| Backend import | PASS | `backend.app.main` imported and FastAPI app constructed |
| Backend local health | PARTIAL | TestClient returned 200 for `/` and `/health`; protected `/api/v1/health` returned 401 without a token |
| Backend capability discovery | PASS | `/api/v1/capabilities` returned 200 and exposes only loadable registry entries |
| Backend full runtime | BLOCKED | Docker stack did not start and the full test suite timed out |
| Frontend build | PASS | `npm run build` completed and generated 39 routes |
| PostgreSQL | BLOCKED | No Docker containers or images existed after the build/start timeout |
| Redis | BLOCKED | No Docker containers or images existed after the build/start timeout |
| Qdrant | BLOCKED | No Docker containers or images existed after the build/start timeout |
| Ollama | BLOCKED | No Docker containers or images existed after the build/start timeout |
| Model provider | BLOCKED | LiteLLM provider error before benchmark measurement |

## Local Capability Evidence

Direct execution of `apps.trading_analyst.get_app().run(...)` returned a structured result with market, risk, portfolio and strategy fields. This is a local capability proof, not a complete User -> Frontend -> API -> Auth -> Workspace -> Capability -> Artifact -> Memory -> Telemetry flow.

The integration workflow `trading_analysis_with_knowledge` returned `success=True`, but logged connection refused errors for all four requested market-data timeframes and produced no output keys. This is a false-success risk and prevents treating the integration path as reliable.
