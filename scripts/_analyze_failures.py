import asyncio
import json
from pathlib import Path
from real_cases.benchmark import load_cases_from_disk
from apps.security_engineer.engine import SecurityEngineerEngine
from apps.security_engineer.schemas import SecurityAssessmentRequest, AssessmentType

alias_map = {
    "sql_injection": ["sql", "injection", "select", "concatenation"],
    "secret": ["api_key", "token", "password", "private_key", "secret", "aws_access_key", "bearer"],
    "deserialization": ["pickle", "yaml", "marshal", "deserialization", "loads"],
    "command_injection": ["os.system", "subprocess", "popen", "command injection", "shell=true"],
    "ssrf": ["ssrf", "server-side request", "unsanitized url", "fetch"],
    "xss": ["xss", "innerhtml", "document.write", "cross-site"],
    "weak_crypto": ["md5", "sha1", "random.randint", "math.random", "insecure random"],
    "debug_enabled": ["debug=true", "debug = true"],
    "open_exposure": ["0.0.0.0/0", "public", "allow all"],
    "privilege_escalation": ["root", "sudo", "admin", "privilege", "setuid"],
    "insecure_ssl": ["cert_none", "verify=false", "disable_warnings", "ssl"],
    "vulnerability": ["cve", "outdated", "vulnerability", "old_key"],
    "access_control": ["authorization", "role", "ownership", "idor", "permission"],
    "hardening": ["hardening", "cis", "benchmark", "baseline"],
    "compliance": ["compliance", "gdpr", "hipaa", "pci", "soc2", "iso27001"],
    "security": ["security", "vulnerability", "finding", "risk"],
}

detectable = {
    "sql_injection", "secret", "deserialization", "command_injection",
    "ssrf", "xss", "weak_crypto", "debug_enabled", "open_exposure",
    "privilege_escalation", "insecure_ssl", "vulnerability",
}

def is_detectable(finding_type):
    return finding_type.lower() in detectable

def score_case(actual_issues, actual_secrets, expected_findings):
    if not expected_findings:
        return 1.0, 0, 0
    
    detectable_list = [ef for ef in expected_findings if is_detectable(ef)]
    undetectable_list = [ef for ef in expected_findings if not is_detectable(ef)]
    
    if not detectable_list:
        return 1.0, 0, 0
    
    actual_text = " ".join(
        f"{i.get('category', '')} {i.get('title', '')} {i.get('description', '')} {i.get('remediation', '')}"
        for i in actual_issues
    ).lower()
    for s in actual_secrets:
        actual_text += f" {s.get('type', '')} {s.get('location', '')} {s.get('evidence', '')}".lower()
    
    matched = 0
    for ef in detectable_list:
        ef_lower = ef.lower()
        if ef_lower in actual_text:
            matched += 1
            continue
        aliases = alias_map.get(ef_lower, [ef_lower])
        if any(alias in actual_text for alias in aliases):
            matched += 1
            continue
        tokens = ef_lower.split()
        if len(tokens) > 1 and all(t in actual_text for t in tokens):
            matched += 1
            continue
    
    if matched > 0:
        score = matched / len(detectable_list)
    elif actual_issues or actual_secrets:
        score = 0.5
    else:
        score = 0.0
    return score, matched, len(detectable_list)

async def main():
    cases = load_cases_from_disk("real_cases/security")
    cases = [c for c in cases if c.category in {"security"} or c.vendor in {"security", "generic"}]
    engine = SecurityEngineerEngine()
    failures = []
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
        score, matched, total = score_case(actual_issues, actual_secrets, case.expected_findings)
        if score < 0.8:
            failures.append({
                "case_id": case.id,
                "expected_findings": case.expected_findings,
                "score": score,
                "matched": matched,
                "total": total,
                "findings_count": len(actual_issues),
                "secrets_count": len(actual_secrets),
                "actual_categories": list(set(i.get("category", "") for i in actual_issues)),
                "actual_titles": list(set(i.get("title", "") for i in actual_issues)),
                "actual_secret_types": list(set(s.get("type", "") for s in actual_secrets)),
            })
    Path("tmp_failures.json").write_text(json.dumps(failures, indent=2), encoding="utf-8")
    print(f"Total failures: {len(failures)}")
    for f in failures:
        print(f"  {f['case_id']}: score={f['score']}, matched={f['matched']}/{f['total']}, findings={f['findings_count']}, secrets={f['secrets_count']}")
        print(f"    expected: {f['expected_findings']}")
        print(f"    categories: {f['actual_categories']}")
        print(f"    titles: {f['actual_titles']}")
        print(f"    secret_types: {f['actual_secret_types']}")

if __name__ == "__main__":
    asyncio.run(main())
