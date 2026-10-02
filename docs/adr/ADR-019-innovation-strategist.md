# ADR-019: Innovation Strategist Engine Architecture

|Campo|Valor|
|-------|-------|
|**ID ADR**|ADR-019|
|**Status**|Accepted|
|**Date**|2026-10-02|
|**Decision Maker**|Platform Architecture Board|
|**Related RFC**|RFC-0039|

## Context

Innovation Strategist capability pack needs to provide trend analysis, foresight modeling, and R&D portfolio management for ECP users to identify innovation opportunities and plan strategic initiatives.

## Decision

1. **Trend Analysis**: Natural language processing on market intelligence feeds for trend identification; uses TF-IDF (scikit-learn) with fallback to keyword extraction.
2. **Foresight Modeling**: Scenario tree generation for future state planning; reuses Scenario Simulator patterns.
3. **R&D Portfolio**: Portfolio optimization using efficient frontier algorithms (scipy); fallback to balanced allocation heuristic.
4. **Technology Radar**: Quadrant-based technology assessment with adoption scoring.
5. **Integration with Cognitive Pipeline**: Innovation insights feed into Decision Intelligence for strategic planning; consumes Knowledge Graph for cross-domain trend analysis.

## Alternatives Considered

- **External trend intelligence platform**: Rejected — vendor lock-in, external API dependency.
- **Custom LLM for trend synthesis**: Rejected — high compute cost, hallucination risk.

## Consequences

- Adds `innovation_engine.py` to `apps/innovation_strategist/`
- Integrates with Cross-Domain Knowledge Graph for trend correlation
- No external API dependencies

## Cross-Capability Proof

- Decision Intelligence consumes scenario forecasts for strategic planning
- Business Intelligence consumes innovation KPIs for dashboards
- Knowledge Engineer consumes trend insights for ontology enrichment
