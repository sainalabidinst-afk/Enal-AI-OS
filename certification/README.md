# ENAL AI OS — Capability Certification Framework

This directory contains the governance framework for certifying Capability Packs within ENAL AI OS.

## Directory Structure

```
certification/
├── schema/
│   ├── capability-certificate.schema.json
│   ├── audit-report.schema.json
│   ├── benchmark-record.schema.json
│   ├── golden-test-suite.schema.json
│   ├── real-case-validation.schema.json
│   ├── production-readiness.schema.json
│   └── certification-review.schema.json
├── scripts/
│   ├── run_audit.py
│   ├── generate_certificates.py
│   └── dashboard.py
├── checklist/
│   └── audit-checklist.md
├── audits/
│   └── {capability_id}-audit.json
├── benchmarks/
│   └── {capability_id}-benchmark.json
├── golden-tests/
│   └── {capability_id}/
├── real-cases/
│   └── {capability_id}/
├── reports/
│   └── {capability_id}-audit-report.txt
├── certificates/
│   └── {capability_id}-certificate.json
├── dashboard.json
├── README.md
├── README-golden-tests.md
├── README-real-cases.md
├── README-production-readiness.md
└── README-certification-review.md
```

## Phases

| Phase | Artifact | Status |
|-------|----------|--------|
| Phase 1.1 — Capability Audit | `audits/{capability_id}-audit.json` | ✅ Scripted |
| Phase 1.2 — Benchmark Audit | `benchmarks/{capability_id}-benchmark.json` | 🟡 Scaffolded |
| Phase 1.3 — Golden Test Expansion | `golden-tests/{capability_id}/` | 🟡 Scaffolded |
| Phase 1.4 — Real Case Validation | `real-cases/{capability_id}/` | 🟡 Scaffolded |
| Phase 1.5 — Production Readiness Review | `production-readiness.json` | 🟡 Scaffolded |
| Phase 1.6 — Certification Review | `certificates/{capability_id}-certificate.json` | ✅ Scripted |

## Usage

### Run All Audits
```bash
python certification/scripts/run_audit.py --all
```

### Run Single Capability Audit
```bash
python certification/scripts/run_audit.py --capability trading_analyst
```

### Generate Certificates
```bash
python certification/scripts/generate_certificates.py --all
```

### Generate Dashboard
```bash
python certification/scripts/dashboard.py
```

## Grading

| Score Range | Grade | Certification Level |
|-------------|-------|---------------------|
| 90 - 100 | A | Certified |
| 80 - 89 | B | Certified |
| 70 - 79 | C | Provisional |
| 60 - 69 | D | Experimental |
| < 60 | F | Experimental |

## Current Status

Run `python certification/scripts/dashboard.py` to see the current certification status of all capabilities.
