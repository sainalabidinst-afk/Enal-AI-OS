<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary

Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/rfcs/RFC-0010-database-engineer.md`
- Judul: Rfc 0010 Database Engineer
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# RFC-0010: Database Engineer Capability Pack

| Field | Value |
|-------|-------|
| **RFC ID** | RFC-0010 |
| **Status** | Draft |
| **Version** | 0.1.0 |
| **Author** | Enal AI OS Core Team |
| **Target Release** | v1.2.0 (Capability Excellence phase) |
| **Capability Pack** | Database Engineer |
| **Capability ID** | `database-engineer` |
| **Category** | Database |
| **Quality Target** | A- (≥85) |
| **Maturity Target** | Level 3 — Production Ready |
| **Reference RFC** | RFC-0010 |

---

## Motivation

ECP's Code Engineer generates database schemas, DevOps Assistant deploys database containers, and Data Engineer processes datasets. However, none of these packs provide deep database expertise—query optimization, index recommendation, migration planning, or performance analysis.
> Terjemahan Indonesia: ECP's Code Engineer generates database schemas, DevOps Assistant deploys database containers, dan Data Engineer processes datasets. However, none dari these packs menyediakan deep database expertise—query optimization, index recommendation, migration planning, or performance analysis.

Currently:
> Terjemahan Indonesia: Saat ini:

1. **Schema design is basic** — generated schemas lack optimization for query patterns, data type choices, and normalization levels.
2. **No query optimization** — generated SQL is syntactically correct but often poorly optimized.
3. **Migrations are manual** — no automated migration script generation, rollback planning, or conflict resolution.
4. **No index recommendation** — schemas lack indexes for common query patterns, leading to slow queries.
5. **Performance analysis is absent** — no detection of deadlocks, slow queries, or resource contention.
6. **No replication strategy** — no guidance on replication setup, backup strategies, or high availability.

The Database Engineer Capability Pack becomes the database expert layer, providing schema design, query optimization, migration management, replication planning, backup/recovery, and performance analysis for ECP's database operations.
> Terjemahan Indonesia: Database Engineer kapabilitas Pack becomes database expert layer, providing schema design, query optimization, migration management, replication planning, backup/recovery, dan performance analysis untuk ECP's database operations.

---

## Problem Statement

Without a dedicated Database Engineer Capability Pack:
> Terjemahan Indonesia: Without sebuah dedicated Database Engineer kapabilitas Pack:

- **No schema optimization** — generated schemas are functional but not performance-optimized for real-world query patterns.
- **No query performance analysis** — slow queries, missing indexes, and inefficient joins are not detected in generated SQL.
- **Migrations are error-prone** — no automated rollback planning, no conflict detection between migration branches.
- **No index recommendation** — missing indexes cause performance degradation that goes undetected.
- **Deadlock and performance issues are not anticipated** — no analysis of locking patterns or resource contention.
- **No backup and recovery strategy** — generated database deployments lack backup planning or disaster recovery.
- **Replication is not designed** — no guidance on read replicas, failover, or multi-region setups.

---

## Goals

1. **Schema Design** — Design optimized database schemas with appropriate data types, normalization, and constraints.
2. **Query Optimization** — Analyze and optimize SQL queries for performance.
3. **Migration Management** — Generate migration scripts with rollback planning and conflict resolution.
4. **Index Recommendation** — Recommend indexes based on query patterns and data access patterns.
5. **Replication Planning** — Design replication strategies for availability and performance.
6. **Backup and Recovery** — Plan backup strategies and recovery procedures.
7. **Performance Analysis** — Detect slow queries, deadlocks, and resource contention patterns.

### Success Criteria

| Metric | Target | Grade |
|--------|--------|-------|
| Schema Quality | ≥90% (schemas follow best practices) | A |
| Query Optimization | ≥85% (slow queries identified and improved) | A |
| Migration Safety | ≥95% (rollback plans present and correct) | A |
| Index Recommendation | ≥90% (missing indexes identified) | A |
| Performance Detection | ≥90% (slow queries, deadlocks detected) | A |
| Backup Coverage | ≥95% (backup strategies recommended) | A |
| Explainability | ≥90% (findings explained with remediation) | A |
| Consistency | ≥90% (same input produces same analysis) | A |

---

## Non-Goals

1. **Live database administration** — Database Engineer analyzes and recommends; it does not execute against live databases.
2. **Database-as-a-Service provisioning** — Focus is on design and optimization, not infrastructure provisioning.
3. **Replacing dedicated DBA tools** — Tools like pt-query-digest, SQL Server Profiler, or pg_stat_statements remain the source of truth.
4. **Database engine development** — Not building or modifying database engines.
5. **Core modification** — All implementation resides within the Database Engineer Capability Pack.

---

## Capability Scope

### Core Capabilities

| Capability | Description | Inputs | Outputs |
|-----------|-------------|--------|---------|
| Schema Design | Design optimized schemas with proper data types, normalization, constraints | Requirements, entity-relationship model | Schema DDL + design recommendations |
| Query Optimization | Analyze and fix slow or inefficient SQL queries | SQL queries, execution plans, query statistics | Optimized queries + performance recommendations |
| Migration Management | Generate forward and rollback migration scripts | Schema changes, current schema version | Migration script + rollback script + conflict analysis |
| Replication Planning | Design replication strategies for HA and performance | Topology requirements, workload profile | Replication design + setup steps |
| Backup and Recovery | Plan backup strategies and recovery procedures | Database type, RTO/RPO requirements | Backup plan + recovery runbook |
| Index Recommendation | Recommend indexes based on query patterns | Query logs, schema, access patterns | Index recommendations + priority ranking |
| Performance Analysis | Detect slow queries, deadlocks, and contention | Query logs, execution stats, lock waits | Performance report + remediation guidance |

### Out of Scope

- Live database administration or monitoring
- Database server provisioning or maintenance
- SQL query execution against production databases
- Database engine-specific tuning beyond configuration recommendations
- Cloud database service configuration (AWS RDS, Cloud SQL settings)

---

## Public Contracts

### Input Contract: Database Engineering Request

```json
{
  "request_id": "uuid",
  "operation": "schema_design | query_optimization | migration | index_recommendation | replication_plan | backup_plan | performance_analysis",
  "database_type": "postgresql | mysql | sqlite | mongodb | sqlserver",
  "schema": {
    "tables": [
      {
        "name": "string",
        "columns": [{"name": "string", "type": "string", "constraints": ["string"]}],
        "primary_key": ["string"],
        "foreign_keys": [{"column": "string", "references": "string", "references_column": "string"}]
      }
    ]
  },
  "queries": ["string — SQL queries to optimize"],
  "workload_profile": {
    "read_write_ratio": 0.0,
    "peak_qps": 0,
    "data_volume_gb": 0.0,
    "query_patterns": ["select | insert | update | delete | join | aggregate"]
  },
  "current_schema_version": "string",
  "target_schema_version": "string",
  "rto_hours": 0.0,
  "rpo_minutes": 0
}
```

### Output Contract: Database Engineering Report

```json
{
  "request_id": "uuid",
  "operation": "string",
  "findings": [
    {
      "id": "string",
      "category": "schema | query_performance | index | migration | replication | backup | deadlock",
      "severity": "critical | high | medium | low",
      "title": "string",
      "description": "string",
      "evidence": "object — query, table, execution plan",
      "recommendation": "string",
      "estimated_improvement": "string",
      "confidence": 0.0
    }
  ],
  "schema_recommendations": [
    {
      "table": "string",
      "column": "string",
      "current_type": "string",
      "recommended_type": "string",
      "reason": "string",
      "impact": "low | medium | high"
    }
  ],
  "index_recommendations": [
    {
      "table": "string",
      "columns": ["string"],
      "type": "btree | hash | gin | gsi",
      "priority": "high | medium | low",
      "estimated_query_time_saved_ms": 0,
      "confidence": 0.0
    }
  ],
  "migration_plan": {
    "forward_script": "string — SQL migration script",
    "rollback_script": "string — SQL rollback script",
    "conflicts": ["string"],
    "risk_score": 0.0,
    "estimated_downtime_minutes": 0
  },
  "replication_design": {
    "strategy": "master_slave | master_master | multi_master",
    "read_replicas": 0,
    "failover_scenario": "string",
    "expected_rto_minutes": 0,
    "expected_rpo_minutes": 0
  },
  "backup_plan": {
    "strategy": "full_incremental | differential | continuous_archiving",
    "schedule": "string",
    "backup_storage": "string",
    "retention_policy": "string",
    "recovery_steps": ["string"]
  },
  "performance_report": {
    "slow_queries": [
      {
        "query": "string",
        "current_execution_time_ms": 0,
        "estimated_optimized_time_ms": 0,
        "bottleneck": "string"
      }
    ],
    "deadlock_patterns": ["string"],
    "contention_areas": ["string"]
  },
  "summary": {
    "total_findings": 0,
    "critical_count": 0,
    "high_count": 0,
    "medium_count": 0,
    "low_count": 0,
    "overall_risk": "critical | high | medium | low",
    "confidence": 0.0
  }
}
```

### Database Analysis Record (Experience Memory)

```json
{
  "record_id": "uuid",
  "request_id": "uuid",
  "timestamp": "ISO 8601",
  "database_type": "string",
  "operation": "string",
  "tables_analyzed": 0,
  "queries_optimized": 0,
  "indexes_recommended": 0,
  "migration_risk_score": 0.0,
  "outcome": "success | partial | failed | revised",
  "revisions": [{"revision_id": "uuid", "changes": "string"}]
}
```

---

## Integration Points (Capability Graph)

```
Consumer Capability Pack (Code Engineer, Data Engineer, DevOps Assistant)
    │
    │  submits database artifact for analysis via task/intent
    ▼
