"""
HTML Report Generator
=======================

Generates an HTML dashboard from CCE results.

Includes:
- Overall pass rate and average scores
- Per-vendor capability breakdown
- Regression alerts
- Confidence calibration table
- Trend visualization (simple CSS bars)

Usage:
    from benchmarks.report_generator import generate_html_report
    from benchmarks.cce import CCEResult

    generate_html_report(cce_result, Path("report.html"))
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


def _status_badge(score: float, thresholds: tuple[float, float] = (85.0, 70.0)) -> str:
    if score >= thresholds[0]:
        return '<span class="badge badge-success">Healthy</span>'
    if score >= thresholds[1]:
        return '<span class="badge badge-warning">At Risk</span>'
    return '<span class="badge badge-danger">Critical</span>'


def _trend_icon(trend: str) -> str:
    return {"up": "&#9650;", "down": "&#9660;", "stable": "&#9644;"}.get(trend, "&#9644;")


def _trend_class(trend: str) -> str:
    return {"up": "trend-up", "down": "trend-down", "stable": "trend-stable"}.get(trend, "trend-stable")


def generate_html_report(result: Any, output_path: Path) -> Path:
    summary = result.summary
    capabilities = summary.get("capabilities", {})
    regressions = summary.get("regressions", [])
    calibration = result.calibration or {}
    bins = calibration.get("bins", [])

    rows = []
    for vendor, cap in sorted(capabilities.items()):
        cap_score = cap.get("avg_capability_score", 0)
        score = cap.get("avg_score", 0)
        passed = cap.get("passed", 0)
        total = cap.get("cases", 1)
        regression = cap.get("regression", False)
        trend = cap.get("trend", "stable")
        previous = cap.get("previous_score")
        rows.append(
            f"""
            <tr class="{'regression' if regression else ''}">
              <td>{html.escape(vendor)}</td>
              <td>{total}</td>
              <td>{passed}/{total}</td>
              <td>{_status_badge(cap_score)}</td>
              <td>
                <div class="score-bar"><div class="score-fill" style="width:{min(cap_score, 100)}%"></div></div>
                <span class="score-text">{cap_score:.1f}</span>
              </td>
              <td>
                <div class="score-bar"><div class="score-fill" style="width:{min(score * 100, 100)}%"></div></div>
                <span class="score-text">{score:.2f}</span>
              </td>
              <td>{cap.get('parser', 0):.1f}</td>
              <td>{cap.get('reasoning', 0):.1f}</td>
              <td>{cap.get('evidence', 0):.1f}</td>
              <td>{cap.get('compliance', 0):.1f}</td>
              <td>{cap.get('executive_report', 0):.1f}</td>
              <td class="{_trend_class(trend)}">{_trend_icon(trend)} {trend}</td>
              <td>{f"{previous:.1f}" if previous is not None else '—'}</td>
            </tr>
            """
        )

    regression_rows = ""
    for r in regressions:
        regression_rows += f"""
        <tr class="regression">
          <td>{html.escape(r['vendor'])}</td>
          <td>{r['previous']:.2f}</td>
          <td>{r['current']:.2f}</td>
          <td class="delta-negative">{r['delta']:+.2f}</td>
        </tr>
        """

    calibration_rows = ""
    for b in bins:
        calibration_rows += f"""
        <tr>
          <td>{html.escape(b['label'])}</td>
          <td>{b['count']}</td>
          <td>{b['correct']}</td>
          <td>{b['accuracy']:.0%}</td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>CCE Report — {html.escape(summary.get('run_id', ''))}</title>
