"""
Security Engineer — Secret Detector.

Detects hardcoded secrets, API keys, passwords, tokens, and certificates
in source code, configuration files, environment files, and CI/CD pipelines.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any

from apps.security_engineer.schemas import SecretFinding, SecretType, Severity

logger = logging.getLogger(__name__)


# High-entropy string patterns (potential API keys/tokens).
_HEX_PATTERNS = [
    (r'["\'][a-f0-9]{32}["\']', "32-char hex string (possible API key)"),
    (r'["\'][a-f0-9]{40}["\']', "40-char hex string (possible GitHub token)"),
    (r'["\'][a-f0-9]{64}["\']', "64-char hex string (possible private key)"),
    (r'["\'][a-f0-9]{128}["\']', "128-char hex string (possible RSA key)"),
]

# Base64 patterns.
_BASE64_PATTERNS = [
    (r'["\'][A-Za-z0-9+/]{40,}={0,2}["\']', "Long base64 string (possible token/key)"),
    (r'["\'][A-Za-z0-9_-]{20,}["\']', "Long URL-safe base64 string (possible JWT)"),
]

# Explicit secret assignment patterns.
_SECRET_ASSIGNMENT_PATTERNS = [
    # API keys
    (r'(?i)(api[_-]?key\s*=\s*["\'])([^"\']{8,})(["\'])', "api_key", SecretType.api_key, Severity.critical),
    (r'(?i)(apikey\s*=\s*["\'])([^"\']{8,})(["\'])', "apikey", SecretType.api_key, Severity.critical),
    (r'(?i)(secret[_-]?key\s*=\s*["\'])([^"\']{8,})(["\'])', "secret_key", SecretType.api_key, Severity.critical),
    (r'(?i)(access[_-]?key\s*=\s*["\'])([^"\']{8,})(["\'])', "access_key", SecretType.api_key, Severity.critical),
    (r'(?i)(bearer\s+)([A-Za-z0-9._-]{20,})', "Bearer token", SecretType.token, Severity.critical),

    # AWS credentials
    (r'(?i)(aws[_-]?access[_-]?key[_-]?id\s*=\s*["\'])([A-Z0-9]{20})(["\'])', "AWS access key ID", SecretType.api_key, Severity.critical),
    (r'(?i)(aws[_-]?secret[_-]?access[_-]?key\s*=\s*["\'])([^"\']{40})(["\'])', "AWS secret access key", SecretType.api_key, Severity.critical),
    (r'AKIA[0-9A-Z]{16}', "AWS access key ID pattern", SecretType.api_key, Severity.critical),

    # GitHub tokens
    (r'ghp_[A-Za-z0-9]{36}', "GitHub personal access token", SecretType.token, Severity.critical),
    (r'gho_[A-Za-z0-9]{36}', "GitHub OAuth token", SecretType.token, Severity.critical),
    (r'github_pat_[A-Za-z0-9_]{22,}', "GitHub fine-grained PAT", SecretType.token, Severity.critical),

    # Private keys
    (r'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----', "Private key block", SecretType.private_key, Severity.critical),
    (r'-----BEGIN CERTIFICATE-----', "Certificate block", SecretType.certificate, Severity.high),

    # Passwords
    (r'(?i)(password\s*=\s*["\'])([^"\']{4,})(["\'])', "password", SecretType.password, Severity.high),
    (r'(?i)(passwd\s*=\s*["\'])([^"\']{4,})(["\'])', "passwd", SecretType.password, Severity.high),
    (r'(?i)(pwd\s*=\s*["\'])([^"\']{4,})(["\'])', "pwd", SecretType.password, Severity.high),
    (r'(?i)(password|passwd|pwd)["\']\s*:\s*["\']([^"\']{4,})["\']', "password_in_dict", SecretType.password, Severity.high),

    # Database passwords
    (r'\bpostgres://[^:]+:([^@]+)@', "PostgreSQL connection string with password", SecretType.password, Severity.high),
    (r'\bmongodb(\+srv)?://[^:]+:([^@]+)@', "MongoDB connection string with password", SecretType.password, Severity.high),

    # Generic token patterns
    (r'(?i)(token\s*=\s*["\'])([^"\']{20,})(["\'])', "token", SecretType.token, Severity.high),
    (r'(?i)(auth[_-]?token\s*=\s*["\'])([^"\']{20,})(["\'])', "auth_token", SecretType.token, Severity.high),

    # Slack tokens
    (r'xox[baprs]-[A-Za-z0-9-]+', "Slack API token", SecretType.token, Severity.critical),

    # Generic cloud credentials
    (r'(?i)(gcp[_-]?service[_-]?account[_-]?key)', "GCP service account key", SecretType.api_key, Severity.critical),
    (r'(?i)(client[_-]?secret\s*=\s*["\'])([^"\']{8,})(["\'])', "client_secret", SecretType.api_key, Severity.high),
]

# False positive filter patterns — things that look like secrets but aren't.
_FALSE_POSITIVE_FILTERS = [
    r'["\']\s*(none|null|true|false|yes|no|placeholder|example|your[_-]?key[_-]?here|xxx+)["\']',
    r'["\']<[^>]+>["\']',  # template placeholders
    r'["\']\s*\$\{.*\}["\']',  # environment variable references
    r'["\']\s*\{\{.*\}\}["\']',  # template variables
    r'["\']test["\']',
    r'["\']dummy["\']',
    r'["\']fake["\']',
]


@dataclass
class DetectionResult:
    """Result of a secret detection sweep."""
    findings: list[SecretFinding]
    raw_matches: list[tuple[str, str, str]]


class SecretDetector:
    """
    Detects hardcoded secrets and credentials in source code.

    Usage::

        detector = SecretDetector()
        findings = detector.scan(source_code, file_path="config.py")
    """

    MIN_SECRET_LENGTH = 8
    MAX_SECRET_DISPLAY_LENGTH = 4  # Only show first/last chars for safety

    def scan(
        self,
        source_code: str,
        file_path: str = "<unknown>",
        env_vars: dict[str, str] | None = None,
    ) -> list[SecretFinding]:
        """
        Scan source code for hardcoded secrets.

        Args:
            source_code: Source code or config file content.
            file_path: Path for evidence reporting.
            env_vars: Environment variables to check for insecure defaults.

        Returns:
            List of SecretFinding objects.
        """
        findings: list[SecretFinding] = []
        seen: set[str] = set()

        # Check explicit assignment patterns.
        for pattern, label, secret_type, severity in _SECRET_ASSIGNMENT_PATTERNS:
            for match in re.finditer(pattern, source_code, re.IGNORECASE):
                # Extract the secret value (group 2 if present, else full match).
                last_index = match.lastindex or 0
                if last_index >= 2:
                    secret_value = match.group(2)
                else:
                    secret_value = match.group(1) if last_index >= 1 else match.group(0)

                # Filter false positives.
                if self._is_false_positive(secret_value, match.group(0)):
                    continue

                # Filter weak/placeholder values.
                if self._is_placeholder(secret_value):
                    continue

                line_num = source_code[:match.start()].count("\n") + 1
                key = f"{file_path}:{line_num}:{label}"
                if key in seen:
                    continue
                seen.add(key)

                redacted = self._redact(secret_value)

                findings.append(SecretFinding(
                    type=secret_type,
                    location=f"{file_path}:{line_num}",
                    severity=severity,
                    remediation=self._get_rotation_guidance(secret_type, label),
                    confidence=0.9,
                    id=f"secret-{line_num}-{label}",
                    evidence={
                        "type": label,
                        "redacted_value": redacted,
                        "line": line_num,
                        "file": file_path,
                    },
                ))

        # Check high-entropy hex strings.
        for pattern, description in _HEX_PATTERNS:
            for match in re.finditer(pattern, source_code):
                line_num = source_code[:match.start()].count("\n") + 1
                value = match.group(0).strip("\"'")

                if self._is_false_positive(value, match.group(0)):
                    continue
                if self._is_placeholder(value):
                    continue

                key = f"{file_path}:{line_num}:hex"
                if key in seen:
                    continue
                seen.add(key)

                findings.append(SecretFinding(
                    type=SecretType.other,
                    location=f"{file_path}:{line_num}",
                    severity=Severity.high,
                    remediation="If this is a secret, rotate it immediately and move to a secure vault.",
                    confidence=0.7,
                    evidence={
                        "description": description,
                        "redacted_value": self._redact(value),
                        "entropy_score": self._estimate_entropy(value),
                    },
                ))

        # Check base64 patterns.
        for pattern, description in _BASE64_PATTERNS:
            for match in re.finditer(pattern, source_code):
                line_num = source_code[:match.start()].count("\n") + 1
                value = match.group(0).strip("\"'")

                if self._is_false_positive(value, match.group(0)):
                    continue
                if self._is_placeholder(value):
                    continue

                key = f"{file_path}:{line_num}:base64"
                if key in seen:
                    continue
                seen.add(key)

                findings.append(SecretFinding(
                    type=SecretType.token,
                    location=f"{file_path}:{line_num}",
                    severity=Severity.high,
                    remediation="If this is a credential, rotate and store in a secrets manager.",
                    confidence=0.65,
                    evidence={
                        "description": description,
                        "redacted_value": self._redact(value),
                        "entropy_score": self._estimate_entropy(value),
                    },
                ))

        # Check environment variables for insecure defaults.
        if env_vars:
            for key, value in env_vars.items():
                if self._looks_like_secret_name(key) and not self._is_placeholder(value):
                    findings.append(SecretFinding(
                        type=SecretType.api_key,
                        location=f"env:{key}",
                        severity=Severity.high,
                        remediation="Move environment variable to a secrets manager.",
                        confidence=0.8,
                        evidence={"env_key": key, "has_value": bool(value)},
                    ))

        return findings

    def _is_false_positive(self, value: str, full_match: str) -> bool:
        """Check if a matched value is a known false positive."""
        for fp_pattern in _FALSE_POSITIVE_FILTERS:
            if re.search(fp_pattern, full_match, re.IGNORECASE):
                return True
        return False

    def _is_placeholder(self, value: str) -> bool:
        """Check if a value is a placeholder or template."""
        lowered = value.lower().strip().strip("\"'")
        placeholders = {
            "none", "null", "true", "false", "yes", "no",
            "placeholder", "example", "test", "dummy", "fake",
            "xxx", "xxxx", "your_key_here", "your_key",
            "<key>", "<secret>", "<password>", "<token>",
            "changeme", "change_me", "your-secret-here",
        }
        if lowered in placeholders:
            return True
        if lowered.startswith("<") and lowered.endswith(">"):
            return True
        if "{}" in lowered or "${" in lowered:
            return True
        # Very short values are unlikely to be real secrets.
        if len(lowered) < self.MIN_SECRET_LENGTH:
            return True
        # Common variable names assigned to themselves.
        if lowered == value.strip("\"'"):
            return False
        return False

    def _looks_like_secret_name(self, key: str) -> bool:
        """Check if an environment variable name suggests it holds a secret."""
        lowered = key.lower()
        return any(kw in lowered for kw in (
            "key", "secret", "token", "password", "pwd", "credential", "auth",
        ))

    def _redact(self, value: str) -> str:
        """Redact a secret value for safe display."""
        cleaned = value.strip("\"'")
        if len(cleaned) <= self.MAX_SECRET_DISPLAY_LENGTH * 2:
            return "*" * len(cleaned)
        show = self.MAX_SECRET_DISPLAY_LENGTH
        return f"{cleaned[:show]}...{cleaned[-show:]}"

    def _estimate_entropy(self, value: str) -> float:
        """Estimate Shannon entropy of a string (0-1)."""
        import math
        from collections import Counter

        cleaned = value.strip("\"'")
        if not cleaned:
            return 0.0

        counts = Counter(cleaned)
        total = len(cleaned)
        entropy = -sum((c / total) * math.log2(c / total) for c in counts.values())
        # Normalize to 0-1 (max entropy for printable ASCII is ~6.5 bits)
        return round(min(1.0, entropy / 6.5), 4)

    def _get_rotation_guidance(self, secret_type: SecretType, label: str) -> str:
        """Get rotation guidance for a specific secret type."""
        guidance = {
            SecretType.api_key: "Rotate the API key in your provider's console and store the new key in a secrets manager (e.g., HashiCorp Vault, AWS Secrets Manager).",
            SecretType.password: "Change the password immediately and enforce a strong password policy. Use a password manager for storage.",
            SecretType.token: "Revoke the current token and generate a new one. Implement token rotation policies.",
            SecretType.private_key: "Revoke the compromised key pair and generate a new one. Audit access logs for unauthorized use.",
            SecretType.certificate: "Reissue the certificate and revoke the old one. Review certificate transparency logs.",
            SecretType.other: "Rotate this credential and store it securely.",
        }
        return guidance.get(secret_type, "Rotate this credential and store it securely.")
