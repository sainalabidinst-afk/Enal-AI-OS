# RFC-0021: Sertifikasi DevOps Assistant — Level 4 Domain Expert

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Tim Dokumentasi
**Pemilik Canonical:** Pimpinan Tata Kelola Dokumentasi
**Diverifikasi Terakhir:** 2026-08-05
**Versi:** 1.0.0
**Status:** Aktif
<!-- DOCUMENT_METADATA_END -->

|Bidang|Nilai|
|-------|-------|
|**ID RFC**|RFC-0021|
|**Status**|Draf|
|**Versi**|0.1.0|
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

Capability Pack DevOps Assistant saat ini memiliki fondasi rekayasa DevOps yang solid tetapi kedalaman domainnya masih terbatas pada generasi pipeline dan konfigurasi dasar. Saat ini:

1. **Infrastructure design terbatas** — Hanya mendukung Kubernetes dasar, tanpa Terraform, Pulumi, atau multi-cloud.
2. **GitOps tidak diimplementasikan** — ArgoCD, Flux, dan Continuous Delivery belum ada.
3. **Policy as Code terbatas** — OPA, Sentinel, Kyverno belum diimplementasikan.
4. **Chaos Engineering tidak ada** — Tidak ada dukungan untuk fault injection experiments.
5. **Multi-cloud belum ada** — Tidak ada dukungan untuk AWS, Azure, GCP secara mendalam.

RFC-0021 mengangkat DevOps Assistant ke Level 4 — Pakar Domain dengan infrastruktur yang lebih kompleks, GitOps, Policy as Code, dan Chaos Engineering.

---

## Pernyataan Masalah

Tanpa sertifikasi Level 4:

- **Infrastruktur tidak dapat diskalakan** — Hanya Kubernetes dasar, tanpa dukungan enterprise.
- **Tidak ada GitOps** — Continuous Delivery dan GitOps workflows tidak terotomatis.
- **Kebijakan tidak terjamin** — Tidak ada enforcement kebijakan sebagai kode.
- **Tidak ada Chaos Engineering** — Tidak ada validasi ketahanan sistem.
- **Multi-cloud tidak didukung** — Tidak ada portabilitas antar cloud.

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

- Golden Test Suite: 10 skenario (sudah dibuat)
- Real Cases: 100 kasus di `real_cases/devops/`
- Benchmark: ≥95% kebenaran pada konfigurasi yang dihasilkan
- Security Audit: OWASP Top 10, secret detection, injection prevention
- Performance: < 3s per pipeline generation

---

## Referensi

- RFC-0014: Infrastructure Engineer
- RFC-0008: Security Engineer
- CAPABILITY_GUIDE.md: Spesifikasi Capability Pack
