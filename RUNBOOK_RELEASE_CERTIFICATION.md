
# RUNBOOK - Release Certification

<!-- DOCUMENT_METADATA_START -->
**Pemilik:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Terakhir Diverifikasi:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Documentation for RUNBOOK_RELEASE_CERTIFICATION
<!-- DOCUMENT_METADATA_END -->

## Prerequisites

### Environment
- Python 3.11 or higher
- pip package manager
- Virtual environment (recommended)

### Directory Structure
```
E:\Enal\Enal-AI-OS/
â”œâ”€â”€ backend/           # Backend API
â”œâ”€â”€ benchmarks/        # Benchmark scripts
â”œâ”€â”€ real_cases/        # Real case dataset
â””â”€â”€ pyproject.toml     # Workspace config
```

### Environment Variables
Create `.env` file in project root:
```
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
QDRANT_URL=...
SECRET_KEY=your-secret-key
```

---

## Installation

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate virtual environment
# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 3. Install dependencies
pip install -e ./backend
pip install -e .
```

---

## Running Benchmark

### Local Benchmark
```bash
# Run Network Engineer benchmark
cd E:\Enal\Enal-AI-OS
python -m benchmarks.network_engineer_benchmark
```

### API Benchmark
```bash
# Start API server
uvicorn backend.app.main:app --reload --port 8000

# Run via API
curl -X POST http://localhost:8000/api/v1/benchmark/run
```

---

## Verifying Results

### Output Files
- `benchmarks/reports/network_benchmark.json` - Full results JSON
- `benchmarks/reports/network_benchmark.csv` - Results CSV

### Success Criteria
- Pass rate >= 95%
- Average latency < 2000ms
- All 30 real cases processed

---

## Certification Artifacts

Save these files as certification evidence:
1. `real_cases/SPRINT_5A1_REPORT.md`
2. `real_cases/SPRINT_5A2_REPORT.md`
3. `real_cases/SPRINT_5A3_REPORT.md`
4. `real_cases/SPRINT_5A4_REPORT.md`
5. `real_cases/SPRINT_5A5_REPORT.md`
6. `real_cases/RELEASE_VERIFICATION_REPORT.md`
7. `benchmarks/reports/network_benchmark.json` (after execution)
8. `benchmarks/reports/network_benchmark.csv` (after execution)