# Evaluation

Scenario: infra-002 - HA Cluster PostgreSQL

## Architecture Review
- 3-node cluster with Patroni for automatic failover
- Synchronous replication across nodes correctly configured
- Etcd quorum for consensus properly set up
- Load balancer (HAProxy) fronting database nodes

## Improvements
- Add backup/restore procedures (pgBackRest)
- Implement connection pooling (PgBouncer)
- Monitor replication lag with custom metrics
