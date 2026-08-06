"""
Generate comprehensive certification summary combining Audit, Benchmark, and Production Readiness scores.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CERTIFICATION_DIR = ROOT / "certification"
AUDIT_DIR = CERTIFICATION_DIR / "audits"
BENCHMARK_DIR = CERTIFICATION_DIR / "benchmarks"
CERTIFICATE_DIR = CERTIFICATION_DIR / "certificates"


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def build_summary() -> dict[str, Any]:
    summary = {
        "generatedAt": "",
        "totalCapabilities": 0,
        "dimensions": {
            "audit": {"averageScore": 0, "certified": 0, "provisional": 0, "experimental": 0},
            "benchmark": {"averageScore": 0, "gradeA": 0, "gradeB": 0, "gradeC": 0, "gradeD": 0, "gradeF": 0},
            "productionReadiness": {"averageScore": 0, "passed": 0, "failed": 0},
        },
        "capabilities": [],
    }

    capabilities = []
    for audit_path in sorted(AUDIT_DIR.glob("*-audit.json")):
        capability_id = audit_path.stem.replace("-audit", "")
        audit = load_json(audit_path)
        benchmark = load_json(BENCHMARK_DIR / f"{capability_id}-benchmark.json")
        production_readiness = load_json(BENCHMARK_DIR / f"{capability_id}-production-readiness.json")

        if not audit:
            continue

        capabilities.append({
            "capabilityId": capability_id,
            "capabilityName": audit.get("capability_name", capability_id),
            "audit": {
                "score": audit.get("overall_score", 0),
                "grade": audit.get("grade", "F"),
                "status": audit.get("status", "Failed"),
                "percentage": round(audit.get("overall_score", 0) / 150 * 100, 2),
            },
            "benchmark": {
                "overallScore": benchmark.get("overallScore", 0) if benchmark else 0,
                "grade": benchmark.get("grade", "F") if benchmark else "F",
                "passed": benchmark.get("passed", False) if benchmark else False,
                "functional": benchmark.get("functional", {}).get("score", 0) if benchmark else 0,
                "performance": benchmark.get("performance", {}).get("score", 0) if benchmark else 0,
                "scalability": benchmark.get("scalability", {}).get("score", 0) if benchmark else 0,
                "reliability": benchmark.get("reliability", {}).get("score", 0) if benchmark else 0,
            } if benchmark else None,
            "productionReadiness": {
                "overallScore": production_readiness.get("overallScore", 0) if production_readiness else 0,
                "passed": production_readiness.get("passed", False) if production_readiness else False,
                "capabilityReadiness": production_readiness.get("capabilityReadiness", {}).get("score", 0) if production_readiness else 0,
                "platformReadiness": production_readiness.get("platformReadiness", {}).get("overallScore", 0) if production_readiness else 0,
            } if production_readiness else None,
        })

    summary["totalCapabilities"] = len(capabilities)

    if capabilities:
        avg_audit = sum(c["audit"]["score"] for c in capabilities) / len(capabilities)
        summary["dimensions"]["audit"]["averageScore"] = round(avg_audit / 150 * 100, 2)
        summary["dimensions"]["audit"]["certified"] = sum(1 for c in capabilities if c["audit"]["grade"] in {"A", "B"})
        summary["dimensions"]["audit"]["provisional"] = sum(1 for c in capabilities if c["audit"]["grade"] == "C")
        summary["dimensions"]["audit"]["experimental"] = sum(1 for c in capabilities if c["audit"]["grade"] in {"D", "F"})

        benchmarks = [c["benchmark"] for c in capabilities if c["benchmark"]]
        if benchmarks:
            avg_benchmark = sum(b["overallScore"] for b in benchmarks) / len(benchmarks)
            summary["dimensions"]["benchmark"]["averageScore"] = round(avg_benchmark, 2)
            summary["dimensions"]["benchmark"]["gradeA"] = sum(1 for b in benchmarks if b["grade"] == "A")
            summary["dimensions"]["benchmark"]["gradeB"] = sum(1 for b in benchmarks if b["grade"] == "B")
            summary["dimensions"]["benchmark"]["gradeC"] = sum(1 for b in benchmarks if b["grade"] == "C")
            summary["dimensions"]["benchmark"]["gradeD"] = sum(1 for b in benchmarks if b["grade"] == "D")
            summary["dimensions"]["benchmark"]["gradeF"] = sum(1 for b in benchmarks if b["grade"] == "F")

        prs = [c["productionReadiness"] for c in capabilities if c["productionReadiness"]]
        if prs:
            avg_pr = sum(p["overallScore"] for p in prs) / len(prs)
            summary["dimensions"]["productionReadiness"]["averageScore"] = round(avg_pr, 2)
            summary["dimensions"]["productionReadiness"]["passed"] = sum(1 for p in prs if p["passed"])
            summary["dimensions"]["productionReadiness"]["failed"] = sum(1 for p in prs if not p["passed"])

    summary["capabilities"] = sorted(capabilities, key=lambda x: x["capabilityId"])
    return summary


def save_summary(summary: dict[str, Any]) -> Path:
    import datetime
    summary["generatedAt"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    path = CERTIFICATION_DIR / "certification-summary.json"
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return path


def print_summary(summary: dict[str, Any]) -> None:
    print("=" * 70)
    print("ENAL AI OS — Certification Summary")
    print("=" * 70)
    print(f"Total Capabilities : {summary['totalCapabilities']}")
    print()

    audit = summary["dimensions"]["audit"]
    print("Audit Dimension:")
    print(f"  Average Score : {audit['averageScore']}%")
    print(f"  Certified     : {audit['certified']}")
    print(f"  Provisional   : {audit['provisional']}")
    print(f"  Experimental  : {audit['experimental']}")
    print()

    benchmark = summary["dimensions"]["benchmark"]
    print("Benchmark Dimension:")
    print(f"  Average Score : {benchmark['averageScore']}%")
    print(f"  Grade A       : {benchmark['gradeA']}")
    print(f"  Grade B       : {benchmark['gradeB']}")
    print(f"  Grade C       : {benchmark['gradeC']}")
    print(f"  Grade D       : {benchmark['gradeD']}")
    print(f"  Grade F       : {benchmark['gradeF']}")
    print()

    pr = summary["dimensions"]["productionReadiness"]
    print("Production Readiness Dimension:")
    print(f"  Average Score : {pr['averageScore']}%")
    print(f"  Passed        : {pr['passed']}")
    print(f"  Failed        : {pr['failed']}")
    print()

    print("Capability Details:")
    print("-" * 70)
    for c in summary["capabilities"]:
        audit_pct = c["audit"]["percentage"]
        benchmark_score = c["benchmark"]["overallScore"] if c["benchmark"] else 0
        pr_score = c["productionReadiness"]["overallScore"] if c["productionReadiness"] else 0
        print(f"  {c['capabilityId']:<20} audit={audit_pct:5.1f}% benchmark={benchmark_score:5.1f}% pr={pr_score:5.1f}%")
    print("=" * 70)


def main() -> int:
    summary = build_summary()
    path = save_summary(summary)
    print_summary(summary)
    print(f"\nSaved to: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
