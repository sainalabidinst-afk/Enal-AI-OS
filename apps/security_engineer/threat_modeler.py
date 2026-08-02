"""
Security Engineer — Threat Modeler.

Performs STRIDE-based threat modeling: identifies attack surface,
trust boundaries, data flows, and threats (Spoofing, Tampering,
Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege).
"""

from __future__ import annotations

import logging
import re
from typing import Any

from apps.security_engineer.schemas import (
    ThreatModelEntry,
    ThreatModelResult,
    ThreatCategory,
    Severity,
)

logger = logging.getLogger(__name__)


_STRIDE_PATTERNS: dict[ThreatCategory, list[tuple[str, str, str]]] = {
    ThreatCategory.spoofing: [
        (r'(?i)(oauth|auth|login|token|password|credential)', "Authentication mechanism detected", "Implement multi-factor authentication and proper token validation"),
        (r'(?i)(user_input|request\.user|current_user)', "User identity in request flow", "Validate user identity through trusted identity provider"),
    ],
    ThreatCategory.tampering: [
        (r'(?i)(json\.parse|deserialize|eval|pickle\.loads)', "Unsafe deserialization", "Use safe deserialization with schema validation"),
        (r'(?i)(query.*\+|concat|f["\'].*SELECT|f["\'].*INSERT)', "Dynamic query construction", "Use parameterized queries"),
        (r'(?i)(innerHTML|document\.write)', "DOM manipulation", "Sanitize and encode all DOM inputs"),
    ],
    ThreatCategory.repudiation: [
        (r'(?i)(delete|remove|drop|archive)', "Destructive operation", "Implement audit logging for all destructive actions"),
        (r'(?i)(update|modify|edit)', "Data modification", "Log all data modifications with user context and timestamp"),
    ],
    ThreatCategory.info_disclosure: [
        (r'(?i)(print|console\.log|logger\.debug|dump|var_dump|pprint)', "Debug/logging output", "Remove debug output in production; implement log redaction"),
        (r'(?i)(except.*pass|except.*:|except:)', "Bare except (error swallowing)", "Log exceptions with sanitized details"),
        (r'(?i)(pickle|marshal|yaml\.load\b)', "Unsafe deserialization", "Replace with safe alternatives (json, yaml.safe_load)"),
    ],
    ThreatCategory.denial_service: [
        (r'(?i)(for\s+.*in.*:|while\s+|loop)', "Unbounded loop", "Implement circuit breakers and rate limiting"),
        (r'(?i)(read\(\)|file\.read|open\()', "File/resource access without limit", "Add resource limits and timeouts"),
        (r'(?i)(requests\.get|fetch\(|http\.request)', "External HTTP call", "Implement timeouts and retry with backoff"),
    ],
    ThreatCategory.elevation_privilege: [
        (r'(?i)(eval|exec|os\.system|subprocess|__import__|globals\(\)|locals\(\))', "Arbitrary code execution", "Run with least privilege; sandbox untrusted code"),
        (r'(?i)(sudo|root|admin\b)', "Privilege escalation", "Implement least-privilege access control"),
        (r'(?i)(shell=True|shell_exec|passthru)', "Shell execution", "Use parameterized command execution without shell"),
    ],
}

# Attack surface indicators.
_ATTACK_SURFACE_INDICATORS = [
    (r'(?i)(api|endpoint|route|webhook|callback|listener)', "API/network endpoint"),
    (r'(?i)(database|db|sql|query|mongo|redis|cache)', "Database or cache layer"),
    (r'(?i)(file|filesystem|disk|path|directory)', "File system access"),
    (r'(?i)(auth|login|token|session|password|credential)', "Authentication system"),
    (r'(?i)(payment|billing|invoice|charge)', "Payment processing"),
    (r'(?i)(upload|download|file.*input|multipart)', "File upload/download"),
    (r'(?i)(email|smtp|send.*mail)', "Email system"),
    (r'(?i)(queue|message|kafka|rabbit|sqs|sns)', "Message queue"),
    (r'(?i)(config|env|setting|secret|credential)', "Configuration/secrets"),
]

# Trust boundary indicators.
_TRUST_BOUNDARY_PATTERNS = [
    (r'(?i)(public.*api|external.*service|internet|client.*request)', "External client boundary"),
    (r'(?i)(database|db|storage|persistence)', "Data persistence boundary"),
    (r'(?i)(cache|redis|memcached)', "Caching layer boundary"),
    (r'(?i)(microservice|service.*boundary|domain)', "Service/microservice boundary"),
    (r'(?i)(admin|internal.*only|privileged)', "Privileged access boundary"),
]


