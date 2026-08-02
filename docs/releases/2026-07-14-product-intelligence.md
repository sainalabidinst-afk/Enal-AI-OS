<!-- BILINGUAL_DOCS_START -->
## Bahasa Indonesia / English

### Ringkasan / Summary
Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.
> Terjemahan Indonesia: Dokumen ini telah disiapkan dalam format bilingual agar mudah dibaca oleh pengguna Indonesia dan pembaca internasional.

- Bahasa Indonesia: konten utama tetap dipertahankan dalam dokumen asli, dan bagian ini memberi konteks ringkas dalam bahasa Indonesia.
- English: the main content remains in the original document, and this section provides a concise bilingual context for international readers.

### Informasi Dokumen / Document Info
- File: `docs/releases/2026-07-14-product-intelligence.md`
- Judul: 2026 07 14 Product Intelligence
- Status: bilingual header added

<!-- BILINGUAL_DOCS_END -->

# Product Intelligence v1.0.0-dev Release Notes

<!-- DOCUMENT_METADATA_START -->
**Owner:** Documentation Team
**Canonical Owner:** Documentation Governance Lead
**Last Verified:** 2026-08-02
**Version:** 1.0.0
**Status:** Active
**SSOT:** Release documentation
<!-- DOCUMENT_METADATA_END -->

**Release Date:** 2026-07-14  
**Milestone:** Product Intelligence  
**Codename:** Capability Benchmark + Quality Intelligence

## Overview

This release transforms Enal AI OS from a config analysis platform into an AI Quality Engineering platform. The system now measures its own capability quality through telemetry, benchmarking, capability scoring, regression detection, and confidence calibration.
> Terjemahan Indonesia: Ini rilis transforms Enal AI OS dari sebuah config analysis platform into sebuah AI kualitas rekayasa platform. sistem now measures its own kapabilitas kualitas through telemetry, benchmarking, kapabilitas scoring, regression detection, dan confidence calibration.

## What Changed

### Backend

- **Telemetry Framework**: JSONL-based event collection for analysis, chat, parser, and reasoning events. KPI aggregation service computes pass rate, evidence coverage, compliance coverage, false positive rate, and more.
- **Benchmark Framework**: Async `BenchmarkRunner` with `httpx.AsyncClient` connection pooling, `asyncio.Semaphore` concurrency control (default 5), and `ProgressCallback` protocol for real-time progress.
- **Capability Scoring**: Per-case capability breakdown across 5 dimensions: parser, reasoning, evidence, compliance, and executive report. Each dimension scored 0-100, averaged into total capability score.
- **Golden Expected Results**: Benchmark cases now support `expected.json` with structured expected findings, risk/confidence thresholds, and compliance targets. Case directories follow the `sample_hotspot/` pattern with `config.rsc`, `expected.json`, `report.md`, and `metadata.yaml`.
- **CCE API**: `POST /api/v1/benchmark/run` now returns `capability_score` and `capability_breakdown` per result. `GET /api/v1/benchmark/capability-scores` aggregates per vendor. `GET /api/v1/benchmark/cce/status` shows latest CCE status with regression alerts and calibration data.

### New Modules

- `benchmarks/cce.py` â€” Continuous Capability Evaluation runner. Executes full benchmark suite, computes capability scores, detects regressions against previous runs/baseline, runs confidence calibration, persists history, and generates HTML reports.
- `benchmarks/trend_analyzer.py` â€” Trend analysis and regression detection. Computes per-vendor trend direction (`up`/`down`/`stable`) and flags regressions where capability score drops by â‰¥5 points.
- `benchmarks/calibration.py` â€” Confidence calibration analyzer. Bins results by confidence score and computes empirical accuracy per bin, detecting overconfidence and underconfidence.
- `benchmarks/report_generator.py` â€” HTML dashboard generator. Produces visual reports with capability breakdown tables, regression alerts, confidence calibration tables, and CSS-styled trend indicators.

### CI/CD

- `.github/workflows/cce.yml` â€” Automated CCE on every push/PR to `main`. Fails build on regression detection. Uploads HTML report as artifact. Generates GitHub Badge URL.

### Data

- `real_cases/mikrotik/sample_hotspot/` â€” First real case with golden expected results, report, and metadata.
- `benchmarks/cce_history/` â€” Runtime-generated CCE history storage (gitignored).

## Migration Notes

- `BenchmarkRunner._load_expected()` now searches `expected.json` inside the case directory first, then falls back to legacy `<filename>.expected.json`.
- `BenchmarkRunner._load_case_content()` supports both absolute paths and relative `real_cases/<vendor>/<filename>` paths.
- `BenchmarkResult` now includes `capability_score` and `capability_breakdown`.
- `ExpectedResult.from_dict()` supports nested `{"expected": {...}, "metadata": {...}}` format.

## Validation

- All benchmark modules pass `ruff` lint.
- All imports verified.
- Existing test suite: 74 passed, 18 failed (pre-existing, unrelated to this release).

## Next Steps

- Capability Excellence Campaign: raise each capability score to target KPIs.
- Continuous Capability Evaluation (CCE) integration into daily development workflow.
- 30-day dogfooding period with real-world cases.
- Developer Preview with CCE quality gate active.
