"""
Generic Benchmark Dashboard Generator
=======================================

Generates an HTML dashboard from any benchmark result.

Usage:
    python benchmarks/generate_dashboard.py --pack "Trading Analyst" --module benchmarks.trading_analyst_benchmark --function run_trading_benchmark
    python benchmarks/generate_dashboard.py --pack "Code Engineer" --module benchmarks.code_engineer_benchmark --function run_code_engineer_benchmark
"""

from __future__ import annotations

import argparse
import asyncio
import html
import importlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

NON_DIMENSION_KEYS = {
    'overall', 'overall_score', 'passed', 'passed_target', 'pass_rate',
    'overall_percentage', 'generated_at', 'grade', 'target_grade',
    'target_percentage', 'results', 'total_scenarios', 'passed_cases',
    'failed_cases', 'avg_latency_ms', 'vendor_breakdown',
    'scenarios_run', 'evidence_total', 'domains_detected',
    'domain_evidence_count', 'total_cases', 'total_architecture_findings',
    'total_secure_coding_findings', 'architecture_by_category',
    'security_by_category', 'scenario_details', 'problems_detected',
    'problems_missed', 'false_positives', 'avg_capability_score',
    'total', 'failed', 'total_findings', 'summary', 'compliance_report',
    'findings', 'raw', 'market', 'strategy', 'bias', 'confidence',
    'risk_level', 'reasoning_steps', 'counter_scenario', 'evidence',
    'signal', 'action', 'top_evidence', 'analyzers', 'domain',
    'timestamp', 'scenario_id', 'name', 'category',
    'min_problems', 'min_solutions', 'solutions_proposed',
    'min_problems_required', 'min_solutions_required',
    'execution_time_ms', 'capability_score', 'errors',
    'findings_matched', 'expected_findings', 'vendor',
    'title', 'parser', 'compliance', 'executive_report',
    'description', 'expected_patterns', 'detected_patterns',
    'expected', 'actual', 'matched', 'total_findings',
    'compliance_standards', 'threat_model', 'hardening_score',
    'dependency_vulnerabilities', 'secret_count', 'owasp_findings',
    'vulnerability_count', 'trend', 'previous_score',
    'regression', 'capabilities', 'cases', 'bins', 'calibration',
    'confidence_bins', 'predicted', 'actual', 'count',
}


def _is_dimension(key: str, value: Any) -> bool:
    if not isinstance(value, (int, float)):
        return False
    if key in NON_DIMENSION_KEYS:
        return False
    return True


def normalize_report(pack_name: str, raw_result: Any, target: float = 0.9) -> dict[str, Any]:
    if hasattr(raw_result, 'to_dict'):
        data = raw_result.to_dict()
    elif isinstance(raw_result, dict):
        data = raw_result
    else:
        raise TypeError(f"Unsupported report type: {type(raw_result)}")

    overall_score = 0.0
    for key in ('overall_score', 'overall_percentage'):
        if key in data and isinstance(data[key], (int, float)):
            overall_score = float(data[key])
            break
    if overall_score == 0.0 and 'overall' in data and isinstance(data['overall'], (int, float)):
        overall_score = float(data['overall']) * 100.0
    if overall_score == 0.0 and 'pass_rate' in data and isinstance(data['pass_rate'], (int, float)):
        overall_score = float(data['pass_rate']) * 100.0
    if overall_score == 0.0 and 'avg_score' in data and isinstance(data['avg_score'], (int, float)):
        overall_score = float(data['avg_score']) * 100.0

    passed = False
    for key in ('passed', 'passed_target'):
        if key in data and isinstance(data[key], bool):
            passed = bool(data[key])
            break
    if not passed and 'pass_rate' in data and isinstance(data['pass_rate'], (int, float)):
        passed = float(data['pass_rate']) >= target
    if not passed:
        passed = overall_score >= target * 100.0

    generated_at = data.get('generated_at', datetime.utcnow().isoformat())
    if hasattr(generated_at, 'isoformat'):
        generated_at = generated_at.isoformat()

    dimensions = []
    for key, value in data.items():
        if _is_dimension(key, value):
            score = float(value)
            if 0.0 <= score <= 1.0:
                display = score * 100.0
            else:
                display = score
            dimensions.append({
                'name': key.replace('_', ' ').title(),
                'score': display,
                'raw_score': score,
            })

    scenarios = []
    for key in ('results', 'scenario_details', 'cases', 'entries'):
        if key in data and isinstance(data[key], list):
            scenarios = data[key]
            break

    grade = 'F'
    if overall_score >= 95.0:
        grade = 'A+'
    elif overall_score >= 90.0:
        grade = 'A'
    elif overall_score >= 80.0:
        grade = 'B'
    elif overall_score >= 70.0:
        grade = 'C'
    elif overall_score >= 60.0:
        grade = 'D'

    return {
        'pack_name': pack_name,
        'generated_at': generated_at,
        'overall_score': overall_score,
        'passed': passed,
        'grade': grade,
        'dimensions': dimensions,
        'scenarios': scenarios,
        'raw': data,
    }


