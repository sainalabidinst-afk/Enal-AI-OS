# CAPABILITY REGISTRY TRUTH
**Date:** 2026-08-08  
**Source:** apps/__init__.py (line 49-69)  
**Status:** SINGLE SOURCE OF TRUTH

---

## ACTUAL REGISTERED CAPABILITIES

Total: **19 capabilities**

| # | Capability ID | Directory | Registered | Loadable |
|---|---------------|-----------|------------|----------|
| 1 | trading-analyst | apps/trading_analyst/ | YES | YES |
| 2 | network-engineer | apps/network_engineer/ | YES | YES |
| 3 | devops-assistant | apps/devops_assistant/ | YES | YES |
| 4 | code-engineer | apps/code_engineer/ | YES | YES |
| 5 | research-assistant | apps/research_assistant/ | YES | YES |
| 6 | full-stack-engineer | apps/full_stack_engineer/ | YES | YES |
| 7 | self-development | apps/self_development/ | YES | YES |
| 8 | decision-intelligence | apps/decision_intelligence/ | YES | YES |
| 9 | system-architect | apps/system_architect/ | YES | YES |
| 10 | security-engineer | apps/security_engineer/ | YES | YES |
| 11 | data-engineer | apps/data_engineer/ | YES | YES |
| 12 | database-engineer | apps/database_engineer/ | YES | YES |
| 13 | qa-engineer | apps/qa_engineer/ | YES | YES |
| 14 | business-analyst | apps/business_analyst/ | YES | YES |
| 15 | documentation-engineer | apps/documentation_engineer/ | YES | YES |
| 16 | product-manager | apps/product_manager/ | YES | YES |
| 17 | infrastructure-engineer | apps/infrastructure_engineer/ | YES | YES |
| 18 | ai-engineer | apps/ai_engineer/ | YES | YES |
| 19 | ui-ux-designer | apps/ui_ux_designer/ | YES | YES |

---

## DISCREPANCY ANALYSIS

**Certification Claim:** 22 capabilities  
**Actual Registry:** 19 capabilities  
**Difference:** -3 capabilities

**Missing from registry (but exist as packages):**
- `apps/integration/` — EvidenceAdapter, IntegrationEngine (cross-capability integration)
- `apps/organization/` — AgentRegistry, capability_graph (organizational runtime)
- `apps/society/` — SocietyRuntime (multi-agent society simulation)

**Assessment:** These 3 packages are NOT user-facing capabilities. They are infrastructure/support packages:
- `integration` — internal integration layer between capabilities
- `organization` — agent registry and organizational structure
- `society` — multi-agent society simulation runtime

**Decision:** These are NOT capabilities in the sense of user-facing domain expertise. They are platform infrastructure. The certification incorrectly counts them as capabilities.

**Correct Action:** Update certification-summary.json to reflect 19 capabilities, not 22. Remove integration, organization, society from capability certification.

---

## ACTION REQUIRED

1. **UPDATE** certification-summary.json to reflect actual 19 capabilities
2. **REMOVE** integration, organization, society from capability certification (they are infrastructure, not capabilities)
3. **VERIFY** all 19 registered capabilities are executable
4. **UPDATE** all certification documents to match

---

## SINGLE SOURCE OF TRUTH

**Registry truth = apps/__init__.py APPS dictionary**

Any certification, benchmark, or documentation claiming different count is STALE/INVALID.