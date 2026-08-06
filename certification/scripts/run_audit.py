"""
Capability Certification Framework — Phase 1.1: Capability Audit Runner

Usage:
    python certification/scripts/run_audit.py --capability trading_analyst
    python certification/scripts/run_audit.py --all
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
APPS_DIR = ROOT / "apps"
DOCS_DIR = ROOT / "docs" / "capabilities"
FRONTEND_CAPABILITY_DIR = ROOT / "frontend" / "components" / "workspace" / "apps"
CERTIFICATION_DIR = ROOT / "certification"
AUDIT_OUTPUT_DIR = CERTIFICATION_DIR / "audits"
REPORT_OUTPUT_DIR = CERTIFICATION_DIR / "reports"
CERTIFICATE_OUTPUT_DIR = CERTIFICATION_DIR / "certificates"
GOLDEN_TESTS_DIR = CERTIFICATION_DIR / "golden-tests"
REAL_CASES_DIR = CERTIFICATION_DIR / "real-cases"


@dataclass
class Finding:
    severity: str
    description: str
    location: str


@dataclass
class AreaResult:
    name: str
    score: int = 0
    max_score: int = 10
    status: str = "Skipped"
    findings: list[Finding] = field(default_factory=list)


@dataclass
class AuditReport:
    schema_version: str = "1.0.0"
    capability_id: str = ""
    capability_name: str = ""
    audit_version: str = "1.0.0"
    overall_score: int = 0
    grade: str = "F"
    status: str = "Failed"
    areas: list[AreaResult] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)
    auditor: str = "Capability Audit Runner"
    completed_at: str = ""


def discover_capabilities() -> list[str]:
    capabilities = []
    if APPS_DIR.exists():
        for path in APPS_DIR.iterdir():
            if path.is_dir() and path.name != "__pycache__":
                capabilities.append(path.name)
    return sorted(capabilities)


def capability_slug(name: str) -> str:
    return name.replace("_", "-")


def load_doc(name: str) -> str | None:
    doc_path = DOCS_DIR / f"{capability_slug(name)}.md"
    if doc_path.exists():
        return doc_path.read_text(encoding="utf-8")
    return None


def run_pytest_for(name: str) -> tuple[bool, str]:
    test_file = ROOT / "tests" / f"test_{name}.py"
    if not test_file.exists():
        return False, f"Missing test file: {test_file}"
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_file), "-q", "--tb=short"],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
            env={**os.environ, "PYTHONPATH": str(ROOT)},
            timeout=180,
        )
        passed = result.returncode == 0
        output = result.stdout[-4000:] if result.stdout else ""
        error = result.stderr[-2000:] if result.stderr else ""
        return passed, (output + "\n" + error).strip()
    except Exception as exc:
        return False, str(exc)


def check_contract_compliance(name: str) -> AreaResult:
    findings: list[Finding] = []
    score = 10
    app_dir = APPS_DIR / name
    py_files = list(app_dir.glob("*.py"))

    engine_files = [
        p
        for p in py_files
        if p.name
        in {
            "engine.py",
            "orchestrator.py",
            "execution_engine.py",
            "runtime.py",
            "kernel.py",
            "executive.py",
        }
        or "engine" in p.name.lower()
    ]
    schema_files = [
        p
        for p in py_files
        if p.name
        in {
            "schemas.py",
            "models.py",
            "contracts.py",
            "capability_contract.py",
        }
        or "schema" in p.name.lower()
        or "model" in p.name.lower()
    ]
    worker_files = [
        p
        for p in py_files
        if p.name
        in {
            "worker.py",
            "__init__.py",
        }
        or "worker" in p.name.lower()
    ]

    if not engine_files:
        try:
            source_blobs = [p.read_text(encoding="utf-8", errors="ignore") for p in py_files]
            has_engine_class = any("class .*Engine" in text for text in source_blobs)
            if not has_engine_class:
                findings.append(Finding("Critical", "No engine-like module detected", str(app_dir)))
                score -= 5
        except Exception:
            findings.append(Finding("Critical", "No engine-like module detected", str(app_dir)))
            score -= 5
    if not schema_files:
        findings.append(Finding("Major", "No schema/contract module detected", str(app_dir)))
        score -= 3
    if not worker_files:
        findings.append(Finding("Minor", "No worker/entry module detected", str(app_dir)))
        score -= 1

    status = "Passed" if score >= 7 else "Failed" if score <= 3 else "Conditional"
    return AreaResult(name="Contract Compliance", score=max(score, 0), status=status, findings=findings)


def check_test_coverage(name: str) -> AreaResult:
    findings: list[Finding] = []
    score = 10
    passed, output = run_pytest_for(name)
    if not passed:
        findings.append(Finding("Major", "Test suite failed or missing", output[:500]))
        score -= 4
    if "passed" not in output.lower():
        findings.append(Finding("Minor", "Could not determine pass count", ""))
        score -= 2
    status = "Passed" if score >= 7 else "Failed" if score <= 3 else "Conditional"
    return AreaResult(name="Test Coverage", score=max(score, 0), status=status, findings=findings)


def check_documentation(name: str) -> AreaResult:
    findings: list[Finding] = []
    score = 10
    doc = load_doc(name)
    if not doc:
        findings.append(Finding("Critical", "Missing capability documentation", f"docs/capabilities/{capability_slug(name)}.md"))
        score -= 6
    else:
        if len(doc.strip()) < 200:
            findings.append(Finding("Minor", "Documentation appears too short", ""))
            score -= 2
    status = "Passed" if score >= 7 else "Failed" if score <= 3 else "Conditional"
    return AreaResult(name="Documentation", score=max(score, 0), status=status, findings=findings)


def check_observability(name: str) -> AreaResult:
    findings: list[Finding] = []
    score = 10
    app_dir = APPS_DIR / name
    has_logs = any(app_dir.glob("**/*log*.py"))
    has_metrics = any(app_dir.glob("**/*metric*.py"))
    has_observability = any(app_dir.glob("**/observability*.py"))
    if not has_logs and not has_metrics and not has_observability:
        findings.append(Finding("Minor", "No dedicated observability module detected", str(app_dir)))
        score -= 3
    elif not has_observability and (has_logs or has_metrics):
        score = 9
    status = "Passed" if score >= 7 else "Failed" if score <= 3 else "Conditional"
    return AreaResult(name="Observability", score=max(score, 0), status=status, findings=findings)


def check_security(name: str) -> AreaResult:
    findings: list[Finding] = []
    score = 10
    app_dir = APPS_DIR / name
    has_security = any(app_dir.glob("**/*security*.py")) or any(app_dir.glob("**/*sanitize*.py")) or any(app_dir.glob("**/*auth*.py"))
    if not has_security:
        findings.append(Finding("Minor", "No dedicated security module detected", str(app_dir)))
        score -= 2
    status = "Passed" if score >= 7 else "Failed" if score <= 3 else "Conditional"
    return AreaResult(name="Security", score=max(score, 0), status=status, findings=findings)


def check_lifecycle(name: str) -> AreaResult:
    findings: list[Finding] = []
    score = 10
    app_dir = APPS_DIR / name
    has_lifecycle = any(app_dir.glob("**/*lifecycle*.py")) or any(app_dir.glob("**/*loader*.py")) or any(app_dir.glob("**/*manager*.py"))
    if not has_lifecycle:
        findings.append(Finding("Minor", "No dedicated lifecycle module detected", str(app_dir)))
        score -= 2
    status = "Passed" if score >= 7 else "Failed" if score <= 3 else "Conditional"
    return AreaResult(name="Lifecycle Integration", score=max(score, 0), status=status, findings=findings)


def check_decision_integration(name: str) -> AreaResult:
    findings: list[Finding] = []
    score = 10
    app_dir = APPS_DIR / name
    has_decision = any(app_dir.glob("**/*decision*.py")) or any(app_dir.glob("**/*evidence*.py")) or any(app_dir.glob("**/*reasoning*.py"))
    if not has_decision:
        findings.append(Finding("Minor", "No decision integration module detected", str(app_dir)))
        score -= 2
    status = "Passed" if score >= 7 else "Failed" if score <= 3 else "Conditional"
    return AreaResult(name="Decision Integration", score=max(score, 0), status=status, findings=findings)


def check_explainability(name: str) -> AreaResult:
    findings: list[Finding] = []
    score = 10
    app_dir = APPS_DIR / name
    has_explainability = any(app_dir.glob("**/*explain*.py")) or any(app_dir.glob("**/*reasoning*.py")) or any(app_dir.glob("**/*evidence*.py"))
    if not has_explainability:
        findings.append(Finding("Minor", "No dedicated explainability module detected", str(app_dir)))
        score -= 3
    elif not any(app_dir.glob("**/explainability*.py")) and not any(app_dir.glob("**/*explain*.py")):
        score = 8
    status = "Passed" if score >= 7 else "Failed" if score <= 3 else "Conditional"
    return AreaResult(name="Explainability", score=max(score, 0), status=status, findings=findings)


def check_domain_knowledge(name: str) -> AreaResult:
    findings: list[Finding] = []
    score = 10
    app_dir = APPS_DIR / name
    has_knowledge = any(app_dir.glob("**/*knowledge*.py")) or any(app_dir.glob("**/*model*.py")) or any(app_dir.glob("**/*schema*.py"))
    if not has_knowledge:
        findings.append(Finding("Minor", "No dedicated knowledge module detected", str(app_dir)))
        score -= 2
    status = "Passed" if score >= 7 else "Failed" if score <= 3 else "Conditional"
    return AreaResult(name="Domain Knowledge", score=max(score, 0), status=status, findings=findings)


def check_engine_correctness(name: str) -> AreaResult:
    findings: list[Finding] = []
    score = 10
    app_dir = APPS_DIR / name
    has_engine = any(app_dir.glob("**/engine.py")) or any(app_dir.glob("**/orchestrator.py")) or any(app_dir.glob("**/execution_engine.py"))
    if not has_engine:
        findings.append(Finding("Minor", "No engine module detected", str(app_dir)))
        score -= 2
    status = "Passed" if score >= 7 else "Failed" if score <= 3 else "Conditional"
    return AreaResult(name="Engine Correctness", score=max(score, 0), status=status, findings=findings)


def check_api_stability(name: str) -> AreaResult:
    findings: list[Finding] = []
    score = 10
    app_dir = APPS_DIR / name
    has_schemas = any(app_dir.glob("**/schemas.py")) or any(app_dir.glob("**/models.py")) or any(app_dir.glob("**/contracts.py"))
    if not has_schemas:
        findings.append(Finding("Minor", "No API schema/contract module detected", str(app_dir)))
        score -= 2
    status = "Passed" if score >= 7 else "Failed" if score <= 3 else "Conditional"
    return AreaResult(name="API Stability", score=max(score, 0), status=status, findings=findings)


def check_error_handling(name: str) -> AreaResult:
    findings: list[Finding] = []
    score = 10
    app_dir = APPS_DIR / name
    has_error_handling = any(app_dir.glob("**/*error*.py")) or any(app_dir.glob("**/*exception*.py")) or any(app_dir.glob("**/*retry*.py"))
    if not has_error_handling:
        findings.append(Finding("Minor", "No dedicated error handling module detected", str(app_dir)))
        score -= 2
    status = "Passed" if score >= 7 else "Failed" if score <= 3 else "Conditional"
    return AreaResult(name="Error Handling", score=max(score, 0), status=status, findings=findings)


def check_performance(name: str) -> AreaResult:
    findings: list[Finding] = []
    score = 10
    app_dir = APPS_DIR / name
    has_performance = any(app_dir.glob("**/*performance*.py")) or any(app_dir.glob("**/*benchmark*.py")) or any(app_dir.glob("**/*worker*.py"))
    if not has_performance:
        findings.append(Finding("Minor", "No performance optimization module detected", str(app_dir)))
        score -= 3
    elif not any(app_dir.glob("**/worker*.py")):
        score = 8
    status = "Passed" if score >= 7 else "Failed" if score <= 3 else "Conditional"
    return AreaResult(name="Performance Target", score=max(score, 0), status=status, findings=findings)


def check_golden_tests(name: str) -> AreaResult:
    findings: list[Finding] = []
    score = 6
    golden_dir = GOLDEN_TESTS_DIR / name
    expected_categories = [
        "functional.json",
        "edge-cases.json",
        "invalid-input.json",
        "regression.json",
        "explainability.json",
        "performance.json",
        "contract-compliance.json",
    ]
    if golden_dir.exists() and golden_dir.is_dir():
        present = [p.name for p in golden_dir.iterdir() if p.is_file() and p.suffix == ".json"]
        missing = [c for c in expected_categories if c not in present]
        if not missing:
            score = 10
        else:
            score = 6 + (len(expected_categories) - len(missing))
            findings.append(Finding("Minor", f"Missing golden test categories: {', '.join(missing)}", str(golden_dir)))
    else:
        findings.append(Finding("Minor", "No golden test directory found", str(golden_dir)))
    status = "Passed" if score >= 7 else "Failed" if score <= 3 else "Conditional"
    return AreaResult(name="Golden Tests", score=max(score, 0), status=status, findings=findings)


def check_real_cases(name: str) -> AreaResult:
    findings: list[Finding] = []
    score = 5
    real_cases_dir = REAL_CASES_DIR / name
    scenarios_file = real_cases_dir / "scenarios.json"
    if scenarios_file.exists():
        try:
            scenarios = json.loads(scenarios_file.read_text(encoding="utf-8"))
            scenario_count = len(scenarios.get("scenarios", []))
            if scenario_count >= 5:
                score = 10
            elif scenario_count >= 3:
                score = 8
            elif scenario_count >= 1:
                score = 6
            else:
                findings.append(Finding("Minor", "No real-case scenarios defined", str(scenarios_file)))
        except Exception:
            findings.append(Finding("Minor", "Invalid scenarios.json", str(scenarios_file)))
    else:
        findings.append(Finding("Minor", "No real-case scenarios file found", str(real_cases_dir)))
    status = "Passed" if score >= 7 else "Failed" if score <= 3 else "Conditional"
    return AreaResult(name="Real Cases", score=max(score, 0), status=status, findings=findings)


AUDIT_CHECKS = [
    check_contract_compliance,
    check_api_stability,
    check_domain_knowledge,
    check_engine_correctness,
    check_explainability,
    check_decision_integration,
    check_lifecycle,
    check_observability,
    check_error_handling,
    check_documentation,
    check_security,
    check_performance,
    check_test_coverage,
    check_golden_tests,
    check_real_cases,
]


def score_to_grade(percentage: float) -> str:
    if percentage >= 90:
        return "A"
    if percentage >= 80:
        return "B"
    if percentage >= 70:
        return "C"
    if percentage >= 60:
        return "D"
    return "F"


def determine_status(grade: str, overall_score: int, max_score: int) -> str:
    percentage = (overall_score / max_score) * 100
    if percentage >= 90:
        return "Passed"
    if percentage >= 70:
        return "Conditional"
    return "Failed"


def audit_capability(name: str) -> AuditReport:
    areas = [check(name) for check in AUDIT_CHECKS]
    overall_score = sum(area.score for area in areas)
    max_score = sum(area.max_score for area in areas)
    percentage = (overall_score / max_score) * 100 if max_score else 0
    grade = score_to_grade(percentage)
    status = determine_status(grade, overall_score, max_score)

    critical = sum(1 for area in areas for f in area.findings if f.severity == "Critical")
    major = sum(1 for area in areas for f in area.findings if f.severity == "Major")
    minor = sum(1 for area in areas for f in area.findings if f.severity == "Minor")
    corrective = [
        f.description
        for area in areas
        for f in area.findings
        if f.severity in {"Critical", "Major"}
    ]

    return AuditReport(
        capability_id=name,
        capability_name=name.replace("_", " ").title(),
        overall_score=overall_score,
        grade=grade,
        status=status,
        areas=areas,
        summary={
            "criticalFindings": critical,
            "majorFindings": major,
            "minorFindings": minor,
            "correctiveActions": corrective,
        },
        completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    )


def render_text_report(report: AuditReport) -> str:
    lines = [
        f"Capability Audit Report: {report.capability_name} ({report.capability_id})",
        "=" * 60,
        f"Overall Score : {report.overall_score}",
        f"Grade         : {report.grade}",
        f"Status        : {report.status}",
        f"Completed At  : {report.completed_at}",
        "",
        "Area Breakdown:",
        "-" * 60,
    ]
    for area in report.areas:
        findings_summary = ", ".join(f.severity for f in area.findings) if area.findings else "None"
        lines.append(f"  {area.name:<30} {area.score:>3}/{area.max_score:<3} {area.status:<12} Findings: {findings_summary}")

    lines += [
        "",
        "Summary:",
        f"  Critical Findings : {report.summary.get('criticalFindings', 0)}",
        f"  Major Findings    : {report.summary.get('majorFindings', 0)}",
        f"  Minor Findings    : {report.summary.get('minorFindings', 0)}",
        "",
        "Corrective Actions:",
    ]
    for idx, action in enumerate(report.summary.get("correctiveActions", []), 1):
        lines.append(f"  {idx}. {action}")

    return "\n".join(lines)


def save_report(report: AuditReport) -> Path:
    AUDIT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = AUDIT_OUTPUT_DIR / f"{report.capability_id}-audit.json"
    json_path.write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")

    report_output = REPORT_OUTPUT_DIR / f"{report.capability_id}-audit-report.txt"
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(render_text_report(report), encoding="utf-8")
    return json_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Capability Audit for Phase 1.1")
    parser.add_argument("--capability", help="Specific capability ID to audit")
    parser.add_argument("--all", action="store_true", help="Audit all capabilities")
    args = parser.parse_args()

    capabilities = discover_capabilities()
    if not capabilities:
        print("No capabilities discovered under apps/")
        return 1

    targets = capabilities if args.all else ([args.capability] if args.capability else capabilities[:1])

    for name in targets:
        if name not in capabilities:
            print(f"Unknown capability: {name}")
            return 1
        report = audit_capability(name)
        path = save_report(report)
        print(render_text_report(report))
        print(f"\nSaved audit artifact: {path}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
