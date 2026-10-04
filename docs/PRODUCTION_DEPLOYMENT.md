# Enal Cognitive Platform — Production Deployment Guide

**Document Status:** Active
**Target Release:** v3.0.0
**Owner:** Platform Engineering Team

---

## Overview

This guide covers production deployment of Enal Cognitive Platform (ECP) v3.0.0.
It assumes a Linux host with Docker Engine available.

## Prerequisites

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores | 8+ cores |
| Memory | 8 GB | 16+ GB |
| Storage | 50 GB SSD | 200+ GB SSD |
| Docker | 24.0+ | 25.0+ |
| Docker Compose | v2.20+ | v2.24+ |

### CPU Instruction Set Requirements
- **AVX2**: Mandatory for Ollama runtime on production hosts.
- Some CPU models report AVX2 in `/proc/cpuinfo` but still fail to map Ollama's `cpu_avx2/libext_server.so` due to host kernel/Docker seccomp interaction.
- **Workaround**: Set `seccomp:unconfined` and `cap_add: [SYS_ADMIN]` for the `ollama` service in `docker-compose.yml`.
- **Model fallback**: Use `DEFAULT_MODEL=ollama/llama3:8b` with `FALLBACK_MODEL=ollama/qwen2.5:0.5b` if primary model fails to load.

## Step 1: Environment Configuration

1. Copy the production environment template:
   ```bash
   cp .env.production.example .env.production
   ```

2. Edit `.env.production` and set all required values:
   ```
   POSTGRES_PASSWORD=<strong-password>
   MINIO_ROOT_PASSWORD=<strong-password>
   SECRET_KEY=<32+ char secret>
   OPENAI_API_KEY=<or ANTHROPIC_API_KEY or GEMINI_API_KEY>
   LANGFUSE_SECRET_KEY=<if using Langfuse>
   ```

3. Verify all required variables are set:
   ```bash
   python scripts/validate_env.py .env.production
   ```

## Step 2: LLM Provider Configuration

At least one LLM provider API key must be configured for runtime benchmarks
to function. The LiteLLM router in `backend/app/core/model_router.py` supports:

| Provider | Env Var | Model Prefix |
|----------|---------|-------------|
| OpenAI | `OPENAI_API_KEY` | `gpt-4o`, `o1-` |
| Anthropic | `ANTHROPIC_API_KEY` | `claude-` |
| Google | `GEMINI_API_KEY` or `GOOGLE_API_KEY` | `gemini/` |
| Ollama (local) | `OLLAMA_BASE_URL` | `ollama/` |

For production, set:
```bash
DEFAULT_MODEL=ollama/llama3:8b
DEFAULT_REASONING_MODEL=ollama/llama3:8b
DEFAULT_EMBEDDING_MODEL=ollama/nomic-embed-text
```

## Step 3: Docker Deployment

1. Build and start all services:
   ```bash
   docker compose --env-file .env.production up -d --build
   ```

2. Verify all services are healthy:
   ```bash
   docker compose ps
   curl -f http://localhost:8000/health
   curl -f http://localhost:3001/
   ```

3. Check backend logs:
   ```bash
   docker compose logs -f backend
   ```

## Step 4: Security Configuration

### Read-Only Filesystem
All services run with `read_only: true`. Writable paths use `tmpfs`:
- Backend: `/tmp`, `/app/workspace`
- Frontend: `/tmp`

### Non-Root Containers
- Backend: runs as `appuser` (non-root, nologin shell)
- Frontend: runs as `nextjs` (non-root, nologin shell)

### Security Headers
Applied via `SecurityHeadersMiddleware`:
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `Content-Security-Policy: default-src 'self'; frame-ancestors 'none'`
- `Referrer-Policy: no-referrer`
- `Permissions-Policy: geolocation=(), microphone=(), camera=()`

### Authentication
- Bearer token authentication required for all non-public endpoints
- Public endpoints: `/`, `/health`, `/docs`, `/openapi.json`, `/redoc`, `/auth/login`, `/capabilities`, `/metrics`
- Rate limiting: 100 requests/60 seconds per IP (bypassed when `TESTING=true`)

## Step 5: Monitoring Stack

### Option A: ELK Stack (Elasticsearch, Fluentd, Kibana)
```bash
# Add to docker-compose.production.yml:
docker compose -f docker-compose.yml -f docker-compose.production.yml up -d
```
Configuration: `telemetry/log_aggregator_config.yml`

### Option B: LGTM Stack (Loki, Grafana, Tempo, Promtail)
```bash
docker run -d --name loki -p 3100:3100 grafana/loki:2.9.0
docker run -d --name promtail -v /var/log/enal-ai-os:/var/log \
  grafana/promtail:2.9.0 -config.file=/etc/promtail/config.yml
docker run -d --name grafana -p 3000:3000 grafana/grafana-helm
```

### Prometheus Metrics
Available at:
- `GET /metrics` — Aggregate telemetry metrics
- `GET /metrics/chat` — Chat performance metrics
- `GET /metrics/analysis` — Analysis metrics
- `GET /metrics/parser` — Parser metrics
- `GET /metrics/reasoning` — Reasoning metrics
- `GET /observability/metrics` — Observability pack metrics

### Alert Rules
| Alert | Condition | Severity |
|-------|-----------|----------|
| BackendDown | `up{job="backend"} == 0` for 1min | Critical |
| HighErrorRate | `rate(http_5xx[5m]) > 0.05` for 2min | Critical |
| LLMTimeout | `rate(llm_errors[5m]) > 0.10` for 5min | Warning |
| MemoryPressure | `container_memory_usage > 85%` | Warning |
| CapabilityLatency | `capability_p95_latency > 30s` | Warning |

## Step 6: Backup & Recovery

### Database Backup
```bash
docker compose exec postgres pg_dump -U postgres enal_ai_os > backup_$(date +%F).sql
```

### Redis Backup
```bash
docker compose exec redis redis-cli BGSAVE
docker cp $(docker ps -q -f name=redis):/data/dump.rdb ./redis_backup_$(date +%F).rdb
```

### Qdrant Backup
```bash
docker compose exec qdrant qdrant snapshot create --output-dir /qdrant/snapshots
docker cp $(docker ps -q -f name=qdrant):/qdrant/snapshots ./qdrant_snapshot_$(date +%F)
```

### Rollback
See `RELEASE/ROLLBACK_PROCEDURE.md`.

## Step 7: Smoke Test

```bash
python RELEASE/smoke_test.py
```

This tests:
- API health (`/`)
- Health endpoint (`/health`)
- Capabilities listing (`/api/v1/capabilities`)
- Authentication enforcement (401 without token)

## Step 8: Failure Simulation

Validate alerting with the failure simulation script:
```bash
python scripts/simulate_failure.py --scenario all --report
```

This simulates 8 failure scenarios and generates a JSON report of triggered alerts.

## Production Readiness Checklist

- [x] `.env.production` configured with all required secrets
- [x] LLM provider configured (`OPENAI_API_KEY` or equivalent)
- [x] `SECRET_KEY` set to 32+ characters
- [x] Docker images built with non-root user
- [x] Read-only filesystem enabled
- [x] Security headers configured
- [x] Authentication enforced (fail-closed)
- [x] Rate limiting configured
- [x] Health checks passing
- [x] Monitoring stack (ELK or Loki) running
- [x] Alert rules configured
- [x] Backup job scheduled
- [x] Smoke test passing
- [x] Failure simulation completed
- [x] Rollback procedure documented and tested