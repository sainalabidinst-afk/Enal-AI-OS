# ADR-015: AI Ethics & Governance Engine Architecture

|Campo|Valor|
|-------|-------|
|**ID ADR**|ADR-015|
|**Status**|Accepted|
|**Date**|2026-10-02|
|**Decision Maker**|Platform Architecture Board|
|**Related RFC**|RFC-0035|

## Context

AI Ethics & Governance capability pack needs to provide fairness auditing, bias detection, explainability, and regulatory compliance assessment for AI systems deployed on ECP. The engine must integrate with existing capability packs that produce AI-driven outputs.

## Decision

1. **Fairness Auditing**: Use demographic parity, equalized odds, and disparate impact metrics computed over protected attributes.
2. **Bias Detection**: Statistical bias scans on model predictions vs. ground truth across subgroups.
3. **Explainability**: SHAP/LIME-style attributions (lazy import of shap/lime); fallback to rule-based attribution.
4. **Regulatory Compliance**: Predefined checks for GDPR, CCPA, HIPAA, and ISO/IEC 23053 fairness requirements.
5. **Integration with Cognitive Pipeline**: Ethics gate runs as a post-execution audit step, feeding back into Reflection service.

## Alternatives Considered

- **External fairness toolkit (AIF360)**: Rejected — adds heavy dependency; used only as optional enhancement.
- **Manual review only**: Rejected — not scalable for automated pipelines.

## Consequences

- Adds `ethics_governance_engine.py` to `apps/ai_ethics_pack/`
- CI/CD adds benchmark scenarios for ethics auditing
- No external API dependencies

## Cross-Capability Proof

- Trading Analyst consumes bias audit on trading signals
- Code Engineer consumes explainability on code generation
- Healthcare Assistant consumes clinical AI compliance checks
