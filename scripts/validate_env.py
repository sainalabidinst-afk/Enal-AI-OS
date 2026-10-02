#!/usr/bin/env python3
"""
Environment Validation Script
==============================
Validates a .env file for production deployment of Enal Cognitive Platform.

Checks for:
  - All required variables present
  - No empty required values
  - SECRET_KEY meets minimum length (32 chars)
  - At least one LLM provider configured
  - No hardcoded/placeholder secrets

Usage:
  python scripts/validate_env.py .env.production
  python scripts/validate_env.py .env.production --strict
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


REQUIRED_VARS = {
    "POSTGRES_PASSWORD": "Database password must be set",
    "SECRET_KEY": "Application secret key must be set (32+ chars)",
    "MINIO_ROOT_USER": "MinIO root user must be set",
    "MINIO_ROOT_PASSWORD": "MinIO root password must be set",
}

REQUIRED_LLM_KEYS = {
    "OPENAI_API_KEY": "OpenAI provider",
    "ANTHROPIC_API_KEY": "Anthropic provider",
    "GEMINI_API_KEY": "Google Gemini provider",
    "GOOGLE_API_KEY": "Google provider",
}

PLACEHOLDER_PATTERNS = [
    (r"dev-secret|change.*me|placeholder|your-", "placeholder secret value"),
    (r"^$", "empty value"),
]


def parse_env_file(filepath: str) -> dict[str, str]:
    """Parse a .env file into a dict."""
    env_vars: dict[str, str] = {}
    path = Path(filepath)
    if not path.exists():
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            env_vars[key.strip()] = value.strip()

    return env_vars


def validate_env(filepath: str, strict: bool = False) -> bool:
    """Validate environment file for production readiness."""
    env_vars = parse_env_file(filepath)
    errors: list[str] = []
    warnings: list[str] = []

    print(f"Validating: {filepath}")
    print(f"Total variables found: {len(env_vars)}")
    print("-" * 60)

    # Check required vars
    for var, msg in REQUIRED_VARS.items():
        value = env_vars.get(var, "")
        if not value:
            errors.append(f"[REQUIRED] {var}: {msg}")
        else:
            for pattern, desc in PLACEHOLDER_PATTERNS:
                if re.search(pattern, value, re.IGNORECASE):
                    errors.append(f"[REQUIRED] {var}: contains {desc} — '{value[:20]}...'")
                    break

    # Check SECRET_KEY length
    secret = env_vars.get("SECRET_KEY", "")
    if secret and len(secret) < 32:
        errors.append(f"[VALIDATION] SECRET_KEY is {len(secret)} chars; minimum 32 required")

    # Check at least one LLM provider
    llm_providers = []
    for var, provider_name in REQUIRED_LLM_KEYS.items():
        value = env_vars.get(var, "")
        if value:
            for pattern, desc in PLACEHOLDER_PATTERNS:
                if re.search(pattern, value, re.IGNORECASE):
                    warnings.append(f"[LLM] {var}: contains {desc}")
                    break
            else:
                llm_providers.append(f"{var} ({provider_name})")

    if not llm_providers:
        if strict:
            errors.append("No LLM provider API key configured. At least one required for production.")
        else:
            warnings.append("No LLM provider API key configured. Runtime benchmarks will be BLOCKED.")

    # Check TESTING flag should be false in production
    testing = env_vars.get("TESTING", "")
    if testing.lower() == "true":
        if strict:
            errors.append("TESTING=true — should be false for production")
        else:
            warnings.append(f"TESTING={testing} — should be 'false' for production")

    # Check DEBUG flag
    debug = env_vars.get("DEBUG", "")
    if debug.lower() == "true":
        warnings.append("DEBUG=true — should be false for production")

    # Print results
    for var, msg in REQUIRED_VARS.items():
        value = env_vars.get(var, "")
        status = "OK" if value and not any(
            re.search(p, value, re.IGNORECASE) for p, _ in PLACEHOLDER_PATTERNS
        ) else "MISSING" if not value else "INVALID"
        print(f"  {var:25s} [{status}]")

    print()
    print("LLM Provider Configuration:")
    if llm_providers:
        for p in llm_providers:
            print(f"  {p:25s} [OK]")
    else:
        print(f"  {'No provider':25s} [MISSING]")

    print()
    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f"  ⚠ {w}")
    if errors:
        print("Errors:")
        for e in errors:
            print(f"  ✗ {e}")

    print("-" * 60)
    if errors:
        print(f"RESULT: FAIL — {len(errors)} error(s), {len(warnings)} warning(s)")
        return False
    elif warnings:
        print(f"RESULT: PASS WITH WARNINGS — {len(warnings)} warning(s)")
        return True
    else:
        print("RESULT: PASS — All validations passed")
        return True


def main():
    parser = argparse.ArgumentParser(description="Validate .env file for ECP production deployment")
    parser.add_argument("env_file", help="Path to .env file to validate")
    parser.add_argument("--strict", action="store_true", help="Exit with error on warnings")
    args = parser.parse_args()

    success = validate_env(args.env_file, strict=args.strict)
    if not success or (args.strict and parser.error):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
