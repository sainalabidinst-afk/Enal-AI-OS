# BENCHMARK INVENTORY
# Network Engineer Benchmark System

## Files
| File | Purpose |
|------|---------|
| `benchmark.py` | Benchmark runner and harness |
| `schema.py` | RealCase and RealCaseEvidence dataclasses |
| `collector.py` | Case persistence utilities |
| `kpi.py` | KPI tracking (empty) |
| `analyzer_rules_mapping.md` | Rule domain classification |
| `RULE_INVENTORY.md` | Rule catalog |
| `RULE_GAP_REPORT.md` | Gap analysis |
| `RULE_COVERAGE.md` | Coverage metrics |

## Benchmark Runner Components
| Component | Location | Description |
|-----------|----------|-------------|
| `BenchmarkHarness` | benchmark.py:34 | Main harness class |
| `BenchmarkResult` | benchmark.py:16 | Result dataclass |
| `load_cases_from_disk()` | benchmark.py:173 | Loads cases from real_cases/ |
| `run()` | benchmark.py:38 | Executes single benchmark |
| `run_benchmark_for_category()` | benchmark.py:214 | Batch run by category |
| `summary()` | benchmark.py:156 | Aggregate metrics |

## Evaluator Components
| Component | Location | Description |
|-----------|----------|-------------|
| `_score_parser()` | benchmark.py:116 | Parser quality scoring |
| `_score_reasoning()` | benchmark.py:124 | Reasoning quality scoring |
| `_score_evidence()` | benchmark.py:137 | Evidence quality scoring |
| `_score_compliance()` | benchmark.py:143 | Compliance scoring |
| `_score_executive_report()` | benchmark.py:149 | Report quality scoring |

## Expected Results
- `expected.json` per case directory
- Contains: vendor, device_type, expected.critical/high/medium/low, compliance_score_min, risk_max, metadata.description

## Output Analyzer
- `analyze_attachment()` in backend/app/core/attachments/analyzer.py
- Returns AttachmentAnalysisResult with: ast, summary, risk_score, recommendations

## Report Generator
- Executive summary in analysis result
- Capability scores in benchmark result