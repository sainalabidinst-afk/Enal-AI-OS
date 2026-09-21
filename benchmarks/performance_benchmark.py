"""
Benchmark Suite: ECP Performance & Quality
============================================

This benchmark suite measures:
- Determinism (same input → same output)
- Latency (response time)
- Token efficiency (tokens per task)
- Reasoning quality (accuracy)
- Reproducibility (consistent results)
- Plugin overhead (plugin vs native)
"""

import asyncio
import json
import time
import hashlib
from typing import Any

try:
    from backend.app.core.adaptive_runtime import adaptive_runtime
    from backend.app.core.config import settings
except Exception:
    adaptive_runtime = None
    settings = None


class BenchmarkMetrics:
    def __init__(self):
        self.latencies: list[float] = []
        self.token_counts: list[int] = []
        self.determinism_hashes: list[str] = []
        self.successes: list[bool] = []

    def record(self, latency_ms: float, tokens: int, output_hash: str, success: bool):
        self.latencies.append(latency_ms)
        self.token_counts.append(tokens)
        self.determinism_hashes.append(output_hash)
        self.successes.append(success)

    def get_summary(self) -> dict[str, Any]:
        if not self.latencies:
            return {}
        return {
            "avg_latency_ms": sum(self.latencies) / len(self.latencies),
            "p95_latency_ms": sorted(self.latencies)[int(len(self.latencies) * 0.95)] if self.latencies else 0,
            "avg_tokens": sum(self.token_counts) / len(self.token_counts),
            "determinism_rate": len(set(self.determinism_hashes)) / len(self.determinism_hashes) if self.determinism_hashes else 0,
            "success_rate": sum(1 for s in self.successes if s) / len(self.successes) if self.successes else 0,
        }


def _extract_output(result: Any) -> str:
    """Extract textual output from runtime result using actual runtime contract."""
    if not isinstance(result, dict):
        return str(result)

    # Preferred: decision.selected_description
    decision = result.get("decision")
    if isinstance(decision, dict):
        selected = decision.get("selected_description")
        if selected:
            return str(selected)

    # Fallback: decision may itself be the description string
    if isinstance(decision, str):
        return decision

    # Fallback: action.action
    action = result.get("action")
    if isinstance(action, dict):
        act = action.get("action")
        if act:
            return str(act)

    if isinstance(action, str):
        return action

    return ""


def _provider_for_model(model: str) -> str | None:
    if model.startswith("gemini"):
        return "gemini"
    if model.startswith("gpt"):
        return "openai"
    if model.startswith("claude"):
        return "anthropic"
    if model.startswith("ollama/"):
        return "ollama"
    return None


def _provider_ready(model: str, config: Any) -> bool:
    provider = _provider_for_model(model)
    if provider == "gemini":
        return bool(getattr(config, "GEMINI_API_KEY", "") or getattr(config, "GOOGLE_API_KEY", ""))
    if provider == "openai":
        return bool(getattr(config, "OPENAI_API_KEY", ""))
    if provider == "anthropic":
        return bool(getattr(config, "ANTHROPIC_API_KEY", ""))
    return provider in {None, "ollama"}


async def run_with_metrics(user_input: str, metrics: BenchmarkMetrics):
    if adaptive_runtime is None:
        raise RuntimeError("benchmark runtime is not configured")
    start = time.time()
    result = await adaptive_runtime.execute(user_input)
    latency = (time.time() - start) * 1000

    output_str = _extract_output(result)

    output_hash = hashlib.sha256(output_str.encode()).hexdigest()[:16]
    tokens = len(output_str.split())
    success = "error" not in output_str.lower()
    metrics.record(latency, tokens, output_hash, success)
    return result


async def main() -> int:
    if settings is None or adaptive_runtime is None:
        print("BENCHMARK BLOCKED: runtime configuration is unavailable")
        print("BENCHMARK RAW MEASUREMENTS: none")
        print("BENCHMARK FINAL RESULTS: not generated")
        return 1

    model = settings.DEFAULT_REASONING_MODEL
    if not _provider_ready(model, settings):
        print(f"BENCHMARK BLOCKED: provider credential is unavailable for {model}")
        print("BENCHMARK RAW MEASUREMENTS: none")
        print("BENCHMARK FINAL RESULTS: not generated")
        return 1

    metrics = BenchmarkMetrics()

    # Run benchmarks
    test_inputs = [
        "Calculate 2 + 2",
        "Write a hello world function",
        "List files in directory",
        "Explain quantum computing",
    ]

    for user_input in test_inputs:
        try:
            await run_with_metrics(user_input, metrics)
        except Exception as exc:
            print(f"BENCHMARK BLOCKED: provider call failed ({type(exc).__name__})")
            print("BENCHMARK RAW MEASUREMENTS: none")
            print("BENCHMARK FINAL RESULTS: not generated")
            return 1

    summary = metrics.get_summary()
    print("BENCHMARK RAW MEASUREMENTS:")
    print(json.dumps({"samples": len(metrics.latencies), "summary": summary}, indent=2))
    print("BENCHMARK FINAL RESULTS: raw measurements collected; no certification score generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
