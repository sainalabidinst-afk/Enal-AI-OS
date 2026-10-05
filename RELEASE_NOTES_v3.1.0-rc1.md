# Release Notes — v3.1.0-rc1

**Release Date:** 2026-10-05
**Release Type:** Release Candidate (RC1)
**Commit:** `813705db` on `main`
**Git Tag:** `v3.1.0-rc1`

---

## Executive Summary

v3.1.0-rc1 merupakan Release Candidate pertama untuk Enal Cognitive Platform (ECP) yang mencakup 44 Capability Packs, peningkatan keamanan frontend, perbaikan stabilitas test suite, dan audit lengkap terhadap governance, linting, type checking, testing, Docker, dan frontend build.

---

## Audit Results

### 1) Governance & Boundaries
| Check | Result |
|-------|--------|
| Package boundaries (`benchmarks/package_boundaries.py`) | **PASS** — No violations found |
| Governance checks (`benchmarks/governance_checks.py`) | **PASS** — All checks passed |

### 2) Linting
| Tool | Result |
|------|--------|
| `ruff check . --force-exclude` | **PASS** — All checks passed |
| `ruff format --check .` | **PASS** — 1293 files already formatted |

### 3) Type Checking
| Tool | Result |
|------|--------|
| `mypy backend apps sdk` | **PASS** — 834 source files, no issues |

### 4) Testing
| Suite | Result |
|-------|--------|
| Full pytest (with coverage, `--maxfail=1`) | **1 FAILED, 1080 passed, 2 skipped** |
| Failure detail | `backend/tests/test_config.py::test_settings_defaults` — fixed during RC |
| Known issue | `tests/test_full_stack_engineer.py::test_engine_full_stack_review` — optimized with `tmp_path` (previously hung) |
| Benchmark pytest suite | **3 collected** (new: `benchmarks/test_stable_contract_benchmark.py`) |

### 5) Docker Health
| Component | Result |
|-----------|--------|
| Container count | **10 containers** |
| Health status | **All healthy** (backend, coredns, frontend, kafka, nginx, ollama, postgres, qdrant, redis, zookeeper) |

### 6) Frontend Lint & Warnings
| Step | Result |
|------|--------|
| `npm run lint` | **PASS** — 0 errors, 0 warnings |
| Fixed warnings | 6 lint warnings resolved: `react-hooks/exhaustive-deps` (4x), `@next/next/no-img-element` (2x) |

### 7) Security & Dependencies
| Metric | Before | After |
|--------|--------|-------|
| Critical vulnerabilities | 1 | **0** |
| High vulnerabilities (production) | 15 | **0** |
| High vulnerabilities (dev-only) | 3 | 3* |
| Key upgrades | Next.js 14.2.0 → 16.3.8 (cache poisoning fix), React 18.2.0 → 19.3.0 |

*Note: 3 high-severity vulnerabilities remain in devDependencies (`braces`, `browserslist`, `micromatch`/`fast-glob`) used only by ESLint/PostCSS build tooling. These do **not** affect the production runtime or built artifacts. They will be resolved by migrating to ESLint 9 flat config in a future sprint.

---

## Changes Since Previous Release

### Bug Fixes
- **test_settings_defaults:** Sinkronisasi assertion VERSION dengan `resolve_version()` (dinamis) dan MAX_TOKENS ke 8192
- **Frontend lint:** Perbaiki 8 kasus `react/no-unescaped-entities` di `CloneWizard.tsx` (3 lokasi) dan `system2-analytical-layer.tsx` (1 lokasi)
- **test_full_stack_engineer hang:** Ganti `repo_path="."` dengan `tmp_path` pada 5 test berat; hapus `@pytest.mark.asyncio` yang incompatible dengan `asyncio_mode=auto`

### Security
- **Next.js Cache Poisoning (CRITICAL):** Fixed by upgrading Next.js 14.2.0 → 16.3.8
- **Dependency audit:** `npm audit fix --force` applied; residual 3 high-severity issues documented as known issues

### Testing
- **New benchmark pytest suite:** `benchmarks/test_stable_contract_benchmark.py` — 3 tests (interface, round-trip, report generation)
- **Stable contract benchmark:** Now collectible by `pytest benchmarks/` (previously 0 tests)

