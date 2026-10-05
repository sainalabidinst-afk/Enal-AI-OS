# Smoke Test Checklist — v3.1.0-rc1

## Pre-Deployment

- [x] Git tag `v3.1.0-rc1` created and pushed
- [x] Frontend lint: 0 errors, 0 warnings
- [x] Frontend build verified: Next.js 16.3.8, 56 pages
- [x] Docker images pushed to Docker Hub:
  - `docker.io/chokyrasta/enal-ai-os-backend:3.1.0-rc1` (956MB)
  - `docker.io/chokyrasta/enal-ai-os-frontend:3.1.0-rc1` (270MB)
- [x] Images verified in registry with digest:
  - Backend: `sha256:0ba79df431fbd1d7355bb27af9c11124106c8b1a7c8def3591499806bd388c31`
  - Frontend: `sha256:e0a8ca608a32b1b8c23b7ca73bae92e63f5f984d087730621e9fe3630a584614`
- [x] Kubernetes manifests created: `k8s/enal-ai-os-v3.1.0-rc1.yaml`
- [ ] Kubernetes manifests applied to cluster
- [ ] Environment variables configured (`.env` or ConfigMap)

> **Registry:** `docker.io/chokyrasta/` (Docker Hub)
> **Manifest:** `k8s/enal-ai-os-v3.1.0-rc1.yaml`

## Security Notes

- **npm vulnerabilities:** 3 high-severity issues remain in devDependencies (`braces`, `browserslist`, `micromatch`/`fast-glob`). These affect only build tooling (ESLint/PostCSS) and are **not included in production builds**. They will be resolved by migrating to ESLint 9 flat config in the next sprint.
- **Production runtime:** Secure. Built Next.js artifacts do not contain vulnerable devDependencies.

## Health Checks

```bash
# Backend health
curl -f https://staging.enal-ai-os.example.com/health
# Expected: {"version":"3.1.0rc1", "status":"healthy"}

# Frontend accessibility
curl -f https://staging.enal-ai-os.example.com/
# Expected: HTTP 200, page title contains "Enal AI OS"
```

## Capability Pack Validation

### Pack 1: Trading Analyst
```bash
curl -X POST https://staging.enal-ai-os.example.com/api/v1/capabilities/execute \
  -H "Content-Type: application/json" \
  -d '{
    "pack": "trading_analyst",
    "operation": "market_analysis",
    "inputs": {
      "symbol": "BTCUSD",
      "timeframe": "1h"
    },
    "context": {"project_id": "smoke-test", "language": "python"}
  }'
```
**Expected:** HTTP 200, response contains `operation: "market_analysis"`, no errors

### Pack 2: Code Engineer
```bash
curl -X POST https://staging.enal-ai-os.example.com/api/v1/capabilities/execute \
  -H "Content-Type: application/json" \
  -d '{
    "pack": "code_engineer",
    "operation": "code_review",
    "inputs": {
      "source_code": "def add(a, b):\n    return a + b\n",
      "filename": "calculator.py"
    },
    "context": {"project_id": "smoke-test", "language": "python"}
  }'
```
**Expected:** HTTP 200, response contains `code_review` with findings

### Pack 3: Network Engineer
```bash
curl -X POST https://staging.enal-ai-os.example.com/api/v1/capabilities/execute \
  -H "Content-Type: application/json" \
  -d '{
    "pack": "network_engineer",
    "operation": "topology_analysis",
    "inputs": {
      "device_list": ["router1", "switch1"]
    },
    "context": {"project_id": "smoke-test", "language": "python"}
  }'
```
**Expected:** HTTP 200, response contains `topology_analysis` result

## Backend Activation (Multi-Provider Market Data)

The trading feed uses a **multi-provider aggregator with automatic fallback**:
1. **BinanceProvider** — public REST API, no key required (primary)
2. **YahooFinanceProvider** — yfinance library, delayed data (fallback)

If Binance fails (rate limit, connection error), the aggregator automatically falls back to Yahoo Finance. This ensures the smoke test is resilient to API issues.

### Step 1: Start Live Feed
```bash
curl -X POST http://localhost:8000/api/v1/trading/feed/start \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{"symbol":"BTCUSDT","timeframes":["15m","1h","4h"]}'
```
**Expected:** Feed starts polling. Backend logs show provider attempts (Binance → Yahoo Finance fallback if needed).

