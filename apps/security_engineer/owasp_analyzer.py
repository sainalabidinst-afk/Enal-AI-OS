"""
Security Engineer — OWASP Top 10 Analyzer.

Detects OWASP Top 10 (2021) vulnerability categories in source code:
1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable and Outdated Components
7. Identification and Authentication Failures
8. Software and Data Integrity Failures
9. Security Logging and Monitoring Failures
10. Server-Side Request Forgery (SSRF)

Focuses on: SQL Injection, XSS, Command Injection, SSRF, CSRF,
broken authentication, and insecure deserialization.
"""

from __future__ import annotations

import ast
import logging
import re
from typing import Any

from apps.security_engineer.schemas import Finding, Severity

logger = logging.getLogger(__name__)


# SQL injection patterns — string formatting/concatenation with SQL keywords.
_SQL_INJECTION_PATTERNS = [
    (r'(SELECT|INSERT|UPDATE|DELETE|DROP|UNION)\s+.*\+\s*["\'].*["\']', "string concatenation in SQL"),
    (r'(SELECT|INSERT|UPDATE|DELETE|DROP|UNION)\s+.*\+\s*\w', "string concatenation with variable in SQL"),
    (r'(SELECT|INSERT|UPDATE|DELETE|DROP|UNION)\s+.*%s.*%', "format string in SQL"),
    (r'execute\s*\(\s*["\'].*\{.*\}.*["\']', "f-string in SQL execute"),
    (r'execute\s*\(\s*["\'].*%s.*["\']', "%s formatting in SQL execute"),
    (r'f["\'].*(SELECT|INSERT|UPDATE|DELETE|DROP|UNION).*\{.*\}.*["\']', "f-string SQL query"),
    (r'\+\s*["\'<]\s*(SELECT|INSERT|UPDATE|DELETE|DROP|UNION)', "string concatenation with SQL keyword"),
    (r'(SELECT|INSERT|UPDATE|DELETE|DROP|UNION)\s+.*"[^"]*"\s*\+\s*', "string + variable in SQL context"),
]

# XSS patterns — unescaped output, innerHTML assignment.
_XSS_PATTERNS = [
    (r'\.innerHTML\s*=', "innerHTML assignment (potential XSS)"),
    (r'document\.write\s*\(', "document.write (potential XSS)"),
    (r'v-html\s*=', "v-html directive (Vue XSS)"),
    (r'\{\{.*\}\}\s*$', "unescaped template output"),
    (r'dangerouslySetInnerHTML', "dangerouslySetInnerHTML (React XSS)"),
]

# Command injection patterns.
_CMD_INJECTION_PATTERNS = [
    (r'os\.system\s*\(', "os.system call (command injection)"),
    (r'subprocess\.(call|Popen|run)\s*\(.*shell\s*=\s*True', "subprocess with shell=True"),
    (r'subprocess\.(call|Popen|run)\s*\(.*\+.*\)', "subprocess with string concatenation"),
    (r'os\.popen\s*\(', "os.popen call"),
    (r'eval\s*\(', "eval call (code injection)"),
    (r'exec\s*\(', "exec call (code injection)"),
]

# SSRF patterns.
_SSRF_PATTERNS = [
    (r'requests\.(get|post|put|delete)\s*\(.*\+', "unsanitized URL in HTTP request"),
    (r'urllib\.request\.urlopen\s*\(.*\+', "unsanitized URL in urlopen"),
    (r'fetch\s*\(.*\+', "unsanitized URL in fetch"),
    (r'requests\.(get|post|put|delete)\s*\(\s*\w+\s*\)', "unsanitized URL in HTTP request"),
    (r'urllib\.request\.urlopen\s*\(\s*\w+\s*\)', "unsanitized URL in urlopen"),
    (r'requests\.post\s*\(\s*["\']https?://', "unsanitized URL in HTTP POST request"),
    (r'urllib\.request\.urlretrieve\s*\(', "unsanitized URL in urlretrieve"),
    (r'requests\.(get|post|put|delete)\s*\(\s*["\']http', "unsanitized URL in HTTP request"),
]