Execution Runtime
    │
    │  routes to Database Engineer Domain Engine
    ▼
Database Engineer Engine
    │
    │  ┌──────────────────────────────────────────┐
    │  │ 1. Schema Design                         │
    │  │ 2. Query Optimization                    │
    │  │ 3. Migration Management                  │
    │  │ 4. Index Recommendation                  │
    │  │ 5. Replication Planning                  │
    │  │ 6. Backup and Recovery                   │
    │  │ 7. Performance Analysis → Experience     │
    │  │    Memory                                │
    │  └──────────────────────────────────────────┘
    │
    │  returns Database Engineering Report
    ▼
Consumer Capability Pack
    │
    │  receives optimization recommendations
    ▼
User / Human Approval Loop
```

### Task Template

| Task | Subtasks |
|------|----------|
| Database Analysis | Schema analysis → Query analysis → Index recommendation → Migration planning → Replication design → Backup planning → Performance analysis → Report |

---

## Consumer Capability Packs

| Consumer Capability Pack | Use Case |
|--------------------------|----------|
| **Code Engineer** | Review generated schema DDL, optimize queries, recommend indexes |
| **Data Engineer** | Optimize ETL/ELT query performance, recommend partitioning |
| **DevOps Assistant** | Review database deployment configurations, backup/restore planning |

---

## Dependencies

### Internal Dependencies (Shared Contracts)

1. **Execution Runtime** — Task routing and orchestration (per ADR-002)
2. **Experience Memory** — Database analysis records persistence (per ADR-011)
3. **Shared Contracts** — Task/Intent definition and result schema (per ADR-006)

### Database Engines Supported

1. **PostgreSQL** — Primary support: pg_catalog, explain plans, indexing strategies
2. **MySQL** — MySQL-specific query optimization and indexing
3. **SQLite** — Lightweight schema and query analysis
4. **MongoDB** — NoSQL schema design and query optimization
5. **SQL Server** — SQL Server-specific optimization (future)

### No Core Changes Required

All implementation resides within the Database Engineer Capability Pack:
> Terjemahan Indonesia: All implementation resides within Database Engineer kapabilitas Pack:

```
apps/
└── database_engineer/
    ├── engine.py              # Domain Engine (per ADR-004)
    ├── worker.py              # Thin adapter (per ADR-003)
    ├── schemas.py             # Public contracts
    ├── schema_designer.py     # Schema design
    ├── query_optimizer.py     # Query optimization
    ├── migration_manager.py   # Migration management
    ├── index_advisor.py       # Index recommendation
    ├── replication_planner.py # Replication planning
    ├── backup_planner.py      # Backup and recovery
    ├── performance_analyzer.py # Performance analysis
    └── dialect/               # SQL dialect-specific analyzers
        ├── postgresql.py
        ├── mysql.py
        └── sqlite.py
