# Enal AI OS — Rollback Procedure v1.0.0-rc1

## Overview

This document defines the tested rollback procedure for Enal AI OS v1.0.0-rc1.
In case of deployment failure or critical issue, follow this procedure to restore service to the previous stable version.

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
3. Update docker-compose.yml image tags to previous version
4. Redeploy stack:
   ```bash
   docker compose up -d --force-recreate
   ```
5. Verify health:
   ```bash
   curl -f http://localhost:8000/health
   curl -f http://localhost:3001/
   ```
6. Monitor logs for 5 minutes:
   ```bash
   docker compose logs -f backend frontend
   ```

**Estimated Time:** 5-10 minutes

---

### Option B: Full Rollback (Including Database)

**When to use:** Database migration issue, data corruption, or complete system failure

**Steps:**
1. Stop all services:
   ```bash
   docker compose down
   ```
2. Restore database from backup:
   ```bash
   # Example using pg_restore
   pg_restore -U postgres -d enal_ai_os /backups/enal_ai_os_<date>.dump
   ```
3. Reset application state (if applicable):
   ```bash
   # Clear Redis cache if needed
   docker compose up -d redis
   docker compose exec redis redis-cli FLUSHALL
   ```
4. Deploy previous version (see Option A steps 1-4)
5. Run smoke tests:
   ```bash
   python scripts/validate_baseline.py
   ```
6. Verify data integrity:
   - Check critical records exist
   - Verify user sessions/workspaces accessible
   - Test core capabilities (chat, execution, workspace)

**Estimated Time:** 15-30 minutes

---

## Rollback Decision Tree

```
Deployment Issue Detected
├── Health checks failing
│   ├── Backend unhealthy → Option A
│   └── Database unavailable → Option B
├── Application error rate > 5%
│   └── Option A
├── Data inconsistency detected
│   └── Option B
└── Security incident
    └── Option B + incident response
```

---

## Post-Rollback Verification

After rollback, verify:

- [ ] All services healthy (`docker compose ps`)
- [ ] Health endpoints returning 200
- [ ] No error spikes in logs
- [ ] Database connectivity confirmed
- [ ] Core user journeys functional:
  - [ ] Chat/Conversation
  - [ ] Workspace management
  - [ ] Execution/Agent runs
  - [ ] Trading analysis (if applicable)
- [ ] Frontend accessible and API communication working

---

## Communication

During rollback:
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
