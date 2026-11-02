"""Offline deterministic benchmark for the Digital Twin Engine."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from apps.digital_twin_engine.engine import DigitalTwinEngine

FIXTURE_PATH = (
    Path(__file__).resolve().parent.parent
    / "tests"
    / "fixtures"
    / "digital_twin_engine"
    / "scenario.json"
)


def _fixture() -> dict[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def test_state_mirroring() -> float:
    fixture = _fixture()
    engine = DigitalTwinEngine()
    twin = engine.mirror_state(fixture["initial_state"])
    status = engine.get_status()
    return float(
        twin.system_state == fixture["initial_state"]
        and status.system_state_keys == list(fixture["initial_state"])
        and status.mirror_health == "healthy"
    )


def test_simulation_is_reproducible() -> float:
    fixture = _fixture()
    results = []
    for _ in range(2):
        engine = DigitalTwinEngine()
        engine.mirror_state(fixture["initial_state"])
        results.append(
            engine.run_simulation(
                fixture["scenario"],
                fixture["parameters"],
                iterations=fixture["iterations"],
            )
        )

    first, second = results
    return float(
        first.success
        and first.iterations == fixture["iterations"]
        and first.statistics == second.statistics
        and first.statistics["min"] <= first.statistics["mean"] <= first.statistics["max"]
    )


def run_benchmark() -> dict[str, float]:
    results = {
        "state_mirroring": test_state_mirroring(),
        "simulation_reproducibility": test_simulation_is_reproducible(),
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
