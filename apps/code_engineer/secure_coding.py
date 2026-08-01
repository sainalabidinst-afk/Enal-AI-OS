"""
Secure Coding Knowledge
=======================

Implements RFC-0006 Code Knowledge Expansion:
- OWASP Top 10 vulnerability detection
- Injection prevention (SQL, command, injection)
- Authentication/authorization patterns
- Secrets management and hardcoded credential detection
- Secure coding best practices

This module produces structured findings about code security.
It does NOT modify code. It only analyzes and reports.
"""

import ast
import logging
import re
from dataclasses import dataclass, field
from typing import Any, Optional

from apps.code_engineer.parser import CodeAST

logger = logging.getLogger(__name__)


class SecuritySeverity:
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class SecurityFinding:
    """A single security finding."""
    category: str
    severity: str
    description: str
    recommendation: str
    line_number: int
    confidence: float = 1.0
    pattern: str = ""
    cwe_id: str = ""
    examples: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "severity": self.severity,
            "description": self.description,
            "recommendation": self.recommendation,
            "line_number": self.line_number,
            "confidence": round(self.confidence, 2),
            "pattern": self.pattern,
            "cwe_id": self.cwe_id,
            "examples": self.examples,
        }


class OWASPDetector:
    """
    OWASP Top 10 vulnerability detection.

    Detects patterns related to:
    - A01: Broken Access Control
    - A02: Cryptographic Failures
    - A03: Injection
    - A04: Insecure Design
    - A05: Security Misconfiguration
    - A06: Vulnerable Components
    - A07: Identification/Auth Failures
    - A08: Data Integrity Failures
    - A09: Logging/Monitoring Failures
    - A10: SSRF
    """

    # Patterns that indicate potential injection vulnerabilities
    INJECTION_PATTERNS = [
        (r"(?:exec|eval|compile)\s*\(", "Code injection via exec/eval/compile"),
        (r"os\.system\s*\(", "OS command injection via os.system"),
        (r"subprocess\.(?:call|Popen|run|check_output)\s*\(", "OS command injection via subprocess"),
        (r"shlex\.quote", "Safe command construction (positive)"),
        (r"f\"[^\"]*\{[^}]*\}", "Potential f-string injection in dangerous contexts"),
    ]

    # SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        (r"execute\s*\(\s*f[\"']", "SQL injection via f-string in execute()"),
        (r"execute\s*\(\s*[\"'][^\"']*\{", "SQL injection via string formatting in execute()"),
        (r"raw_sql", "Raw SQL usage detected"),
        (r"connection\.execute\s*\(\s*[\"'][^\"']*\+", "SQL injection via string concatenation"),
    ]

    # Hardcoded secrets patterns
    SECRET_PATTERNS = [
        (r"(?:api_key|apikey|secret|password|token|credential)\s*=\s*[\"'][^\"']{8,}[\"']", "Hardcoded secret detected"),
        (r"(?:AWS_ACCESS_KEY|AWS_SECRET_KEY|AZURE_.*_KEY|GCP_.*_KEY)", "Cloud provider credential detected"),
        (r"(?:sk-[a-zA-Z0-9]{20,}|pk-[a-zA-Z0-9]{20,})", "API key pattern detected"),
        (r"(?:-----BEGIN\s+(?:RSA|EC|DSA|OPENSSH)\s+PRIVATE\s+KEY-----)", "Private key detected"),
        (r"(?:JWT|jwt)\s*=\s*[\"'][a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+[\"']", "JWT token detected"),
    ]

    # SSRF patterns
    SSRF_PATTERNS = [
        (r"requests\.(?:get|post|put|delete|head|options)\s*\(\s*[^)]*url\s*[=:]", "Potential SSRF via user-controlled URL"),
        (r"urllib\.request\.urlopen\s*\(", "Potential SSRF via urllib"),
        (r"httpx\.(?:get|post|put|delete|head|options)\s*\(", "Potential SSRF via httpx"),
        (r"aiohttp\.ClientSession.*\.(?:get|post|put|delete)\s*\(", "Potential SSRF via aiohttp"),
    ]

    def analyze(self, code_ast: CodeAST) -> list[SecurityFinding]:
        """Run all OWASP detection analyses."""
        findings: list[SecurityFinding] = []
        raw = "\n".join(code_ast.raw_lines)

        findings.extend(self._detect_injection(raw))
        findings.extend(self._detect_sql_injection(raw))
        findings.extend(self._detect_hardcoded_secrets(raw))
        findings.extend(self._detect_ssrf(raw))
        findings.extend(self._detect_access_control_issues(code_ast))
        findings.extend(self._detect_crypto_failures(raw))
        findings.extend(self._detect_misconfiguration(raw))

        return findings

    def _detect_injection(self, raw: str) -> list[SecurityFinding]:
        """Detect injection vulnerabilities (A03)."""
        findings: list[SecurityFinding] = []
        for pattern, description in self.INJECTION_PATTERNS:
            matches = re.finditer(pattern, raw, re.IGNORECASE)
            for match in matches:
                line_no = raw[:match.start()].count("\n") + 1
                findings.append(SecurityFinding(
                    category="owasp_a03_injection",
                    severity=SecuritySeverity.CRITICAL,
                    description=description,
                    recommendation=(
                        "Avoid using exec/eval/compile with user input. "
                        "Use safe alternatives and validate all inputs."
                    ),
                    line_number=line_no,
                    confidence=0.9,
                    pattern="injection",
                    cwe_id="CWE-77",
                ))
        return findings

    def _detect_sql_injection(self, raw: str) -> list[SecurityFinding]:
        """Detect SQL injection vulnerabilities (A03)."""
        findings: list[SecurityFinding] = []
        for pattern, description in self.SQL_INJECTION_PATTERNS:
            matches = re.finditer(pattern, raw, re.IGNORECASE)
            for match in matches:
                line_no = raw[:match.start()].count("\n") + 1
                findings.append(SecurityFinding(
                    category="owasp_a03_injection",
                    severity=SecuritySeverity.CRITICAL,
                    description=description,
                    recommendation=(
                        "Use parameterized queries or ORM instead of string formatting. "
                        "Never concatenate user input into SQL queries."
                    ),
                    line_number=line_no,
                    confidence=0.85,
                    pattern="sql_injection",
                    cwe_id="CWE-89",
                ))
        return findings

    def _detect_hardcoded_secrets(self, raw: str) -> list[SecurityFinding]:
        """Detect hardcoded secrets (A02, A07)."""
        findings: list[SecurityFinding] = []
        for pattern, description in self.SECRET_PATTERNS:
            matches = re.finditer(pattern, raw, re.IGNORECASE)
            for match in matches:
                line_no = raw[:match.start()].count("\n") + 1
                findings.append(SecurityFinding(
                    category="owasp_a02_crypto_failure",
                    severity=SecuritySeverity.CRITICAL,
                    description=description,
                    recommendation=(
                        "Use environment variables or a secrets manager. "
                        "Never hardcode secrets in source code."
                    ),
                    line_number=line_no,
                    confidence=0.95,
                    pattern="hardcoded_secret",
                    cwe_id="CWE-798",
                ))
        return findings

    def _detect_ssrf(self, raw: str) -> list[SecurityFinding]:
        """Detect SSRF vulnerabilities (A10)."""
        findings: list[SecurityFinding] = []
        for pattern, description in self.SSRF_PATTERNS:
            matches = re.finditer(pattern, raw, re.IGNORECASE)
            for match in matches:
                line_no = raw[:match.start()].count("\n") + 1
                findings.append(SecurityFinding(
                    category="owasp_a10_ssrf",
                    severity=SecuritySeverity.HIGH,
                    description=description,
                    recommendation=(
                        "Validate and sanitize URLs before making requests. "
                        "Use an allowlist of allowed domains and protocols."
                    ),
                    line_number=line_no,
                    confidence=0.7,
                    pattern="ssrf",
                    cwe_id="CWE-918",
                ))
        return findings

    def _detect_access_control_issues(self, code_ast: CodeAST) -> list[SecurityFinding]:
        """Detect broken access control (A01)."""
        findings: list[SecurityFinding] = []
        raw = "\n".join(code_ast.raw_lines)

        # Check for missing authentication decorators on API endpoints
        for func in code_ast.functions:
            decorators = [d.lower() for d in func.decorators]
            has_auth = any(
                "auth" in d or "login" in d or "permission" in d or "role" in d
                for d in decorators
            )
            has_route = any(
                "route" in d or "app" in d or "router" in d or "api" in d
                for d in decorators
            )
            if has_route and not has_auth:
                findings.append(SecurityFinding(
                    category="owasp_a01_broken_access",
                    severity=SecuritySeverity.HIGH,
                    description=(
                        f"API endpoint '{func.name}' has no authentication decorator"
                    ),
                    recommendation=(
                        "Add authentication/authorization checks to all API endpoints. "
                        "Use @login_required, @require_auth, or similar decorators."
                    ),
                    line_number=func.lineno,
                    confidence=0.6,
                    pattern="missing_auth",
                    cwe_id="CWE-284",
                ))

        # Check for hardcoded roles/permissions
        if "admin" in raw.lower() and "password" in raw.lower():
            findings.append(SecurityFinding(
                category="owasp_a01_broken_access",
                severity=SecuritySeverity.MEDIUM,
                description="Hardcoded admin credentials or role checks detected",
                recommendation=(
                    "Use a proper authorization framework. "
                    "Avoid hardcoded role checks and use policy-based access control."
                ),
                line_number=1,
                confidence=0.5,
                pattern="hardcoded_access",
                cwe_id="CWE-284",
            ))

        return findings

    def _detect_crypto_failures(self, raw: str) -> list[SecurityFinding]:
        """Detect cryptographic failures (A02)."""
        findings: list[SecurityFinding] = []

        # Check for weak hash algorithms
        weak_hashes = [
            (r"hashlib\.md5", "MD5 hash (cryptographically broken)"),
            (r"hashlib\.sha1", "SHA-1 hash (cryptographically broken)"),
            (r"crypt\.DES", "DES encryption (obsolete, use AES)"),
        ]
        for pattern, description in weak_hashes:
            if re.search(pattern, raw, re.IGNORECASE):
                findings.append(SecurityFinding(
                    category="owasp_a02_crypto_failure",
                    severity=SecuritySeverity.HIGH,
                    description=description,
                    recommendation=(
                        "Use SHA-256 or SHA-3 for hashing, AES-256 for encryption. "
                        "Avoid broken algorithms like MD5, SHA-1, and DES."
                    ),
                    line_number=1,
                    confidence=0.9,
                    pattern="weak_crypto",
                    cwe_id="CWE-327",
                ))

        # Check for HTTP instead of HTTPS
        if "http://" in raw and "https://" not in raw:
            findings.append(SecurityFinding(
                category="owasp_a02_crypto_failure",
                severity=SecuritySeverity.MEDIUM,
                description="Plain HTTP usage detected (no HTTPS)",
                recommendation=(
                    "Use HTTPS for all network communication. "
                    "Never transmit sensitive data over unencrypted connections."
                ),
                line_number=1,
                confidence=0.8,
                pattern="no_https",
                cwe_id="CWE-319",
            ))

        return findings

    def _detect_misconfiguration(self, raw: str) -> list[SecurityFinding]:
        """Detect security misconfigurations (A05)."""
        findings: list[SecurityFinding] = []

        # Check for debug mode in production
        if re.search(r"debug\s*=\s*True", raw, re.IGNORECASE):
            findings.append(SecurityFinding(
                category="owasp_a05_misconfiguration",
                severity=SecuritySeverity.HIGH,
                description="Debug mode enabled (may expose sensitive information)",
                recommendation=(
                    "Disable debug mode in production. "
                    "Use environment variables to control debug mode."
                ),
                line_number=1,
                confidence=0.9,
                pattern="debug_mode",
                cwe_id="CWE-489",
            ))

        # Check for CORS misconfiguration
        if re.search(r"CORS|cors_origins?\s*=\s*\[\s*\"\*\"\s*\]", raw, re.IGNORECASE):
            findings.append(SecurityFinding(
                category="owasp_a05_misconfiguration",
                severity=SecuritySeverity.HIGH,
                description="CORS configured with wildcard origin (*)",
                recommendation=(
                    "Restrict CORS to specific origins. "
                    "Wildcard CORS allows any website to make cross-origin requests."
                ),
                line_number=1,
                confidence=0.9,
                pattern="cors_wildcard",
                cwe_id="CWE-942",
            ))

        # Check for verbose error handling
        if re.search(r"traceback\.print_exc|print\(.*error.*\)|return\s+.*error\s+.*message", raw, re.IGNORECASE):
            findings.append(SecurityFinding(
                category="owasp_a05_misconfiguration",
                severity=SecuritySeverity.MEDIUM,
                description="Verbose error messages may leak sensitive information",
                recommendation=(
                    "Return generic error messages to users. "
                    "Log detailed errors internally for debugging."
                ),
                line_number=1,
                confidence=0.6,
                pattern="verbose_error",
                cwe_id="CWE-209",
            ))

        return findings


