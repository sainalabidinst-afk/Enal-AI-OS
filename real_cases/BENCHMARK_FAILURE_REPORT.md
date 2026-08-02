<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `real_cases/BENCHMARK_FAILURE_REPORT.md`
- Judul: Benchmark Failure Report
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Benchmark Failure Report

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

## Critical Bug Fixed

### Bug #1: Missing expected_findings Population
**Location**: `real_cases/benchmark.py:load_cases_from_disk()` (line 205-238)
**Root Cause**: Function created RealCase with `expected_findings=[]` instead of deriving from expected.json tags
**Fix**: Added `_derive_expected_findings()` function to map expected tags to finding strings

### Bug #2: Parser Type Mismatch in text_config.py
**Location**: `backend/app/core/attachments/parsers/network/text_config.py:19`
**Root Cause**: `meta.attachment_type.config` compared against itself, always returning True for any extension
**Fix**: Added proper import and comparison against AttachmentType enum values

### Bug #3: Missing Telemetry Module
**Location**: `backend/app/core/telemetry/` 
**Root Cause**: Directory did not exist, causing ImportError in multiple API files
**Fix**: Created `__init__.py`, `service.py`, `aggregator.py`

## Case Analysis

### Expected vs Actual Finding Comparison

Based on expected.json analysis, findings are expected through tag-based matching:
> Terjemahan Indonesia: Based pada expected.json analysis, findings adalah expected through tag-based matching:

| Vendor | Categories | Tag Coverage |
|--------|------------|------------|
| MikroTik | 10 | security, telnet, ssh, vpn, firewall, acl, nat, routing, vlan, bridge, wireless, hotspot, dhcp, qos, ha, bgp, watchdog |
| Cisco | 10 | wireless, ssid, ospf, routing, vpn, services, qos, vlan, security, nat, firewall, acl, ha, hsrp |
| Fortinet | 9 | wireless, vpn, vlan, services, security, routing, firewall, qos, nat, ha |

## Missing Expected Findings Pattern

The expected.json files define:
> Terjemahan Indonesia: Expected.json files define:
- Severity counts (critical, high, medium, low)
- Tags for categorization
- Risk score thresholds
- Compliance score thresholds

But `expected_findings` list was not populated. The fix derives finding strings from tags.
> Terjemahan Indonesia: But expected_findings list was not populated. fix derives finding strings dari tags.

## Impact

Without the fix, benchmark matching would always fail with 0% because `expected_findings` was empty, causing:
> Terjemahan Indonesia: Without fix, benchmark matching would always fail dengan 0% because expected_findings was empty, causing:
- score = 0 / max(0, 1) = 0
- passed = False (0 >= 0.8 is False)
