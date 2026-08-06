import json
from pathlib import Path

audit = json.loads(Path("certification/audits/code_engineer-audit.json").read_text())
for area in audit["areas"]:
    if area["score"] < 10:
        print(f"{area['name']}: {area['score']}/10")
        for f in area["findings"]:
            print(f"  - {f['severity']}: {f['description']}")
