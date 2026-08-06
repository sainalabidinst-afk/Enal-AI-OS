"""
Capability Certification Framework — Re-Audit Runner

Usage:
    python certification/scripts/run_reaudit.py --all
    python certification/scripts/run_reaudit.py --capability trading_analyst
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
AUDIT_DIR = ROOT / "certification" / "audits"
REPORT_OUTPUT_DIR = ROOT / "certification" / "reports"
THRESHOLD_CERTIFIED = 80
THRESHOLD_PROVISIONAL = 70


def load_audit(capability_id: str) -> dict[str, Any] | None:
    path = AUDIT_DIR / f"{capability_id}-audit.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def grade_from_score(score: int, max_score: int = 150) -> str:
    pct = (score / max_score) * 100 if max_score else 0
    if pct >= 90:
        return "A"
    if pct >= 80:
        return "B"
    if pct >= 70:
        return "C"
    if pct >= 60:
        return "D"
    return "F"


def status_from_grade(grade: str) -> str:
    if grade in {"A", "B"}:
        return "Passed"
    if grade == "C":
        return "Conditional"
    return "Failed"


def certification_level(grade: str) -> str:
    if grade in {"A", "B"}:
        return "Certified"
    if grade == "C":
        return "Provisional"
    return "Experimental"


def render_reaudit_report(audit: dict[str, Any]) -> str:
    grade = grade_from_score(audit.get("overall_score", 0))
    status = status_from_grade(grade)
    level = certification_level(grade)
    pct = (audit.get("overall_score", 0) / 150) * 100

    lines = [
        f"Re-Audit Report: {audit.get('capability_name', audit.get('capability_id'))}",
        "=" * 60,
        f"Overall Score : {audit.get('overall_score')}/150 ({pct:.1f}%)",
        f"Grade         : {grade}",
        f"Status        : {status}",
        f"Level         : {level}",
        f"Completed At  : {audit.get('completed_at')}",
        "",
        "Corrective Actions:",
    ]
    for idx, action in enumerate(audit.get("summary", {}).get("correctiveActions", []), 1):
        lines.append(f"  {idx}. {action}")

    if pct >= THRESHOLD_CERTIFIED:
        lines.append("")
        lines.append("[OK] Meets Certified threshold (>=80%)")
    elif pct >= THRESHOLD_PROVISIONAL:
        lines.append("")
        lines.append("[WARN] Meets Provisional threshold (>=70%)")
    else:
        lines.append("")
        lines.append("[FAIL] Below Provisional threshold (<70%)")

    return "\n".join(lines)


def save_reaudit_report(audit: dict[str, Any]) -> Path:
    REPORT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_OUTPUT_DIR / f"{audit['capability_id']}-reaudit-report.txt"
    report_path.write_text(render_reaudit_report(audit), encoding="utf-8")
    return report_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Re-Audit and validate certification thresholds")
    parser.add_argument("--capability", help="Specific capability ID to re-audit")
    parser.add_argument("--all", action="store_true", help="Re-audit all capabilities")
    args = parser.parse_args()

    audit_files = sorted(AUDIT_DIR.glob("*-audit.json"))
    if not audit_files:
        print("No audit reports found. Run run_audit.py first.")
        return 1

    targets = []
    if args.all:
        targets = [path.stem.replace("-audit", "") for path in audit_files]
    elif args.capability:
        targets = [args.capability]

    if not targets:
        parser.print_help()
        return 1

    certified = 0
    provisional = 0
    experimental = 0
    total = 0

    for capability_id in targets:
        audit = load_audit(capability_id)
        if not audit:
            print(f"Audit report not found for: {capability_id}")
            continue

        total += 1
        grade = grade_from_score(audit.get("overall_score", 0))
        level = certification_level(grade)
        if level == "Certified":
            certified += 1
        elif level == "Provisional":
            provisional += 1
        else:
            experimental += 1

        print(render_reaudit_report(audit))
        print()
        save_reaudit_report(audit)

    print("=" * 60)
    print("Summary:")
    print(f"  Total       : {total}")
    print(f"  Certified   : {certified}")
    print(f"  Provisional : {provisional}")
    print(f"  Experimental: {experimental}")
    print(f"  Threshold   : Certified >= {THRESHOLD_CERTIFIED}%, Provisional >= {THRESHOLD_PROVISIONAL}%")

    if certified == total:
        print("\n[OK] All capabilities meet Certified threshold. Ready for Benchmark Audit.")
        return 0

    if provisional + certified == total:
        print("\n[WARN] All capabilities are Provisional or better. Continue corrective actions to reach Certified.")
        return 0

    print("\n[FAIL] Some capabilities are below Provisional threshold. Corrective actions required.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
