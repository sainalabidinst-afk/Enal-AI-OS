# Database Engineer — Spesifikasi Capability

**Versi:** 2.0.0
**Status:** Production Ready (RFC-0010)
**Target Kualitas:** A (≥90), Domain Expert (L4)
**Sertifikasi:** Certified Lifecycle (RFC-0010)

---

## 1. Tujuan

Database Engineer adalah **otoritas rekayasa database** untuk ECP — Capability Pack yang menangani schema design, query optimization, migration management, index recommendation, replication planning, backup/recovery planning, dan performance analysis database.

Capability Pack ini menganalisis skema database, query SQL, dan workload profile untuk memberikan rekomendasi desain dan optimasi — **tanpa memodifikasi Core**.

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- **Schema Design** — Desain skema teroptimasi dengan tipe data, normalisasi, constraint
- **Query Optimization** — Analisis dan perbaikan SQL yang lambat atau tidak efisien
- **Migration Management** — Menghasilkan migration script maju dan rollback
- **Index Recommendation** — Rekomendasi indeks berdasarkan pola query
- **Replication Planning** — Merancang strategi replikasi untuk HA dan kinerja
- **Backup & Recovery** — Rencana strategi backup dan prosedur pemulihan
- **Performance Analysis** — Mendeteksi slow query, deadlock, contention
- **Execution Plan Analysis** — Analisis explain plan untuk query optimization
- **Partitioning Strategy** — Rekomendasi partitioning untuk large tables
- **High Availability Design** — Merancang topology HA dan failover
- **Experience Memory** — Merekam hasil ke riwayat

### Di Luar Cakupan
- Administrasi database langsung
- Penyediaan infrastruktur database
- Eksekusi SQL ke database produksi
- Konfigurasi layanan database berbasis cloud
- Modifikasi kontrak Core

---

## 3. Kontrak

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

### Output: Laporan Database
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
    "steps": ["Verify backup integrity", "Restore backup", "..."]
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

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `schema_design` | Menganalisis dan mengoptimalkan skema | schema, database_type | Schema Recommendations |
| `query_optimization` | Mengoptimalkan query SQL | queries, database_type | Findings + Optimized Queries |
| `migration` | Menghasilkan migration script | from_version, to_version, schema | Migration Plan |
| `index_recommendation` | Merekomendasikan indeks | queries, schema, workload_profile | Index Recommendations |
| `replication_plan` | Mendesain topologi replikasi | workload_profile, database_type | Replication Design |
| `backup_plan` | Merencanakan strategi backup | database_type, rto, rpo | Backup Plan |
| `performance_analysis` | Menganalisis performa | queries, schema, workload_profile | Findings + Performance Stats |

---

## 5. Modul Analyzer

| Modul | Tanggung Jawab |
|--------|----------------|
| `schema_designer.py` | Menganalisis dan merekomendasikan perbaikan skema |
| `query_optimizer.py` | Menganalisis dan mengoptimalkan query SQL |
| `migration_manager.py` | Menghasilkan migration script dan rollback |
| `index_advisor.py` | Merekomendasikan indeks berdasarkan pola query |
| `replication_planner.py` | Merancang strategi replikasi |
| `backup_planner.py` | Merencanakan strategi backup dan pemulihan |
| `performance_analyzer.py` | Mendeteksi slow query, deadlock, contention |
| `database_knowledge.py` | Pengetahuan khusus vendor (PostgreSQL, MySQL, MongoDB, Redis, Timeseries) |
| `partitioning_advisor.py` | Merekomendasikan strategi partitioning untuk large tables |
| `ha_designer.py` | Merancang topology HA dan failover strategy |

---

## 6. Dimensi Benchmark

**Hasil Terverifikasi:**
- Overall: 95.00%
- Pass rate: 100%
- Status: PASS (A Certified)


| Dimensi | Target | Grade |
|-----------|--------|-------|
| Schema Quality | ≥95% | A |
| Query Optimization | ≥95% | A |
| Migration Safety | ≥95% | A |
| Index Recommendation | ≥95% | A |
| Performance Detection | ≥95% | A |
| Backup Coverage | ≥95% | A |
| Explainability | ≥90% | A |
| Consistency | ≥95% | A |