```

**ADR Impact:** None. No Core, Runtime, Kernel, or shared contract modification required.

---

## Benchmark Specification

### Benchmark Framework

| Dimension | Definition | Measurement | Target |
|-----------|------------|-------------|--------|
| **Schema Quality** | % of schemas following best practices | % of schemas with correct data types, constraints | ≥90% |
| **Query Optimization** | % of slow queries identified and improved | % of queries with performance improvement | ≥85% |
| **Migration Safety** | % of migrations with correct rollback plans | % of migrations with valid rollback | ≥95% |
| **Index Recommendation** | % of missing indexes identified | % of queries that would benefit from recommended indexes | ≥90% |
| **Performance Detection** | % of slow queries, deadlocks detected | % of ground truth issues found | ≥90% |
| **Backup Coverage** | % of databases with backup strategy | % of scenarios with backup plan | ≥95% |
| **Explainability** | Clarity of findings and recommendations | Human evaluation score | ≥90% |
| **Consistency** | Same input produces same output | Variance across 10 runs < 5% | ≥90% |

### Benchmark Dataset

- **100 database projects** covering:
  - PostgreSQL: e-commerce, analytics, SaaS multi-tenant
  - MySQL: web applications, CMS, OLTP systems
  - SQLite: embedded applications, mobile apps
  - MongoDB: document stores, content management
> Terjemahan Indonesia: PostgreSQL: e-commerce, analytics, SaaS multi-tenant MySQL: web applications, CMS, OLTP systems SQLite: embedded applications, mobile apps MongoDB: dokumen stores, konten management

### Benchmark Dimensions Detail

| Scenario Type | Description | Ground Truth |
|---------------|-------------|-------------|
| Slow Query | Unoptimized query with missing indexes | Expert-optimized query |
| Deadlock | Concurrent transactions with lock contention | Deadlock detection logs |
| Migration | Schema change requiring forward + rollback scripts | Expert-reviewed migration |
| Rollback | Safe rollback from a migration | Manual rollback procedures |
| Index Recommendation | Query with missing beneficial index | Expert-identified indexes |

---

## Golden Test Specification

| # | Scenario | Expected Outcome | Acceptance Criteria |
|---|----------|-----------------|---------------------|
| 1 | Slow query without index | Index recommended, query optimized | ≥90% query improvement |
| 2 | Migration with conflict | Rollback script + conflict analysis | ≥95% migration safety |
| 3 | Deadlock-prone transactions | Deadlock detected, lock order recommended | ≥90% detection |
| 4 | Schema with wrong data types | Data type recommendations provided | ≥90% correctness |
| 5 | Missing index on foreign key | Index recommended | ≥90% detection |
| 6 | Backup planning for PostgreSQL | Backup strategy with RTO/RPO | ≥95% coverage |
| 7 | Replication design for HA | Master-slave with failover plan | ≥90% completeness |
| 8 | Query with N+1 problem | N+1 detected, JOIN/Eager loading suggested | ≥90% detection |
| 9 | Index recommendation for aggregation | Index for GROUP BY suggested | ≥90% detection |
| 10 | Rollback script validation | Rollback produces correct schema | ≥95% correctness |

### Golden Test Acceptance Criteria

- All 10 golden test scenarios pass at ≥90% of acceptance criteria (100% pass)
- Overall Database Engineer golden test pass rate ≥90%
- All migration plans include rollback scripts
- No harmful recommendations in generated DDL

---

## Real Case Requirements

### The Directory

`real_cases/database_engineer/` must contain:
> Terjemahan Indonesia: Real_cases/database_engineer/ must contain:

| Requirement | Minimum Count |
|-------------|---------------|
| Real database projects from actual usage | 20 |
| Cases with slow query optimization | 5 |
| Cases with migration and rollback planning | 5 |
| Cases with deadlock analysis | 3 |
| Cases with index recommendations | 5 |
| Cases with expert review/validation | 15 |

### Real Case Structure

```
real_cases/database_engineer/<case_id>/
├── input/
│   ├── schema.sql
│   ├── queries.sql
│   └── workload_profile.json
├── output/
│   ├── report.json          # Full Database Engineering Report
│   └── recommendations.md   # Human-readable recommendations
└── evaluation.md            # Ground truth, expert review, lessons learned
```

### Real Case Targets

| Metric | Target |
|--------|--------|
| Real cases logged | ≥20 (Level 3) → ≥100 (Level 4) |
| Real case quality score (expert review) | ≥90% |
| Query performance improvement (avg) | ≥40% reduction in execution time |

---

## Definition of Done

```text
Definition of Done — Database Engineer Capability Pack

