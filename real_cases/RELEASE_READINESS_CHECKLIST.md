# Release Readiness Checklist

## Environment Prerequisites
- [ ] Python 3.11+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -e ./backend`)
- [ ] Environment variables configured

## Source Code
- [ ] Telemetry module exists (`backend/app/core/telemetry/`)
- [ ] Parser bugs fixed (`text_config.py:19`)
- [ ] Cross-file indentation fixed (`cross_file.py`)
- [ ] Expected findings derivation implemented (`benchmark.py`)
- [ ] Logging added to exception handlers

## Dataset
- [ ] 30 real cases present (MikroTik: 10, Cisco: 10, Fortinet: 10)
- [ ] All expected.json files valid
- [ ] All config files readable

## Reports
- [ ] SPRINT_5A1_REPORT.md present
- [ ] SPRINT_5A2_REPORT.md present
- [ ] SPRINT_5A3_REPORT.md present
- [ ] SPRINT_5A4_REPORT.md present
- [ ] SPRINT_5A5_REPORT.md present
- [ ] RELEASE_VERIFICATION_REPORT.md present
- [ ] RUNBOOK_RELEASE_CERTIFICATION.md present
- [ ] DOCUMENT_CONSISTENCY_REPORT.md present

## Benchmark Execution
- [ ] Run `python -m benchmarks.network_engineer_benchmark`
- [ ] Verify pass rate >= 95%
- [ ] Verify avg latency < 2000ms
- [ ] Save `benchmarks/reports/network_benchmark.json`
- [ ] Save `benchmarks/reports/network_benchmark.csv`

## Final Certification
- [ ] All checklist items verified
- [ ] Benchmark results documented
- [ ] GOLD STANDARD CERTIFIED status determined