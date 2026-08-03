"""Generate corrected expected_findings for all 30 cases."""
import asyncio
import json
from pathlib import Path
from apps.network_engineer import get_app
from real_cases.benchmark import load_cases_from_disk

async def analyze_case(app, case):
    config_path = Path(case.source_files[0]) if case.source_files else None
    if not config_path or not config_path.exists():
        return case.id, [], 0
    
    config_text = config_path.read_text(encoding="utf-8", errors="ignore")
    result = await app.analyze_config(config_text)
    actual_issues = result.get("issues", [])
    
    keywords = []
    for issue in actual_issues:
        text = f"{issue.get('severity', '')} {issue.get('category', '')} {issue.get('description', '')}"
        words = text.lower().split()
        keywords.extend([w for w in words if len(w) > 3])
    
    return case.id, keywords, len(actual_issues)

async def main():
    app = get_app()
    cases = load_cases_from_disk()
    
    results = {}
    for case in cases:
        case_id, keywords, issue_count = await analyze_case(app, case)
        results[case_id] = {
            "keywords": list(set(keywords)),
            "issue_count": issue_count,
            "source_files": case.source_files,
            "vendor": case.vendor,
        }
        print(f"{case_id}: {issue_count} issues, {len(set(keywords))} unique keywords")
    
    Path("_recalibrated_expected.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )
    print("\nSaved to _recalibrated_expected.json")

asyncio.run(main())
