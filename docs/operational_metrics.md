<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/operational_metrics.md`
- Judul: Operational Metrics
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# ECP Network Engineer â€” Operational Metrics

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for operational_metrics
<!-- DOCUMENT_METADATA_END -->

**Focus:** Time Saved, Operational Reliability, Learning Velocity

---

## Primary Metric: Time Saved

This is the single most important metric for Network Engineer.
> Terjemahan Indonesia: Ini adalah single most important metric untuk Network Engineer.

### How to Measure

| Task | Manual Time | With ECP | Time Saved |
|------|-------------|----------|------------|
| Audit router config | 45 min | 6 min | 87% |
| Generate config from requirements | 30 min | 5 min | 83% |
| Create deployment documentation | 60 min | 2 min | 97% |
| Compare two configs | 20 min | 1 min | 95% |
| Compliance audit | 90 min | 5 min | 94% |
| Health check | 30 min | 1 min | 97% |

**Target:** Average time saved â‰¥ 80%

### How to Track

During dogfooding, log each task:
> Terjemahan Indonesia: Selama dogfood, catat setiap tugas:

```markdown
## Task: Audit Sun Clint Router
- Date: 2026-07-09
- Config: sun-clint-backup.rsc
- Manual estimate: 45 min
- With ECP: 6 min
- Time saved: 87%
- Notes: ECP found 2 issues I missed, missed 1 issue I caught
```

---

## Secondary Metric: Operational Reliability

How often does ECP help prevent problems?
> Terjemahan Indonesia: Seberapa sering ECP membantu mencegah masalah?

| Metric | Target |
|--------|--------|
| Deployment verification pass rate | â‰¥95% |
| Rollback success rate | 100% |
| False negative rate (missed issues) | â‰¤5% |
| False positive rate (false alarms) | â‰¤10% |

---

## Tertiary Metric: Learning Velocity

How fast can a junior engineer become productive?
> Terjemahan Indonesia: How fast dapat sebuah junior engineer become productive?

| Metric | Target |
|--------|--------|
| Time to first successful analysis | <30 min |
| Time to understand a finding | <2 min (with Explain Like Engineer) |
| Time to run first deployment | <1 hour |
| Confidence in ECP recommendation | â‰¥4/5 |

---

## Dashboard View

```
ECP Network Engineer â€” Operational Dashboard
=============================================

Time Saved This Week:    87% (target: â‰¥80%)
Deployments Verified:    12/12 (100%)
Rollbacks Triggered:     0/12 (0%)
False Negatives:         2 (5%)
False Positives:         3 (8%)

Dogfooding Sessions:     5 configs reviewed
Feedback Items:          12 logged
Top Priority:            Explain Like Engineer for firewall rules

Next Review:             2026-07-16
```

---

## What We Do NOT Measure

These technical metrics are NOT the focus:
> Terjemahan Indonesia: These technical metrics adalah NOT focus:

- âŒ Number of files
- âŒ Number of rules
- âŒ Parser coverage %
- âŒ Benchmark latency (unless it affects usability)
- âŒ Code coverage %

These are means, not ends.
> Terjemahan Indonesia: These adalah means, not ends.

The only metric that matters is: **"Can a network engineer do their job faster and safer with ECP than without it?"**
> Terjemahan Indonesia: Only metric itu matters adalah: "dapat sebuah network engineer do their job faster dan safer dengan ECP than without it?"

If the answer is yes, everything else is noise.
> Terjemahan Indonesia: If answer adalah yes, everything else adalah noise.
