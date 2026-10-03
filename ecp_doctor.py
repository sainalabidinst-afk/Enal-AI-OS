#!/usr/bin/env python3
"""
ECP Doctor — One-Command Development Health Check
==================================================

Runs lint, typecheck, tests, governance checks, and benchmarks in sequence.
Inspired by the developer_onboarding.md guide.

Usage:
    ecp doctor                         # Run all checks
    ecp doctor --lint --typecheck      # Run specific checks
    ecp doctor --fast                  # Skip slow checks (benchmarks)
    ecp doctor --fix                   # Apply auto-fixes before checking
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


@dataclass
class CheckResult:
    name: str
    passed: bool
    duration_ms: float
    output: str = ""


@dataclass
class DoctorReport:
    results: list[CheckResult] = field(default_factory=list)
    all_passed: bool = True

    def add(self, result: CheckResult) -> None:
        self.results.append(result)
        if not result.passed:
            self.all_passed = False


def run_command(cmd: list[str], cwd: Path = PROJECT_ROOT, timeout: int = 120) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = proc.stdout + proc.stderr
        return proc.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, f"Command timed out after {timeout}s"
    except FileNotFoundError as e:
        return False, str(e)


def check_ruff(fix: bool = False) -> CheckResult:
    check_dirs = [
        str(PROJECT_ROOT / "apps"),
        str(PROJECT_ROOT / "backend" / "app"),
        str(PROJECT_ROOT / "benchmarks"),
    ]
    ts_dir = str(PROJECT_ROOT / "tests")
    if Path(ts_dir).exists():
        check_dirs.append(ts_dir)
    cmd = ["ruff", "check"]
    if fix:
        cmd = ["ruff", "check", "--fix"]
    start = time.perf_counter()
    passed, output = run_command(cmd + check_dirs)
    duration = (time.perf_counter() - start) * 1000
    return CheckResult("Ruff (lint)", passed, duration, output)


def check_black() -> CheckResult:
    check_dirs = [
        str(PROJECT_ROOT / "apps"),
        str(PROJECT_ROOT / "backend" / "app"),
        str(PROJECT_ROOT / "benchmarks"),
    ]
    ts_dir = str(PROJECT_ROOT / "tests")
    if Path(ts_dir).exists():
        check_dirs.append(ts_dir)
    cmd = ["black", "--check"] + check_dirs
    start = time.perf_counter()
    passed, output = run_command(cmd)
    duration = (time.perf_counter() - start) * 1000
    return CheckResult("Black (format)", passed, duration, output)


def check_mypy() -> CheckResult:
    cmd = [
        "python",
        "-m",
        "mypy",
        str(PROJECT_ROOT / "apps"),
        str(PROJECT_ROOT / "backend" / "app" / "core"),
        "--ignore-missing-imports",
        "--explicit-package-bases",
    ]
    start = time.perf_counter()
    passed, output = run_command(cmd)
    duration = (time.perf_counter() - start) * 1000
    return CheckResult("MyPy (type check)", passed, duration, output)


def check_pytest() -> CheckResult:
    test_dirs = []
    for d in ["tests", "backend/tests"]:
        p = PROJECT_ROOT / d
        if p.exists():
            test_dirs.append(str(p))
    if not test_dirs:
        return CheckResult("Pytest (unit tests)", True, 0, "No test directories found")
    cmd = ["python", "-m", "pytest", "-x", "-q"] + test_dirs
    start = time.perf_counter()
    passed, output = run_command(cmd, timeout=300)
    duration = (time.perf_counter() - start) * 1000
    return CheckResult("Pytest (unit tests)", passed, duration, output)


def check_governance() -> CheckResult:
    cmd = ["python", str(PROJECT_ROOT / "benchmarks" / "governance_checks.py")]
    start = time.perf_counter()
    passed, output = run_command(cmd, cwd=PROJECT_ROOT)
    duration = (time.perf_counter() - start) * 1000
    return CheckResult("Governance Checks", passed, duration, output)


def check_boundaries() -> CheckResult:
    cmd = ["python", str(PROJECT_ROOT / "benchmarks" / "package_boundaries.py")]
    start = time.perf_counter()
    passed, output = run_command(cmd, cwd=PROJECT_ROOT)
    duration = (time.perf_counter() - start) * 1000
    return CheckResult("Package Boundaries", passed, duration, output)


def check_benchmarks(fast: bool = False) -> CheckResult:
    if fast:
        return CheckResult("Benchmarks", True, 0, "Skipped (--fast mode)")
    benchmarks = [
        str(PROJECT_ROOT / "benchmarks" / "voice_interaction_benchmark.py"),
        str(PROJECT_ROOT / "benchmarks" / "translator_expert_benchmark.py"),
    ]
    all_output = ""
    all_passed = True
    start = time.perf_counter()
    for bench in benchmarks:
        bench_path = Path(bench)
        if bench_path.exists():
            passed, output = run_command(["python", bench])
            all_output += output
            if not passed:
                all_passed = False
    duration = (time.perf_counter() - start) * 1000
    return CheckResult("Benchmarks", all_passed, duration, all_output)


def check_ts() -> CheckResult:
    cmd = ["npx", "tsc", "--noEmit", "--skipLibCheck"]
    start = time.perf_counter()
    passed, output = run_command(cmd, cwd=PROJECT_ROOT / "frontend")
    duration = (time.perf_counter() - start) * 1000
    return CheckResult("TypeScript", passed, duration, output)


def print_result(result: CheckResult) -> None:
    status = f"{GREEN}PASS{RESET}" if result.passed else f"{RED}FAIL{RESET}"
    print(f"  {status} {result.name:30s} {result.duration_ms:8.1f}ms")
    if not result.passed and result.output:
        lines = result.output.strip().split("\n")[-5:]
        for line in lines:
            print(f"       {line.strip()}")


def main() -> int:
    parser = argparse.ArgumentParser(description="ECP Doctor — Development health check")
    parser.add_argument("--lint", action="store_true", help="Run lint checks only")
    parser.add_argument("--typecheck", action="store_true", help="Run type checks only")
    parser.add_argument("--test", action="store_true", help="Run tests only")
    parser.add_argument("--gov", action="store_true", help="Run governance checks only")
    parser.add_argument("--benchmark", action="store_true", help="Run benchmarks only")
    parser.add_argument("--fix", action="store_true", help="Apply auto-fixes")
    parser.add_argument("--fast", action="store_true", help="Skip benchmarks")
    args = parser.parse_args()

    run_all = not any([args.lint, args.typecheck, args.test, args.gov, args.benchmark])

    if args.fix:
        print("Applying auto-fixes...")
        run_command(["ruff", "check", "--fix", "apps/", "backend/app/", "benchmarks/", "tests/"])

    print(f"\n{BOLD}ECP Doctor — Health Check{RESET}\n")

    report = DoctorReport()

    checks: list[tuple[bool, Callable[[], CheckResult]]] = [
        (run_all or args.lint, lambda: check_ruff(args.fix)),
        (run_all or args.lint, check_black),
        (run_all or args.typecheck, check_mypy),
        (run_all or args.test and not args.fast, lambda: check_pytest()),
        (run_all or args.gov, check_governance),
        (run_all or args.gov, check_boundaries),
        (run_all or args.benchmark, lambda: check_benchmarks(args.fast)),
    ]

    ts_check = run_all
    if ts_check:
        report.add(check_ts())

    for should_run, check_fn in checks:
        if should_run:
            result = check_fn()
            report.add(result)
            print_result(result)

    if not report.all_passed:
        print(f"\n{RED}{BOLD}Some checks failed!{RESET}\n")
        return 1
    else:
        print(f"\n{GREEN}{BOLD}All checks passed!{RESET}\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())
