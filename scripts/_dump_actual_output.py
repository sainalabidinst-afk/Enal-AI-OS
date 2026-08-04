import asyncio
import json
from pathlib import Path
from real_cases.benchmark import load_cases_from_disk
from apps.security_engineer.engine import SecurityEngineerEngine
from apps.security_engineer.schemas import SecurityAssessmentRequest, AssessmentType

async def main():
    cases = load_cases_from_disk("real_cases/security")
    cases = [c for c in cases if c.category in {"security"} or c.vendor in {"security", "generic"}]
    engine = SecurityEngineerEngine()
    results = []
    for case in cases:
        config_path = Path(case.source_files[0])
        if not config_path.exists():
            continue
        text = config_path.read_text(encoding="utf-8", errors="ignore")
        request = SecurityAssessmentRequest(
            target_type=AssessmentType.full_review,
            target={"source_code": text, "language": "python", "file_path": str(config_path)},
            standards=["owasp_top10", "cis"],
            check_secrets=True,
            check_dependencies=False,
            include_remediation=True,
            include_compliance_mapping=True,
        )
        report = engine.review(request)
        actual_issues = [i.to_dict() if hasattr(i, "to_dict") else i.__dict__ for i in report.findings]
        actual_secrets = [s.to_dict() if hasattr(s, "to_dict") else s.__dict__ for s in report.secrets]
        actual_text = " ".join(
            f"{i.get('category', '')} {i.get('title', '')} {i.get('description', '')} {i.get('remediation', '')}"
            for i in actual_issues
        ).lower()
        for s in actual_secrets:
            actual_text += f" {s.get('type', '')} {s.get('location', '')} {s.get('evidence', '')}".lower()
        results.append({
            "case_id": case.id,
            "expected_findings": case.expected_findings,
            "findings_count": len(actual_issues),
            "secrets_count": len(actual_secrets),
            "actual_text": actual_text[:800],
            "actual_categories": list(set(i.get("category", "") for i in actual_issues)),
            "actual_titles": list(set(i.get("title", "") for i in actual_issues))[:10],
            "actual_secret_types": list(set(s.get("type", "") for s in actual_secrets)),
            "actual_secret_locations": list(set(s.get("location", "") for s in actual_secrets)),
        })
    Path("tmp_actual_output.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote {len(results)} results to tmp_actual_output.json")

if __name__ == "__main__":
    asyncio.run(main())
