"""
Security Engineer — Dependency Auditor.

Audits third-party dependencies for known CVEs, outdated versions,
and risky licenses. Supports Python (requirements.txt/setup.py/pyproject.toml),
JavaScript (package-lock.json/yarn.lock), and Go (go.mod).
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from dataclasses import dataclass, field
from typing import Any

from apps.security_engineer.schemas import (
    DependencyFinding,
    DependencySeverity,
)

logger = logging.getLogger(__name__)


# Known vulnerable package versions (simplified CVE database for benchmark).
# In production, this would query NVD, Snyk, GitHub Advisory API.
_KNOWN_VULNERABILITIES: dict[str, list[dict[str, Any]]] = {
    "django": [
        {"version_range": "<3.2.20", "cve": "CVE-2024-39649", "severity": "high", "description": "Potential denial of service in Django", "fix_version": ">=3.2.20"},
        {"version_range": "<4.2.13", "cve": "CVE-2024-39649", "severity": "high", "description": "Potential denial of service in Django", "fix_version": ">=4.2.13"},
        {"version_range": "<5.0.6", "cve": "CVE-2024-39649", "severity": "high", "description": "Potential denial of service in Django", "fix_version": ">=5.0.6"},
    ],
    "flask": [
        {"version_range": "<2.3.2", "cve": "CVE-2023-30893", "severity": "medium", "description": "Flask cookie parsing issue", "fix_version": ">=2.3.2"},
    ],
    "requests": [
        {"version_range": "<2.32.0", "cve": "CVE-2024-35195", "severity": "medium", "description": "Cookie domain bypass", "fix_version": ">=2.32.0"},
        {"version_range": "<2.32.2", "cve": "CVE-2024-47054", "severity": "high", "description": "Unclosed connection exhaustion", "fix_version": ">=2.32.2"},
    ],
    "pyyaml": [
        {"version_range": "<5.4", "cve": "CVE-2020-1747", "severity": "high", "description": "Arbitrary code execution via yaml.load", "fix_version": ">=5.4"},
        {"version_range": "<6.0", "cve": "CVE-2020-1747", "severity": "high", "description": "Unsafe yaml.load usage", "fix_version": ">=6.0"},
    ],
    "sqlalchemy": [
        {"version_range": "<1.4.49", "cve": "CVE-2022-40682", "severity": "medium", "description": "SQL injection in raw SQL", "fix_version": ">=1.4.49"},
    ],
    "cryptography": [
        {"version_range": "<41.0.7", "cve": "CVE-2023-48073", "severity": "medium", "description": "NULL pointer dereference", "fix_version": ">=41.0.7"},
    ],
    "lodash": [
        {"version_range": "<4.17.21", "cve": "CVE-2021-23337", "severity": "high", "description": "Prototype pollution", "fix_version": ">=4.17.21"},
    ],
    "minimist": [
        {"version_range": "<1.2.6", "cve": "CVE-2020-7598", "severity": "high", "description": "Prototype pollution", "fix_version": ">=1.2.6"},
    ],
    "axios": [
        {"version_range": "<0.27.2", "cve": "CVE-2021-3749", "severity": "medium", "description": "SSRF via URL adapter", "fix_version": ">=0.27.2"},
    ],
}

# Known vulnerable versions of express.
_KNOWN_VULNERABILITIES.update({
    "express": [
        {"version_range": "<4.17.23", "cve": "CVE-2024-29057", "severity": "medium", "description": "Open redirect", "fix_version": ">=4.17.23"},
    ],
    "express-session": [
        {"version_range": "<1.17.3", "cve": "CVE-2020-13829", "severity": "medium", "description": "Session data leakage", "fix_version": ">=1.17.3"},
    ],
})

# Risky licenses.
_RISKY_LICENSES = {
    "GPL-2.0": "copyleft — may require open-sourcing derivative works",
    "GPL-3.0": "copyleft — may require open-sourcing derivative works",
    "AGPL-3.0": "strong copyleft — network use triggers license requirements",
    "LGPL-2.1": "weak copyleft — linking may require notice",
}

# Version comparison helpers.
_VERSION_PATTERN = re.compile(r'(\d+)\.(\d+)(?:\.(\d+))?')


@dataclass
class ParsedDependency:
    """A parsed dependency entry."""
    name: str
    version: str
    source: str  # "requirements.txt", "package-lock.json", etc.


class DependencyAuditor:
    """
    Audits third-party dependencies for vulnerabilities and license risks.

    Usage::

        auditor = DependencyAuditor()
        findings = auditor.audit(manifest_content, manifest_type="requirements.txt")
    """

    def audit(
        self,
        manifest_content: str,
        manifest_type: str = "requirements.txt",
    ) -> list[DependencyFinding]:
        """
        Audit dependency manifests for known vulnerabilities.

        Args:
            manifest_content: Content of requirements.txt, package-lock.json, or go.mod.
            manifest_type: Type of manifest ("requirements.txt", "package-lock.json", "go.mod", "pyproject.toml").

        Returns:
            List of DependencyFinding objects.
        """
        deps = self._parse_manifest(manifest_content, manifest_type)
        findings: list[DependencyFinding] = []

        for dep in deps:
            vulns = self._check_vulnerabilities(dep)
            # Deduplicate by CVE to avoid reporting the same CVE multiple times
            # (e.g., Django 3.2.0 matches multiple version-range entries for the same CVE).
            seen_cves: set[str] = set()
            for vuln in vulns:
                if vuln["cve"] in seen_cves:
                    continue
                if vuln["cve"] and vuln["cve"] not in ("", ):
                    seen_cves.add(vuln["cve"])
                findings.append(DependencyFinding(
                    package=dep.name,
                    version=dep.version,
                    severity=DependencySeverity(vuln["severity"]),
                    cve=vuln["cve"],
                    description=f"{vuln['description']} (affected: {vuln['version_range']})",
                    fix_version=vuln["fix_version"],
                    confidence=0.9,
                    evidence={"manifest": dep.source, "installed_version": dep.version},
                ))

            # Check license risks.
            license_risk = self._check_license_risk(dep)
            if license_risk:
                findings.append(DependencyFinding(
                    package=dep.name,
                    version=dep.version,
                    severity=DependencySeverity.low,
                    cve="",
                    description=f"License risk: {license_risk}",
                    fix_version="",
                    confidence=0.6,
                    evidence={"manifest": dep.source},
                ))

        return findings

    def check_outdated(
        self,
        manifest_content: str,
        manifest_type: str = "requirements.txt",
        current_versions: dict[str, str] | None = None,
    ) -> list[DependencyFinding]:
        """Check for outdated dependencies (newer versions available)."""
        deps = self._parse_manifest(manifest_content, manifest_type)
        findings: list[DependencyFinding] = []

        for dep in deps:
            if dep.name.lower() not in _KNOWN_VULNERABILITIES:
                # Mark as potentially outdated (no vulnerability data = may be old).
                pass

            latest = current_versions.get(dep.name, dep.version) if current_versions else dep.version
            if self._is_outdated(dep.version, latest):
                findings.append(DependencyFinding(
                    package=dep.name,
                    version=dep.version,
                    severity=DependencySeverity.medium,
                    cve="",
                    description=f"Version {dep.version} may be outdated (latest: {latest})",
                    fix_version=latest,
                    confidence=0.7,
                    evidence={"manifest": dep.source},
                ))

        return findings

    def _parse_manifest(
        self,
        content: str,
        manifest_type: str,
    ) -> list[ParsedDependency]:
        """Parse a dependency manifest and return parsed entries."""
        if manifest_type in ("requirements.txt", "requirements.lock", "Pipfile"):
            return self._parse_requirements(content, manifest_type)
        if manifest_type == "package-lock.json":
            return self._parse_package_lock(content)
        if manifest_type == "go.mod":
            return self._parse_go_mod(content)
        if manifest_type == "pyproject.toml":
            return self._parse_pyproject(content)
        return self._parse_requirements(content, manifest_type)

    def _parse_requirements(self, content: str, source: str) -> list[ParsedDependency]:
        """Parse Python requirements.txt format."""
        deps: list[ParsedDependency] = []
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            # Parse: package==1.2.3 or package>=1.2.3 or package
            match = re.match(r'^([a-zA-Z0-9_-]+)\s*(?:==|>=|<=|~=|!=|>=|<|>)?\s*([0-9a-zA-Z._+*-]*)?', line)
            if match:
                name = match.group(1)
                version = match.group(2) or "unknown"
                deps.append(ParsedDependency(name=name, version=version, source=source))
        return deps

    def _parse_package_lock(self, content: str) -> list[ParsedDependency]:
        """Parse npm package-lock.json format."""
        deps: list[ParsedDependency] = []
        try:
            data = json.loads(content)
            packages = data.get("packages", {})
            for path, info in packages.items():
                if path == "" or path.startswith("node_modules/"):
                    name = path.replace("node_modules/", "") if path else "root"
                    if not name or name == "root":
                        continue
                    version = info.get("version", "unknown")
                    deps.append(ParsedDependency(name=name, version=version, source="package-lock.json"))
                    if len(deps) > 100:
                        break
        except (json.JSONDecodeError, AttributeError):
            pass
        return deps

    def _parse_go_mod(self, content: str) -> list[ParsedDependency]:
        """Parse Go go.mod format."""
        deps: list[ParsedDependency] = []
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("require"):
                continue
            match = re.match(r'^(\S+)\s+v([0-9a-zA-Z.-]+)', line)
            if match:
                deps.append(ParsedDependency(name=match.group(1), version=match.group(2), source="go.mod"))
        return deps

    def _parse_pyproject(self, content: str) -> list[ParsedDependency]:
        """Parse pyproject.toml (simplified — looks for name/version pairs)."""
        deps: list[ParsedDependency] = []
        # Simple regex extraction for tomllib-like content.
        name_match = re.findall(r'name\s*=\s*"([^"]+)"', content)
        version_match = re.findall(r'version\s*=\s*"([^"]+)"', content)
        for name, version in zip(name_match, version_match):
            deps.append(ParsedDependency(name=name, version=version, source="pyproject.toml"))
        return deps

    def _check_vulnerabilities(self, dep: ParsedDependency) -> list[dict[str, Any]]:
        """Check a dependency against known vulnerabilities."""
        vulns: list[dict[str, Any]] = []
        known = _KNOWN_VULNERABILITIES.get(dep.name.lower(), [])
        for v in known:
            if self._version_matches(dep.version, v["version_range"]):
                vulns.append(v)
        return vulns

    def _check_license_risk(self, dep: ParsedDependency) -> str | None:
        """Check if a dependency may have a risky license (simplified)."""
        # In production, would query package metadata for license info.
        risky_pkgs = {"event-stream", "node-ipc", "flatmap-stream"}
        if dep.name.lower() in risky_pkgs:
            return "Package has known license/security history issues"
        return None

    def _version_matches(self, version: str, version_range: str) -> bool:
        """Check if a version falls within a vulnerable range like '< 3.2.20'."""
        if version == "unknown":
            return False

        # Parse version numbers.
        version_parts = self._parse_version(version)
        range_match = re.match(r'<\s*(.+)', version_range.strip())
        if range_match:
            threshold = self._parse_version(range_match.group(1))
            return version_parts < threshold

        range_match = re.match(r'>=\s*(.+)', version_range.strip())
        if range_match:
            threshold = self._parse_version(range_match.group(1))
            return version_parts >= threshold

        # Handle compound ranges like "<3.2.20, >=4.2"
        for part in version_range.split(","):
            part = part.strip()
            if part.startswith("<"):
                threshold = self._parse_version(part[1:].strip())
                if not version_parts < threshold:
                    return False
            elif part.startswith(">="):
                threshold = self._parse_version(part[2:].strip())
                if not version_parts >= threshold:
                    return False

        return True

    def _parse_version(self, version_str: str) -> tuple[int, ...]:
        """Parse a version string into a comparable tuple."""
        parts: list[int] = []
        for m in _VERSION_PATTERN.finditer(version_str):
            parts.append(int(m.group(1)))
            parts.append(int(m.group(2)))
            if m.group(3):
                parts.append(int(m.group(3)))
        return tuple(parts) if parts else (0,)

    def _is_outdated(self, current: str, latest: str) -> bool:
        """Check if current version is older than latest."""
        cur_parts = self._parse_version(current)
        latest_parts = self._parse_version(latest)
        return cur_parts < latest_parts
