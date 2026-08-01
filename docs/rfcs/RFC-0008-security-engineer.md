# RFC-0008: Security Engineer Capability Pack

| Field | Value |
|-------|-------|
| **RFC ID** | RFC-0008 |
| **Status** | Draft |
| **Version** | 0.1.0 |
| **Author** | Enal AI OS Core Team |
| **Target Release** | v1.2.0 (Capability Excellence phase) |
| **Capability Pack** | Security Engineer |
| **Capability ID** | `security-engineer` |
| **Category** | Security |
| **Quality Target** | A- (≥85) |
| **Maturity Target** | Level 3 — Production Ready |
| **Reference RFC** | RFC-0008 |

---

## Motivation

ECP's existing Capability Packs generate code, configurations, and deployments. Each produces outputs that carry security risk, but there is no dedicated security reasoning layer that systematically evaluates, detects, and remediates vulnerabilities across all artifacts.

Currently:

1. **Security checks are embedded** — Code Engineer has basic OWASP awareness, Network Engineer has firewall auditing, but there is no unified security framework.
2. **Threat modeling is absent** — No systematic analysis of attack surface, trust boundaries, or threat actors before deployment.
3. **Secret detection is ad hoc** — No centralized detection and rotation recommendation for credentials in code or configuration.
4. **Dependency risk is not tracked** — Vulnerabilities in third-party packages are not systematically audited or correlated with exploit availability.
5. **Compliance is not mapped** — Security findings are not tied to compliance frameworks (SOC 2, ISO 27001, HIPAA, PCI-DSS).

The Security Engineer Capability Pack becomes the dedicated security layer that analyzes all ECP-generated artifacts against industry standards, detects threats and vulnerabilities, and provides remediation guidance with compliance mapping.

---

## Problem Statement

Without a dedicated Security Engineer Capability Pack:

- **No unified vulnerability detection** — security findings are pack-specific; SQL injection is checked by Code Engineer, firewall misconfigurations by Network Engineer, but no single view exists.
- **OWASP Top 10 coverage is incomplete** — only a subset of issues is detected, and detection quality varies by pack.
- **Threat modeling is manual** — no automated analysis of trust boundaries, data flow, or attack surface.
- **No secret detection pipeline** — credentials in code, configuration, or artifacts are not systematically identified or flagged.
- **Dependency vulnerabilities are not audited** — third-party package vulnerabilities (CVEs) are not tracked or prioritized.
- **Compliance is not enforced** — security findings are not mapped to compliance requirements, making audit preparation manual and error-prone.
- **False positives and negatives are not tracked per domain** — no feedback loop to improve detection precision.

---

## Goals

1. **OWASP Top 10 Analysis** — Detect all 10 vulnerability categories in code, configurations, and artifacts.
2. **Threat Modeling** — Analyze system architecture for attack surface, trust boundaries, and threat actors.
3. **Secret Detection** — Identify hardcoded secrets, credentials, API keys, and tokens across all outputs.
4. **Vulnerability Analysis** — Detect and prioritize known vulnerabilities (CVEs) in dependencies.
5. **Dependency Audit** — Audit third-party packages for known vulnerabilities, outdated versions, and risky licenses.
6. **Security Review** — Perform systematic security review of generated artifacts and configurations.
7. **Configuration Hardening** — Identify and remediate insecure configuration defaults.
8. **Compliance Mapping** — Map findings to SOC 2, ISO 27001, HIPAA, PCI-DSS, and other compliance frameworks.

### Success Criteria

| Metric | Target | Grade |
|--------|--------|-------|
| Detection Rate | ≥95% (all known vulnerabilities detected) | A- |
| False Positive Rate | <5% | A- |
| Threat Coverage | ≥90% (all defined threat categories analyzed) | A- |
| Secret Detection | ≥95% (hardcoded secrets found) | A- |
| Dependency CVE Coverage | ≥90% (known CVEs in dependencies identified) | A- |
| Compliance Mapping | ≥95% (findings mapped to relevant controls) | A- |
| Explainability | ≥90% (findings explained with remediation guidance) | A- |
| Consistency | ≥90% (same input produces same findings across runs) | A- |

---

## Non-Goals

