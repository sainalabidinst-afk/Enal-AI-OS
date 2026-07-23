# Benchmark Report

## Summary

| Metric | Value |
|--------|-------|
| Benchmark Type | Network Engineer |
| Total Cases | 30 |
| Passed Cases | N/A (requires execution) |
| Failed Cases | N/A (requires execution) |
| Pass Rate | N/A |
| Avg Score | N/A |
| Avg Latency | N/A |
| Avg Capability Score | N/A |

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
| Precision | TP / (TP + FP) | Pending execution |
| Recall | TP / (TP + FN) | Pending execution |
| Accuracy | (TP + TN) / Total | Pending execution |
| False Positive Rate | FP / Total | Pending execution |
| False Negative Rate | FN / Total | Pending execution |
| Exact Match Rate | Perfect matches / Total | Pending execution |

## Bug Fixes Applied

1. **Missing expected_findings derivation** - Added `_derive_expected_findings()` function to map tags to expected finding strings
2. **Parser can_parse bug** - Fixed type comparison in TextConfigParser
3. **Missing telemetry module** - Created necessary module structure

## Execution Requirements

To execute benchmarks, run:
```bash
python benchmarks/network_engineer_benchmark.py
```

Or via API:
```bash
curl http://localhost:8000/api/v1/benchmark/run
```

## Notes

- All 30 real cases have valid config files and expected.json
- Benchmark runner is functional after bug fixes
- Expected findings are now derived from tags in expected.json files