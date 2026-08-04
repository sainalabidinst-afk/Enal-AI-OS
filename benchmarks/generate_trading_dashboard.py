"""
Trading Analyst Benchmark Dashboard Generator
==============================================

Generates an HTML dashboard from trading analyst benchmark results.

Usage:
    python benchmarks/generate_trading_dashboard.py [--scenarios N]
"""

from __future__ import annotations

import argparse
import asyncio
import html
import json
from datetime import datetime
from pathlib import Path

from benchmarks.trading_analyst_benchmark import (
    DOMAINS,
    BENCHMARK_TIMEFRAMES,
    run_trading_benchmark,
    _seed_scenario,
    _run_scenario,
    _analyze_domains,
    _score_reasoning,
    _score_coverage,
    _score_explainability,
    _score_safety,
    _score_consistency,
)


def _status_badge(score: float) -> str:
    if score >= 95.0:
        return '<span class="badge badge-success">A+</span>'
    if score >= 90.0:
        return '<span class="badge badge-success">A</span>'
    if score >= 80.0:
        return '<span class="badge badge-warning">B</span>'
    return '<span class="badge badge-danger">F</span>'


def _score_bar(score: float) -> str:
    return (
        f'<div class="score-bar"><div class="score-fill" style="width:{min(score, 100):.1f}%"></div></div>'
        f'<span class="score-text">{score:.1f}%</span>'
    )


def generate_dashboard(report, output_path: Path) -> Path:
    grade = "A+" if report.overall_score >= 95.0 else "A" if report.overall_score >= 90.0 else "B" if report.overall_score >= 80.0 else "F"

    domain_rows = ""
    for domain in DOMAINS:
        count = report.domain_evidence_count.get(domain, 0)
        detected = "YES" if domain in report.domains_detected else "NO"
        domain_rows += f"""
            <tr>
              <td>{html.escape(domain)}</td>
              <td>{count}</td>
              <td>{detected}</td>
            </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Trading Analyst Benchmark Dashboard</title>
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
</style>
</head>
<body>
<div class="container">
  <h1>Trading Analyst Benchmark Dashboard</h1>
  <div class="subtitle">Generated: {report.generated_at.isoformat()} · {report.scenarios_run} scenarios · {len(report.domains_detected)}/{len(DOMAINS)} domains</div>

  <div class="grid">
    <div class="card">
      <div class="metric">{grade}</div>
      <div class="metric-label">Grade</div>
    </div>
    <div class="card">
      <div class="metric">{report.overall_score:.1f}%</div>
      <div class="metric-label">Overall Score</div>
    </div>
    <div class="card">
      <div class="metric {'pass' if report.passed else 'fail'}">{'PASS' if report.passed else 'FAIL'}</div>
      <div class="metric-label">Status</div>
    </div>
  </div>

  <div class="section">
    <h2 style="margin-top:0;font-size:16px;">Dimension Scores</h2>
    <div style="overflow-x:auto;">
      <table>
        <thead>
          <tr><th>Dimension</th><th>Score</th><th>Grade</th></tr>
        </thead>
        <tbody>
          <tr><td>Reasoning</td><td>{_score_bar(report.reasoning_score)}</td><td>{_status_badge(report.reasoning_score)}</td></tr>
          <tr><td>Coverage</td><td>{_score_bar(report.coverage_score)}</td><td>{_status_badge(report.coverage_score)}</td></tr>
          <tr><td>Explainability</td><td>{_score_bar(report.explainability_score)}</td><td>{_status_badge(report.explainability_score)}</td></tr>
          <tr><td>Consistency</td><td>{_score_bar(report.consistency_score)}</td><td>{_status_badge(report.consistency_score)}</td></tr>
          <tr><td>Safety</td><td>{_score_bar(report.safety_score)}</td><td>{_status_badge(report.safety_score)}</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="section">
    <h2 style="margin-top:0;font-size:16px;">Knowledge Domain Coverage</h2>
    <div style="overflow-x:auto;">
      <table>
        <thead>
          <tr><th>Domain</th><th>Evidence Count</th><th>Detected</th></tr>
        </thead>
        <tbody>
          {domain_rows}
        </tbody>
      </table>
    </div>
  </div>

  <div class="section">
    <h2 style="margin-top:0;font-size:16px;">Raw Report</h2>
    <pre style="background:#f6f8fa;padding:12px;border-radius:8px;overflow:auto;font-size:13px;">{html.escape(json.dumps(report.to_dict(), indent=2))}</pre>
  </div>
</div>
</body>
</html>"""

    output_path.write_text(html_content, encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Trading Analyst Benchmark Dashboard")
    parser.add_argument("--scenarios", type=int, default=20, help="Number of scenarios")
    parser.add_argument("--output", type=str, default="benchmarks/reports/trading_dashboard.html", help="Output path")
    args = parser.parse_args()

    report = asyncio.run(run_trading_benchmark(num_scenarios=args.scenarios))
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    generate_dashboard(report, output_path)
    print(f"Dashboard generated: {output_path}")
    print(f"Overall Score: {report.overall_score:.1f}% ({'PASS' if report.passed else 'FAIL'})")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