1. **Active penetration testing against live systems** — Security Engineer analyzes outputs; it does not perform live exploitation.
2. **Incident response execution** — Security Engineer identifies and recommends; incident response requires human execution.
3. **Replacing dedicated security tools** — SAST/DAST tools remain the source of truth; Security Engineer provides orchestration and correlation.
4. **Vulnerability disclosure** — Security Engineer does not disclose vulnerabilities externally.
5. **Core modification** — All implementation resides within the Security Engineer Capability Pack.

---

## Capability Scope

### Core Capabilities

| Capability | Description | Inputs | Outputs |
|-----------|-------------|--------|---------|
| OWASP Top 10 Analysis | Detect injection, XSS, SSRF, CSRF, broken auth, etc. in code and configs | Source code, API specs, configuration files | Finding list with severity, OWASP category, remediation |
| Threat Modeling | Analyze architecture for attack surface, trust boundaries, data flows | Architecture diagrams, data flow descriptions | Threat model with STRIDE analysis |
| Secret Detection | Identify hardcoded secrets, credentials, API keys, tokens | Code, configs, environment files, CI/CD pipelines | Secret findings with type, severity, rotation guidance |
| Vulnerability Analysis | Detect known vulnerabilities in application code | Source code, dependency manifests | Vulnerability report with CVE references |
| Dependency Audit | Audit third-party packages for CVEs, outdated versions, license risks | dependency manifests (requirements.txt, package-lock.json, etc.) | Dependency report with CVEs, upgrade paths, licenses |
| Security Review | Systematic review of artifacts for security posture | Generated artifacts, configurations, code | Security review report with prioritized findings |
| Configuration Hardening | Identify insecure defaults and recommend hardening | Configuration files, security baselines | Hardening recommendations mapped to benchmarks |
| Compliance Mapping | Map findings to compliance frameworks | Security findings, compliance requirements | Compliance mapping report |

### Out of Scope

- Live exploit execution
- Production incident response
- Vulnerability disclosure to vendors
- Security orchestration and automated response (SOAR)
- Network penetration testing against live infrastructure
- Hardware security module operations

---

## Public Contracts

### Input Contract: Security Assessment Request

```json
{
  "assessment_id": "uuid",
  "target_type": "code | config | dependency | architecture | full_review",
  "target": {
    "source_code": "string — code content or repository path",
    "config_files": ["string — configuration file contents"],
    "dependencies": ["string — dependency manifest content"],
    "architecture": "object — architecture description"
  },
  "standards": ["OWASP-Top-10", "STRIDE", "CIS", "SOC-2", "ISO-27001", "HIPAA", "PCI-DSS", "NIST-CSF"],
  "include_remediation": true,
  "include_compliance_mapping": true,
  "check_secrets": true,
  "check_dependencies": true,
  "scan_depth": "quick | thorough"
}
```

### Output Contract: Security Assessment Report

```json
{
  "assessment_id": "uuid",
  "target_type": "string",
  "findings": [
    {
      "id": "string",
      "category": "string — OWASP category, STRIDE threat, or CIS benchmark",
      "severity": "critical | high | medium | low",
      "title": "string",
      "description": "string",
      "evidence": "object — file, line, code snippet",
      "remediation": "string",
      "owasp_mapping": "string — OWASP Top 10 category if applicable",
      "compliance_mapping": ["string — compliance frameworks"],
      "confidence": 0.0
    }
  ],
  "secrets": [
    {
      "id": "string",
      "type": "api_key | password | token | certificate | other",
      "location": "string — file path or config section",
      "severity": "critical | high | medium | low",
      "rotation_required": true,
      "confidence": 0.0
    }
  ],
  "dependency_findings": [
    {
      "package": "string",
      "version": "string",
      "severity": "critical | high | medium | low",
      "cve": "string — CVE identifier",
      "description": "string",
      "fix_version": "string",
      "confidence": 0.0
    }
  ],
  "threat_model": {
    "attack_surface": "string — description of exposed surfaces",
    "trust_boundaries": ["string"],
    "data_flows": ["string"],
    "threats": ["string — STRIDE threats identified"],
    "risk_rating": "critical | high | medium | low"
  },
  "summary": {
    "total_findings": 0,
    "critical_count": 0,
    "high_count": 0,
    "medium_count": 0,
    "low_count": 0,
    "overall_risk": "critical | high | medium | low",
    "compliance_score": 0.0,
    "recommendations_count": 0
  },
  "compliance_report": {
    "standards": ["string"],
    "mapped_findings": 0,
    "compliance_percentage": {},
    "gaps": ["string"]
  }
}
```