class ThreatModeler:
    """
    Performs STRIDE-based threat modeling on architectures and code.

    Usage::

        modeler = ThreatModeler()
        result = modeler.model(architecture_desc, source_code)
    """

    def model(
        self,
        architecture_description: str = "",
        source_code: str = "",
        components: list[str] | None = None,
        data_flows: list[str] | None = None,
    ) -> ThreatModelResult:
        """
        Build a threat model from architecture and code analysis.

        Args:
            architecture_description: Text description of the system architecture.
            source_code: Source code to analyze for threats.
            components: List of component names in the system.
            data_flows: List of data flow descriptions.

        Returns:
            ThreatModelResult with attack surface, trust boundaries, threats.
        """
        attack_surface = self._identify_attack_surface(architecture_description, source_code, components)
        trust_boundaries = self._identify_trust_boundaries(architecture_description, source_code, components)
        flow_list = data_flows or self._infer_data_flows(architecture_description, source_code)
        threats = self._identify_threats(architecture_description, source_code)

        risk_rating = self._compute_risk_rating(threats)

        return ThreatModelResult(
            attack_surface=attack_surface,
            trust_boundaries=trust_boundaries,
            data_flows=flow_list,
            threats=threats,
            risk_rating=risk_rating,
        )

    def _identify_attack_surface(
        self, arch_desc: str, source_code: str, components: list[str] | None
    ) -> str:
        """Identify the attack surface of the system."""
        combined = f"{arch_desc}\n{source_code}"
        surfaces_found: list[str] = []

        for pattern, surface in _ATTACK_SURFACE_INDICATORS:
            if re.search(pattern, combined, re.IGNORECASE):
                surfaces_found.append(surface)

        if components:
            surfaces_found.extend(components)

        if not surfaces_found:
            return "No obvious attack surface components detected from architecture description."

        return f"Attack surface includes: {', '.join(dict.fromkeys(surfaces_found))}"

    def _identify_trust_boundaries(
        self, arch_desc: str, source_code: str, components: list[str] | None
    ) -> list[str]:
        """Identify trust boundaries in the system."""
        combined = f"{arch_desc}\n{source_code}"
        boundaries: list[str] = []

        for pattern, boundary in _TRUST_BOUNDARY_PATTERNS:
            matches = re.finditer(pattern, combined, re.IGNORECASE)
            for match in matches:
                boundaries.append(boundary)

        if components:
            boundaries.append(f"Component boundary: {', '.join(components)}")

        return list(dict.fromkeys(boundaries)) if boundaries else ["No explicit trust boundaries identified"]

    def _infer_data_flows(self, arch_desc: str, source_code: str) -> list[str]:
        """Infer data flows from architecture description and source code."""
        flows: list[str] = []
        combined = f"{arch_desc}\n{source_code}"

        flow_patterns = [
            r'(?i)(user|client).*?(request|send|call).*?(api|endpoint|service)',
            r'(?i)(service).*?(call|communicate).*?(database|db|storage)',
            r'(?i)(message|event).*?(queue|topic|stream)',
            r'(?i)(request).*?(response|reply)',
        ]

        for pattern in flow_patterns:
            for match in re.finditer(pattern, combined, re.IGNORECASE):
                flows.append(match.group(0)[:100])

        return list(dict.fromkeys(flows)) if flows else ["Data flow details not specified in architecture"]

    def _identify_threats(self, arch_desc: str, source_code: str) -> list[ThreatModelEntry]:
        """Identify STRIDE threats from architecture and code."""
        threats: list[ThreatModelEntry] = []
        combined_text = f"{arch_desc}\n{source_code}"

        for threat_category, patterns in _STRIDE_PATTERNS.items():
            for pattern, description, mitigation in patterns:
                for match in re.finditer(pattern, combined_text, re.IGNORECASE):
                    line_num = combined_text[:match.start()].count("\n") + 1
                    threats.append(ThreatModelEntry(
                        threat_type=threat_category,
                        component=f"line {line_num}",
                        description=f"{description} (matched: {match.group(0)[:60]})",
                        likelihood=self._estimate_likelihood(threat_category),
                        impact=self._estimate_impact(threat_category),
                        mitigation=mitigation,
                        confidence=0.8,
                    ))

        # Deduplicate by threat type + component.
        seen: set[str] = set()
        unique: list[ThreatModelEntry] = []
        for t in threats:
            key = f"{t.threat_type.value}:{t.component}"
            if key not in seen:
                seen.add(key)
                unique.append(t)

        return unique[:20]  # cap at 20 threats

    def _estimate_likelihood(self, category: ThreatCategory) -> float:
        """Estimate likelihood for a threat category."""
        likelihoods = {
            ThreatCategory.spoofing: 0.6,
            ThreatCategory.tampering: 0.5,
            ThreatCategory.repudiation: 0.4,
            ThreatCategory.info_disclosure: 0.7,
            ThreatCategory.denial_service: 0.5,
            ThreatCategory.elevation_privilege: 0.3,
        }
        return likelihoods.get(category, 0.5)

    def _estimate_impact(self, category: ThreatCategory) -> float:
        """Estimate impact for a threat category."""
        impacts = {
            ThreatCategory.spoofing: 0.7,
            ThreatCategory.tampering: 0.8,
            ThreatCategory.repudiation: 0.6,
            ThreatCategory.info_disclosure: 0.8,
            ThreatCategory.denial_service: 0.7,
            ThreatCategory.elevation_privilege: 0.9,
        }
        return impacts.get(category, 0.5)

    def _compute_risk_rating(self, threats: list[ThreatModelEntry]) -> Severity:
        """Compute overall risk rating from identified threats."""
        if not threats:
            return Severity.low

        max_risk = max(t.likelihood * t.impact for t in threats)
        high_threats = sum(1 for t in threats if t.likelihood * t.impact >= 0.6)

        if max_risk >= 0.7 or high_threats >= 3:
            return Severity.critical
        if max_risk >= 0.5 or high_threats >= 1:
            return Severity.high
        return Severity.medium
