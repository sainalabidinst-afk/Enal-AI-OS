<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `RELEASE/ROLLBACK_PROCEDURE.md`
- Judul: Rollback Procedure
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Enal AI OS â€” Rollback Procedure v1.0.0-rc1

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for ROLLBACK_PROCEDURE
<!-- DOCUMENT_METADATA_END -->

## Overview

This document defines the tested rollback procedure for Enal AI OS v1.0.0-rc1.
In case of deployment failure or critical issue, follow this procedure to restore service to the previous stable version.
> Terjemahan Indonesia: Ini dokumen defines tested rollback procedure untuk Enal AI OS v1.0.0-rc1. dalam case dari penyebaran failure or critical issue, follow ini procedure untuk restore layanan untuk previous stable versi.

---

## Prerequisites

- Previous stable tag available (e.g., `v0.9.0` or commit hash before `22f581c`)
- Docker images for previous version available in registry
- Database backup from before deployment
- Load balancer / reverse proxy configured for zero-downtime switch

---

## Rollback Options

### Option A: Quick Rollback (Container Redeploy)

**When to use:** Application-level issue, no data migration involved

**Steps:**
1. Identify previous stable tag: `git tag -l "v*" | sort -V | tail -n 2`
2. Pull previous Docker images:
   ```bash
   docker pull enal-ai-os-backend:<previous-tag>
   docker pull enal-ai-os-frontend:<previous-tag>
   ```
> Terjemahan Indonesia: Bash Docker pull enal-AI-os-backend: Docker pull enal-AI-os-frontend:
3. Update docker-compose.yml image tags to previous version
4. Redeploy stack:
   ```bash
   docker compose up -d --force-recreate
   ```
> Terjemahan Indonesia: Bash Docker compose up -d --force-recreate
5. Verify health:
   ```bash
   curl -f http://localhost:8000/health
   curl -f http://localhost:3001/
   ```
> Terjemahan Indonesia: Bash curl -f http://localhost:8000/health curl -f http://localhost:3001/
6. Monitor logs for 5 minutes:
   ```bash
   docker compose logs -f backend frontend
   ```
> Terjemahan Indonesia: Bash Docker compose logs -f backend frontend

**Estimated Time:** 5-10 minutes

---

### Option B: Full Rollback (Including Database)

**When to use:** Database migration issue, data corruption, or complete system failure

**Steps:**
1. Stop all services:
   ```bash
   docker compose down
   ```
> Terjemahan Indonesia: Bash Docker compose down
2. Restore database from backup:
   ```bash
   # Example using pg_restore
   pg_restore -U postgres -d enal_ai_os /backups/enal_ai_os_<date>.dump
   ```
> Terjemahan Indonesia: Bash # Example using pg_restore pg_restore -U postgres -d enal_ai_os /backups/enal_ai_os_.dump
3. Reset application state (if applicable):
   ```bash
   # Clear Redis cache if needed
   docker compose up -d redis
   docker compose exec redis redis-cli FLUSHALL
   ```
> Terjemahan Indonesia: Bash # Clear Redis cache if needed Docker compose up -d redis Docker compose exec redis redis-cli FLUSHALL
4. Deploy previous version (see Option A steps 1-4)
5. Run smoke tests:
   ```bash
   python scripts/validate_baseline.py
   ```
> Terjemahan Indonesia: Bash Python scripts/validate_baseline.py
6. Verify data integrity:
   - Check critical records exist
   - Verify user sessions/workspaces accessible
   - Test core capabilities (chat, execution, workspace)
> Terjemahan Indonesia: Check critical records exist Verify user sessions/workspaces accessible Test core kapabilitas (chat, execution, workspace)

**Estimated Time:** 15-30 minutes

---

## Rollback Decision Tree

```
Deployment Issue Detected
â”œâ”€â”€ Health checks failing
â”‚   â”œâ”€â”€ Backend unhealthy â†’ Option A
â”‚   â””â”€â”€ Database unavailable â†’ Option B
â”œâ”€â”€ Application error rate > 5%
â”‚   â””â”€â”€ Option A
â”œâ”€â”€ Data inconsistency detected
â”‚   â””â”€â”€ Option B
â””â”€â”€ Security incident
    â””â”€â”€ Option B + incident response
```

---

## Post-Rollback Verification

After rollback, verify:
> Terjemahan Indonesia: Setelah rollback, verifikasi:

- [ ] All services healthy (`docker compose ps`)
- [ ] Health endpoints returning 200
- [ ] No error spikes in logs
- [ ] Database connectivity confirmed
- [ ] Core user journeys functional:
  - [ ] Chat/Conversation
  - [ ] Workspace management
  - [ ] Execution/Agent runs
  - [ ] Trading analysis (if applicable)
> Terjemahan Indonesia: [ ] Chat/Conversation [ ] Workspace management [ ] Execution/agen runs [ ] Trading analysis (if applicable)
- [ ] Frontend accessible and API communication working

---

## Communication

During rollback:
> Terjemahan Indonesia: Selama pengembalian:
1. Notify stakeholders of incident and rollback initiation
2. Update status page if applicable
3. Document incident timeline
4. After stabilization, conduct post-mortem

---

## Previous Versions

| Tag | Commit | Date | Notes |
|-----|--------|------|-------|
| v1.0.0-rc1 | 22f581c | 2026-07-31 | Current release candidate |
| v0.9.0 | (previous) | - | Last stable production version |

---

## Contacts

- **On-Call Engineer:** (define in your runbook)
- **DevOps Lead:** (define in your runbook)
- **Security Contact:** (define in your runbook)