# CSRF patterns — missing CSRF token.
_CSRF_PATTERNS = [
    (r'@app\.(get|post|put|delete)\s*\(.*methods\s*=\s*\[.*POST', "POST route without CSRF protection"),
    (r'\.post\s*\(.*method:', "AJAX POST without CSRF token"),
]

# Insecure deserialization patterns (A08:2021).
_DESERIALIZATION_PATTERNS = [
    (r'(?i)\bpickle\.loads?\b', "pickle deserialization (arbitrary code execution)"),
    (r'(?i)\bmarshal\.loads?\b', "marshal deserialization (unsafe)"),
    (r'(?i)\byaml\.load\s*\(\s*$', "yaml.load without safe_load"),
    (r'(?i)\bcPickle\.(load|loads)\b', "cPickle deserialization"),
    (r'(?i)\bos\.system\s*\(', "os.system call (command injection)"),
    (r'(?i)\beval\s*\(', "eval call (code injection)"),
    (r'(?i)\bexec\s*\(', "exec call (code injection)"),
]

# Insecure crypto patterns (A02:2021).
_INSECURE_CRYPTO_PATTERNS = [
    (r'(?i)\bhashlib\.md5\b', "MD5 hash usage (cryptographically broken)"),
    (r'(?i)\bhashlib\.sha1\b', "SHA-1 hash usage (cryptographically weak)"),
    (r'(?i)\brandom\.(random|randint|choice)\s*\(', "insecure random for security (use secrets)"),
]

# Open redirect patterns (A01:2021).
_OPEN_REDIRECT_PATTERNS = [
    (r'(?i)\bredirect\s*\(\s*\w+\)', "unvalidated redirect"),
]

# Insecure SSL/TLS patterns.
_INSECURE_SSL_PATTERNS = [
    (r'(?i)\bverify_mode\s*=\s*ssl\.CERT_NONE', "SSL verification disabled"),
    (r'(?i)\bverify\s*=\s*False', "SSL verification disabled"),
    (r'(?i)\bcheck_hostname\s*=\s*False', "SSL hostname verification disabled"),
    (r'(?i)\bdisable_warnings\s*\(\s*\)', "SSL warnings disabled"),
]

# SQLi in Python AST.
_SQLI_KEYWORDS = {"select", "insert", "update", "delete", "drop", "union"}


