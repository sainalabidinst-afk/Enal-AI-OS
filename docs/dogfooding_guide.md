<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/dogfooding_guide.md`
- Judul: Dogfooding Guide
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Dogfooding Guide â€” Network Engineer

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for dogfooding_guide
<!-- DOCUMENT_METADATA_END -->

**Duration:** 1â€“2 weeks
**Goal:** Use Network Engineer on real-world configurations to collect feedback before building new features.

## What is Dogfooding?

Dogfooding = using your own product on real work, not just synthetic tests.
> Terjemahan Indonesia: Dogfooding = using your own product pada real work, not just synthetic tests.

For ECP, this means:
> Terjemahan Indonesia: Untuk ECP, ini means:
1. Take real MikroTik configurations from production or lab
2. Run them through Network Engineer
3. Compare ECP's output with your expert judgment
4. Log every mismatch, confusion, or missed finding

## What to Capture

### A. False Positives
ECP flagged something that is actually correct or acceptable.
> Terjemahan Indonesia: ECP flagged something itu adalah actually correct or acceptable.

**Template:**
```
Scenario: [short description]
Config: [file/scenario name]
Finding: [what ECP reported]
Why it's wrong: [why this is actually OK]
Rule: [which rule triggered it]
Suggested fix: [adjust rule threshold, add exception, or ignore context]
```

### B. False Negatives
ECP missed something that is actually a problem.
> Terjemahan Indonesia: ECP missed something itu adalah actually sebuah problem.

**Template:**
```
Scenario: [short description]
Config: [file/scenario name]
Issue: [what should have been flagged]
Why it matters: [security/performance/operational impact]
Suggested rule: [new rule or enhancement]
```

### C. Bad Recommendations
ECP flagged something correctly, but the fix is wrong or impractical.
> Terjemahan Indonesia: ECP flagged something correctly, but fix adalah wrong or impractical.

**Template:**
```
Scenario: [short description]
Config: [file/scenario name]
Problem: [correctly identified]
Current recommendation: [what ECP suggests]
Why it's wrong: [why this fix is bad]
Better recommendation: [what should be suggested]
```

### D. Parser Failures
Config didn't parse correctly.
> Terjemahan Indonesia: Konfigurasi tidak diuraikan dengan benar.

**Template:**
```
Config: [file/scenario name]
Error: [what went wrong]
Snippet: [RouterOS lines that failed]
Expected: [what should have been parsed]
```

### E. UX Confusion
Something was confusing, misleading, or hard to understand.
> Terjemahan Indonesia: Something was confusing, misleading, or hard untuk understand.

**Template:**
```
Feature: [which part of ECP]
Problem: [what was confusing]
Suggestion: [how to improve]
```

## How to Run Dogfooding

### Step 1: Gather Configs
Use real MikroTik configs from:
> Terjemahan Indonesia: Use real MikroTik configs dari:
- Production routers (sanitized)
- Lab/routers in the field
- Backup exports from clients
- Sun Clint project configs

**Minimum:** 10 different configs
**Target:** 20â€“30 configs

### Step 2: Run Analysis
```python
from apps.network_engineer import get_app

app = get_app()
with open("config.rsc") as f:
    config = f.read()

result = await app.analyze_config(config)
print(f"Findings: {len(result['issues'])}")
for issue in result["issues"]:
    print(f"[{issue['severity']}] {issue['category']}: {issue['description']}")
```

### Step 3: Review Findings
For each finding, ask:
> Terjemahan Indonesia: Untuk each finding, ask:
1. Is this real? (True Positive / False Positive)
2. Is the severity correct? (too high / too low / correct)
3. Is the recommendation actionable? (yes / no / needs work)

### Step 4: Compare with Expert Judgment
Write down what YOU would flag vs what ECP flagged.
> Terjemahan Indonesia: Tuliskan apa yang akan ANDA tandai vs apa yang ditandai oleh ECP.

| # | ECP Finding | Your Judgment | Match? | Notes |
|---|-------------|---------------|--------|-------|
| 1 | [ECP finding] | [your finding] | Yes/No | [notes] |
| 2 | ... | ... | ... | ... |

### Step 5: Test Controlled Deployment
If you have a lab MikroTik:
> Terjemahan Indonesia: If you memiliki sebuah lab MikroTik:
1. Run full controlled deployment pipeline
2. Try approved = True
3. Try approved = False
4. Check rollback
5. Review audit trail

If no lab device, simulate with golden test configs.
> Terjemahan Indonesia: If no lab device, simulate dengan golden test configs.

## Feedback Log Format

Create a file: `dogfooding/feedback_YYYY-MM-DD.md`
> Terjemahan Indonesia: Membuat sebuah file: dogfooding/feedback_YYYY-MM-DD.MD

```markdown
# Dogfooding Session â€” 2026-07-09

## Configs Reviewed
- `golden/mikrotik/home/config.rsc` â€” 11 findings
- `golden/mikrotik/office/config.rsc` â€” 13 findings
- [real config from Sun Clint] â€” X findings

## False Positives
### FP-001: [title]
- Config: [which config]
- Rule: [which rule]
- Why wrong: [explanation]
- Fix: [what to change]

## False Negatives
### FN-001: [title]
- Config: [which config]
- Missing: [what should have been flagged]
- Impact: [why it matters]
- Suggested rule: [description]

## Bad Recommendations
### BR-001: [title]
...

## Parser Failures
### PF-001: [title]
...

## UX Confusion
### UX-001: [title]
...

## Summary
- Total configs reviewed: X
- Total findings reviewed: X
- False positives: X
- False negatives: X
- Parser failures: X
- UX issues: X

## Top 5 Priorities for Next Milestone
1. [priority 1]
2. [priority 2]
3. [priority 3]
4. [priority 4]
5. [priority 5]
```

## Success Criteria

Dogfooding is successful when:
> Terjemahan Indonesia: Dogfooding adalah successful when:
1. At least 10 real configs reviewed
2. At least 5 false positives identified
3. At least 5 false negatives identified
4. At least 3 UX issues identified
5. Top 5 priorities for next milestone are clear

## Output

After dogfooding, you should have:
> Terjemahan Indonesia: After dogfooding, you should memiliki:
1. `dogfooding/feedback_YYYY-MM-DD.md` â€” structured feedback
2. Updated golden test scenarios based on real findings
3. Clear priorities for Milestone 3 (Network Operations)

## Important Rules

1. **Do not fix issues during dogfooding.** Just log them.
2. **Do not add new rules during dogfooding.** Just note what's missing.
3. **Do not change parser during dogfooding.** Just note failures.
4. **Focus on quality, not quantity.** 10 configs reviewed deeply > 100 configs skimmed.

Dogfooding is about learning, not building.
> Terjemahan Indonesia: Dogfooding adalah about learning, not building.
