#!/usr/bin/env python3
"""
Smoke Test Script for Enal AI OS v1.0.0-rc1

Run this script after deployment to verify core functionality.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Install with: pip install requests")
    sys.exit(1)

BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3001"


def check_endpoint(name: str, url: str, method: str = "GET", expected_status: int = 200, **kwargs) -> bool:
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=10, **kwargs)
        elif method.upper() == "POST":
            response = requests.post(url, timeout=10, **kwargs)
        else:
            print(f"  [UNKNOWN] {name}: unsupported method {method}")
            return False

        if response.status_code == expected_status:
            print(f"  [PASS] {name}: {response.status_code}")
            return True
        else:
            print(f"  [FAIL] {name}: expected {expected_status}, got {response.status_code}")
            print(f"         Body: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"  [ERROR] {name}: {e}")
        return False


def main() -> int:
    print("=" * 60)
    print("Enal AI OS v1.0.0-rc1 — Smoke Test")
    print("=" * 60)
    print()

    results = []

    print("Backend Health:")
    results.append(check_endpoint("Root", f"{BASE_URL}/"))
    results.append(check_endpoint("Health", f"{BASE_URL}/health"))

    print("\nAPI v1 Endpoints (authenticated):")
    headers = {"Authorization": "Bearer test-token"}
    results.append(check_endpoint("Integration Health", f"{BASE_URL}/api/v1/integration/health", headers=headers))
    results.append(check_endpoint("Trading Health", f"{BASE_URL}/api/v1/trading/health", headers=headers))
    results.append(check_endpoint("Capabilities", f"{BASE_URL}/api/v1/capabilities", headers=headers))
    results.append(check_endpoint("Agents", f"{BASE_URL}/agents", headers=headers))

    print("\nFrontend:")
    results.append(check_endpoint("Frontend", FRONTEND_URL, expected_status=200))

    print("\nSecurity Headers Check:")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        headers_to_check = {
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff",
            "Strict-Transport-Security": "max-age=31536000",
            "Content-Security-Policy": "default-src 'self'",
        }
        for header, expected_value in headers_to_check.items():
            actual = response.headers.get(header, "")
            if expected_value in actual:
                print(f"  [PASS] {header}: {actual}")
                results.append(True)
            else:
                print(f"  [FAIL] {header}: expected '{expected_value}', got '{actual}'")
                results.append(False)
    except Exception as e:
        print(f"  [ERROR] Security headers check failed: {e}")
        results.extend([False] * len(headers_to_check))

    print("\nRate Limiter Check:")
    for i in range(5):
        check_endpoint(f"Rate Limit Request {i+1}", f"{BASE_URL}/health")
        time.sleep(0.1)

    print()
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} checks passed")
    if all(results):
        print("Overall: PASS — Smoke test successful")
        print("=" * 60)
        return 0
    else:
        print("Overall: FAIL — Smoke test failed")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
