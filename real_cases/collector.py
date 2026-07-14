from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from real_cases.schema import RealCase

logger = logging.getLogger(__name__)

REAL_CASES_DIR = Path(__file__).resolve().parent.parent / "real_cases"
DOGFOODING_DIR = REAL_CASES_DIR / "dogfooding"


def save_case(case: RealCase) -> Path:
    case_dir = REAL_CASES_DIR / case.category
    case_dir.mkdir(parents=True, exist_ok=True)
    path = case_dir / f"{case.id}.json"
    path.write_text(json.dumps(case.to_dict(), indent=2), encoding="utf-8")
    logger.info("Real case saved: %s", path)
    return path


def save_dogfooding_entry(
    case_id: str,
    title: str,
    category: str,
    source_files: list[str],
    context: str,
    expected_findings: list[str] | None = None,
    vendor: str = "",
    device_role: str = "",
) -> RealCase:
    case = RealCase(
        id=case_id,
        title=title,
        category=category,
        vendor=vendor,
        device_role=device_role,
        source_files=source_files,
        context=context,
        expected_findings=expected_findings or [],
        tags=["dogfooding"],
    )
    path = save_case(case)
    logger.info("Dogfooding case created: %s", path)
    return case


def record_lesson_learned(case_id: str, lesson: str, capability_gap: str = "", future_recommendation: str = "") -> RealCase | None:
    case = load_case(case_id)
    if not case:
        logger.warning("Real case not found for lesson learned: %s", case_id)
        return None
    case.lesson_learned = lesson
    case.capability_gap = capability_gap
    case.future_recommendation = future_recommendation
    case.updated_at = datetime.utcnow()
    save_case(case)
    logger.info("Lesson learned recorded for case: %s", case_id)
    return case


def record_benchmark_result(
    case_id: str,
    result: dict[str, Any],
    expected_findings: list[str] | None = None,
    expected_risk_score: float | None = None,
    expected_compliance_score: float | None = None,
) -> RealCase | None:
    case = load_case(case_id)
    if not case:
        logger.warning("Real case not found for benchmark result: %s", case_id)
        return None
    case.result = result
    if expected_findings is not None:
        case.expected_findings = expected_findings
    if expected_risk_score is not None:
        case.expected_risk_score = expected_risk_score
    if expected_compliance_score is not None:
        case.expected_compliance_score = expected_compliance_score
    case.updated_at = datetime.utcnow()
    save_case(case)
    logger.info("Benchmark result recorded for case: %s", case_id)
    return case


def load_case(case_id: str) -> RealCase | None:
    for path in REAL_CASES_DIR.rglob(f"{case_id}.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        return RealCase(
            id=data["id"],
            title=data["title"],
            category=data["category"],
            subcategory=data.get("subcategory", ""),
            vendor=data.get("vendor", ""),
            device_role=data.get("device_role", ""),
            source_files=data.get("source_files", []),
            context=data.get("context", ""),
            expected_findings=data.get("expected_findings", []),
            expected_risk_score=data.get("expected_risk_score"),
            expected_compliance_score=data.get("expected_compliance_score"),
            tags=data.get("tags", []),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.utcnow().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.utcnow().isoformat())),
            result=data.get("result"),
            lesson_learned=data.get("lesson_learned", ""),
            capability_gap=data.get("capability_gap", ""),
            future_recommendation=data.get("future_recommendation", ""),
            benchmark_passed=data.get("benchmark_passed"),
            metrics=data.get("metrics", {}),
        )
    return None


def list_cases(category: str | None = None) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    search_dir = REAL_CASES_DIR / category if category else REAL_CASES_DIR
    if not search_dir.exists():
        return cases
    for path in search_dir.rglob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            cases.append(data)
        except Exception:
            continue
    cases.sort(key=lambda item: item.get("created_at", ""), reverse=True)
    return cases
