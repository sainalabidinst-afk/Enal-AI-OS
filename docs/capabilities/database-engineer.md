<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: isi utama dokumen disajikan dalam versi Indonesia di bawah konten asli.
- English: the main prose content is presented in an Indonesian bilingual section below the original content.

### Informasi Dokumen / Document Info
- File: `docs/capabilities/database-engineer.md`
- Judul: Database Engineer
- Status: bilingual content applied

<!-- BILINGUAL_DOCS_END -->

# Database Engineer Capability Specification

## Version: 1.0.0
## Status: Production Ready (RFC-0010)
## Quality Target: A- (≥85)

---

## 1. Purpose

Database Engineer adalah **otoritas rekayasa basis data** untuk ECP — Capability Pack yang
menangani desain skema, optimasi query, manajemen migrasi, rekomendasi indeks,
perencanaan replikasi, rencana backup, dan analisis performa database.
> Terjemahan Indonesia: Database Engineer adalah otoritas rekayasa basis data untuk ECP — kapabilitas Pack yang menangani desain skema, optimasi query, manajemen migrasi, rekomendasi indeks, perencanaan replikasi, rencana backup, dan analisis performa database.

Capability Pack ini menganalisis skema database, query SQL, dan profil beban untuk
memberikan rekomendasi desain dan optimasi — **tanpa memodifikasi Core**.
> Terjemahan Indonesia: Kapabilitas Pack ini menganalisis skema database, query SQL, dan profil beban untuk memberikan rekomendasi desain dan optimasi — tanpa memodifikasi Core.

---

## 2. Scope

### In Scope
- **Schema Design** — Desain skema teroptimasi dengan tipe data, normalisasi, constraint
- **Query Optimization** — Analisa dan perbaiki SQL lambat atau tidak efisien
- **Migration Management** — Generate script migrasi forward dan rollback
- **Index Recommendation** — Rekomendasi indeks berdasarkan pola query
- **Replication Planning** — Desain strategi replikasi untuk HA dan performa
- **Backup and Recovery** — Rencana strategi backup dan prosedur pemulihan
- **Performance Analysis** — Deteksi slow query, deadlock, contention
- **Experience Memory** — Perekaman hasil ke history

### Out of Scope
- Administrasi database live
- Provisioning infrastruktur database
- Eksekusi SQL ke database produksi
- Konfigurasi cloud database service
- Modifikasi Core contracts

---

## 3. Contract

### Input: DatabaseRequest
```json
{
  "request_id": "uuid",
  "operation": "schema_design | query_optimization | migration | index_recommendation | replication_plan | backup_plan | performance_analysis",
  "database_type": "postgresql | mysql | sqlite | mongodb | sqlserver",
  "schema": {
    "tables": [
      {
        "name": "users",
        "columns": [{"name": "id", "type": "INTEGER", "constraints": ["PRIMARY KEY"]}],
        "primary_key": ["id"],
        "foreign_keys": [{"column": "user_id", "references": "users", "references_column": "id"}]
      }
    ]
  },
  "queries": ["SELECT * FROM users WHERE email = ?"],
  "workload_profile": {
    "read_write_ratio": 0.8,
    "peak_qps": 500,
    "data_volume_gb": 50,
    "query_patterns": ["select", "join", "aggregate"]
  },
  "current_schema_version": "v1",
  "target_schema_version": "v2",
  "rto_hours": 4.0,
  "rpo_minutes": 60
}
```

