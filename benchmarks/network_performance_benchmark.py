"""
Performance Benchmark
======================

Benchmarks parser and analyzer performance with various config sizes.
"""

import asyncio
import time
from pathlib import Path
from typing import Any

from apps.network_engineer import get_app


GOLDEN_DIR = Path(__file__).resolve().parents[2] / "golden" / "mikrotik"


def generate_large_config(lines: int) -> str:
    """Generate a large RouterOS config for benchmarking."""
    config_lines = [
        "/system identity",
        "set name=benchmark-router",
        "",
        "/interface ethernet"
    ]

    for i in range(lines // 10):
        config_lines.append(f"set [ find default-name=ether{(i % 10) + 1} ] name=iface{i}")

    config_lines.extend([
        "",
        "/ip address"
    ])

    for i in range(lines // 20):
        config_lines.append(f"add address=192.168.{i // 256}.{i % 256}/24 interface=iface{i} network=192.168.{i // 256}.0")

    config_lines.extend([
        "",
        "/ip firewall filter"
    ])

    for i in range(lines // 15):
        config_lines.append(f"add action=accept chain=input protocol=tcp port={1000 + i}")

    return "\n".join(config_lines)


async def benchmark_scenario(name: str, config_content: str) -> dict[str, Any]:
    """Benchmark a single scenario."""
    app = get_app()

    start_parse = time.perf_counter()
    config = app.parser.parse(config_content)
    parse_time = time.perf_counter() - start_parse

    start_analyze = time.perf_counter()
    analysis = await app.analyze_config(config_content)
    analyze_time = time.perf_counter() - start_analyze

    start_docs = time.perf_counter()
    docs = await app.generate_documentation(config_content)
    docs_time = time.perf_counter() - start_docs

    total_time = parse_time + analyze_time + docs_time

    return {
        "name": name,
        "config_size": len(config_content),
        "parse_time_ms": parse_time * 1000,
        "analyze_time_ms": analyze_time * 1000,
        "docs_time_ms": docs_time * 1000,
        "total_time_ms": total_time * 1000,
        "findings_count": len(analysis.get("issues", [])),
        "docs_chars": len(docs),
    }


async def main():
    print("ECP Network Engineer - Performance Benchmark")
    print("=" * 80)

    scenarios = [
        ("small-500", generate_large_config(500)),
        ("medium-5000", generate_large_config(5000)),
        ("large-50000", generate_large_config(50000)),
    ]

    results = []
    for name, config in scenarios:
        try:
            result = await benchmark_scenario(name, config)
            results.append(result)
            print(f"[{name}] Size: {result['config_size']:,} bytes | "
                  f"Parse: {result['parse_time_ms']:.1f}ms | "
                  f"Analyze: {result['analyze_time_ms']:.1f}ms | "
                  f"Docs: {result['docs_time_ms']:.1f}ms | "
                  f"Total: {result['total_time_ms']:.1f}ms")
        except Exception as e:
            print(f"[FAIL] {name}: {e}")

    print("=" * 80)

    if results:
        avg_total = sum(r["total_time_ms"] for r in results) / len(results)
        print(f"Average total time: {avg_total:.1f}ms")
        print("SUCCESS: Performance benchmark completed")


if __name__ == "__main__":
    asyncio.run(main())