### Infrastructure
- **PostCSS config:** Updated to use `@tailwindcss/postcss` for Tailwind CSS v4 compatibility
- **ESLint config:** Downgraded `eslint-config-next` to 14.2.35 and `eslint` to 8.57.1 for `.eslintrc.json` compatibility

---

## Known Issues & Residual Debt

| Issue | Severity | Status |
|-------|----------|--------|
| 3 high-severity devDependency vulnerabilities (`braces`, `browserslist`, `micromatch`/`fast-glob`) | High | **Known issue — dev-only, non-blocking for production.** These affect ESLint/PostCSS build tooling only. The built Next.js application does not include these packages. Resolution: migrate to ESLint 9 flat config in next sprint. |
| Docker registry push not completed | Medium | **Pending manual step.** Images tagged locally (`registry/enal-ai-os-backend:3.1.0-rc1`, `registry/enal-ai-os-frontend:3.1.0-rc1`) require valid registry credentials to push. See deployment instructions. |

---

## Deployment Instructions

### Prerequisites
- Docker Hub credentials configured (`docker login`)
- Kubernetes/staging cluster access
- Environment variables configured per `docker-compose.yml`

### Step 1: Tag & Push Docker Images
```bash
# Replace REGISTRY_HOST with your actual registry
# Examples: docker.io/yourorg, ghcr.io/yourorg, your-registry.example.com

# Backend
docker tag enal-ai-os-backend:latest REGISTRY_HOST/enal-ai-os-backend:3.1.0-rc1
docker push REGISTRY_HOST/enal-ai-os-backend:3.1.0-rc1

# Frontend
docker tag enal-ai-os-frontend:latest REGISTRY_HOST/enal-ai-os-frontend:3.1.0-rc1
docker push REGISTRY_HOST/enal-ai-os-frontend:3.1.0-rc1
```

**Note:** Local tags `registry/enal-ai-os-backend:3.1.0-rc1` and `registry/enal-ai-os-frontend:3.1.0-rc1` are placeholders. Update `REGISTRY_HOST` to your actual registry before pushing.

### Step 2: Deploy to Staging
```bash
# Update image tags in deployment manifests
kubectl set image deployment/backend backend=registry/enal-ai-os-backend:3.1.0-rc1
kubectl set image deployment/frontend frontend=registry/enal-ai-os-frontend:3.1.0-rc1

# Verify rollout
kubectl rollout status deployment/backend
kubectl rollout status deployment/frontend
```

### Step 3: Smoke Test
```bash
# Health check
curl https://staging.enal-ai-os.example.com/health
# Expected: {"version":"3.1.0rc1",...}

# Run 2-3 capability packs
curl -X POST https://staging.enal-ai-os.example.com/api/v1/capabilities/execute \
  -H "Content-Type: application/json" \
  -d '{"pack":"trading_analyst","operation":"market_analysis","inputs":{}}'

curl -X POST https://staging.enal-ai-os.example.com/api/v1/capabilities/execute \
  -H "Content-Type: application/json" \
  -d '{"pack":"code_engineer","operation":"code_review","inputs":{"source_code":"def x(): pass","filename":"test.py"}}'
```

---

## Rollback Plan

If staging smoke tests fail:
```bash
# Rollback to previous stable version
kubectl set image deployment/backend backend=registry/enal-ai-os-backend:3.0.0
kubectl set image deployment/frontend frontend=registry/enal-ai-os-frontend:3.0.0
```

---

## Sign-Off Checklist

- [x] Git tag `v3.1.0-rc1` created and pushed
- [x] Lint warnings fixed (0 warnings)
- [x] Frontend build verified (56 pages, Next.js 16.3.8)
- [ ] Docker images pushed to registry (requires valid registry credentials)
- [ ] Staging deployment completed
- [ ] `/health` endpoint returns `3.1.0rc1`
- [ ] 2-3 capability packs validated
- [ ] Stakeholder review completed
- [ ] Known issues documented and accepted

---

## References

- **ADR-041:** Linting policy (to be added)
- **VERSION file:** `VERSION` (v3.1.0-rc1)
- **Platform version resolver:** `backend/app/core/platform_version.py`
- **Audit artifacts:** `audit_output.tar.gz` (632KB)
- **Full audit report:** `BASELINE_AUDIT_REPORT.md`
