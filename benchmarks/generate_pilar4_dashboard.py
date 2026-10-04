"""
Governance Metrics Dashboard Generator
=======================================

Reads the Pilar 4 Phase 3 benchmark report and generates:
- Acceptance rate chart
- Remediation success rate chart
- Governance gate latency chart
- Federated sync privacy violation rate chart

Outputs HTML dashboard to benchmarks/reports/pilar4_governance_dashboard.html
"""

from __future__ import annotations

import json
from pathlib import Path

REPORT_PATH = Path("benchmarks/reports/pilar4_phase3_benchmark.json")
OUTPUT_PATH = Path("benchmarks/reports/pilar4_phase3_dashboard.html")


def load_metrics() -> dict | None:
    if not REPORT_PATH.exists():
        return None
    return json.loads(REPORT_PATH.read_text(encoding="utf-8"))


def build_dashboard(metrics: dict | None) -> str:
    if metrics is None:
        return "<html><body><p>No benchmark data available. Run benchmarks/pilar4_phase3_benchmark.py first.</p></body></html>"

    snap = metrics.get("benchmarks", {}).get("governance_metrics", {})
    acceptance_rate = snap.get("pack_synthesis_acceptance_rate", 0) * 100
    remediation_rate = snap.get("remediation_success_rate", 0) * 100
    privacy_rate = snap.get("federated_privacy_violation_rate", 0) * 100
    avg_latency = snap.get("avg_gate_latency_ms", 0)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pilar 4 Governance Metrics Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }}
        .card {{ background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .metric {{ font-size: 24px; font-weight: bold; text-align: center; margin: 10px 0; }}
        .label {{ text-align: center; color: #666; margin-bottom: 15px; }}
        .pass {{ color: #28a745; }}
        .fail {{ color: #dc3545; }}
        .warning {{ color: #ffc107; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Pilar 4 Governance Metrics Dashboard</h1>
        <p>Generated: {metrics.get('generated_at', 'N/A')}</p>
    </div>
    <div class="grid">
        <div class="card">
            <div class="label">Pack Synthesis Acceptance Rate</div>
            <div class="metric {'pass' if acceptance_rate >= 90 else 'fail'}">{acceptance_rate:.1f}%</div>
            <canvas id="acceptanceChart"></canvas>
        </div>
        <div class="card">
            <div class="label">Remediation Success Rate</div>
            <div class="metric {'pass' if remediation_rate >= 95 else 'fail'}">{remediation_rate:.1f}%</div>
            <canvas id="remediationChart"></canvas>
        </div>
        <div class="card">
            <div class="label">Federated Sync Privacy Violation Rate</div>
            <div class="metric {'pass' if privacy_rate == 0 else 'fail'}">{privacy_rate:.1f}%</div>
            <canvas id="privacyChart"></canvas>
        </div>
        <div class="card">
            <div class="label">Avg Governance Gate Latency</div>
            <div class="metric {{'pass' if avg_latency < 500 else 'warning'}}">{avg_latency:.1f} ms</div>
            <canvas id="latencyChart"></canvas>
        </div>
    </div>
    <script>
        const chartOptions = {{
            responsive: true,
            maintainAspectRatio: true,
            plugins: {{
                legend: {{ display: false }}
            }},
            scales: {{
                y: {{ beginAtZero: true, max: 100 }}
            }}
        }};
        new Chart(document.getElementById('acceptanceChart'), {{
            type: 'bar',
            data: {{
                labels: ['Acceptance Rate'],
                datasets: [{{
                    label: 'Actual',
                    data: [{acceptance_rate}],
                    backgroundColor: '{'rgba(40, 167, 69, 0.8)' if acceptance_rate >= 90 else 'rgba(220, 53, 69, 0.8)'}',
                    borderColor: '{'rgba(40, 167, 69, 1)' if acceptance_rate >= 90 else 'rgba(220, 53, 69, 1)'}',
                    borderWidth: 1
                }},
                {{
                    label: 'Target (90%)',
                    data: [90],
                    backgroundColor: 'rgba(0, 123, 255, 0.2)',
                    borderColor: 'rgba(0, 123, 255, 1)',
                    borderWidth: 1
                }}]
            }},
            options: chartOptions
        }});
        new Chart(document.getElementById('remediationChart'), {{
            type: 'bar',
            data: {{
                labels: ['Remediation Success'],
                datasets: [{{
                    label: 'Actual',
                    data: [{remediation_rate}],
                    backgroundColor: '{'rgba(40, 167, 69, 0.8)' if remediation_rate >= 95 else 'rgba(220, 53, 69, 0.8)'}',
                    borderColor: '{'rgba(40, 167, 69, 1)' if remediation_rate >= 95 else 'rgba(220, 53, 69, 1)'}',
                    borderWidth: 1
                }},
                {{
                    label: 'Target (95%)',
                    data: [95],
                    backgroundColor: 'rgba(0, 123, 255, 0.2)',
                    borderColor: 'rgba(0, 123, 255, 1)',
                    borderWidth: 1
                }}]
            }},
            options: chartOptions
        }});
        new Chart(document.getElementById('privacyChart'), {{
            type: 'bar',
            data: {{
                labels: ['Privacy Violation Rate'],
                datasets: [{{
                    label: 'Actual',
                    data: [{privacy_rate}],
                    backgroundColor: '{'rgba(40, 167, 69, 0.8)' if privacy_rate == 0 else 'rgba(220, 53, 69, 0.8)'}',
                    borderColor: '{'rgba(40, 167, 69, 1)' if privacy_rate == 0 else 'rgba(220, 53, 69, 1)'}',
                    borderWidth: 1
                }},
                {{
                    label: 'Target (0%)',
                    data: [0],
                    backgroundColor: 'rgba(0, 123, 255, 0.2)',
                    borderColor: 'rgba(0, 123, 255, 1)',
                    borderWidth: 1
                }}]
            }},
            options: chartOptions
        }});
        new Chart(document.getElementById('latencyChart'), {{
            type: 'bar',
            data: {{
                labels: ['Avg Latency (ms)'],
                datasets: [{{
                    label: 'Actual',
                    data: [{avg_latency}],
                    backgroundColor: '{'rgba(40, 167, 69, 0.8)' if avg_latency < 500 else 'rgba(255, 193, 7, 0.8)'}',
                    borderColor: '{'rgba(40, 167, 69, 1)' if avg_latency < 500 else 'rgba(255, 193, 7, 1)'}',
                    borderWidth: 1
                }},
                {{
                    label: 'Target (500ms)',
                    data: [500],
                    backgroundColor: 'rgba(0, 123, 255, 0.2)',
                    borderColor: 'rgba(0, 123, 255, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                ...chartOptions,
                scales: {{
                    y: {{ beginAtZero: true, max: 500 }}
                }}
            }}
        }});
    </script>
</body>
</html>"""


def main() -> None:
    metrics = load_metrics()
    dashboard = build_dashboard(metrics)
    OUTPUT_PATH.write_text(dashboard, encoding="utf-8")
    print(f"Dashboard written: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
