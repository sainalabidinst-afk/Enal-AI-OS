# Infrastructure Engineer — Spesifikasi Capability

**Versi:** 1.0.0
**Status:** Draft (RFC-0014)
**Target Kualitas:** A (≥90)

---

## 1. Tujuan

Infrastructure Engineer adalah **otoritas desain infrastruktur** untuk ECP — Capability Pack yang menerjemahkan kebutuhan bisnis (SLA, biaya, keamanan) menjadi spesifikasi infrastruktur yang dapat dieksekusi, terukur, dan handal untuk Kubernetes, klaster HA, storage, dan disaster recovery.

Capability Pack ini merancang klaster Kubernetes, topologi klaster HA, solusi storage, rencana DR — **tanpa memodifikasi Core**.

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- **Kubernetes Design** — Desain klaster K8s, workload, jaringan, RBAC, network policy
- **HA Cluster Design** — Desain klaster HA dengan failover, load balancer, dan quorum
- **Storage Design** — Desain block, file, object, dan storage terdistribusi (Ceph)
- **Disaster Recovery Planning** — Strategi DR, RPO/RTO, backup schedule
- **Infrastructure Assessment** — Gap analysis dan rekomendasi peningkatan
- **Security Hardening** — CIS Kubernetes Benchmark, encryption, access control
- **Cost Estimation** — Estimasi biaya infrastruktur bulanan
- **Compliance** — Check kepatuhan (CIS, SOC2, ISO 27001)

### Di Luar Cakupan
- Provisioning otomatis (Terraform, CloudFormation, Pulumi)
- Monitoring operasional (Prometheus, Grafana, OpenTelemetry)
- Manajemen konfigurasi (Ansible, Chef, Puppet)
- Penanganan insiden (PagerDuty, Opsgenie)
- Implementasi CI/CD
- Modifikasi kontrak Core

---

## 3. Kontrak

### Input: InfrastructureEngineerRequest
```json
{
  "request_id": "uuid",
  "operation": "kubernetes_design | ha_cluster_design | storage_design | disaster_recovery_plan | infrastructure_assessment",
  "business_context": {
    "domain": "e-commerce | fintech | healthcare",
    "project_name": "string",
    "description": "string"
  },
  "quality_attributes": {
    "availability_target": "99.9%",
    "performance_target": "< 200ms",
    "durability_target": "99.999999999%",
    "security_target": "OWASP + CIS benchmarks"
  },
  "infrastructure_type": "kubernetes | ha_cluster | storage | disaster_recovery | hybrid",
  "output_format": "yaml | json | markdown | terraform | helm",
  "inputs": {
    "cluster_name": "string",
    "node_count": 3,
    "instance_type": "t3.medium",
    "storage_specs": [{"name": "string", "size_gb": 100, "type": "block", "tier": "hot"}],
    "strategy": "warm_standby",
    "rpo_minutes": 60,
    "rto_minutes": 240
  }
}
```

### Output: InfrastructureEngineerReport
```json
{
  "request_id": "uuid",
  "operation": "string",
  "kubernetes_spec": {
    "cluster_name": "string",
    "kubernetes_version": "1.28",
    "network_policy": true,
    "rbac_enabled": true,
    "pod_security_standard": "restricted",
    "resource_quotas": true,
    "limit_ranges": true,
    "nodes": [{"count": 3, "instance_type": "t3.large", "labels": {}}],
    "network": {"cidr": "10.0.0.0/16", "subnet_count": 3}
  },
  "cluster_spec": {
    "cluster_name": "string",
    "ha_mode": "active_standby",
    "nodes": [{"count": 3}],
    "failover": {"mode": "active_standby", "heartbeat_interval_seconds": 5},
    "load_balancer": "haproxy"
  },
  "storage_specs": [
    {"name": "vol-1", "size_gb": 100, "storage_type": "block", "storage_tier": "hot", "replicas": 3, "encryption": true}
  ],
  "dr_plan": {
    "strategy": "warm_standby",
    "primary_region": "us-east-1",
    "secondary_region": "us-west-2",
    "rpo": {"rpo_minutes": 15, "rto_minutes": 60},
    "backup_schedule": {"frequency": "daily", "retention_days": 30}
  },
  "cost_estimate": {"total_monthly": 240.0},
  "security_hardening": ["PodSecurityStandard 'restricted' diaktifkan", "..."],
  "compliance_status": {"rpo_within_target": true, "backup_encrypted": true},
  "recommendations": ["string"],
  "quality_score": 0.92,
  "explanation": "string"
}
```

---

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `kubernetes_design` | Desain klaster Kubernetes | SLA target, instance type, node count | KubernetesSpec |
| `ha_cluster_design` | Desain klaster HA | SLA target, node count, shared storage | ClusterSpec |
| `storage_design` | Desain solusi storage | Kapasitas, I/O requirements, tier | VolumeSpec, StorageClassSpec |
| `disaster_recovery_plan` | Rencana DR | RPO/RTO target, anggaran, region | DRPlan |
| `infrastructure_assessment` | Penilaian infrastruktur | Current state, target state | Laporan gap + rekomendasi |

---

## 5. Modul Designer

| Modul | Tanggung Jawab |
|--------|----------------|
| `kubernetes_designer.py` | Desain klaster Kubernetes, node, jaringan, keamanan |
| `ha_cluster_designer.py` | Desain klaster HA, failover, load balancer, quorum |
| `storage_designer.py` | Desain block, file, object, distributed storage |
| `disaster_recovery.py` | Perencanaan DR, RPO/RTO, backup schedule |

---

## 6. Dimensi Benchmark

| Dimensi | Target | Grade |
|-----------|--------|-------|
| Kualitas Desain K8s | ≥90% | A |
| Ketersediaan Klaster | ≥99.9% | A |
| Kualitas Desain Storage | ≥90% | A |
| Akurasi DR Plan | RPO/RTO ±5% dari target | A |
| Skor Keamanan | ≥95% | A+ |
| Keakuratan Estimasi Biaya | ±10% dari aktual | A |
| Kepatuhan | ≥95% | A |
| Konsistensi | ≥90% | A |

---

## 7. Dependensi

- **apps/base.py** — Definisi model dasar
- **apps/infrastructure_engineer/schemas.py** — Kontrak publik
- **apps/infrastructure_engineer/engine.py** — Domain engine
- **apps/infrastructure_engineer/worker.py** — Adaptor tipis (ADR-003)

---

## 8. Contoh Penggunaan

```python
from apps.infrastructure_engineer.engine import InfrastructureEngineerEngine
from apps.infrastructure_engineer.schemas import InfrastructureEngineerRequest, OperationType, BusinessContext, QualityAttributes

engine = InfrastructureEngineerEngine()
request = InfrastructureEngineerRequest(
    operation=OperationType.kubernetes_design,
    business_context=BusinessContext(domain="e-commerce", project_name="shop-api"),
    quality_attributes=QualityAttributes(availability_target="99.9%"),
    inputs={"cluster_name": "shop-cluster", "node_count": 3, "instance_type": "t3.large"},
)
report = engine.design(request)
print(f"Cluster: {report.kubernetes_spec.cluster_name}")
print(f"Quality score: {report.quality_score:.0%}")
print(f"Nodes: {len(report.kubernetes_spec.nodes)} node pools")
```
