# Go-to-Market — Demo Use Case Scenarios
# =========================================
# Production-ready demo scenarios for Vertical Industry Packs.
# Each scenario is designed for a 5-minute live demo with measurable outcomes.

# ============================================================================
# 1. FINANCE ANALYST — "CFO Board Meeting Prep"
# ============================================================================
#
# Persona: CFO of a Series-A fintech startup
# Problem: Need board presentation on runway, scenario analysis, and compliance controls
#
# Scenario Flow:
#   1. User uploads 12-month financial statement (CSV format)
#   2. Finance Analyst computes:
#      - Gross margin: 72%
#      - Current ratio: 2.8x
#      - Cash runway: 14 months
#   3. User asks: "What happens if revenue drops 20% next quarter?"
#      → Scenario Analysis: Cash runway drops to 9 months, margin compression to 64%
#   4. User asks: "Map this to SOX control requirements"
#      → Control Check: All 15 key controls identified, 3 gaps flagged
#
# Demo Script:
#   POST /capabilities/finance-analyst/execute
#   {
#     "message": "I have $2.1M in cash, $180K monthly burn, 72% gross margin.
#                 Run scenario analysis for 20% revenue drop and map to SOX controls.",
#     "workspace_id": "demo-finance-cfo"
#   }
#
# Expected Outcome:
#   - Financial summary with 5 ratios
#   - 3 scenarios (baseline, -10%, -20%) with runway projections
#   - SOX control checklist with 3 gaps identified
#   - Compliance boundary flag: "Not investment advice" disclaimer
#
# Time: ~3-4 minutes
# Key Metric: Board-ready output in <60s

# ============================================================================
# 2. LEGAL ADVISOR — "M&A Contract Review"
# ============================================================================
#
# Persona: General Counsel at mid-market SaaS company
# Problem: Reviewing 15 contracts for an acquisition — need clause consistency check
#
# Scenario Flow:
#   1. Upload Master Service Agreement (MSA) template
#   2. Upload 14 customer contracts
#   3. Legal Advisor extracts 47 clauses from MSA, identifies:
#      - 3 contracts missing limitation-of-liability clause
#      - 2 contracts with conflicting indemnity language
#      - 1 contract referencing expired playbook rule
#   4. Generate obligation register: 127 obligations across 15 contracts
#   5. Conflict detection: 5 inter-contract conflicts flagged
#
# Demo Script:
#   POST /capabilities/legal-advisor/execute
#   {
#     "message": "Review these 15 contracts against our MSA playbook.
#                 Extract clauses, check for deviations, register obligations,
#                 and flag any conflicts between contracts.",
#     "workspace_id": "demo-legal-gc"
#   }
#
# Expected Outcome:
#   - Clause extraction: 47 clauses from MSA, 420 from 14 contracts
#   - Deviation report: 3 missing clauses, 5 deviations
#   - Obligation register: 127 obligations with deadlines
#   - Conflict report: 5 inter-contract conflicts
#   - Compliance boundary: "Not legal advice — requires attorney review"
#
# Time: ~4-5 minutes
# Key Metric: 90% clause coverage, 0 false-positive conflicts

# ============================================================================
# 3. HSE SPECIALIST — "Construction Site Safety Assessment"
# ============================================================================
#
# Persona: HSE Manager at a construction company
# Problem: Pre-job safety assessment for steel erection at 40th floor
#
# Scenario Flow:
#   1. User describes: "Steel erection, 40th floor, wind 15 mph, crew of 6"
#   2. HSE Specialist identifies 12 hazards:
#      - Fall from height (8ft+ = critical risk)
#      - Steel handling (pinch points, dropped load)
#      - Wind effects (crane operation limits)
#      - Electrical proximity (overhead lines)
#      - Confined space (steel column interiors)
#   3. Risk scoring: 3 critical (8-10), 5 high (6-7), 4 medium (4-5)
#   4. Control review: 7 controls in place, 5 gaps identified
#   5. Compliance check against ISO 45001: 8/10 mandatory clauses addressed
#
# Demo Script:
#   POST /capabilities/hse-specialist/execute
#   {
#     "message": "We're doing steel erection on the 40th floor.
#                 Wind speed 15 mph. Crew of 6 ironworkers.
#                 Existing controls: harnesses, safety nets, spotter,
#                 crane load chart reviewed. Analyze hazards, score risks,
#                 review controls, and check ISO 45001 compliance.",
#     "workspace_id": "demo-hse-construction"
#   }
#
# Expected Outcome:
#   - 12 hazards identified with severity ratings
#   - Risk matrix: 3 critical, 5 high, 4 medium
#   - 5 control gaps with hierarchy-of-control recommendations
#   - ISO 45001 compliance: 8/10 clauses addressed
#   - Escalation flag: "Permit-to-work system required for critical risks"
#
# Time: ~2-3 minutes
# Key Metric: 95% hazard detection rate, 0 critical risks missed