Functional
- [ ] Schema Design produces optimized DDL with appropriate data types and constraints
- [ ] Query Optimization identifies and fixes slow/inefficient queries
- [ ] Migration Management generates forward + rollback scripts with conflict analysis
- [ ] Index Recommendation identifies missing indexes based on query patterns
- [ ] Replication Planning designs strategies for HA and performance
- [ ] Backup and Recovery plans with RTO/RPO alignment
- [ ] Performance Analysis detects slow queries, deadlocks, and contention

Benchmark
- [ ] Schema Quality ≥ 90% (grade A-)
- [ ] Query Optimization ≥ 85%
- [ ] Migration Safety ≥ 95%
- [ ] Index Recommendation ≥ 90%
- [ ] Performance Detection ≥ 90%
- [ ] Backup Coverage ≥ 95%
- [ ] Explainability ≥ 90%
- [ ] Consistency ≥ 90%

Golden Tests
- [ ] All 10 pack golden test scenarios pass at ≥90% of acceptance criteria (100% pass)

Real Cases
- [ ] ≥ 20 real cases logged in real_cases/database_engineer/
- [ ] Evaluation notes recorded for each case
- [ ] ≥ 5 cases with slow query optimization
- [ ] ≥ 5 cases with migration and rollback planning
- [ ] ≥ 3 cases with deadlock analysis
- [ ] ≥ 5 cases with index recommendations

