import json

d = json.load(open("benchmarks/reports/network_benchmark_v2.json", encoding="utf-8"))
for r in d["results"]:
    print(f"{r['case_id']:<45} score={r['score']:.2f} matched={r['findings_matched']}/{r['expected_findings']} passed={r['passed']}")