# ============================================================================
# 4. SUPPLY CHAIN ANALYST — "Port Disruption Contingency"
# ============================================================================
#
# Persona: Supply Chain Director at consumer electronics company
# Problem: Typhoon disrupting Shanghai port — need alternative routing
#
# Scenario Flow:
#   1. Current situation: 12,000 units/week through Shanghai port
#   2. Supply Chain Analyst evaluates 4 alternatives:
#      - Option A: Ningbo port (+2 days, +$15K/week)
#      - Option B: Busan port (+3 days, +$22K/week)
#      - Option C: Singapore transshipment (+4 days, +$35K/week)
#      - Option D: Air freight (+1 day, +$180K/week)
#   3. Demand forecasting: 2-week backlog expected from delay
#   4. Risk assessment: Shanghai closure 5-7 days, Ningbo 10% capacity
#   5. Route optimization: Hybrid — 60% Ningbo, 40% Busan, air for priority SKUs
#
# Demo Script:
#   POST /capabilities/supply-chain-analyst/execute
#   {
#     "message": "Shanghai port is closed due to typhoon.
#                 We ship 12,000 units/week from Shanghai.
#                 Suppliers in Ningbo (2hr drive), Busan (ferry available),
#                 Singapore (transshipment hub).
#                 Air freight available at 10x cost.
#                 Run demand forecast, risk assessment, and route optimization.
#                 Prioritize our 3 premium SKUs for air freight.",
#     "workspace_id": "demo-supplychain-director"
#   }
#
# Expected Outcome:
#   - Demand forecast: 2-week backlog, 15% surge post-clearance
#   - Risk assessment: Shanghai closure (7 days), supplier backup capacity
#   - Route optimization: Hybrid plan with cost impact ($45K/week incremental)
#   - Inventory recommendation: Pre-position 3,000 units in regional DC
#   - Lead time: +2.5 days average (vs +7 days if no action taken)
#
# Time: ~3-4 minutes
# Key Metric: Cost-minimized contingency plan in <90s

# ============================================================================
# 5. CROSS-PACK: "Pharmaceutical Plant Commissioning"
# ============================================================================
#
# Persona: Plant Manager + General Counsel + HSE Director + Supply Chain VP
# Problem: Commissioning a new $200M pharmaceutical manufacturing facility
#
# Multi-pack Scenario:
#   1. Infrastructure Engineer: designs facility utilities (steam, water, HVAC)
#   2. HSE Specialist: safety assessment for chemical storage and handling
#   3. Compliance Officer: GMP, FDA, ISO 13485 compliance mapping
#   4. Legal Advisor: contract review for EPC, equipment procurement
#   5. Supply Chain Analyst: critical equipment and raw material supply chain
#   6. Finance Analyst: capital expenditure analysis and ROI projection
#
# Demo Script (executed sequentially in shared workspace):
#   POST /capabilities/infrastructure-engineer/execute
#   POST /capabilities/hse-specialist/execute
#   POST /capabilities/compliance-officer/execute
#   POST /capabilities/legal-advisor/execute
#   POST /capabilities/supply-chain-analyst/execute
#   POST /capabilities/finance-analyst/execute
#
# Expected Outcome:
#   - 6 integrated reports with cross-references
#   - Risk register: 47 items across all domains
#   - Compliance heatmap: 96% GMP, 92% FDA, 100% ISO 13485
#   - Financial projection: 4.2-year payback, 18.5% IRR
#   - Supply chain: 3 critical suppliers, 2 single-source risks
#
# Time: ~5 minutes (parallel execution possible)
# Key Metric: End-to-end facility readiness assessment in <300s

# ============================================================================
# Demo Environment Setup
# ============================================================================
#
# Prerequisites:
#   1. ECP v3.0.0 running with all 43 capability packs loaded
#   2. LLM provider configured (gpt-4o recommended)
#   3. Demo workspace pre-created: "demo-sessions"
#   4. Sample data files uploaded to workspace
#
# Quick Start:
#   export ECP_API_URL=http://localhost:8000
#   export ECP_API_TOKEN=<your-token>
#   # Run all demo scenarios:
#   python scripts/run_gtm_demos.py
