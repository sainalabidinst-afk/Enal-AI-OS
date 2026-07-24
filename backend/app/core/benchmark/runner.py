from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from pathlib import Path
from typing import Any, Protocol

import httpx

from backend.app.core.benchmark.models import (
    BenchmarkCase,
    BenchmarkResult,
    BenchmarkSuite,
    CapabilityScore,
    ExpectedResult,
)
from backend.app.core.telemetry.service import record_analysis_event

logger = logging.getLogger(__name__)


class ProgressCallback(Protocol):
    async def __call__(self, case_id: str, passed: bool, score: float, capability_score: float) -> None: ...


class BenchmarkRunner:
    def __init__(self, base_url: str = "http://localhost:8000", concurrency: int = 5) -> None:
        self.base_url = base_url.rstrip("/")
        self.concurrency = concurrency

    async def run_suite(self, suite: BenchmarkSuite, progress: ProgressCallback | None = None) -> BenchmarkSuite:
        suite.results = []
        semaphore = asyncio.Semaphore(self.concurrency)

        async with httpx.AsyncClient(
            timeout=httpx.Timeout(60.0),
            limits=httpx.Limits(max_connections=self.concurrency + 10, max_keepalive_connections=self.concurrency),
        ) as client:
            async def run(case: BenchmarkCase) -> BenchmarkResult:
                async with semaphore:
                    return await self.run_case(case, client=client, progress=progress)

            tasks = [asyncio.create_task(run(case)) for case in suite.cases]
            results = await asyncio.gather(*tasks, return_exceptions=False)
            suite.results = list(results)
        return suite

    async def run_case(
        self,
        case: BenchmarkCase,
        client: httpx.AsyncClient,
        progress: ProgressCallback | None = None,
    ) -> BenchmarkResult:
        analysis_id = str(uuid.uuid4())
        started = time.perf_counter()
        details: dict[str, Any] = {}
        passed = False
        score = 0.0
        findings = 0
        risk_score = 0.0
        confidence = 0.0
        expected = case.expected or self._load_expected(case)
        result_details: dict[str, Any] = {}
        capability_breakdown = CapabilityScore(vendor=case.vendor)

        try:
            content = self._load_case_content(case)
            if not content:
                raise FileNotFoundError(f"Case content not found for {case.case_id}")

            boundary = f"benchmark{uuid.uuid4().hex}"
            payload = (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="files"; filename="{case.filename}"\r\n'
                f"Content-Type: application/octet-stream\r\n\r\n"
            ).encode("utf-8") + content.encode("utf-8", errors="ignore") + f"\r\n--{boundary}--\r\n".encode("utf-8")

            response = await client.post(
                f"{self.base_url}/api/v1/attachments/analyze",
                content=payload,
                headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            )
            response.raise_for_status()
            data = response.json()

            total_ms = (time.perf_counter() - started) * 1000
            ast = data.get("ast", {}) or {}
            findings_list = ast.get("findings", []) or []
            findings = len(findings_list)
            risk_score = float(data.get("risk_score", 0) or 0)
            confidence = float(data.get("confidence", 0) or 0)
            vendor = ast.get("vendor") or data.get("vendor") or case.vendor
            device_type = ast.get("device_role") or data.get("device_role") or case.device_type
            parser = ast.get("format") or ""

            record_analysis_event(
                analysis_id=analysis_id,
                status="success",
                workspace_id="",
                vendor=vendor,
                device_type=device_type,
                parser=parser,
                total_time_ms=round(total_ms, 2),
                findings=findings,
                confidence=confidence,
                executive_report=bool(data.get("summary")),
                benchmark_case_id=case.case_id,
            )

            details = {
                "summary": data.get("summary"),
                "vendor": vendor,
                "parser": parser,
            }
            result_details = {
                "summary": data.get("summary"),
                "vendor": vendor,
                "parser": parser,
                "ast": ast,
            }

            score = self._score_case(case, expected, findings=findings, risk_score=risk_score, confidence=confidence, ast=ast)
            self._capability_score(case, expected, findings=findings, risk_score=risk_score, confidence=confidence, ast=ast)
            capability_breakdown = self._compute_capability_breakdown(
                case, expected, ast=ast, data=data, findings_list=findings_list
            )
            capability_breakdown.compute_total()
            passed = score >= 0.6
        except Exception as exc:
            details["error"] = str(exc)
            record_analysis_event(
                analysis_id=analysis_id,
                status="error",
                error=str(exc),
                benchmark_case_id=case.case_id,
            )

        if progress:
            try:
                await progress(case.case_id, passed, score, capability_breakdown.total)
            except Exception:
                pass

        return BenchmarkResult(
            case_id=case.case_id,
            passed=passed,
            score=score,
            findings=findings,
            risk_score=risk_score,
            confidence=confidence,
            analysis_time_ms=0.0,
            details=result_details if result_details else details,
            expected=expected,
            capability_score=capability_breakdown.total,
            capability_breakdown=capability_breakdown,
        )

    def _load_case_content(self, case: BenchmarkCase) -> str:
        path = Path(case.filename)
        if path.exists():
            return path.read_text(encoding="utf-8", errors="ignore")
        path = Path("real_cases") / case.vendor / case.filename
        if path.exists():
            return path.read_text(encoding="utf-8", errors="ignore")
        return ""

    def _load_expected(self, case: BenchmarkCase) -> ExpectedResult:
        expected_path = Path(case.filename).parent / "expected.json"
        if not expected_path.exists():
            expected_path = Path("real_cases") / case.vendor / (Path(case.filename).stem + ".expected.json")
        if not expected_path.exists():
            vendor_dir = Path("real_cases") / case.vendor
            if vendor_dir.exists():
                for p in vendor_dir.rglob("expected.json"):
                    return ExpectedResult.from_dict(json.loads(p.read_text(encoding="utf-8")))
            return ExpectedResult(vendor=case.vendor, device_type=case.device_type)
        try:
            return ExpectedResult.from_dict(json.loads(expected_path.read_text(encoding="utf-8")))
        except Exception as exc:
            logger.warning("Failed to parse expected.json for %s: %s", case.case_id, exc)
            return ExpectedResult(vendor=case.vendor, device_type=case.device_type)

    def _score_case(
        self,
        case: BenchmarkCase,
        expected: ExpectedResult,
        findings: int = 0,
        risk_score: float = 0.0,
        confidence: float = 0.0,
        ast: dict[str, Any] | None = None,
    ) -> float:
        score = 0.0
        if findings >= expected.findings_min:
            score += 0.25
        if risk_score <= expected.risk_max:
            score += 0.25
        if confidence >= expected.confidence_min:
            score += 0.25
        if expected.expected_keywords and ast:
            text = json.dumps(ast, ensure_ascii=False).lower()
            if all(keyword.lower() in text for keyword in expected.expected_keywords):
                score += 0.25
        return round(score, 2)

    def _capability_score(
        self,
        case: BenchmarkCase,
        expected: ExpectedResult,
        findings: int = 0,
        risk_score: float = 0.0,
        confidence: float = 0.0,
        ast: dict[str, Any] | None = None,
    ) -> float:
        score = 0.0
        score += 0.25 if findings >= expected.findings_min else 0.0
        score += 0.25 if risk_score <= expected.risk_max else 0.0
        score += 0.25 if confidence >= expected.confidence_min else 0.0
        if expected.expected_keywords and ast:
            text = json.dumps(ast, ensure_ascii=False).lower()
            matched = sum(1 for keyword in expected.expected_keywords if keyword.lower() in text)
            score += 0.25 * (matched / len(expected.expected_keywords))
        return round(score * 100, 2)

    def _compute_capability_breakdown(
        self,
        case: BenchmarkCase,
        expected: ExpectedResult,
        ast: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        findings_list: list[dict[str, Any]] | None = None,
    ) -> CapabilityScore:
        if not ast or not findings_list:
            return CapabilityScore(vendor=case.vendor)

        breakdown = CapabilityScore(vendor=case.vendor)

        breakdown.parser = self._score_parser(case, expected, ast=ast)
        breakdown.reasoning = self._score_reasoning(case, expected, ast=ast, findings_list=findings_list)
        breakdown.evidence = self._score_evidence(findings_list)
        breakdown.compliance = self._score_compliance(ast)
        breakdown.executive_report = self._score_executive_report(data)

        return breakdown

    def _score_parser(self, case: BenchmarkCase, expected: ExpectedResult, ast: dict[str, Any]) -> float:
        if not ast:
            return 0.0
        vendor_match = 100.0 if ast.get("vendor") == case.vendor else 50.0
        has_findings = 100.0 if ast.get("findings") else 0.0
        has_structure = 100.0 if ast.get("interfaces") or ast.get("firewall") or ast.get("routing") else 50.0
        return round((vendor_match + has_findings + has_structure) / 3, 2)

    def _score_reasoning(
        self, case: BenchmarkCase, expected: ExpectedResult, ast: dict[str, Any], findings_list: list[dict[str, Any]]
    ) -> float:
        if not findings_list:
            return 0.0
        with_recommendations = sum(1 for f in findings_list if f.get("recommendation"))
        with_confidence = sum(1 for f in findings_list if f.get("confidence") is not None)
        with_evidence_refs = sum(1 for f in findings_list if f.get("evidence"))
        scores = [
            min(100.0, (with_recommendations / max(len(findings_list), 1)) * 100),
            min(100.0, (with_confidence / max(len(findings_list), 1)) * 100),
            min(100.0, (with_evidence_refs / max(len(findings_list), 1)) * 100),
        ]
        return round(sum(scores) / len(scores), 2)

    def _score_evidence(self, findings_list: list[dict[str, Any]]) -> float:
        if not findings_list:
            return 0.0
        with_evidence = sum(1 for f in findings_list if f.get("evidence"))
        return round((with_evidence / len(findings_list)) * 100, 2)

    def _score_compliance(self, ast: dict[str, Any]) -> float:
        compliance = ast.get("compliance_score")
        if compliance is None:
            return 0.0
        return round(float(compliance) * 100, 2)

    def _score_executive_report(self, data: dict[str, Any]) -> float:
        if data.get("summary"):
            return 100.0
        return 0.0