class OWASPAnalyzer:
    """
    Analyzes source code for OWASP Top 10 vulnerabilities.

    Supports Python (AST-based + regex) and JavaScript/TypeScript (regex-based).

    Usage::

        analyzer = OWASPAnalyzer()
        findings = analyzer.analyze(source_code, language="python")
    """

    def analyze(
        self,
        source_code: str,
        language: str = "python",
        file_path: str = "<unknown>",
    ) -> list[Finding]:
        """
        Analyze source code for OWASP Top 10 vulnerabilities.

        Args:
            source_code: Source code content.
            language: python | javascript | typescript.
            file_path: Path for evidence reporting.

        Returns:
            List of Finding objects with severity, category, and remediation.
        """
        findings: list[Finding] = []

        if language == "python":
            findings.extend(self._analyze_python(source_code, file_path))
        elif language in ("javascript", "typescript"):
            findings.extend(self._analyze_javascript(source_code, file_path))

        return findings

    def _analyze_python(self, source_code: str, file_path: str) -> list[Finding]:
        """Analyze Python code using AST + regex."""
        findings: list[Finding] = []

        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return findings

        # AST-based SQL injection detection.
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_func_name(node)
                if func_name in ("execute", "executemany", "raw"):
                    findings.extend(self._check_sql_injection_call(node, source_code, file_path))

        # AST-based f-string SQL injection detection in assignments.
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and isinstance(node.value, ast.JoinedStr):
                        if self._is_fstring_sql_injection(node.value):
                            findings.append(Finding(
                                category="A03:2021-Injection",
                                severity=Severity.high,
                                title="SQL injection via f-string in assignment",
                                description="SQL query constructed using f-string interpolation in variable assignment.",
                                evidence={"file": file_path, "line": node.lineno, "ast_type": "JoinedStr"},
                                remediation="Use parameterized queries with placeholders.",
                                owasp_mapping="A03:2021-Injection",
                                confidence=0.85,
                            ))

        # AST-based eval/exec detection.
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_func_name(node)
                if func_name == "eval":
                    findings.append(Finding(
                        category="A03:2021-Injection",
                        severity=Severity.high,
                        title="Use of eval() detected",
                        description="eval() allows arbitrary code execution.",
                        evidence={"file": file_path, "line": node.lineno},
                        remediation="Replace eval() with ast.literal_eval() or a safe parser.",
                        owasp_mapping="A03:2021-Injection",
                        confidence=0.95,
                    ))
                elif func_name == "exec":
                    findings.append(Finding(
                        category="A03:2021-Injection",
                        severity=Severity.high,
                        title="Use of exec() detected",
                        description="exec() allows arbitrary code execution.",
                        evidence={"file": file_path, "line": node.lineno},
                        remediation="Remove exec() or use safer alternatives.",
                        owasp_mapping="A03:2021-Injection",
                        confidence=0.95,
                    ))
                if func_name == "system" and self._get_module_name(node) == "os":
                    findings.append(Finding(
                        category="A03:2021-Injection",
                        severity=Severity.critical,
                        title="os.system() call detected",
                        description="os.system() enables command injection.",
                        evidence={"file": file_path, "line": node.lineno},
                        remediation="Use subprocess with shell=False and argument list.",
                        owasp_mapping="A03:2021-Injection",
                        confidence=0.95,
                    ))

        # Regex-based detection (covers both languages).
        findings.extend(self._regex_patterns(source_code, file_path, _CMD_INJECTION_PATTERNS, "A03:2021-Injection", Severity.critical))
        findings.extend(self._regex_patterns(source_code, file_path, _SQL_INJECTION_PATTERNS, "A03:2021-Injection", Severity.high))
        findings.extend(self._regex_patterns(source_code, file_path, _XSS_PATTERNS, "A03:2021-Injection", Severity.high))
        findings.extend(self._regex_patterns(source_code, file_path, _SSRF_PATTERNS, "A10:2021-Server-Side Request Forgery", Severity.high))
        findings.extend(self._regex_patterns(source_code, file_path, _CSRF_PATTERNS, "A01:2021-Broken Access Control", Severity.medium))
        findings.extend(self._regex_patterns(source_code, file_path, _DESERIALIZATION_PATTERNS, "A08:2021-Software and Data Integrity Failures", Severity.high))
        findings.extend(self._regex_patterns(source_code, file_path, _INSECURE_CRYPTO_PATTERNS, "A02:2021-Cryptographic Failures", Severity.high))
        findings.extend(self._regex_patterns(source_code, file_path, _OPEN_REDIRECT_PATTERNS, "A01:2021-Broken Access Control", Severity.medium))
        findings.extend(self._regex_patterns(source_code, file_path, _INSECURE_SSL_PATTERNS, "A02:2021-Cryptographic Failures", Severity.high))

        return findings

    def _analyze_javascript(self, source_code: str, file_path: str) -> list[Finding]:
        """Analyze JavaScript/TypeScript code using regex."""
        findings: list[Finding] = []
        findings.extend(self._regex_patterns(source_code, file_path, _XSS_PATTERNS, "A03:2021-Injection", Severity.high))
        findings.extend(self._regex_patterns(source_code, file_path, _CMD_INJECTION_PATTERNS, "A03:2021-Injection", Severity.critical))
        findings.extend(self._regex_patterns(source_code, file_path, _SSRF_PATTERNS, "A10:2021-SSRF", Severity.high))
        findings.extend(self._regex_patterns(source_code, file_path, _CSRF_PATTERNS, "A01:2021-Broken Access Control", Severity.medium))
        return findings

    def _check_sql_injection_call(
        self, node: ast.Call, source_code: str, file_path: str
    ) -> list[Finding]:
        """Check if a SQL execute call uses unsafe string formatting."""
        findings: list[Finding] = []

        if not node.args:
            return findings

        first_arg = node.args[0]

        # Check for f-strings with SQL keywords.
        if isinstance(first_arg, ast.JoinedStr):
            for value in first_arg.values:
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    if any(kw in value.value.upper() for kw in _SQLI_KEYWORDS):
                        findings.append(Finding(
                            category="A03:2021-Injection",
                            severity=Severity.critical,
                            title="SQL injection via f-string in execute()",
                            description="SQL query constructed using f-string interpolation.",
                            evidence={"file": file_path, "line": node.lineno, "ast_type": "JoinedStr"},
                            remediation="Use parameterized queries with placeholders.",
                            owasp_mapping="A03:2021-Injection",
                            confidence=0.95,
                        ))
                        break

        # Check for .format() calls.
        if isinstance(first_arg, ast.Call):
            func_name = self._get_func_name(first_arg)
            if func_name == "format":
                findings.append(Finding(
                    category="A03:2021-Injection",
                    severity=Severity.critical,
                    title="SQL injection via .format() in execute()",
                    description="SQL query constructed using string.format().",
                    evidence={"file": file_path, "line": node.lineno},
                    remediation="Use parameterized queries with placeholders.",
                    owasp_mapping="A03:2021-Injection",
                    confidence=0.9,
                ))

        # Check for string concatenation with SQL keywords.
        if isinstance(first_arg, ast.BinOp):
            if self._is_binop_sql_injection(first_arg):
                findings.append(Finding(
                    category="A03:2021-Injection",
                    severity=Severity.critical,
                    title="SQL injection via string concatenation in execute()",
                    description="SQL query constructed using string concatenation.",
                    evidence={"file": file_path, "line": node.lineno},
                    remediation="Use parameterized queries with placeholders.",
                    owasp_mapping="A03:2021-Injection",
                    confidence=0.9,
                ))

        return findings

    def _is_binop_sql_injection(self, node: ast.BinOp) -> bool:
        """Check if a BinOp (string concatenation) involves SQL keywords."""
        for child in ast.walk(node):
            if isinstance(child, ast.Constant) and isinstance(child.value, str):
                if any(kw in child.value.upper() for kw in _SQLI_KEYWORDS):
                    return True
        return False

    def _is_fstring_sql_injection(self, node: ast.JoinedStr) -> bool:
        """Check if a JoinedStr (f-string) involves SQL keywords."""
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                if any(kw in value.value.upper() for kw in _SQLI_KEYWORDS):
                    return True
        return False

    def _regex_patterns(
        self,
        source_code: str,
        file_path: str,
        patterns: list[tuple[str, str]],
        category: str,
        severity: Severity,
    ) -> list[Finding]:
        """Apply regex patterns and produce findings."""
        findings: list[Finding] = []
        seen: set[str] = set()

        for pattern, description in patterns:
            for match in re.finditer(pattern, source_code, re.IGNORECASE | re.MULTILINE):
                line_num = source_code[:match.start()].count("\n") + 1
                key = f"{file_path}:{line_num}:{pattern}"
                if key in seen:
                    continue
                seen.add(key)

                findings.append(Finding(
                    category=category,
                    severity=severity,
                    title=f"{category} — {description}",
                    description=f"{description} at line {line_num}.",
                    evidence={"file": file_path, "line": line_num, "pattern": pattern},
                    remediation=self._get_remediation(category),
                    owasp_mapping=category,
                    confidence=0.85,
                ))

        return findings

    def _get_func_name(self, node: ast.Call) -> str:
        """Extract function name from a Call AST node."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        if isinstance(node.func, ast.Attribute):
            return node.func.attr
        return ""

    def _get_module_name(self, node: ast.Call) -> str:
        """Extract module name from a Call AST node."""
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            return node.func.value.id
        return ""

    def _get_remediation(self, category: str) -> str:
        """Get remediation guidance by OWASP category."""
        remediations = {
            "A03:2021-Injection": "Use parameterized queries, input validation, and output encoding. Never concatenate user input into SQL, commands, or HTML.",
            "A01:2021-Broken Access Control": "Implement proper CSRF tokens, access control checks, and ensure proper session management.",
            "A10:2021-Server-Side Request Forgery": "Validate and sanitize URL inputs, use allowlists for target hosts, and disable unnecessary URL schemes.",
        }
        return remediations.get(category, "Review OWASP Top 10 guidance for this category and apply mitigations.")
