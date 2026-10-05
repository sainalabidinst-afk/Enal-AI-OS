#!/usr/bin/env python3
"""Run smoke evaluation against a running backend.

Usage:
    python scripts/run_smoke_evaluation.py --base-url http://localhost:8000
"""

from __future__ import annotations

import argparse
import sys
import time

import requests


def wait_for_backend(base_url: str, timeout: int = 150) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            pass
        time.sleep(5)
    return False


def run_benchmark(base_url: str, token: str | None = None) -> dict:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.post(f"{base_url}/api/v1/benchmark/run", headers=headers, timeout=300)
    response.raise_for_status()
    return response.json()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run smoke benchmark evaluation")
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--token", default=None)
    args = parser.parse_args()

    print(f"Waiting for backend at {args.base_url} ...")
    if not wait_for_backend(args.base_url):
        print("Backend did not become ready in time", file=sys.stderr)
        return 1
    print("Backend is healthy. Running benchmark suite...")

    result = run_benchmark(args.base_url, args.token)
    summary = result.get("summary", {})
    print(f"Suite: {result.get('suite_id')}")
    print(f"Total: {summary.get('total')}")
    print(f"Passed: {summary.get('passed')}")
    print(f"Failed: {summary.get('failed')}")
    print(f"Avg score: {summary.get('avg_score')}")
    print(f"Avg capability score: {summary.get('avg_capability_score')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
