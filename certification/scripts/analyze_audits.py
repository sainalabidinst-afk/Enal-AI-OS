"""
Analyze audit results and identify weakest areas across all capabilities.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT_DIR = ROOT / "certification" / "audits"


def analyze() -> None:
    audits = []
    for path in sorted(AUDIT_DIR.glob("*-audit.json")):
        audit = json.loads(path.read_text(encoding="utf-8"))
        audits.append(audit)

    print(f"Total capabilities: {len(audits)}")
    print()

    # Overall scores
    scores = [a["overall_score"] for a in audits]
    avg = sum(scores) / len(scores) if scores else 0
    print(f"Average score: {avg:.1f}/150 ({avg/150*100:.1f}%)")
    print(f"Min score: {min(scores)}/150")
    print(f"Max score: {max(scores)}/150")
    print()

    # Area analysis
    area_scores = {}
    for audit in audits:
        for area in audit.get("areas", []):
            name = area["name"]
            if name not in area_scores:
                area_scores[name] = []
            area_scores[name].append(area["score"])

    print("Area Analysis (sorted by average score):")
    print("-" * 60)
    area_avgs = []
    for name, scores in area_scores.items():
        avg_score = sum(scores) / len(scores)
        area_avgs.append((name, avg_score, scores))
    area_avgs.sort(key=lambda x: x[1])

    for name, avg_score, scores in area_avgs:
        min_score = min(scores)
        max_score = max(scores)
        below_7 = sum(1 for s in scores if s < 7)
        print(f"  {name:<30} avg={avg_score:5.1f}/10  min={min_score}  max={max_score}  below_7={below_7}/{len(scores)}")
    print()

    # Findings analysis
    all_findings = []
    for audit in audits:
        for area in audit.get("areas", []):
            for finding in area.get("findings", []):
                all_findings.append({
                    "capability": audit["capability_id"],
                    "area": area["name"],
                    "severity": finding["severity"],
                    "description": finding["description"],
                    "location": finding.get("location", ""),
                })

    print(f"Total findings: {len(all_findings)}")
    severity_counts = Counter(f["severity"] for f in all_findings)
    print(f"Severity distribution: {dict(severity_counts)}")
    print()

    # Top issues
    print("Top issues (by frequency):")
    issue_counts = Counter(f["description"] for f in all_findings)
    for desc, count in issue_counts.most_common(20):
        print(f"  [{count}x] {desc}")
    print()

    # Capabilities needing most improvement
    print("Capabilities needing most improvement:")
    for audit in sorted(audits, key=lambda a: a["overall_score"])[:10]:
        pct = audit["overall_score"] / 150 * 100
        print(f"  {audit['capability_id']:<20} {audit['overall_score']:>3}/150 ({pct:5.1f}%)  grade={audit['grade']}")
    print()

    # Corrective actions summary
    print("Corrective actions needed:")
    corrective_counts = Counter()
    for audit in audits:
        for action in audit.get("summary", {}).get("correctiveActions", []):
            corrective_counts[action] += 1
    for action, count in corrective_counts.most_common(20):
        print(f"  [{count}x] {action}")


if __name__ == "__main__":
    analyze()
