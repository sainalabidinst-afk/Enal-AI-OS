import json
from pathlib import Path

audits = [json.loads(p.read_text()) for p in sorted(Path("certification/audits").glob("*-audit.json"))]
for a in audits:
    print(f"{a['capability_id']}: score={a['overall_score']} grade={a['grade']}")
    for area in a["areas"]:
        if area["score"] < 8:
            print(f"  {area['name']}: {area['score']}/{area['max_score']}")
