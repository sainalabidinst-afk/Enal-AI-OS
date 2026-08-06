"""
Capability Certification Framework — Dashboard Generator

Usage:
    python certification/scripts/dashboard.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_DIR = ROOT / "certification" / "certificates"
DASHBOARD_DIR = ROOT / "certification"
DASHBOARD_FILE = DASHBOARD_DIR / "dashboard.json"


def load_certificates() -> list[dict[str, Any]]:
    certificates = []
    for path in sorted(CERTIFICATE_DIR.glob("*-certificate.json")):
        try:
            certificates.append(json.loads(path.read_text(encoding="utf-8")))
        except Exception:
            continue
    return certificates


def build_dashboard(certificates: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(certificates)
    if total == 0:
        return {"generatedAt": "", "totalCapabilities": 0, "summary": {}, "capabilities": []}

    certified = sum(1 for c in certificates if c.get("certificationLevel") == "Certified")
    provisional = sum(1 for c in certificates if c.get("certificationLevel") == "Provisional")
    experimental = sum(1 for c in certificates if c.get("certificationLevel") == "Experimental")
    active = sum(1 for c in certificates if c.get("status") == "Active")
    avg_score = sum(c.get("overallScore", 0) for c in certificates) / total

    grade_distribution: dict[str, int] = {}
    for c in certificates:
        grade = c.get("grade", "F")
        grade_distribution[grade] = grade_distribution.get(grade, 0) + 1

    capabilities = []
    for c in certificates:
        capabilities.append({
            "capabilityId": c.get("capabilityId"),
            "capabilityName": c.get("capabilityName"),
            "grade": c.get("grade"),
            "certificationLevel": c.get("certificationLevel"),
            "overallScore": c.get("overallScore"),
            "status": c.get("status"),
            "certificationDate": c.get("certificationDate"),
            "expirationDate": c.get("expirationDate"),
        })

    return {
        "generatedAt": "",
        "totalCapabilities": total,
        "summary": {
            "certified": certified,
            "provisional": provisional,
            "experimental": experimental,
            "active": active,
            "averageScore": round(avg_score, 2),
            "gradeDistribution": grade_distribution,
        },
        "capabilities": sorted(capabilities, key=lambda x: x.get("capabilityId", "")),
    }


def save_dashboard(dashboard: dict[str, Any]) -> Path:
    import datetime
    dashboard["generatedAt"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    DASHBOARD_FILE.write_text(json.dumps(dashboard, indent=2), encoding="utf-8")
    return DASHBOARD_FILE


def main() -> int:
    certificates = load_certificates()
    if not certificates:
        print("No certificates found. Run generate_certificates.py first.")
        return 1

    dashboard = build_dashboard(certificates)
    path = save_dashboard(dashboard)
    summary = dashboard["summary"]
    print("Certification Dashboard")
    print("=" * 40)
    print(f"Total Capabilities : {dashboard['totalCapabilities']}")
    print(f"Certified          : {summary['certified']}")
    print(f"Provisional        : {summary['provisional']}")
    print(f"Experimental       : {summary['experimental']}")
    print(f"Active             : {summary['active']}")
    print(f"Average Score      : {summary['averageScore']}%")
    print(f"Grade Distribution : {summary['gradeDistribution']}")
    print(f"\nDashboard saved to: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
