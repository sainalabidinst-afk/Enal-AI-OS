# ADR-020: DevSecOps Engine Architecture

|Campo|Valor|
|-------|-------|
|**ID ADR**|ADR-020|
|**Status**|Accepted|
|**Date**|2026-10-02|
|**Decision Maker**|Platform Architecture Board|
|**Related RFC**|RFC-0040|

## Context

DevSecOps capability pack needs to provide CI/CD security gates, dependency scanning, and runtime policy enforcement for ECP users to build secure software supply chains.

## Decision

1. **Dependency Scanning**: SCA using pip-audit/safety (lazy import); fallback to requirements.txt parsing for known CVE patterns.
2. **Security Gates**: Policy-as-code evaluation using OPA (lazy import of opa-sdk); fallback to regex-based policy checks.
3. **Container Security**: Image vulnerability scanning patterns (docker scan / trivy) documented; actual scanning done via external integration hooks.
4. **Runtime Policy**: Admission control rules for Kubernetes (OPA Gatekeeper patterns); evaluated via policy engine.
5. **Integration with Cognitive Pipeline**: Security audit runs as pre-execution gate; findings feed into Compliance Officer for audit evidence.

## Alternatives Considered

- **Commercial SAST/DAST platform**: Rejected — external API dependency, licensing cost.
- **Custom security engine**: Rejected — insufficient coverage, maintenance burden.

## Consequences

- Adds `devsecops_engine.py` to `apps/devsecops/`
- Integrates with Compliance Officer for audit evidence generation
- No external API dependencies

## Cross-Capability Proof

- Code Engineer consumes security fix recommendations for code review
- DevOps Assistant consumes CI/CD security gate configuration
- Security Engineer consumes dependency vulnerability intelligence
- Compliance Officer consumes runtime policy compliance evidence