### Step 2: Verify Feed Status
```bash
curl http://localhost:8000/api/v1/trading/feed/status \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```
**Expected:** `{"status":"running","symbol":"BTCUSDT",...}`

### Step 3: Run Market Analysis
```bash
curl -X POST http://localhost:8000/api/v1/trading/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{"symbol":"BTCUSDT","timeframes":["1h","4h"]}'
```
**Expected:** HTTP 200 with market analysis data.

### Step 4: Check Live Regime
```bash
curl http://localhost:8000/api/v1/trading/regime/live \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```
**Expected:** JSON with regime, confidence, volatility, trend_strength.

## Observability Validation

> **Note:** The console requires authentication. Use the test account below to access protected views.

### Test Account
- **Username:** `test`
- **Password:** `test`
- **Permissions:** `default`

### Quick Login via API
```bash
# Get access token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test&password=test"

# Response: {"access_token":"<JWT>","token_type":"bearer","expires_in":3600}
```

### Browser Login
1. Navigate to `http://localhost:3001/login`
2. Enter username: `test`, password: `test`
3. After login, navigate to `http://localhost:3001/console/observability`

### Observability Panel Checks
After completing backend activation and login:

- [ ] **Market Engine** status shows `running` (not "Connecting...")
- [ ] **Confidence trend** chart displays data points (≥2 ticks)
- [ ] **Capability latency** shows ms values
- [ ] **Agent metrics** populated (tick count, throughput)
- [ ] **Learning progress** shows training iterations
- [ ] **Alerts** panel shows system events (if any)

## Frontend Validation

- [ ] Homepage loads (HTTP 200)
- [ ] `/apps/trading` page renders without console errors
- [ ] `/apps/code` page renders without console errors
- [ ] Console → Packs page lists capability packs
- [ ] No uncaught JavaScript errors in browser console

## Rollback Criteria

Trigger rollback if any of the following occur:
- [ ] `/health` returns non-200 or version mismatch
- [ ] Any capability pack returns HTTP 500
- [ ] Frontend build fails to load (blank page or CSS/JS 404)
- [ ] Database migration errors in backend logs
- [ ] Memory usage > 90% on backend pods for > 5 minutes

## Deployment to Kubernetes

### Prerequisites
- `kubectl` configured with cluster access
- Docker Hub credentials configured (`kubectl create secret docker-registry ...`)
- Secrets created: `enal-ai-os-secrets` with `secret-key` and `database-url`

### Step 1: Apply Manifests
```bash
kubectl apply -f k8s/enal-ai-os-v3.1.0-rc1.yaml
```

### Step 2: Verify Rollout
```bash
kubectl rollout status deployment/enal-ai-os-backend -n enal-ai-os
kubectl rollout status deployment/enal-ai-os-frontend -n enal-ai-os
```

### Step 3: Verify Image Tags
```bash
kubectl get deployment enal-ai-os-backend -n enal-ai-os -o jsonpath='{.spec.template.spec.containers[0].image}'
kubectl get deployment enal-ai-os-frontend -n enal-ai-os -o jsonpath='{.spec.template.spec.containers[0].image}'
```

**Expected output:**
```
docker.io/chokyrasta/enal-ai-os-backend:3.1.0-rc1
docker.io/chokyrasta/enal-ai-os-frontend:3.1.0-rc1
```

### Step 4: Verify Registry Digests
```bash
# Backend
kubectl get deployment enal-ai-os-backend -n enal-ai-os -o jsonpath='{.spec.template.status.containerStatuses[0].imageID}'
# Expected: docker-pullable://docker.io/chokyrasta/enal-ai-os-backend@sha256:0ba79df...

# Frontend
kubectl get deployment enal-ai-os-frontend -n enal-ai-os -o jsonpath='{.spec.template.status.containerStatuses[0].imageID}'
# Expected: docker-pullable://docker.io/chokyrasta/enal-ai-os-frontend@sha256:e0a8ca6...
```

## Rollback Command

```bash
kubectl set image deployment/backend backend=registry/enal-ai-os-backend:3.0.0
kubectl set image deployment/frontend frontend=registry/enal-ai-os-frontend:3.0.0
kubectl rollout status deployment/backend
kubectl rollout status deployment/frontend
```

## Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Release Engineer | | | |
| QA Lead | | | |
| Product Owner | | | |
| Security Officer | | | |