### Security Findings (Experience Memory)

```json
{
  "record_id": "uuid",
  "assessment_id": "uuid",
  "timestamp": "ISO 8601",
  "target_type": "string",
  "total_findings": 0,
  "critical_count": 0,
  "high_count": 0,
  "resolved": [
    {"finding_id": "string", "resolution": "string", "timestamp": "ISO 8601"}
  ],
  "false_positives": [
    {"finding_id": "string", "rationale": "string", "timestamp": "ISO 8601"}
  ],
  "fp_rate": 0.0,
  "detection_rate": 0.0
}
```

---

## Integration Points (Capability Graph)

```
Consumer Capability Pack (Code Engineer, Network Engineer, DevOps Assistant)
    │
    │  submits artifact for security assessment via task/intent
    ▼
Execution Runtime
    │
    │  routes to Security Engineer Domain Engine
    ▼
Security Engineer Engine
    │
    │  ┌──────────────────────────────────────────────┐
    │  │ 1. OWASP Top 10 Analysis                     │
    │  │ 2. Secret Detection                          │
    │  │ 3. Dependency Audit                          │
    │  │ 4. Threat Modeling                            │
    │  │ 5. Vulnerability Analysis                     │
    │  │ 6. Configuration Hardening                    │
    │  │ 7. Security Review                             │
    │  │ 8. Compliance Mapping → Experience Memory     │
    │  └──────────────────────────────────────────────┘
    │
    │  returns Security Assessment Report
    ▼
Consumer Capability Pack
    │
    │  receives findings + remediation + compliance mapping
    ▼
User / Human Approval Loop
```

### Task Template

| Task | Subtasks |
|------|----------|
| Security Assessment | Target analysis → OWASP scan → Secret detection → Dependency audit → Threat modeling → Vulnerability analysis → Hardening review → Compliance mapping → Report |

---

## Consumer Capability Packs

| Consumer Capability Pack | Use Case |
|--------------------------|----------|
| **Code Engineer** | Security review of generated code, OWASP scanning, secret detection in source |
| **DevOps Assistant** | Security audit of generated configurations, container hardening, CI/CD security |
| **Network Engineer** | Security review of network configurations, firewall policy analysis, compliance auditing |
| **System Architect** | Threat modeling for architecture proposals, security-by-design validation |

---

## Dependencies

### Internal Dependencies (Shared Contracts)

1. **Execution Runtime** — Task routing and orchestration (per ADR-002)
2. **Experience Memory** — Security findings persistence (per ADR-011)
3. **Shared Contracts** — Task/Intent definition and result schema (per ADR-006)

### External Knowledge Bases

1. **OWASP Top 10 (2021)** — Vulnerability classification
2. **CWE (Common Weakness Enumeration)** — Weakness taxonomy
3. **CVE Database** — Known vulnerability references
4. **CIS Benchmarks** — Configuration hardening baselines
5. **Compliance frameworks** — SOC 2, ISO 27001, HIPAA, PCI-DSS, NIST-CSF

### No Core Changes Required

All implementation resides within the Security Engineer Capability Pack:

```
apps/
└── security_engineer/
    ├── engine.py                  # Domain Engine (per ADR-004)
    ├── worker.py                  # Thin adapter (per ADR-003)
    ├── schemas.py                 # Public contracts
    ├── owasp_analyzer.py          # OWASP Top 10 analysis
    ├── threat_modeler.py          # Threat modeling (STRIDE)
    ├── secret_detector.py         # Secret detection
    ├── vulnerability_scanner.py   # Vulnerability analysis
    ├── dependency_auditor.py      # Dependency audit
    ├── hardening_reviewer.py      # Configuration hardening
    ├── compliance_mapper.py       # Compliance mapping
    └── knowledge_base.py          # Security knowledge
```

**ADR Impact:** None. No Core, Runtime, Kernel, or shared contract modification required.

---

## Benchmark Specification

### Benchmark Framework