def _status_badge(score: float) -> str:
    if score >= 95.0:
        return '<span class="badge badge-success">A+</span>'
    if score >= 90.0:
        return '<span class="badge badge-success">A</span>'
    if score >= 80.0:
        return '<span class="badge badge-warning">B</span>'
    if score >= 70.0:
        return '<span class="badge badge-warning">C</span>'
    return '<span class="badge badge-danger">F</span>'


def _score_bar(score: float) -> str:
    return (
        f'<div class="score-bar"><div class="score-fill" style="width:{min(score, 100):.1f}%"></div></div>'
        f'<span class="score-text">{score:.1f}%</span>'
    )


def generate_dashboard(pack_name: str, report: dict[str, Any], output_path: Path) -> Path:
    status_class = "pass" if report["passed"] else "fail"
    status_text = "PASS" if report["passed"] else "FAIL"

    dimension_rows = ""
    for dim in report['dimensions']:
        dimension_rows += f"""
            <tr>
              <td>{html.escape(dim['name'])}</td>
              <td>{_score_bar(dim['score'])}</td>
              <td>{_status_badge(dim['score'])}</td>
            </tr>
        """

    scenario_rows = ""
    scenarios_section = ""
    if report.get('scenarios'):
        headers_set = set()
        for row in report['scenarios']:
            if isinstance(row, dict):
                headers_set.update(row.keys())
        headers = [h for h in sorted(headers_set) if h not in ('raw', 'market', 'strategy', 'evidence', 'analyzers', 'domain')]
        if headers:
            header_cells = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
            tbody = ""
            for row in report['scenarios']:
                if not isinstance(row, dict):
                    continue
                cells = ""
                for h in headers:
                    val = row.get(h, "")
                    if isinstance(val, bool):
                        val = "PASS" if val else "FAIL"
                    elif isinstance(val, (dict, list)):
                        val = json.dumps(val, default=str)
                    cells += f"<td>{html.escape(str(val))}</td>"
                tbody += f"<tr>{cells}</tr>"
            scenario_rows = f"<thead><tr>{header_cells}</tr></thead><tbody>{tbody}</tbody>"

    if scenario_rows:
        scenarios_section = f"""
  <div class="section">
    <h2 style="margin-top:0;font-size:16px;">Scenario Results</h2>
    <div style="overflow-x:auto;">
      <table>
        {scenario_rows}
      </table>
    </div>
  </div>
"""

    if not dimension_rows:
        dimension_rows = '<tr><td colspan="3" style="color:#656d76;">No dimension data available</td></tr>'

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(pack_name)} Benchmark Dashboard</title>
<style>
  :root {{ color-scheme: light; }}
  body {{ font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 0; background: #f6f7fb; color: #1f2328; }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 24px; }}
  h1 {{ margin: 0 0 4px; font-size: 22px; }}
  .subtitle {{ color: #656d76; margin-bottom: 16px; }}
  .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
  .card {{ background: #ffffff; border: 1px solid #d0d7de; border-radius: 12px; padding: 16px; box-shadow: 0 1px 0 rgba(0,0,0,0.04); }}
  .metric {{ font-size: 28px; font-weight: 700; }}
  .metric-label {{ color: #656d76; font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; }}
  .section {{ background: #ffffff; border: 1px solid #d0d7de; border-radius: 12px; padding: 16px; margin-top: 16px; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #e6e8eb; font-size: 14px; }}
  th {{ color: #656d76; font-weight: 600; font-size: 12px; text-transform: uppercase; }}
  .score-bar {{ width: 100%; height: 10px; background: #e6e8eb; border-radius: 999px; overflow: hidden; margin-top: 4px; }}
  .score-fill {{ height: 100%; background: #2da44e; border-radius: 999px; }}
  .score-text {{ font-weight: 600; font-size: 13px; }}
  .badge {{ padding: 2px 8px; border-radius: 999px; font-size: 12px; font-weight: 600; }}
  .badge-success {{ background: #dafbe1; color: #1a7f37; }}
  .badge-warning {{ background: #fff8c5; color: #9a6700; }}
  .badge-danger {{ background: #ffebe9; color: #cf222e; }}
  .pass {{ color: #1a7f37; font-weight: 700; }}
  .fail {{ color: #cf222e; font-weight: 700; }}
  .error {{ background: #ffebe9; border-color: #cf222e; }}
  .error .metric {{ color: #cf222e; }}
</style>
</head>
<body>
<div class="container">
  <h1>{html.escape(pack_name)} Benchmark Dashboard</h1>
  <div class="subtitle">Generated: {html.escape(str(report['generated_at']))} · {len(report['dimensions'])} dimensions</div>
  <div class="grid">
    <div class="card">
      <div class="metric">{html.escape(report['grade'])}</div>
      <div class="metric-label">Grade</div>
    </div>
    <div class="card">
      <div class="metric">{report['overall_score']:.1f}%</div>
      <div class="metric-label">Overall Score</div>
    </div>
    <div class="card">
      <div class="metric {status_class}">{status_text}</div>
      <div class="metric-label">Status</div>
    </div>
  </div>

  <div class="section">
    <h2 style="margin-top:0;font-size:16px;">Score Breakdown by Dimension</h2>
    <div style="overflow-x:auto;">
      <table>
        <thead>
          <tr><th>Dimension</th><th>Score</th><th>Grade</th></tr>
        </thead>
        <tbody>
          {dimension_rows}
        </tbody>
      </table>
    </div>
  </div>

  {scenarios_section}

  <div class="section">
    <h2 style="margin-top:0;font-size:16px;">Raw Report</h2>
    <pre style="background:#f6f8fa;padding:12px;border-radius:8px;overflow:auto;font-size:13px;">{html.escape(json.dumps(report['raw'], indent=2, default=str))}</pre>
  </div>
</div>
</body>
</html>"""

    output_path.write_text(html_content, encoding="utf-8")
    return output_path


def run_benchmark(module_path: str, function_name: str) -> Any:
    module = importlib.import_module(module_path)
    fn = getattr(module, function_name)
    if asyncio.iscoroutinefunction(fn):
        return asyncio.run(fn())
    return fn()


def run_and_generate(pack_name: str, module_path: str, function_name: str, output_path: Path, target: float = 0.9) -> dict[str, Any]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        raw = run_benchmark(module_path, function_name)
        report = normalize_report(pack_name, raw, target=target)
    except Exception as exc:
        report = {
            'pack_name': pack_name,
            'generated_at': datetime.utcnow().isoformat(),
            'overall_score': 0.0,
            'passed': False,
            'grade': 'F',
            'dimensions': [],
            'scenarios': [],
            'raw': {'error': str(exc)},
        }
    try:
        generate_dashboard(pack_name, report, output_path)
    except Exception as exc:
        report['generation_error'] = str(exc)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Generic Benchmark Dashboard Generator")
    parser.add_argument("--pack", required=True, help="Pack display name")
    parser.add_argument("--module", required=True, help="Benchmark module path (e.g. benchmarks.trading_analyst_benchmark)")
    parser.add_argument("--function", required=True, help="Benchmark run function name")
    parser.add_argument("--output", required=True, help="Output HTML path")
    parser.add_argument("--target", type=float, default=0.9, help="Pass target (default 0.9)")
    args = parser.parse_args()

    output_path = Path(args.output)
    run_and_generate(args.pack, args.module, args.function, output_path, target=args.target)
    print(f"Dashboard generated: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
