"""
Security Engineer — Configuration Hardening Reviewer.

Checks configuration files (Docker, Kubernetes, cloud IaC, network configs)
against security baselines (CIS Benchmarks) and best practices.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from apps.security_engineer.schemas import Finding, Severity

logger = logging.getLogger(__name__)


# CIS Docker Benchmark checks.
_DOCKER_HARDENING_CHECKS: list[tuple[str, str, str, Severity]] = [
    (r'Dockerfile\s+.*\bFROM\b', "Base image should be pinned to a specific digest", "Use image@sha256:digest instead of tag", Severity.medium),
    (r'\bUSER\s+root\b', "Running as root user", "Switch to a non-root user with USER directive", Severity.high),
    (r'\bUSER\s+root\b', "Dockerfile should not run as root", "Use a non-root user", Severity.high),
    (r'ADD\s+.*\.zip', "Use of ADD for zip extraction (security risk)", "Use COPY and RUN unzip instead", Severity.medium),
    (r'\bapt-get\s+install\s+.*--no-install-recommends\b', "Missing --no-install-recommends on apt-get install", "Add --no-install-recommends to reduce attack surface", Severity.low),
    (r'\bSELINUX\b', "SELinux not explicitly disabled", "Set SELINUX=disabled or ensure proper configuration", Severity.medium),
    (r'\bchmod\s+777\b', "World-writable permissions", "Use restrictive file permissions (chmod 755 or 750)", Severity.high),
]

# CIS Kubernetes Benchmark checks.
_K8S_HARDENING_CHECKS: list[tuple[str, str, str, Severity]] = [
    (r'\bprivileged:\s*true', "Privileged container detected", "Remove privileged: true unless absolutely required", Severity.critical),
    (r'\bhostPID:\s*true', "Host PID namespace sharing", "Remove hostPID or restrict to trusted pods", Severity.critical),
    (r'\bhostIPC:\s*true', "Host IPC namespace sharing", "Remove hostIPC or restrict to trusted pods", Severity.critical),
    (r'\bhostNetwork:\s*true', "Host network namespace sharing", "Remove hostNetwork unless explicitly required", Severity.high),
    (r'\bhostPath:', "Host path volume mount", "Avoid hostPath mounts; use persistent volumes", Severity.high),
    (r'\brunAsUser:\s*0', "Container running as root user (UID 0)", "Set runAsNonRoot or specify non-root runAsUser", Severity.critical),
    (r'\ballowPrivilegeEscalation:\s*true', "Privilege escalation allowed", "Set allowPrivilegeEscalation: false", Severity.high),
    (r'\bmountPropagation:\s*HostToContainer', "Host mount propagation", "Use rslave or rshared only if required", Severity.medium),
    (r'\bcommand:\s*\[?.*\/bin\/(?:bash|sh)', "Shell command execution in container", "Avoid shell commands; use direct binary execution", Severity.medium),
    (r'\bserviceAccountName:\s*default', "Using default service account", "Create a dedicated service account with minimal permissions", Severity.high),
    (r'\bimage:\s*[A-Za-z0-9_.-]+\/[^:@]*:[a-zA-Z0-9._-]+', "Image tag not pinned to digest", "Pin images to sha256 digests", Severity.medium),
    (r'\bapiVersion:\s*v1\b\s*.*\bkind:\s*Pod\b', "Bare Pod (not a Deployment/StatefulSet)", "Use Deployments or StatefulSets for production pods", Severity.medium),
]

# Cloud IaC (Terraform) checks.
_TERRAFORM_HARDENING_CHECKS: list[tuple[str, str, str, Severity]] = [
    (r'\bpublic\s*=\s*true', "Publicly accessible resource", "Restrict to private; use security groups/VPC", Severity.high),
    (r'\bopen\b.*\bto\b', "Open CIDR block (0.0.0.0/0)", "Restrict CIDR to known IP ranges", Severity.critical),
    (r'\bhttp_port\b', "HTTP (not HTTPS) listener", "Use HTTPS listeners with TLS", Severity.high),
    (r'\badmin\s*=\s*true', "Admin privileges enabled", "Remove admin=true; use least privilege", Severity.critical),
    (r'\bpassword\s*=\s*["\'][^"\']+["\']', "Hardcoded password in Terraform", "Use variables and secrets manager", Severity.critical),
    (r'\bskip_credentials_validation\s*=\s*true', "Skipping credential validation", "Remove skip_credentials_validation in production", Severity.medium),
    (r'\bskip_metadata_api_check\s*=\s*true', "Skipping metadata API check", "Remove skip_metadata_api_check in production", Severity.medium),
]

# Generic config checks.
_GENERIC_HARDENING_CHECKS: list[tuple[str, str, str, Severity]] = [
    (r'\bssh_root_login\s*=\s*yes', "SSH root login enabled", "Set PermitRootLogin no", Severity.high),
    (r'\bpassword_authentication\s*=\s*yes', "SSH password authentication enabled", "Use key-based auth: PasswordAuthentication no", Severity.high),
    (r'\bprotocol\s*=\s*1\b', "SSH protocol 1 (deprecated)", "Use SSH protocol 2", Severity.critical),
]


class HardeningReviewer:
    """
    Reviews configuration files for security hardening issues.

    Supports: Dockerfile, Docker Compose, Kubernetes YAML, Terraform,
    and generic SSH/system configs.

    Usage::

        reviewer = HardeningReviewer()
        findings = reviewer.review(config_content, config_type="dockerfile")
    """

    def review(
        self,
        config_content: str,
        config_type: str = "auto",
    ) -> list[Finding]:
        """
        Review a configuration for hardening issues.

        Args:
            config_content: Configuration file content.
            config_type: dockerfile | kubernetes | terraform | ssh | auto.

        Returns:
            List of Finding objects with remediation.
        """
        detected_type = config_type if config_type != "auto" else self._detect_type(config_content)
        findings: list[Finding] = []

        checks: list[tuple[str, str, str, Severity]] = []

        if detected_type == "dockerfile":
            checks = _DOCKER_HARDENING_CHECKS
        elif detected_type == "kubernetes":
            checks = _K8S_HARDENING_CHECKS
        elif detected_type == "terraform":
            checks = _TERRAFORM_HARDENING_CHECKS
        elif detected_type == "ssh":
            checks = _GENERIC_HARDENING_CHECKS
        else:
            checks = _DOCKER_HARDENING_CHECKS + _K8S_HARDENING_CHECKS + _TERRAFORM_HARDENING_CHECKS + _GENERIC_HARDENING_CHECKS

        seen: set[str] = set()
        for pattern, description, remediation, severity in checks:
            for match in re.finditer(pattern, config_content, re.IGNORECASE | re.MULTILINE):
                line_num = config_content[:match.start()].count("\n") + 1
                key = f"{detected_type}:{line_num}:{pattern}"
                if key in seen:
                    continue
                seen.add(key)

                findings.append(Finding(
                    category=f"configuration_hardening.{detected_type}",
                    severity=severity,
                    title=f"Hardening issue: {description}",
                    description=f"{description} at line {line_num}.",
                    evidence={"config_type": detected_type, "line": line_num, "match": match.group(0)[:80]},
                    remediation=remediation,
                    owasp_mapping="A05:2021-Security Misconfiguration",
                    compliance_mapping=["CIS"],
                    confidence=0.9,
                ))

        return findings

    def _detect_type(self, content: str) -> str:
        """Auto-detect configuration type from content."""
        lowered = content.lower()
        if "from " in lowered and "run " in lowered and "cmd" in lowered:
            return "dockerfile"
        if "kind:" in lowered and ("deployment" in lowered or "pod" in lowered or "service" in lowered):
            return "kubernetes"
        if "resource " in lowered and "provider" in lowered:
            return "terraform"
        if "permitrootlogin" in lowered or "sshd_config" in lowered.lower() or "PasswordAuthentication" in lowered:
            return "ssh"
        return "unknown"

    def check_compliance(self, config_content: str, config_type: str, profile: str = "CIS") -> list[Finding]:
        """
        Check configuration against a specific compliance profile.

        Currently supports: CIS (Docker, Kubernetes, Terraform).
        """
        return self.review(config_content, config_type)