Documentation
- [ ] Capability Guide updated (CAPABILITY_GUIDE.md — Database Engineer section)
- [ ] API reference / contract updated (this RFC + schemas.py)
- [ ] Real case evaluation summary published

SDK
- [ ] Pack accessible via SDK without Core changes
- [ ] Database Engineer callable via Execution Runtime task routing

Performance
- [ ] Latency P95 < 3000ms for single database analysis
- [ ] Latency P95 < 8000ms for multi-table schema with 50+ queries

Security
- [ ] No known P0/P1 security issues
- [ ] Generated DDL does not contain unsafe permissions

Regression
- [ ] No regression in existing Capability Pack benchmark dimensions
- [ ] Benchmark reproducible (documented command + persisted result)

Release Notes
- [ ] Capability Changelog updated
```

---

## Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Query optimization recommendations are incorrect | Medium — performance degradation | Medium | Conservative recommendations with confidence scores; user review required |
| Migration rollback scripts fail in production | Critical — data loss | Low | Extensive validation on test schemas; automated rollback simulation |
| Index recommendations cause write performance degradation | Medium — slower writes | Medium | Cost-benefit analysis; consider read/write ratio |
| Deadlock analysis misses complex patterns | Medium — undetected contention | Medium | Pattern-based + heuristic analysis; regular update cycle |
| Schema design recommendations conflict with existing apps | Medium — migration complexity | High | Schema version tracking; backward compatibility checks |
| Replication plan doesn't account for network latency | Medium — failover delays | Low | Latency-aware design; multi-region considerations |
| Backup plan doesn't meet actual RPO | Medium — data loss window | Low | RPO validation checks; retention policy alignment |

---

## ADR Impact

**Does this require Core changes?** No.

Database Engineer is a **new Capability Pack** that follows the established patterns:
> Terjemahan Indonesia: Database Engineer adalah sebuah new kapabilitas Pack itu follows established patterns:

- **ADR-001 (Core Pipeline Freeze):** No Core changes. All logic in `apps/database_engineer/`.
- **ADR-002 (Capability Pack Independence):** Database Engineer communicates with other packs via Execution Runtime tasks and shared contracts only. No direct imports.
- **ADR-003 (Worker = Adapter Only):** A thin Worker routes tasks to the Domain Engine.
- **ADR-004 (Domain Engine Owns Business Logic):** All database analysis logic resides in `apps/database_engineer/engine.py`.
- **ADR-005 (Human Approval Required):** All DDL/script generation is recommendation; execution requires explicit user approval.
- **ADR-006 (Capability Contract v1 Frozen):** Uses the existing Capability Contract for node and subtask template registration. No contract changes.
- **ADR-007 (Conversation Boundary):** Database Engineer is invoked through Execution Runtime, not directly by Conversation Manager.
- **ADR-008 (Core Change Requires Cross-Capability Proof):** Not applicable — no Core changes.

**ADR Required:** None. This is a new Capability Pack, not a Core modification.

---

## Rollout Plan

### Phase 1: Prototype (RFC → Experimental)

**Duration:** 5 weeks

- [ ] Create `apps/database_engineer/` package structure
- [ ] Implement basic schema analysis for PostgreSQL
- [ ] Implement query optimization (missing index detection)
- [ ] Implement basic index recommendation
- [ ] Define public contracts (Database Request, Report)
- [ ] Implement thin Worker adapter
- [ ] Create 10 golden test scenarios
- [ ] Integration: Code Engineer → Database Engineer (schema review)
- [ ] Integration: Data Engineer → Database Engineer (ETL query optimization)
- **Gate:** 10 golden tests pass at ≥80%

### Phase 2: Full Capabilities (Experimental → Stable)

**Duration:** 7 weeks

- [ ] Implement migration management with rollback planning
- [ ] Implement replication planning (master-slave patterns)
- [ ] Implement backup and recovery planning
- [ ] Implement performance analysis (slow queries, deadlocks)
- [ ] Add MySQL and SQLite dialect support
- [ ] Expand golden tests to 10 full scenarios
- [ ] Log ≥20 real cases from Code Engineer and DevOps usage
- [ ] **Benchmark:** 100 projects, ≥90% schema quality, ≥95% migration safety
- [ ] **Integration:** DevOps Assistant starts using Database Engineer for deployment review
- **Gate:** All 10 golden tests pass at ≥90%; benchmark ≥90%

### Phase 3: Ecosystem (Stable → Certified)

**Duration:** 6 weeks

- [ ] All 3 consumer packs fully integrated
- [ ] Add MongoDB schema design support
- [ ] Deadlock analysis validated on real workloads
- [ ] Independent audit of migration safety and index recommendations
- [ ] Public benchmark dashboard available
- [ ] **Benchmark:** ≥90% across all dimensions sustained
- [ ] **Real Cases:** ≥100 cases with ≥80% expert validation
- **Gate:** Independent audit passed; benchmark ≥90% sustained

---

## Future Enhancements

### Fase 2 (Post-v1.0.0 Release)

1. **Database Migration Orchestration** — Automated migration sequencing across environments
2. **Query Plan Visualization** — Interactive visualization of execution plans and bottlenecks
3. **Partition Strategy Advisor** — Recommend partitioning schemes for large tables
4. **Capacity Planning** — Predict storage and compute requirements based on growth projections

### Fase 3 (Enterprise)

1. **Multi-Database Orchestration** — Manage schemas and migrations across PostgreSQL, MySQL, MongoDB, SQL Server
2. **Database Security Assessment** — Privilege analysis, data masking recommendations, encryption at rest
3. **Cross-Workspace Database Governance** — Central policy management and compliance reporting
4. **Database Performance Observability** — Continuous monitoring and alerting for production databases

### Long-term

1. **Automated Database Tuning** — ML-based parameter tuning and index optimization
2. **Database Failure Prediction** — Predict failures based on performance metrics and query patterns
3. **Database Cost Optimization** — Recommend cost-optimal database configurations and instance types
4. **Database Architecture Advisor** — Recommend database topology, sharding, and caching strategies
