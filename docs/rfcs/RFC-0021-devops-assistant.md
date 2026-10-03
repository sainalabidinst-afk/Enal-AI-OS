# RFC-0021: Sertifikasi DevOps Assistant — Level 4 Domain Expert

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 2026-10-02
**Versi:** 1.1.0
**Status:** Aktif
<!-- DOCUMENT_METADATA_END -->

|Bidang|Nilai|
|-------|-------|
|**ID RFC**|RFC-0021|
|**Status**|Diterima — Level 4 Domain Expert (A+)|
|**Versi**|1.1.0|
|**Penulis**|Tim Inti AI OS Akhir|
|**Target Rilis**|v1.3.0 (fase Keunggulan Kemampuan)|
|**Capability Pack**|Asisten DevOps|
|**ID Kemampuan**|`devops-assistant`|
|**Kategori**|DevOps|
|**Target Kualitas**|A+ (≥95)|
|**Target Kematangan**|Level 4 — Pakar Domain|
|**Referensi RFC**|RFC-0021|

---

## Motivasi

Capability Pack DevOps Assistant telah mencapai Level 4 — Pakar Domain dengan dukungan infrastruktur kompleks, GitOps, Policy as Code, Chaos Engineering, dan Multi-Cloud. RFC-0021 mendokumentasikan sertifikasi Level 4 ini.

Implementasi saat ini:
1. **Infrastructure design lanjutan** — Kubernetes, Terraform generation, multi-cloud
2. **GitOps** — ArgoCD, Flux, declarative continuous delivery
3. **Policy as Code** — OPA, Sentinel, Kyverno dukungan
4. **Chaos Engineering** — Fault injection experiments
5. **Multi-cloud** — AWS, Azure, GCP konfigurasi
6. **Observability lanjutan** — Distributed tracing, SLI/SLO/SLA, incident response

---

## Pernyataan Masalah

---

## Tujuan

### 1. Infrastructure Design Lanjutan
- **Terraform & Pulumi** — IaC generation untuk multi-cloud
- **Kubernetes Advanced** — Operators, Service Mesh, Policy Enforcement
- **Service Mesh** — Istio, Linkerd configuration
- **GitOps** — ArgoCD, Flux, declarative continuous delivery
- **Platform Engineering** — IDP, Developer Portal

### 2. Policy as Code
- **OPA (Open Policy Agent)** — Rego policies untuk Kubernetes, Terraform
- **Sentinel** — HashiCorp policies
- **Kyverno** — Kubernetes-native policies
- **Conftest** — General purpose policy testing

### 3. Chaos Engineering
- **Fault Injection** — Pod kill, network latency, CPU stress
- **Experiment Design** — Hypothesis, blast radius, rollback
- **Steady State Hypothesis** — Automated verification

### 4. Multi-Cloud
- **AWS** — EKS, RDS, S3, Lambda configurations
- **Azure** — AKS, SQL Database, Blob Storage, Functions
- **GCP** — GKE, Cloud SQL, Cloud Storage, Cloud Functions
- **Service Mapping** — Cross-cloud service equivalents

### 5. Observability Lanjutan
- **Distributed Tracing** — OpenTelemetry, Jaeger, Zipkin
- **SLI/SLO/SLA** — Service level management
- **Incident Response** — Automated runbooks, escalation policies

---

## Dependensi

- RFC-0014 (Infrastructure Engineer) — Arsitektur infrastruktur dasar
- RFC-0008 (Security Engineer) — Kebijakan keamanan

---

## Kriteria Penerimaan

- Golden Test Suite: 10 skenario
- Real Cases: 100 kasus di `real_cases/devops/`
- Benchmark: `benchmarks/devops_assistant_benchmark.py` — 10 skenario, hasil 100% (A+)
- Security Audit: OWASP Top 10, secret detection, injection prevention
- Performance: < 3s per pipeline generation

---

## Definisi Selesai

```text
Definition of Done — DevOps Assistant Certification RFC

Functional
- [x] Infrastructure design (Terraform, Kubernetes, Service Mesh)
- [x] GitOps support (ArgoCD, Flux)
- [x] Policy as Code (OPA, Sentinel, Kyverno)
- [x] Chaos Engineering (fault injection, experiment design)
- [x] Multi-cloud support (AWS, Azure, GCP)
- [x] Advanced observability (distributed tracing, SLI/SLO/SLA)

Benchmark
- [x] 100% pass rate on 10 benchmark scenarios (A+)
- [x] 100+ real cases in real_cases/devops/
- [x] Golden test suite: 10 scenarios passing
- [x] Performance: < 3s per pipeline generation

Documentation
- [x] Capability guide: docs/capabilities/devops-assistant.md
- [x] Benchmark dashboard: benchmarks/dashboards/devops_assistant_dashboard.html
- [x] Benchmark report: benchmarks/reports/devops_assistant_benchmark.json

Regression
- [x] No regression in existing capability pack dimensions
- [x] Benchmark reproducible (documented command + persisted result)

Release Notes
- [x] Capability Changelog updated
```

---

## Referensi

- RFC-0014: Infrastructure Engineer
- RFC-0008: Security Engineer
- CAPABILITY_GUIDE.md: Spesifikasi Capability Pack
