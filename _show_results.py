import json
from pathlib import Path

report = json.loads(Path('benchmarks/reports/network_benchmark_v2.json').read_text())
for r in report['results']:
    pct = f"{r['score']:.0%}"
    print(f"{r['case_id']}: {pct} ({r['findings_matched']}/{r['expected_findings']})")
