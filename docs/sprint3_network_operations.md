<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/sprint3_network_operations.md`
- Judul: Sprint3 Network Operations
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# ECP Network Engineer â€” Milestone 3: Network Operations

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for sprint3_network_operations
<!-- DOCUMENT_METADATA_END -->

**Status:** Planned
**Focus:** Operational workflows, not protocol automation

---

## Deliverables

### 1. Configuration Compare

**Goal:** Compare two configuration backups and show semantic diff + impact analysis.

**User Story:**
> "As a network engineer, I want to compare backup A with backup B so I can see exactly what changed and whether it's safe."

**Features:**
- Load two backup files
- Semantic diff (same engine as Milestone 2, but applied to backups)
- Impact analysis: what services/interfaces are affected
- Markdown report

**Acceptance Criteria:**
- Can load any two golden test configs
- Shows added/removed/modified rules by category
- Identifies potentially risky changes (firewall, NAT, routes)
- Generates Markdown report

---

### 2. Compliance Audit

**Goal:** Check configuration against a policy and show Pass/Fail.

**User Story:**
> "As a network engineer, I want to run a compliance audit so I can prove the router meets company policy."

**Features:**
- Define policy as simple rules (JSON/YAML)
- Check config against policy
- Pass/Fail per rule
- Overall compliance score
- Markdown report

**Sample Policy:**
```yaml
rules:
  - id: SSH-RESTRICTED
    check: "ssh must not be open to 0.0.0.0/0"
    severity: critical
  - id: PASSWORD-SET
    check: "admin password must be set"
    severity: critical
  - id: BACKUP-CONFIGURED
    check: "backup must be configured"
    severity: warning
  - id: NTP-ENABLED
    check: "NTP must be enabled"
    severity: info
```

**Acceptance Criteria:**
- Can define custom policy
- Checks config against each rule
- Shows Pass/Fail with evidence
- Generates compliance score

---

### 3. Health Report

**Goal:** One-click health score for a router.

**User Story:**
> "As a network engineer, I want a health score so I can quickly assess router condition."

**Features:**
- Health Score (0â€“100)
- Security Score (0â€“100)
- Performance Score (0â€“100)
- Maintainability Score (0â€“100)
- Overall Score
- Breakdown by category
- Markdown report

**Scoring Logic:**
- Start at 100
- Subtract points for each finding by severity:
  - Critical: -20
  - Warning: -10
  - Info: -5
  - Suggestion: -2
> Terjemahan Indonesia: Kritis: -20 Peringatan: -10 Info: -5 Saran: -2
- Floor at 0

**Acceptance Criteria:**
- Generates scores for any golden test config
- Scores are consistent (same config = same score)
- Breakdown shows which issues affect each score
- Markdown report with visual indicators

---

### 4. Change Impact Analysis

**Goal:** Before deployment, predict what will be affected by the change.

**User Story:**
> "As a network engineer, I want to know what will break before I deploy, so I can prepare."

**Features:**
- Analyze current config + proposed diff
- Identify affected services:
  - Firewall changes â†’ connectivity impact
  - NAT changes â†’ internet access impact
  - Route changes â†’ traffic blackhole risk
  - DHCP changes â†’ lease impact
  - Interface changes â†’ device isolation
> Terjemahan Indonesia: Perubahan firewall â†’ dampak konektivitas Perubahan NAT â†’ dampak akses internet Perubahan rute â†’ risiko lubang hitam lalu lintas Perubahan DHCP â†’ dampak sewa Perubahan antarmuka â†’ isolasi perangkat
- Predict impact level (Low/Medium/High/Critical)
- Suggest mitigation steps

**Acceptance Criteria:**
- Can analyze any golden test diff
- Identifies at least: firewall, NAT, route, interface, DHCP impacts
- Predicts impact level correctly for known scenarios
- Suggests actionable mitigations

---

### 5. Explain Like Engineer

**Goal:** Explain configuration rules in plain language for onboarding.

**User Story:**
> "As a junior network engineer, I want to understand what each rule does so I can learn."

**Features:**
- Click on any finding/rule
- Get explanation:
  - What this rule does
  - Why it was created
  - What happens if removed
  - Dependencies (what else depends on this)
  - Common mistakes
> Terjemahan Indonesia: What ini rule does Why it was created What happens if removed Dependencies (what else depends pada ini) Common mistakes
- Plain language, not jargon-heavy

**Example Output:**
```
Rule: masquerade on WAN
------------------------
What it does:
  Allows all devices on the LAN to access the internet by
  translating their private IPs to the router's public IP.

Why it exists:
  Without this, LAN devices cannot reach the internet.
  Only the router itself would have internet access.

Impact if removed:
  - LAN devices lose internet access
  - Hotspot users cannot browse
  - DHCP clients can get IPs but no internet

Dependencies:
  - Requires WAN interface to have public IP
  - Often paired with srcnat chain rule
  - Works with FastTrack for performance

Common mistakes:
  - Applying to LAN interface instead of WAN
  - Forgetting to create DHCP server
  - Not setting default route
```

**Acceptance Criteria:**
- Can explain all 45 analysis rules
- Explanations are accurate and actionable
- Dependencies are correctly identified
- Plain language suitable for junior engineers

---

## What We Will NOT Build in Milestone 3

- BGP automation
- MPLS automation
- CAPsMAN automation
- WireGuard automation
- Multi-router orchestration
- Live MikroTik API integration

These are consequences of good operational understanding, not prerequisites.
> Terjemahan Indonesia: These adalah consequences dari good operational understanding, not prerequisites.

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Configuration Compare Accuracy | â‰¥95% |
| Compliance Audit Coverage | â‰¥90% of common policies |
| Health Score Correlation | â‰¥0.8 with expert judgment |
| Change Impact Accuracy | â‰¥80% for known scenarios |
| Explanation Completeness | 100% of 45 rules explained |
| Golden Test Pass | â‰¥95% |
| Dogfooding Feedback Items | â‰¥20 items logged |
| Time Saved (dogfooding) | â‰¥50% vs manual analysis |

---

## Prerequisites

- Milestone 2 baseline frozen (`v1.0.0-dev+network-sprint2`)
- Dogfooding completed (1â€“2 weeks)
- Feedback from at least 10 real configs reviewed
- Top 5 priorities from dogfooding documented

---

## Definition of Done

- [ ] Configuration Compare works on all golden test scenarios
- [ ] Compliance Audit passes all policy test cases
- [ ] Health Report generates consistent scores
- [ ] Change Impact Analysis predicts impacts correctly
- [ ] Explain Like Engineer covers all 45 rules
- [ ] All Milestone 3 tests pass (â‰¥95%)
- [ ] Dogfooding feedback incorporated
- [ ] Documentation updated
- [ ] Demo ready
