from __future__ import annotations

import json
import logging
import os
from collections import defaultdict
from pathlib import Path
from typing import Any

from fastapi import APIRouter

from backend.app.core.benchmark.models import BenchmarkCase, BenchmarkSuite
from backend.app.core.benchmark.runner import BenchmarkRunner

logger = logging.getLogger(__name__)
router = APIRouter()
runner = BenchmarkRunner()
CCE_HISTORY_DIR = Path(__file__).resolve().parent.parent.parent / "benchmarks" / "cce_history"


def _load_suite_from_disk(base_dir: str = "real_cases") -> BenchmarkSuite:
    suite = BenchmarkSuite(suite_id="real-world-v1", name="Real World Benchmark v1")
    if not os.path.isdir(base_dir):
        return suite
    for vendor in sorted(os.listdir(base_dir)):
        vendor_dir = os.path.join(base_dir, vendor)
        if not os.path.isdir(vendor_dir):
            continue
        for root, dirs, files in os.walk(vendor_dir):
            dirs.sort()
            has_config = any(f in files for f in ("config.rsc", "config.txt", "sample_hotspot.txt"))
            if not has_config:
                continue
            case_name = Path(root).name
            config_file = None
            for f in ("config.rsc", "config.txt", "sample_hotspot.txt"):
                if f in files:
                    config_file = f
                    break
            if not config_file:
                continue
            case_path = os.path.join(root, config_file)
            suite.cases.append(
                BenchmarkCase(
                    case_id=f"{vendor}:{case_name}",
                    vendor=vendor,
                    device_type="",
                    category="real-world",
                    filename=case_path,
                    expected_findings_min=0,
                    expected_risk_max=1.0,
                    expected_confidence_min=0.0,
                    tags=[vendor, case_name],
                )
            )
    return suite


@router.get("/benchmark/suite")
async def get_benchmark_suite():
    suite = _load_suite_from_disk()
    return {
        "suite_id": suite.suite_id,
        "name": suite.name,
        "case_count": len(suite.cases),
        "cases": [
            {
                "case_id": case.case_id,
                "vendor": case.vendor,
                "filename": case.filename,
                "category": case.category,
                "tags": case.tags,
            }
            for case in suite.cases
        ],
    }


@router.post("/benchmark/run")
async def run_benchmark():
    suite = _load_suite_from_disk()
    if not suite.cases:
        return {
            "suite_id": suite.suite_id,
            "results": [],
            "summary": {"total": 0, "passed": 0, "failed": 0, "avg_score": 0},
        }

    async def progress_callback(
        case_id: str,
        passed: bool,
        score: float,
        capability_score: float,
    ) -> None:
        logger.info(
            "Benchmark progress: %s passed=%s score=%s capability=%s",
            case_id,
            passed,
            score,
            capability_score,
        )

    suite = await runner.run_suite(suite, progress=progress_callback)
    results = [
        {
            "case_id": result.case_id,
            "passed": result.passed,
            "score": result.score,
            "findings": result.findings,
            "risk_score": result.risk_score,
            "confidence": result.confidence,
            "capability_score": result.capability_score,
            "capability_breakdown": {
                "vendor": result.capability_breakdown.vendor
                if result.capability_breakdown
                else result.case_id.split(":")[0],
                "parser": result.capability_breakdown.parser
                if result.capability_breakdown
                else 0.0,
                "reasoning": result.capability_breakdown.reasoning
                if result.capability_breakdown
                else 0.0,
                "evidence": result.capability_breakdown.evidence
                if result.capability_breakdown
                else 0.0,
                "compliance": result.capability_breakdown.compliance
                if result.capability_breakdown
                else 0.0,
                "executive_report": result.capability_breakdown.executive_report
                if result.capability_breakdown
                else 0.0,
                "total": result.capability_breakdown.total
                if result.capability_breakdown
                else 0.0,
            },
            "details": result.details,
        }
        for result in suite.results
    ]
    passed = sum(1 for result in suite.results if result.passed)
    avg_score = (
        round(sum(result.score for result in suite.results) / len(suite.results), 2)
        if suite.results
        else 0
    )
    avg_capability = (
        round(
            sum(result.capability_score for result in suite.results) / len(suite.results),
            2,
        )
        if suite.results
        else 0
    )
    return {
        "suite_id": suite.suite_id,
        "results": results,
        "summary": {
            "total": len(suite.results),
            "passed": passed,
            "failed": len(suite.results) - passed,
            "avg_score": avg_score,
            "avg_capability_score": avg_capability,
        },
    }


@router.get("/benchmark/capability-scores")
async def get_capability_scores():
    suite = _load_suite_from_disk()
    if not suite.cases:
        return {"capabilities": {}}

    async def progress_callback(
        case_id: str,
        passed: bool,
        score: float,
        capability_score: float,
    ) -> None:
        pass

    suite = await runner.run_suite(suite, progress=progress_callback)

    capabilities: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "vendor": "",
            "cases": 0,
            "passed": 0,
            "failed": 0,
            "avg_score": 0.0,
            "avg_capability_score": 0.0,
            "parser": 0.0,
            "reasoning": 0.0,
            "evidence": 0.0,
            "compliance": 0.0,
            "executive_report": 0.0,
        }
    )

    for result in suite.results:
        vendor = result.case_id.split(":")[0]
        cap = capabilities[vendor]
        cap["vendor"] = vendor
        cap["cases"] += 1
        if result.passed:
            cap["passed"] += 1
        else:
            cap["failed"] += 1
        cap["avg_score"] += result.score
        cap["avg_capability_score"] += result.capability_score
        if result.capability_breakdown:
            cap["parser"] += result.capability_breakdown.parser
            cap["reasoning"] += result.capability_breakdown.reasoning
            cap["evidence"] += result.capability_breakdown.evidence
            cap["compliance"] += result.capability_breakdown.compliance
            cap["executive_report"] += result.capability_breakdown.executive_report

    output: dict[str, Any] = {}
    for vendor, cap in capabilities.items():
        count = cap["cases"]
        output[vendor] = {
            "vendor": vendor,
            "cases": count,
            "passed": cap["passed"],
            "failed": cap["failed"],
            "avg_score": round(cap["avg_score"] / count, 2),
            "avg_capability_score": round(cap["avg_capability_score"] / count, 2),
            "parser": round(cap["parser"] / count, 2),
            "reasoning": round(cap["reasoning"] / count, 2),
            "evidence": round(cap["evidence"] / count, 2),
            "compliance": round(cap["compliance"] / count, 2),
            "executive_report": round(cap["executive_report"] / count, 2),
        }

    return {"capabilities": output}


@router.get("/benchmark/cce/status")
async def get_cce_status():
    latest_path = CCE_HISTORY_DIR / "latest.json"
    if not latest_path.exists():
        return {"status": "no_data", "message": "No CCE runs found"}
    try:
        data = json.loads(latest_path.read_text(encoding="utf-8"))
        return {
            "status": "ok",
            "run_id": data.get("run_id"),
            "timestamp": data.get("timestamp"),
            "total_cases": data.get("total_cases", 0),
            "passed_cases": data.get("passed_cases", 0),
            "failed_cases": data.get("failed_cases", 0),
            "avg_score": data.get("avg_score", 0),
            "avg_capability_score": data.get("avg_capability_score", 0),
            "regression_count": len(data.get("regressions", [])),
            "regressions": data.get("regressions", []),
            "capabilities": data.get("capabilities", {}),
            "calibration": data.get("calibration", {}),
        }
    except Exception as exc:
        return {"status": "error", "message": str(exc)}