### Output: DatabaseReport
```json
{
  "request_id": "uuid",
  "operation": "string",
  "findings": [
    {
      "id": "uuid",
      "category": "schema | query_performance | index | migration | replication | backup | deadlock",
      "severity": "critical | high | medium | low",
      "title": "Missing index on users.email",
      "description": "Query scans full table without index",
      "evidence": {"query": "SELECT * FROM users WHERE email = ?"},
      "recommendation": "CREATE INDEX idx_users_email ON users(email)",
      "estimated_improvement": "10x faster",
      "confidence": 0.9
    }
  ],
  "schema_recommendations": [
    {"table": "users", "action": "add_constraint", "priority": "high", "rationale": "..."}
  ],
  "index_recommendations": [
    {"table": "users", "columns": ["email"], "index_type": "btree", "priority": "high"}
  ],
  "migration_plan": {
    "from_version": "v1",
    "to_version": "v2",
    "steps": [{"step_number": 1, "action": "CREATE", "sql": "...", "rollback_sql": "..."}],
    "rollback_available": true
  },
  "replication_design": {
    "strategy": "primary_replica",
    "topology": "1 primary + N read replicas",
    "nodes": [{"role": "primary", "purpose": "write traffic"}],
    "failover_strategy": "automatic",
    "estimated_lag_ms": 50
  },
  "backup_plan": {
    "schedule": "hourly",
    "backup_type": "incremental",
    "retention_days": 30,
    "rto_hours": 4.0,
    "rpo_minutes": 60,
    "steps": ["Verify backup integrity", "Restore backup", ...]
  },
  "performance_stats": {
    "slow_queries": 5,
    "deadlocks_detected": 0,
    "avg_query_time_ms": 150.0,
    "peak_connections": 50,
    "cache_hit_ratio": 0.92
  },
  "explanation": "string — human-readable analysis summary"
}
```

---

## 4. Operations

| Operation | Description | Inputs | Outputs |
|-----------|-------------|--------|---------|
| schema_design | Analyze and optimize schema | schema, database_type | SchemaRecommendations |
| query_optimization | Optimize SQL queries | queries, database_type | Findings + OptimizedQueries |
| migration | Generate migration scripts | from_version, to_version, schema | MigrationPlan |
| index_recommendation | Recommend indexes | queries, schema, workload | IndexRecommendations |
| replication_plan | Design replication topology | workload, database_type | ReplicationDesign |
| backup_plan | Plan backup strategy | database_type, rto, rpo | BackupPlan |
| performance_analysis | Analyze performance | queries, schema, workload | Findings + PerformanceStats |

---

## 5. Analyzer Modules

| Module | Responsibility |
|--------|----------------|
| schema_designer.py | Analyze and recommend schema optimizations |
| query_optimizer.py | Analyze and optimize SQL queries |
| migration_manager.py | Generate migration and rollback scripts |
| index_advisor.py | Recommend indexes based on query patterns |
| replication_planner.py | Design replication strategies |
| backup_planner.py | Plan backup and recovery strategies |
| performance_analyzer.py | Detect slow queries, deadlocks, contention |

---

## 6. Benchmark Dimensions

| Dimension | Target | Grade |
|-----------|--------|-------|
| Schema Quality | ≥90% | A |
| Query Optimization | ≥85% | A |
| Migration Safety | ≥95% | A |
| Index Recommendation | ≥90% | A |
| Performance Detection | ≥90% | A |
| Backup Coverage | ≥95% | A |
| Explainability | ≥90% | A |
| Consistency | ≥90% | A |

---

## 7. Dependencies

- **apps/base.py** — Base model definitions
- **apps/database_engineer/schemas.py** — Public contracts
- **apps/database_engineer/engine.py** — Domain Engine
- **apps/database_engineer/worker.py** — Thin adapter (ADR-003)

---

## 8. Usage Example

```python
from apps.database_engineer.engine import DatabaseEngineerEngine
from apps.database_engineer.schemas import DatabaseRequest, DatabaseType

engine = DatabaseEngineerEngine()
request = DatabaseRequest(
    operation="query_optimization",
    database_type=DatabaseType.postgresql,
    queries=["SELECT * FROM users WHERE email = 'test@example.com'"],
)
report = engine.analyze(request)
print(f"Found {len(report.findings)} optimization opportunities")
```
