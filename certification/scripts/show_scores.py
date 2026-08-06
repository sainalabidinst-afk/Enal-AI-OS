import json
from pathlib import Path

audits = [json.loads(p.read_text()) for p in sorted(Path("certification/audits").glob("*-audit.json"))]
for a in audits:
    score = a["overall_score"]
    pct = score / 150 * 100
    grade = "Certified" if pct >= 80 else "Provisional"
    test_cov = next((x["score"] for x in a["areas"] if x["name"] == "Test Coverage"), 0)
    obs = next((x["score"] for x in a["areas"] if x["name"] == "Observability"), 0)
    contract = next((x["score"] for x in a["areas"] if x["name"] == "Contract Compliance"), 0)
    golden = next((x["score"] for x in a["areas"] if x["name"] == "Golden Tests"), 0)
    real = next((x["score"] for x in a["areas"] if x["name"] == "Real Cases"), 0)
    print(f"{a['capability_id']:<20} {score:>3}/150 ({pct:5.1f}%) {grade:<12} test={test_cov} obs={obs} contract={contract} golden={golden} real={real}")
