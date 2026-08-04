"""
Master Dashboard Generator
===========================

Generates HTML dashboards for all 13 capability packs and an index page.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import html
from benchmarks.generate_dashboard import run_and_generate, normalize_report

DASHBOARD_DIR = Path(__file__).resolve().parent / "dashboards"
DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)


def _slugify(name: str) -> str:
    return name.lower().replace(" ", "_").replace("-", "_")


def _run_devops_benchmark():
    from benchmarks.devops_assistant_benchmark import DevOpsBenchmark
    return DevOpsBenchmark().run()


PACKS = [
    {"name": "Network Engineer", "module": "benchmarks.network_engineer_benchmark_v2", "function": "run_network_benchmark_v2", "target": 0.95},
    {"name": "Code Engineer", "module": "benchmarks.code_engineer_benchmark", "function": "run_code_engineer_benchmark", "target": 0.9},
    {"name": "Research Assistant", "module": "benchmarks.research_assistant_benchmark", "function": "run_benchmark", "target": 0.9},
    {"name": "DevOps Assistant", "module": None, "function": None, "target": 0.9, "runner": _run_devops_benchmark},
    {"name": "Trading Analyst", "module": "benchmarks.trading_analyst_benchmark", "function": "run_trading_benchmark", "target": 0.9},
    {"name": "Self Development", "module": "benchmarks.self_development_benchmark", "function": "run_self_development_benchmark", "target": 0.95},
    {"name": "Decision Intelligence", "module": "benchmarks.decision_intelligence_benchmark", "function": "run_benchmark", "target": 0.9},
    {"name": "System Architect", "module": "benchmarks.system_architect_benchmark", "function": "run_benchmark", "target": 0.9},
    {"name": "Security Engineer", "module": "benchmarks.security_engineer_benchmark", "function": "run_benchmark", "target": 0.9},
    {"name": "Data Engineer", "module": "benchmarks.data_engineer_benchmark", "function": "run_benchmark", "target": 0.85},
    {"name": "Database Engineer", "module": "benchmarks.database_engineer_benchmark", "function": "run_benchmark", "target": 0.85},
    {"name": "QA Engineer", "module": "benchmarks.qa_engineer_benchmark", "function": "run_benchmark", "target": 0.9},
    {"name": "Business Analyst", "module": "benchmarks.business_analyst_benchmark", "function": "run_benchmark", "target": 0.85},
]


def _run_pack(pack: dict) -> dict:
    name = pack["name"]
    output_path = DASHBOARD_DIR / f"{_slugify(name)}_dashboard.html"

    try:
        if "runner" in pack:
            raw = pack["runner"]()
            report = normalize_report(name, raw, target=pack["target"])
            output_path.parent.mkdir(parents=True, exist_ok=True)
            from benchmarks.generate_dashboard import generate_dashboard
            generate_dashboard(name, report, output_path)
        else:
            report = run_and_generate(
                name,
                pack["module"],
                pack["function"],
                output_path,
                target=pack["target"],
            )
    except Exception as exc:
        report = {
            "pack_name": name,
            "generated_at": datetime.utcnow().isoformat(),
            "overall_score": 0.0,
            "passed": False,
            "grade": "F",
            "dimensions": [],
            "scenarios": [],
            "raw": {"error": str(exc)},
        }
        output_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            from benchmarks.generate_dashboard import generate_dashboard
            generate_dashboard(name, report, output_path)
        except Exception:
            pass

    return {
        "name": name,
        "output": output_path.name,
        "overall_score": report.get("overall_score", 0.0),
        "grade": report.get("grade", "F"),
        "passed": report.get("passed", False),
    }


def generate_index(summaries: list[dict]) -> Path:
    rows = ""
    for s in summaries:
        status_class = "pass" if s["passed"] else "fail"
        status_text = "PASS" if s["passed"] else "FAIL"
        rows += f"""
    <tr>
      <td><a href="{html.escape(s['output'])}">{html.escape(s['name'])}</a></td>
      <td>{html.escape(s['grade'])}</td>
      <td>{s['overall_score']:.1f}%</td>
      <td class="{status_class}">{status_text}</td>
    </tr>
"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Capability Pack Benchmark Dashboards</title>
<style>
  :root {{ color-scheme: light; }}
  body {{ font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 0; background: #f6f7fb; color: #1f2328; }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 24px; }}
  h1 {{ margin: 0 0 4px; font-size: 22px; }}
  .subtitle {{ color: #656d76; margin-bottom: 16px; }}
  .section {{ background: #ffffff; border: 1px solid #d0d7de; border-radius: 12px; padding: 16px; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #e6e8eb; font-size: 14px; }}
  th {{ color: #656d76; font-weight: 600; font-size: 12px; text-transform: uppercase; }}
  .pass {{ color: #1a7f37; font-weight: 700; }}
  .fail {{ color: #cf222e; font-weight: 700; }}
  a {{ color: #0969da; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<div class="container">
  <h1>Capability Pack Benchmark Dashboards</h1>
  <div class="subtitle">Generated: {datetime.utcnow().isoformat()} · {len(summaries)} packs</div>
  <div class="section">
    <table>
      <thead>
        <tr><th>Pack</th><th>Grade</th><th>Overall Score</th><th>Status</th></tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>
  </div>
</div>
</body>
</html>"""

    output_path = DASHBOARD_DIR / "index.html"
    output_path.write_text(html_content, encoding="utf-8")
    return output_path


def main() -> int:
    summaries = []
    for pack in PACKS:
        print(f"Generating dashboard: {pack['name']} ...")
        try:
            summary = _run_pack(pack)
            summaries.append(summary)
            print(f"  -> {summary['grade']} {summary['overall_score']:.1f}% {'PASS' if summary['passed'] else 'FAIL'}")
        except Exception as exc:
            print(f"  -> FAILED: {exc}", file=sys.stderr)
            summaries.append({
                "name": pack["name"],
                "output": f"{_slugify(pack['name'])}_dashboard.html",
                "overall_score": 0.0,
                "grade": "F",
                "passed": False,
            })

    print("\nGenerating index ...")
    index_path = generate_index(summaries)
    print(f"Index generated: {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
