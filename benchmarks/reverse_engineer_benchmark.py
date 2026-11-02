"""Offline deterministic benchmark for Reverse Engineer evidence mapping."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from apps.reverse_engineer.models import REATargetType
from apps.reverse_engineer.rea_service import REAService

FIXTURE_DIR = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "reverse_engineer"


def _load_fixture(name: str) -> dict[str, Any]:
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


def test_native_evidence_mapping() -> float:
    result = REAService()._parse_binary_inspection(
        "synthetic:sample.bin",
        _load_fixture("native_inspection.json"),
    )
    evidence = result.evidence[0]
    return float(
        result.target_type == REATargetType.NATIVE
        and evidence.evidence_id == "SYN-NATIVE-001"
        and result.findings == ["The artifact exposes a callable entry point."]
        and evidence.unknowns == ["Runtime behavior was not executed."]
    )


def test_javascript_evidence_and_artifacts_mapping() -> float:
    result = REAService()._parse_js_analysis(
        "synthetic:renderer.js",
        _load_fixture("javascript_inspection.json"),
    )
    return float(
        result.target_type == REATargetType.ELECTRON_JS
        and len(result.evidence) == 1
        and result.artifacts[0].artifact_id == "SYN-ART-001"
        and result.artifacts[0].evidence_refs == ["SYN-JS-001"]
    )


def run_benchmark() -> dict[str, float]:
    results = {
        "native_evidence_mapping": test_native_evidence_mapping(),
        "javascript_evidence_mapping": test_javascript_evidence_and_artifacts_mapping(),
    }
    results["overall"] = round(sum(results.values()) / len(results), 4)
    return results


def main() -> int:
    results = run_benchmark()
    for name, score in results.items():
        print(f"{name}: {score:.2%}")
    return 0 if results["overall"] == 1.0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