Benchmark: `benchmarks/database_engineer_benchmark.py`

---

## 7. Dependensi

- **apps/base.py** — Definisi model dasar
- **apps/database_engineer/schemas.py** — Kontrak publik
- **apps/database_engineer/schema_designer.py** — Analisis dan rekomendasi skema
- **apps/database_engineer/query_optimizer.py** — Analisis dan optimasi query SQL
- **apps/database_engineer/migration_manager.py** — Migration script dan rollback
- **apps/database_engineer/index_advisor.py** — Rekomendasi indeks
- **apps/database_engineer/replication_planner.py** — Strategi replikasi
- **apps/database_engineer/backup_planner.py** — Strategi backup dan pemulihan
- **apps/database_engineer/performance_analyzer.py** — Deteksi slow query, deadlock
- **apps/database_engineer/database_knowledge.py** — Pengetahuan khusus vendor
- **apps/database_engineer/partitioning_advisor.py** — Strategi partitioning
- **apps/database_engineer/ha_designer.py** — Topologi HA dan failover
- **apps/database_engineer/engine.py** — Orchestrator domain engine
- **apps/database_engineer/worker.py** — Adaptor worker tipis (ADR-003)

---

## 8. Contoh Penggunaan

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

---

## 9. Audit Keamanan

| Aspek | Status | Catatan |
|--------|--------|---------|
| Input Validation | ✅ | Query divalidasi untuk tipe dan ukuran |
| SQL Injection Prevention | ✅ | Hanya menganalisis query — tidak mengeksekusi |
| Sensitive Data Handling | ✅ | Tidak mengekspos data sensitif dalam output |
| Access Control | ✅ | Hanya membaca schema dan query — tidak menulis |
| Audit Trail | ✅ | Semua finding dicatat dengan timestamp |

**Catatan Keamanan:**
- Database Engineer hanya menganalisis query dan schema — tidak mengeksekusi SQL.
- Query yang dianalisis di-log tanpa parameter sensitif.
- Migration plan disajikan sebagai recommendation — memerlukan persetujuan manusia untuk execution.

---

## 10. Optimasi Kinerja

| Aspek | Rekomendasi | Dampak |
|--------|-------------|--------|
| Query Optimization | AST-based analysis + pre-compiled patterns | Faster query analysis |
| Schema Analysis | Incremental analysis untuk perubahan skema | Reduced computation |
| Index Advisor | Query fingerprint caching | Avoid recomputation |
| Performance Analyzer | Explain plan caching | Instant re-analysis |
| Migration Manager | Template-based migration generation | Mengurangi LLM call |
| Database Knowledge | Vendor-specific knowledge base | Faster lookup |
| Result Caching | Cache report untuk schema yang tidak berubah | Instant re-scan |

**Target Throughput:**
- Query analysis (100 queries): < 5 detik
- Schema analysis (50 tables): < 3 detik
- Index recommendation: < 2 detik
- Migration plan: < 1 detik

---

## 11. Skenario Golden Test

| # | Skenario | Input | Output yang Diharapkan |
|---|----------|-------|------------------------|
| 1 | Optimalisasi Query Missing Index | SELECT dengan JOIN tanpa index | Missing index + CREATE INDEX recommendation |
| 2 | Rekomendasi Index Komposit | 2 query dengan filter + ORDER BY | 2+ index recommendations |
| 3 | Migration Plan v1 ke v2 | Schema v1, target v2 | Migration plan + rollback SQL |
| 4 | Strategi Replikasi HA | Workload profile, RTO/RPO | Topology + failover strategy |
| 5 | Rencana Backup & Recovery | DB type, RTO/RPO | Backup schedule + recovery procedure |
| 6 | Analisis Deadlock | Concurrent UPDATE queries | Deadlock risk + isolation level rec |
| 7 | Explain Plan Analysis | SELECT dengan GROUP BY | Explain plan + optimization |
| 8 | Desain Skema Multi-Tenant | E-commerce schema + 1000 tenants | RLS policy + partitioning strategy |
| 9 | Partitioning Strategy | Events table 1TB+ | Partition key + maintenance strategy |
| 10 | Desain Database Vector | Embeddings table, vector search | HNSW index + similarity metric |

Golden Tests: `golden_tests/database_engineer/`

