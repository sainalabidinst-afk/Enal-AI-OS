# DevOps Assistant — Spesifikasi Capability

**Versi:** 2.0.0
**Status:** Bersertifikat
**Target Kualitas:** A+ (≥95) — Level 4 — Pakar Domain

---

## 1. Tujuan

DevOps Assistant adalah **otoritas rekayasa DevOps** untuk ECP — Capability Pack yang menghasilkan konfigurasi infrastruktur, pipeline CI/CD, dan saran perbaikan DevOps berbasis bukti.

Capability Pack ini mengintegrasikan 7 modul inti (Pipeline Generator, Infrastructure Designer, Deployment Planner, Monitoring Configurator, Project Scanner, Risk Modeler, Suggestion Generator) melalui pipeline rekayasa terstruktur — **tanpa memodifikasi Core**.

---

## 2. Ruang Lingkup

### Dalam Ruang Lingkup
- **Containerization** — Dockerfile generation dengan best practices
- **CI/CD Generation** — GitHub Actions, GitLab CI pipelines
- **Infrastructure Design** — Kubernetes manifests, Terraform plans
- **Deployment Planning** — Rolling, blue-green, canary strategies
- **Monitoring Configuration** — Prometheus, Grafana dashboards
- **Project Scanning** — Tech debt detection, smell taxonomy
- **Risk Modeling** — Quantitative risk assessment for changes
- **Suggestion Generation** — Prioritized improvements with effort estimation
- **GitOps** — ArgoCD, Flux configurations
- **Policy as Code** — OPA, Sentinel, Kyverno
- **Chaos Engineering** — Fault injection experiments

### Di Luar Cakupan
- Penyediaan akun cloud langsung
- Perintah kejadian produksi
- Operasi pusat data perangkat keras
- Integrasi penyedia cloud kustom
- Biaya optimasi audit

---

## 3. Kontrak

### Input: DevOpsAnalysisRequest
```json
{
  "task": "generate_pipeline | design_infrastructure | plan_deployment | configure_monitoring | scan_project | suggest_improvements",
  "service_name": "string",
  "language": "python | javascript | go | java",
  "platform": "github_actions | gitlab_ci | kubernetes | terraform",
  "project_path": "string (optional)",
  "options": {
    "include_security": true,
    "include_monitoring": true,
    "deployment_strategy": "rolling | blue_green | canary",
    "monitoring_stack": "prometheus | datadog | cloudwatch"
  }
}
```

### Output: DevOpsAnalysisReport
```json
{
  "task": "string",
  "service_name": "string",
  "pipeline": {},
  "infrastructure": {},
  "deployment_plan": {},
  "monitoring_config": {},
  "scan_results": {
    "total_files": 50,
    "issues_found": 5,
    "categories": ["ci_cd", "containerization", "monitoring"]
  },
  "suggestions": [
    {
      "problem_id": "string",
      "solution_type": "string",
      "description": "string",
      "estimated_effort": "low | medium | high",
      "risk": "low | medium | high",
      "confidence": 0.9
    }
  ],
  "risk_assessment": {
    "overall_risk_score": 0.3,
    "risk_breakdown": {}
  }
}
```

---

## 4. Operasi

| Operasi | Deskripsi | Input | Output |
|-----------|-------------|--------|---------|
| `generate_pipeline` | Generasi pipeline CI/CD | service_name, platform, language | PipelineConfig |
| `design_infrastructure` | Desain infrastruktur (K8s, Terraform) | service_name, platform | InfrastructureConfig |
| `plan_deployment` | Rencana deployment | service_name, strategy | DeploymentPlan |
| `configure_monitoring` | Konfigurasi monitoring | service_name, stack | MonitoringConfig |
| `scan_project` | Scan proyek untuk tech debt | project_path | ProjectAnalysis |
| `suggest_improvements` | Saran perbaikan DevOps | pipeline/infra/deployment | List[Suggestion] |
| `model_risk` | Model risiko perubahan | change_description, scope | RiskAssessment |

---

## 5. Modul Analyzer

