# ADR-018: Business Intelligence Engine Architecture

|Campo|Valor|
|-------|-------|
|**ID ADR**|ADR-018|
|**Status**|Accepted|
|**Date**|2026-10-02|
|**Decision Maker**|Platform Architecture Board|
|**Related RFC**|RFC-0038|

## Context

Business Intelligence capability pack needs to provide dashboarding, KPI tracking, and scenario planning for ECP users to monitor business performance and make data-driven decisions.

## Decision

1. **Dashboard Engine**: Declarative dashboard specification with JSON-based layout; rendered via frontend cognitive layer System 3.
2. **KPI Tracking**: Time-series storage via PostgreSQL; lightweight in-memory fallback for ephemeral metrics.
3. **Scenario Planning**: What-if analysis using Monte Carlo simulation (reuses Scenario Simulator RFC-0023 patterns).
4. **Data Visualization**: Chart.js integration on frontend; backend provides pre-computed aggregates.
5. **Integration with Cognitive Pipeline**: BI dashboards consume memory store for business context; feeds into Decision Intelligence for strategic planning.

## Alternatives Considered

- **Commercial BI platform (Tableau, Power BI)**: Rejected — external dependency, licensing cost.
- **Full embedded analytics (Superset, Metabase)**: Rejected — heavy infrastructure requirements.

## Consequences

- Adds `bi_engine.py` to `apps/business_intelligence/`
- Frontend dashboard components registered in capability-browser.tsx
- No external API dependencies

## Cross-Capability Proof

- Finance Analyst consumes financial KPI tracking
- Innovation Strategist consumes market trend dashboards
- SRE Engineer consumes infrastructure KPI tracking
