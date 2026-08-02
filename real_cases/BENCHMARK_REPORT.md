

# Benchmark Report

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Real case study documentation
<!-- DOCUMENT_METADATA_END -->

## Summary

| Metric | Value |
|--------|-------|
| Benchmark Type | Network Engineer |
| Total Cases | 30 |
| MikroTik Cases | 10 (config.rsc format) |
| Cisco Cases | 10 (config.txt format) |
| Fortinet Cases | 10 (config.txt format) |

## Vendor Breakdown

| Vendor | Cases | Status |
|--------|-------|--------|
| MikroTik | 10 | Ready |
| Cisco | 10 | Ready |
| Fortinet | 10 | Ready |
| Other | 0 | - |
| **Total** | **30** | Ready |

## Quality Metrics

| Metric | Formula | Status |
|--------|---------|--------|
| Precision | TP / (TP + FP) | Requires benchmark run |
| Recall | TP / (TP + FN) | Requires benchmark run |
| Accuracy | (TP + TN) / Total | Requires benchmark run |
| False Positive Rate | FP / Total | Requires benchmark run |
| False Negative Rate | FN / Total | Requires benchmark run |
| Exact Match Rate | Perfect matches / Total | Requires benchmark run |

## Bug Fixes Applied

1. **Missing expected_findings derivation** - Added `_derive_expected_findings()` function to map tags to expected finding strings
2. **Parser can_parse bug** - Fixed type comparison in TextConfigParser
3. **Missing telemetry module** - Created necessary module structure

## Expected Findings Matching

Expected findings are derived from `expected.json` tags:

| Tag | Derived Findings |
|-----|-----------------|
| security | ["security issue detected", "insecure configuration"] |
| telnet | ["telnet enabled", "insecure management"] |
| ssh | ["ssh", "secure shell"] |
| vpn | ["vpn", "remote access"] |
| firewall | ["firewall", "access control"] |
| vlan | ["vlan", "switch", "trunk"] |
| bgp | ["bgp", "routing", "peer"] |
| ospf | ["ospf", "routing", "area"] |
| qos | ["queue", "traffic shaping", "priority"] |
| nat | ["nat", "masquerade", "port forwarding"] |
| wireless | ["wireless", "wlan", "ssid"] |

## Execution Commands

```bash
# Local execution
python benchmarks/network_engineer_benchmark.py

# API execution
curl -X POST http://localhost:8000/api/v1/benchmark/run
```

## Notes

- All 30 real cases have valid config files and expected.json
- Benchmark runner is functional after bug fixes
- Expected findings are now derived from tags in expected.json files

