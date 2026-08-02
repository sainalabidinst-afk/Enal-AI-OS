<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `RELEASE/RELEASE_NOTES_v1.0.0-rc1.md`
- Judul: Release Notes V1.0.0 Rc1
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Enal AI OS â€” Release Notes v1.0.0-rc1

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for RELEASE_NOTES_v1.0.0-rc1
<!-- DOCUMENT_METADATA_END -->

**Release Date:** 2026-07-31
**Tag:** v1.0.0-rc1
**Commit:** 22f581c927454f4577a37af2f5be9beb93b04904
**Branch:** main

---

## Security Hardening

### Critical Fixes
- **Command Injection**: Replaced `asyncio.create_subprocess_shell` with `create_subprocess_exec` + `shlex.split` in sandbox runtime
- **SSRF Protection**: Added URL validation in browser agent to block private/internal IP ranges (127.0.0.1, 10.x, 192.168.x, 172.16-31.x, 169.254.169.254)
- **Hardcoded Secrets Removed**: Removed default database password from config.py and docker-compose.yml; credentials now injected via environment variables
- **Authentication Framework**: Added authentication middleware with fail-closed behavior when SECRET_KEY is unset
- **Rate Limiting**: Added per-IP rate limiter (100 requests/60s)
- **Security Headers**: Added HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy

### Authorization
- Implemented RBAC dependency injection (`backend/app/core/auth.py`)
- Wired `require_permission()` to workspace and execution endpoints
- Sensitive operations now enforce READ/WRITE/EXECUTE permissions

### Audit Logging
- Added `AuditLoggingMiddleware` for request-level audit trail
- Logs include: method, path, status code, duration, user identifier

---

## Architecture Improvements

### Circular Import Resolution
- Fixed circular dependency: `cognitive/__init__.py` â†’ `adaptive_runtime.py` â†’ `cognitive_kernel.py` â†’ `cognitive/__init__.py`
- Deferred module-level imports to `__init__` methods where necessary

### Backend/Apps Boundary
- Converted top-level `from apps.*` imports to lazy imports in API routers (`chat.py`, `trading.py`, `capability_discovery.py`)
- Respects architectural boundary: backend should not import apps at module load time

### Capability Wiring
- Populated `apps/organization/__init__.py` with proper exports
- Added `self_development` to capability registry
- Fixed trading analyst wiring to `market_intelligence` package
- Fixed integration orchestrator imports

### Test Suite
- Removed duplicate test file (`test_integration_api.py`)
- Added `httpx2` to dev dependencies
- Fixed test API paths to match actual route registration
- **Result: 426 tests passing, 0 failed**

---

## DevOps Hardening

### Docker Security
- **Backend**: Multi-stage build, non-root user (`appuser`), minimal attack surface
- **Frontend**: Multi-stage build, non-root user (`nextjs`), Next.js standalone output
- **docker-compose.yml**:
  - Read-only filesystem for all services
  - `tmpfs` for `/tmp` where applicable
  - `cap_drop: [ALL]` + `no-new-privileges:true`
  - Resource limits (memory, CPU) per service
  - Healthcheck conditions for `depends_on`
  - Removed hardcoded database password; uses `${POSTGRES_PASSWORD}`
> Terjemahan Indonesia: Read-only filesystem untuk all services tmpfs untuk /tmp where applicable cap_drop: [ALL] + no-new-privileges:true Resource limits (memory, CPU) per layanan Healthcheck conditions untuk depends_on Removed hardcoded database password; uses ${POSTGRES_PASSWORD}

### CI/CD
- Validation gate scripts added (`scripts/validate_*.py`)
- Gate 0-4 cover baseline, security, architecture, capabilities, cognitive validation

---

## API Changes

### Breaking Changes
- **Authentication**: Non-public endpoints now require `Authorization: Bearer <token>` header when `SECRET_KEY` is set
- **Public Endpoints** (no auth required):
  - `GET /`
  - `GET /health`
  - `/docs`, `/openapi.json`, `/redoc`
> Terjemahan Indonesia: DAPATKAN / DAPATKAN /kesehatan /docs, /openapi.json, /redoc

### Migration Notes
- Set `SECRET_KEY` environment variable to enable authentication
- Without `SECRET_KEY`, all non-public endpoints return 401
- Existing clients must be updated to send Bearer tokens

---

## Known Limitations

1. **Authentication**: Current implementation is token-based but does not validate JWT signatures. Intended for development/internal use.
2. **Rate Limiter**: In-memory implementation; not suitable for multi-instance deployments without shared state (Redis).
3. **Audit Logging**: Logs to application log stream; for production, integrate with centralized logging (ELK, Loki, etc.).
4. **Placeholder Capabilities**: `research_assistant`, `self_development`, `devops_assistant` remain simulated/placeholder implementations.

---

## Upgrade Guide

### From Previous Version
1. Set required environment variables: `SECRET_KEY`, `DATABASE_URL`, `POSTGRES_PASSWORD`
2. Update API clients to include `Authorization: Bearer <token>` header
3. Review and update RBAC policies as needed
4. Deploy with new Docker images (multi-stage, non-root)

### Rollback
- Revert to previous tag: `git checkout <previous-tag>`
- Redeploy previous Docker images
- No database schema changes in this release

---

## Validation Results

| Gate | Status |
|------|--------|
| Gate 0 â€” Baseline Freeze | PASS |
| Gate 1 â€” Security Hardening | PASS |
| Gate 2 â€” Architecture Convergence | PASS |
| Gate 3 â€” Capability Wiring | PASS |
| Gate 4 â€” Cognitive Validation | PASS |

**Test Results:** 426 passed, 0 failed
**Build Status:** Ready for containerization
**Security Scan:** P0 issues resolved; P1 issues documented