<style>
  :root {{ color-scheme: light; }}
  body {{ font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 0; background: #f6f7fb; color: #1f2328; }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 24px; }}
  h1 {{ margin: 0 0 4px; font-size: 22px; }}
  .subtitle {{ color: #656d76; margin-bottom: 16px; }}
  .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }}
  .card {{ background: #ffffff; border: 1px solid #d0d7de; border-radius: 12px; padding: 16px; box-shadow: 0 1px 0 rgba(0,0,0,0.04); }}
  .metric {{ font-size: 28px; font-weight: 700; }}
  .metric-label {{ color: #656d76; font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; }}
  .section {{ background: #ffffff; border: 1px solid #d0d7de; border-radius: 12px; padding: 16px; margin-top: 16px; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #e6e8eb; font-size: 14px; }}
  th {{ color: #656d76; font-weight: 600; font-size: 12px; text-transform: uppercase; }}
  tr.regression {{ background: #fff5f5; }}
  .score-bar {{ width: 100%; height: 10px; background: #e6e8eb; border-radius: 999px; overflow: hidden; }}
  .score-fill {{ height: 100%; background: #2da44e; border-radius: 999px; }}
  .score-text {{ font-weight: 600; }}
  .badge {{ padding: 2px 8px; border-radius: 999px; font-size: 12px; font-weight: 600; }}
  .badge-success {{ background: #dafbe1; color: #1a7f37; }}
  .badge-warning {{ background: #fff8c5; color:#9a6700; }}
  .badge-danger {{ background: #ffebe9; color:#cf222e; }}
  .trend-up {{ color: #1a7f37; font-weight: 700; }}
  .trend-down {{ color: #cf222e; font-weight: 700; }}
  .trend-stable {{ color: #656d76; }}
  .delta-negative {{ color: #cf222e; font-weight: 700; }}
  .regressions-table th {{ color: #cf222e; }}
</style>
</head>
<body>
<div class="container">
  <h1>Continuous Capability Evaluation</h1>
  <div class="subtitle">Run {html.escape(summary.get('run_id', ''))} · {summary.get('timestamp', '')}</div>

  <div class="grid">
    <div class="card">
      <div class="metric">{summary.get('total_cases', 0)}</div>
      <div class="metric-label">Total Cases</div>
    </div>
    <div class="card">
      <div class="metric">{summary.get('passed_cases', 0)}/{summary.get('total_cases', 0)}</div>
      <div class="metric-label">Passed</div>
    </div>
    <div class="card">
      <div class="metric">{summary.get('avg_capability_score', 0):.1f}</div>
      <div class="metric-label">Avg Capability Score</div>
    </div>
    <div class="card">
      <div class="metric" style="color: {'#cf222e' if summary.get('regression_count', 0) else '#1a7f37'}">{summary.get('regression_count', 0)}</div>
      <div class="metric-label">Regressions</div>
    </div>
  </div>

  <div class="section">
    <h2 style="margin-top:0;font-size:16px;">Capability Breakdown</h2>
    <div style="overflow-x:auto;">
      <table>
        <thead>
          <tr>
            <th>Vendor</th>
            <th>Cases</th>
            <th>Passed</th>
            <th>Status</th>
            <th>Capability Score</th>
            <th>Benchmark Score</th>
            <th>Parser</th>
            <th>Reasoning</th>
            <th>Evidence</th>
            <th>Compliance</th>
            <th>Executive</th>
            <th>Trend</th>
            <th>Previous</th>
          </tr>
        </thead>
        <tbody>
          {''.join(rows) if rows else '<tr><td colspan="13" style="color:#656d76;text-align:center;">No data available</td></tr>'}
        </tbody>
      </table>
    </div>
  </div>

  <div class="section regressions-table">
    <h2 style="margin-top:0;font-size:16px;color:#cf222e;">Regressions</h2>
    <table>
      <thead>
        <tr><th>Vendor</th><th>Previous</th><th>Current</th><th>Delta</th></tr>
      </thead>
      <tbody>
        {regression_rows if regression_rows else '<tr><td colspan="4" style="color:#656d76;text-align:center;">No regressions detected</td></tr>'}
      </tbody>
    </table>
  </div>

  <div class="section">
    <h2 style="margin-top:0;font-size:16px;">Confidence Calibration</h2>
    <table>
      <thead>
        <tr><th>Confidence Bin</th><th>Count</th><th>Correct</th><th>Accuracy</th></tr>
      </thead>
      <tbody>
        {calibration_rows if calibration_rows else '<tr><td colspan="4" style="color:#656d76;text-align:center;">No calibration data</td></tr>'}
      </tbody>
    </table>
  </div>

  <div class="section">
    <h2 style="margin-top:0;font-size:16px;">Details</h2>
    <pre style="background:#f6f8fa;padding:12px;border-radius:8px;overflow:auto;font-size:13px;">{html.escape(json.dumps(summary, indent=2))}</pre>
  </div>
</div>
</body>
</html>"""

    output_path.write_text(html_content, encoding="utf-8")
    return output_path