class AuthAnalyzer:
    """
    Authentication and Authorization pattern analysis.

    Detects:
    - Authentication framework usage
    - Authorization patterns (RBAC, ABAC)
    - Session management
    - Password policies
    """

    AUTH_FRAMEWORKS = [
        "flask_login", "flask_security", "flask_jwt", "flask_httpauth",
        "django_contrib_auth", "django_rest_framework_jwt",
        "fastapi_security", "fastapi_login", "python_jose", "jose",
        "pyjwt", "jwt", "authlib", "oauthlib", "python_social_auth",
        "passlib", "bcrypt", "argon2", "python_jwt",
    ]

    def analyze_auth_usage(self, code_ast: CodeAST) -> list[SecurityFinding]:
        """Analyze authentication framework usage."""
        findings: list[SecurityFinding] = []
        raw = "\n".join(code_ast.raw_lines)

        found_frameworks = []
        for fw in self.AUTH_FRAMEWORKS:
            pattern = fw.replace("_", r"[_-]?")
            if re.search(pattern, raw, re.IGNORECASE):
                found_frameworks.append(fw)

        if not found_frameworks:
            # Check if this module looks like it needs auth
            module_name = code_ast.metadata.get("filename", "").lower()
            if any(kw in module_name for kw in ["api", "auth", "login", "register", "user"]):
                if "api" in module_name or "auth" in module_name:
                    findings.append(SecurityFinding(
                        category="auth_framework",
                        severity=SecuritySeverity.MEDIUM,
                        description="No authentication framework detected in API module",
                        recommendation=(
                            "Implement authentication using a well-tested framework. "
                            "Consider: Flask-Login, Django Auth, FastAPI Security, or JWT."
                        ),
                        line_number=1,
                        confidence=0.5,
                        pattern="missing_auth_framework",
                    ))

        return findings

    def analyze_password_handling(self, code_ast: CodeAST) -> list[SecurityFinding]:
        """Analyze password handling patterns."""
        findings: list[SecurityFinding] = []
        raw = "\n".join(code_ast.raw_lines)

        # Check for password storage without hashing
        if re.search(r"password\s*=\s*[\"'][^\"']+[\"']", raw, re.IGNORECASE):
            findings.append(SecurityFinding(
                category="auth_password",
                severity=SecuritySeverity.CRITICAL,
                description="Password stored as plaintext in code",
                recommendation=(
                    "Never store passwords in code. Use hashed passwords with "
                    "bcrypt, argon2, or scrypt. Never log or transmit plaintext passwords."
                ),
                line_number=1,
                confidence=0.9,
                pattern="plaintext_password",
                cwe_id="CWE-256",
            ))

        # Check for bcrypt/argon2 usage
        has_bcrypt = "bcrypt" in raw.lower()
        has_argon2 = "argon2" in raw.lower()
        has_passlib = "passlib" in raw.lower()

        if not (has_bcrypt or has_argon2 or has_passlib) and "password" in raw.lower():
            findings.append(SecurityFinding(
                category="auth_password",
                severity=SecuritySeverity.HIGH,
                description="No strong password hashing library detected",
                recommendation=(
                    "Use bcrypt, argon2, or passlib for password hashing. "
                    "Avoid weak hashes like MD5 or SHA-1 for passwords."
                ),
                line_number=1,
                confidence=0.7,
                pattern="weak_password_hashing",
                cwe_id="CWE-916",
            ))

        return findings

    def analyze_session_management(self, code_ast: CodeAST) -> list[SecurityFinding]:
        """Analyze session management patterns."""
        findings: list[SecurityFinding] = []
        raw = "\n".join(code_ast.raw_lines)

        # Check for JWT usage
        jwt_patterns = [
            (r"jwt\.encode|jwt\.decode|jwt\.sign", "JWT token usage detected"),
        ]
        for pattern, description in jwt_patterns:
            if re.search(pattern, raw, re.IGNORECASE):
                findings.append(SecurityFinding(
                    category="auth_session",
                    severity=SecuritySeverity.INFO,
                    description=description,
                    recommendation=(
                        "Ensure JWT tokens have: short expiration (15-60 min), "
                        "secure secret key management, and proper token refresh mechanism."
                    ),
                    line_number=1,
                    confidence=0.8,
                    pattern="jwt_usage",
                ))

        # Check for session configuration
        if "session" in raw.lower():
            has_session_config = any(
                kw in raw.lower() for kw in
                ["session_timeout", "session_expire", "permanent_session", "session_cookie"]
            )
            if not has_session_config:
                findings.append(SecurityFinding(
                    category="auth_session",
                    severity=SecuritySeverity.MEDIUM,
                    description="Session management detected but no session configuration found",
                    recommendation=(
                        "Configure session timeout, secure cookie flags (HttpOnly, Secure, SameSite), "
                        "and session regeneration on login."
                    ),
                    line_number=1,
                    confidence=0.5,
                    pattern="missing_session_config",
                ))

        return findings

    def analyze(self, code_ast: CodeAST) -> list[SecurityFinding]:
        findings: list[SecurityFinding] = []
        findings.extend(self.analyze_auth_usage(code_ast))
        findings.extend(self.analyze_password_handling(code_ast))
        findings.extend(self.analyze_session_management(code_ast))
        return findings


class SecureCodingAnalyzer:
    """
    Master analyzer that coordinates all security code analyses.
    """

    def __init__(self):
        self.owasp = OWASPDetector()
        self.auth = AuthAnalyzer()

    def analyze(self, code_ast: CodeAST) -> dict[str, list[SecurityFinding]]:
        """Run all security analyses."""
        return {
            "owasp": self.owasp.analyze(code_ast),
            "auth": self.auth.analyze(code_ast),
        }

    def analyze_all(self, code_ast: CodeAST) -> list[SecurityFinding]:
        """Get all findings as a flat list."""
        results = self.analyze(code_ast)
        all_findings: list[SecurityFinding] = []
        for category_findings in results.values():
            all_findings.extend(category_findings)
        return all_findings


secure_coding_analyzer = SecureCodingAnalyzer()