| Dimension | Definition | Measurement | Target |
|-----------|------------|-------------|--------|
| **Detection Rate** | % of known vulnerabilities detected | % of ground truth vulnerabilities found | ≥95% |
| **False Positive Rate** | % of findings that are false alarms | False positives / total findings | <5% |
| **Completeness** | Coverage of all security checks | % of OWASP/STRIDE/CIS checks applied | ≥90% |
| **Explainability** | Clarity of findings and remediation | Human evaluation score | ≥90% |
| **Safety** | No false security guarantees | % of safe findings | ≥95% |
| **Efficiency** | Response time and resource usage | Latency P95 < 3000ms | within budget |
| **Consistency** | Same input produces same output | Variance across 10 runs < 5% | ≥90% |
| **Compliance Mapping** | % of findings mapped to standards | Findings mapped / total findings | ≥95% |

### Benchmark Dataset

- **100 security assessments** covering:
  - Code: Python, JavaScript/TypeScript, SQL, Go, Java applications
  - Configurations: Docker, Kubernetes, cloud IaC (Terraform), network configs
  - Dependencies: Python/pip, Node/npm, Go modules, Java/Maven
  - Architecture: microservices, monolith, serverless, hybrid

### Benchmark Dimensions Detail

| Scenario Type | Description | Ground Truth Source |
|---------------|-------------|---------------------|
| SQL Injection | Classic and blind SQLi patterns | OWASP Benchmark, DVWA |
| Cross-Site Scripting (XSS) | Reflected, stored, DOM-based XSS | OWASP Benchmark |
| Server-Side Request Forgery (SSRF) | SSRF to internal/external endpoints | SSRF test suites |
| Cross-Site Request Forgery (CSRF) | Missing CSRF tokens, same-origin issues | OWASP Testing Guide |
| Command Injection | OS command injection patterns | Injection test suites |
| Secret Exposure | Hardcoded credentials, tokens, keys | Gitleaks, TruffleHog test data |
| Dependency CVE | Known CVEs in third-party packages | NVD, Snyk, GitHub Advisory |
| Configuration Hardening | Insecure defaults, missing encryption | CIS Benchmarks |

---

## Golden Test Specification

| # | Scenario | Expected Outcome | Acceptance Criteria |
|---|----------|-----------------|---------------------|
| 1 | SQL Injection in Python code | SQLi detected with remediation | ≥95% detection, <5% FP |
| 2 | Reflected XSS in JavaScript | XSS detected with remediation | ≥95% detection, <5% FP |
| 3 | SSRF in API endpoint | SSRF detected with remediation | ≥95% detection, <5% FP |
| 4 | CSRF on state-changing endpoint | CSRF detected with remediation | ≥95% detection, <5% FP |
| 5 | Command injection in shell call | Cmd injection detected | ≥95% detection, <5% FP |
| 6 | Hardcoded API key in config | Secret detected with rotation advice | ≥95% detection, <5% FP |
| 7 | Dependency with known CVE | CVE identified with fix version | ≥90% detection, <5% FP |
| 8 | Insecure Docker configuration | Hardening recommendations provided | ≥90% coverage, <5% FP |
| 9 | Threat modeling on microservice architecture | Attack surface and threats identified | ≥90% threat coverage |
| 10 | Compliance mapping for SOC 2 | Findings mapped to SOC 2 controls | ≥95% mapping accuracy |

### Golden Test Acceptance Criteria

- All 10 golden test scenarios pass at ≥90% of acceptance criteria (100% pass)
- Overall Security Engineer golden test pass rate ≥90%
- False positive rate <5% across all scenarios
- Full remediation guidance generated for every finding

---

## Real Case Requirements

### Real Case Directory

`real_cases/security_engineer/` must contain:

| Requirement | Minimum Count |
|-------------|---------------|
| Real security assessments from actual usage | 20 |
| Cases with secret exposure findings | 5 |
| Cases with dependency CVE findings | 5 |
| Cases with compliance mapping (SOC 2/ISO 27001) | 10 |
| Cases with threat modeling | 10 |
| Cases with expert review/validation | 15 |

### Real Case Structure

```
real_cases/security_engineer/<case_id>/
├── input/
│   ├── target_type.md
│   ├── source/                 # Source code, configs, or manifests
│   └── standards.txt           # Applicable security standards
├── output/
│   ├── assessment_report.json  # Full Security Assessment Report
│   └── findings_explanation.md
└── evaluation.md               # Ground truth, expert review, lessons learned
```

