# RFC-0031: Legal Advisor Capability Pack

| Field | Value |
|-------|-------|
| **RFC ID** | RFC-0031 |
| **Status** | Draft |
| **Version** | 0.1.0 |
| **Capability Pack** | Legal Advisor |
| **Capability ID** | `legal-advisor` |
| **Category** | Legal |
| **Related ADR** | ADR-011 |

## Summary

Add an optional Legal Advisor pack for organizing legal materials, comparing
contract language against approved playbooks, and surfacing obligations and
issues for qualified human review. It is conditional and must not be activated
without a project need, jurisdiction scope, legal owner, and governance review.

## Motivation

Legal teams need traceable assistance for document review and obligation
tracking. A domain-specific pack can structure that work while keeping
jurisdiction, source dates, and reviewer decisions explicit.

## Scope

- Extract clauses, parties, dates, defined terms, and obligations from supplied
  materials with page or source references.
- Compare clauses to a versioned, user-approved playbook and flag deviations.
- Identify missing, conflicting, or ambiguous terms and produce review questions.
- Summarize supplied legal sources with jurisdiction, effective date, and
  provenance.

Out of scope: legal representation or advice, definitive interpretation of law,
automated filing or signature, legal conclusions without a qualified reviewer,
and research against unapproved sources. A flagged item is not a legal
conclusion.

## Detailed Design

### Engine

`LegalAdvisorEngine` should orchestrate `document_extract`,
`clause_compare`, `obligation_register`, and `source_summary` operations.
Extraction results must retain source spans. Rule or playbook matching should
be deterministic and versioned; generated summaries must distinguish quoted
source material from model-generated explanation.

### Tools and contracts

- `LegalDocumentParser`: parses approved document formats and returns
  source-linked text; rejects unsupported or malformed files.
- `ClauseClassifier`: labels clauses with confidence and abstains below a
  reviewed threshold.
- `PlaybookComparator`: compares against a supplied, versioned playbook and
  reports the matched rule and deviation.
- `ObligationExtractor`: extracts responsible party, action, trigger, deadline,
  and source location; unknown fields remain unknown.
- `LegalSourceRegistry`: accepts only approved sources and records jurisdiction,
  publication/effective dates, and provenance.
- Use versioned request/response contracts. No autonomous external actions;
  access to legal documents must be permission-scoped and audited.

### Governance and boundaries

- Any future pack code accesses Core only through `backend.app.runtime`; direct
  imports from `backend.app.core` internals are prohibited.
- No direct imports from other capability packs; use approved runtime contracts.
- Before activation, add standard package registration, boundary checks,
  `apps/legal_advisor/`, benchmark/golden assets, and approved
  `real_cases/` examples.
- Review `docs/GOVERNANCE_CHARTER.md`, `docs/GOVERNANCE.md`, package boundaries,
  data handling, and applicable legal/privacy policy before merge.

### Benchmark and golden baseline

Ten reviewed baseline scenarios are defined in
`benchmarks/vertical_industry_scenarios.json`, with one-to-one cases in
`golden_tests/legal_advisor/golden_test_suite.json`. They are acceptance
specifications only, not measured benchmark results. A runnable benchmark and
CI gate are contingent on implementation approval and legal-domain review.

## Alternatives Considered

1. One general legal assistant for all jurisdictions — rejected because legal
   sources and interpretation are jurisdiction- and date-dependent.
2. Direct autonomous contract approval — rejected because it would imply legal
   authority and omit required human judgment.
3. Store legal rules in engine code — rejected in favor of versioned,
   project-approved playbooks and sources.

## Compatibility

This draft introduces no runtime code, registration, or public API. Future
contracts must be opt-in and versioned; existing packs are unaffected.

## Security and Safety Considerations

Legal documents may contain privileged, personal, or confidential information.
Enforce least-privilege access, minimize retention, redact logs, and record
source lineage. Label output as assistive, require qualified legal review, and
never claim attorney-client privilege or legal advice.

## Testing Strategy

- Validate ten scenario references and the golden suite structure.
- On implementation, test source-span fidelity, jurisdiction/date handling,
  abstention, malformed inputs, playbook versioning, and permission boundaries.
- Require review by a qualified legal owner; draft scenarios are not legal
  authorities and must not be used as ground-truth law.

## Governance Checklist

- [ ] Confirm project demand, jurisdiction(s), and a qualified legal owner.
- [ ] Review this RFC and ADR-011 through the documented process.
- [ ] Approve source registry, playbooks, access controls, and retention policy.
- [ ] Verify Runtime-facade-only Core access and package boundaries.
- [ ] Review all ten scenarios with qualified counsel before certification.
- [ ] Require human approval for all consequential legal determinations.

## Timeline

Draft and benchmark specification only. Implementation is conditional on
project demand and completion of the governance checklist.

## References

- [Governance Charter](../GOVERNANCE_CHARTER.md)
- [Governance](../GOVERNANCE.md)
- [RFC process](README.md)
- [ADR-011](../adr/ADR-011-legal-advisor.md)