| Modul | File | Tanggung Jawab |
|-------|------|----------------|
| `pipeline_generator.py` | PipelineGenerator | Generasi CI/CD pipeline (GitHub Actions, GitLab CI) |
| `infrastructure_designer.py` | InfrastructureDesigner | Desain K8s manifests, Terraform plans |
| `deployment_planner.py` | DeploymentPlanner | Rencana deployment (rolling, blue-green, canary) |
| `monitoring_configurator.py` | MonitoringConfigurator | Konfigurasi Prometheus, Grafana |
| `project_scanner.py` | DevOpsProjectScanner | Scan proyek untuk tech debt |
| `risk_modeler.py` | RiskModeler | Model risiko kuantitatif |
| `suggestion_generator.py` | SuggestionGenerator | Saran perbaikan berprioritas |
| `schemas.py` | Schemas | Kontrak typed (Problem, Solution, Severity, dll) |
| `smell_taxonomy.py` | SmellTaxonomy | Kategorisasi masalah DevOps |

---

## 6. Dimensi Benchmark

| Dimensi | Target | Grade |
|-----------|--------|-------|
| Pipeline Correctness | ≥95% | A+ |
| Infrastructure Validity | ≥95% | A+ |
| Deployment Safety | ≥95% | A+ |
| Monitoring Coverage | ≥90% | A |
| Tech Debt Detection | ≥90% | A |
| Suggestion Relevance | ≥90% | A |
| Risk Model Accuracy | ≥90% | A |
| Consistency | ≥95% | A+ |

---

## 7. Dependensi

- **apps/base.py** — Definisi model dasar
- **apps/devops_assistant/schemas.py** — Kontrak publik
- **apps/devops_assistant/engine.py** — Domain engine
- **apps/devops_assistant/worker.py** — Adaptor tipis (ADR-003)

---

## 8. Contoh Penggunaan

```python
from apps.devops_assistant.engine import DevOpsEngine

engine = DevOpsEngine()
pipeline = await engine.generate_pipeline("my-service", platform="github_actions")
infra = await engine.design_infrastructure("my-service", platform="kubernetes")
plan = await engine.plan_deployment("my-service", strategy="rolling")
suggestions = engine.suggest_pipeline_improvements(pipeline)
```

---

## 9. Audit Keamanan

### OWASP Top 10
- A03: Injection: Hardcoded secrets dalam Dockerfile, CI/CD secrets exposure
- A05: Security Misconfiguration: Default credentials di container, verbose logging
- A06: Vulnerable Components: Base image yang outdated, dependency dengan CVE
- A09: Logging Failures: Missing audit logging dalam deployment

### Deteksi Rahasia
- Hardcoded API keys, passwords, tokens dalam Dockerfile dan CI config
- GitHub Actions secrets exposure dalam log
- Kubernetes secrets dalam plain text

### Pencegahan Injeksi
- Command injection dalam Dockerfile (avoid `sh -c` dengan input tidak terpercaya)
- YAML injection dalam pipeline triggers
- Template injection dalam IaC

### Validasi Input
- Validasi image tag (avoid `:latest` di production)
- Validasi environment variables
- Validasi resource requests/limits

### Default Aman
- Non-root user dalam container
- Read-only root filesystem
- Drop all capabilities
- Network policy default deny

---

## 10. Optimasi Kinerja

### Strategi Caching
- Pipeline template cache untuk reuse
- Infrastructure config cache untuk environment yang sama
- Scan result cache untuk proyek yang tidak berubah

### Peluang Paralelisme
- Parallel scanning untuk banyak service dalam monorepo
- Independent checks (security, style, complexity) dapat dijalankan paralel
- Multi-cloud cost estimation paralel

### Optimasi Memori
- Streaming scan untuk proyek besar
- Lazy loading untuk smell taxonomy rules
- Disk-based cache untuk large dependency graphs

### Efisiensi Token
- Context compression untuk large manifests
- Incremental scan untuk perubahan kecil
- Template reuse untuk common patterns

---

## 11. Riwayat Perubahan

| Versi | Tanggal | Perubahan |
|-------|---------|-----------|
| 2.0.0 | 2026-08-05 | Level 4 Domain Expert, A+ grade, 10 golden tests, security audit, performance optimization |