### Real Case Targets

| Metric | Target |
|--------|--------|
| Real cases logged | ≥20 (Level 3) → ≥100 (Level 4) |
| Real case quality score (expert review) | ≥90% |
| Findings validated by human reviewer | ≥80% |

---

## Definition of Done

```text
Definition of Done — Security Engineer Capability Pack

Functional
- [ ] OWASP Top 10 Analysis detects all 10 categories in code and configs
- [ ] Threat Modeling produces STRIDE analysis with trust boundaries and data flows
- [ ] Secret Detection identifies hardcoded credentials, API keys, tokens
- [ ] Vulnerability Analysis detects known CVEs in application code
- [ ] Dependency Audit covers pip, npm, Go, and Maven dependencies
- [ ] Security Review produces prioritized findings with remediation
- [ ] Configuration Hardening provides CIS-aligned recommendations
- [ ] Compliance Mapping maps findings to SOC 2, ISO 27001, HIPAA, PCI-DSS

Benchmark
- [ ] Detection Rate ≥ 95% (grade A-)
- [ ] False Positive Rate < 5%
- [ ] Threat Coverage ≥ 90%
- [ ] Secret Detection ≥ 95%
- [ ] Dependency CVE Coverage ≥ 90%
- [ ] Compliance Mapping ≥ 95%
- [ ] Explainability ≥ 90%
- [ ] Consistency ≥ 90%

Golden Tests
- [ ] All 10 pack golden test scenarios pass at ≥90% of acceptance criteria (100% pass)

Real Cases
- [ ] ≥ 20 real cases logged in real_cases/security_engineer/
- [ ] Evaluation notes recorded for each case
- [ ] ≥ 5 cases with secret exposure findings
- [ ] ≥ 5 cases with dependency CVE findings
- [ ] ≥ 10 cases with compliance mapping
- [ ] ≥ 10 cases with threat modeling

Documentation
- [ ] Capability Guide updated (CAPABILITY_GUIDE.md — Security Engineer section)
- [ ] API reference / contract updated (this RFC + schemas.py)
- [ ] Real case evaluation summary published

SDK
- [ ] Pack accessible via SDK without Core changes
- [ ] Security Engineer callable via Execution Runtime task routing

Performance
- [ ] Latency P95 < 3000ms for standard assessments
- [ ] Latency P95 < 8000ms for full architecture review

Security
- [ ] No known P0/P1 security issues in the pack itself
- [ ] Security assessments do not execute payloads or exploit vulnerabilities

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
| High false positive rate undermines trust | High — users ignore findings | Medium | Continuous calibration on 100 assessments; FP feedback loop |
| False negatives (missed vulns) create false security | Critical — production breach | Medium | Multi-source scanning; confidence scoring; human-in-loop validation |
| Dependency on external CVE databases (availability) | Medium — stale vulnerability data | Low | Local cache with TTL; fallback to last-known CVE data |
| Threat modeling over-fits to known patterns | Medium — misses novel attacks | Medium | Pattern-based + heuristic analysis; regular model updates |
| Compliance mapping lags behind framework updates | Low — stale compliance data | High | Quarterly compliance framework sync; version tracking |
| Scan latency on large codebases | Medium — blocks developer workflow | High | Incremental scanning; parallel analysis; caching |
| Secret detection produces false positives on test data | Medium — reduces signal quality | High | Context-aware detection (test vs. prod paths); allowlist support |

---

## ADR Impact

**Does this require Core changes?** No.

Security Engineer is a **new Capability Pack** that follows the established patterns:

- **ADR-001 (Core Pipeline Freeze):** No Core changes. All logic in `apps/security_engineer/`.
- **ADR-002 (Capability Pack Independence):** Security Engineer communicates with other packs via Execution Runtime tasks and shared contracts only. No direct imports.
- **ADR-003 (Worker = Adapter Only):** A thin Worker routes tasks to the Domain Engine.
- **ADR-004 (Domain Engine Owns Business Logic):** All security analysis logic resides in `apps/security_engineer/engine.py`.
- **ADR-005 (Human Approval Required):** Assessments are recommendations; remediation requires explicit user approval.
- **ADR-006 (Capability Contract v1 Frozen):** Uses the existing Capability Contract for node and subtask template registration. No contract changes.
- **ADR-007 (Conversation Boundary):** Security Engineer is invoked through Execution Runtime, not directly by Conversation Manager.
- **ADR-008 (Core Change Requires Cross-Capability Proof):** Not applicable — no Core changes.

**ADR Required:** None. This is a new Capability Pack, not a Core modification.

---

## Rollout Plan

### Phase 1: Prototype (RFC → Experimental)

**Duration:** 5 weeks

- [ ] Create `apps/security_engineer/` package structure
- [ ] Implement OWASP Top 10 analyzer (SQLi, XSS patterns)
- [ ] Implement basic secret detection
- [ ] Define public contracts (Assessment Request, Report)
- [ ] Implement thin Worker adapter
- [ ] Create 10 golden test scenarios (core attack types)
- [ ] Integration: Code Engineer → Security Engineer (code scan)
- [ ] Integration: Network Engineer → Security Engineer (config audit)
- **Gate:** 10 golden tests pass at ≥80%

### Phase 2: Full Capabilities (Experimental → Stable)

**Duration:** 8 weeks

- [ ] Implement Threat Modeling (STRIDE analysis)
- [ ] Implement Dependency Audit (pip, npm, Go, Maven)
- [ ] Implement Vulnerability Analysis (CVE correlation)
- [ ] Implement Configuration Hardening (CIS baselines)
- [ ] Implement Compliance Mapping (SOC 2, ISO 27001)
- [ ] Expand golden tests to 10 full scenarios
- [ ] Log ≥20 real cases from Code Engineer and Network Engineer usage
- [ ] **Benchmark:** 100 assessments, ≥95% detection, <5% FP
- [ ] **Integration:** DevOps Assistant starts using Security Engineer for CI/CD security
- **Gate:** All 10 golden tests pass at ≥90%; benchmark ≥95% detection

### Phase 3: Ecosystem (Stable → Certified)

**Duration:** 6 weeks

- [ ] All 3 consumer packs fully integrated
- [ ] Compliance mapping validated by expert review
- [ ] Dependency audit integrated with real CVE databases
- [ ] Independent audit of detection accuracy and FP rate
- [ ] Public benchmark dashboard available
- [ ] **Benchmark:** ≥95% detection, <5% FP sustained
- [ ] **Real Cases:** ≥100 cases with ≥80% expert validation
- **Gate:** Independent audit passed; benchmark ≥95% sustained

---

## Future Enhancements

### Fase 2 (Post-v1.0.0 Release)

1. **Interactive Application Security Testing (IAST)** — Runtime security analysis during testing
2. **Software Composition Analysis (SCA) Deep Integration** — Real-time dependency monitoring with exploit prediction scoring (EPSS)
3. **Security Chokepoints** — Security checks embedded in CI/CD pipeline stages
4. **Threat Intelligence Feed** — Correlate findings with real-time threat intelligence

### Fase 3 (Enterprise)

1. **Automated Remediation** — Auto-fix low-risk findings with human approval (per ADR-005)
2. **Regulatory Reporting** — Generate audit-ready compliance reports for SOC 2, ISO 27001, HIPAA
3. **Security Scorecard** — Aggregate security posture across all projects and workspaces
4. **Adversarial Simulation** — Red-team style scenario generation against own architecture

### Long-term

1. **Security-by-Design Advisor** — Security guidance integrated into architecture and code design from the start
2. **Vulnerability Prediction** — ML-based prediction of security hotspots before code is written
3. **Security Knowledge Graph** — Link findings, CVEs, threats, and compliance controls in a unified graph
4. **Cross-Workspace Threat Intelligence** — Aggregate anonymized threat data across workspaces (with privacy controls)

---

## Real Case Requirements

*(See [Real Case Requirements](#real-case-requirements) section above for full specification)*

Security Engineer real cases are sourced from:

1. **Code Engineer** — Generated code security reviews with post-fix validation
2. **Network Engineer** — Configuration audits with compliance verification
3. **DevOps Assistant** — CI/CD pipeline security scans with post-deployment verification
4. **System Architect** — Architecture threat modeling with design review feedback
