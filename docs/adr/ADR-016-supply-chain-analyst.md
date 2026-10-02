# ADR-016: Supply Chain Analyst Engine Architecture

|Campo|Valor|
|-------|-------|
|**ID ADR**|ADR-016|
|**Status**|Accepted|
|**Date**|2026-10-02|
|**Decision Maker**|Platform Architecture Board|
|**Related RFC**|RFC-0036|

## Context

Supply Chain Analyst capability pack needs to provide logistics optimization, demand forecasting, and supply chain risk management for ECP users operating in manufacturing, retail, and distribution domains.

## Decision

1. **Demand Forecasting**: Time-series forecasting using Prophet/statsmodels (lazy import); fallback to moving averages.
2. **Optimization Engine**: Linear programming via scipy.optimize (lazy import); fallback to heuristic greedy allocation.
3. **Risk Analysis**: Monte Carlo simulation for supply disruption impact; built on existing Scenario Simulator (RFC-0023).
4. **Inventory Optimization**: EOQ model with constraints, multi-echelon inventory analysis.
5. **Integration with Cognitive Pipeline**: Risk analysis feeds into Decision Intelligence for contingency planning.

## Alternatives Considered

- **Commercial SCOR platform**: Rejected — vendor lock-in, external dependency.
- **Custom ML models**: Rejected — high training cost, requires specialized data.

## Consequences

- Adds `supply_chain_engine.py` to `apps/supply_chain_analyst/`
- Integrates with existing Scenario Simulator for simulation scenarios
- No external API dependencies

## Cross-Capability Proof

- Finance Analyst consumes working capital impact analysis
- Innovation Strategist consumes supply chain trend data
- DevSecOps consumes supply chain security risk for dependencies
