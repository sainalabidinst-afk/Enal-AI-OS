"""
DevOps Smell Taxonomy
=====================

Detects 10 DevOps-specific problems from infrastructure and pipeline artifacts.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from apps.devops_assistant.schemas import Problem, ProblemType

logger = logging.getLogger(__name__)


class DevOpsSmellTaxonomy:
    """Detects DevOps problems in infrastructure and pipeline configurations."""

    def __init__(self) -> None:
        self.rules = [
            ("hardcoded_secret", self._detect_hardcoded_secret),
            ("missing_health_check", self._detect_missing_health_check),
            ("missing_resource_limit", self._detect_missing_resource_limit),
            ("missing_rollback", self._detect_missing_rollback),
            ("outdated_image", self._detect_outdated_image),
            ("insecure_config", self._detect_insecure_config),
            ("missing_monitoring", self._detect_missing_monitoring),
            ("pipeline_break", self._detect_pipeline_break),
            ("missing_backup", self._detect_missing_backup),
            ("policy_violation", self._detect_policy_violation),
        ]

    def analyze(self, artifact: dict[str, Any]) -> list[Problem]:
        problems: list[Problem] = []
        for problem_type, detector in self.rules:
            detected = detector(artifact)
            if detected:
                problems.extend(detected)
        return problems

    def _detect_hardcoded_secret(self, artifact: dict[str, Any]) -> list[Problem]:
        problems: list[Problem] = []
        content = artifact.get("content", "")
        secret_patterns = [
            (r"password\s*=\s*['\"][^'\"]+['\"]", "Hardcoded password detected"),
            (r"api[_-]?key\s*=\s*['\"][^'\"]+['\"]", "Hardcoded API key detected"),
            (r"token\s*=\s*['\"][^'\"]+['\"]", "Hardcoded token detected"),
        ]
        for pattern, description in secret_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                problems.append(Problem(
                    id=f"devops-hardcoded-secret-{len(problems)+1}",
                    type=ProblemType.HARDCODED_SECRET.value,
                    severity="critical",
                    location=artifact.get("path", "unknown"),
                    description=description,
                    impact="Secrets exposed in source code",
                    confidence=0.9,
                    evidence=matches[:3],
                ))
        return problems

    def _detect_missing_health_check(self, artifact: dict[str, Any]) -> list[Problem]:
        problems: list[Problem] = []
        content = artifact.get("content", "")
        if "health" not in content.lower() and "readiness" not in content.lower() and "liveness" not in content.lower():
            problems.append(Problem(
                id=f"devops-missing-health-check-{len(problems)+1}",
                type=ProblemType.MISSING_HEALTH_CHECK.value,
                severity="medium",
                location=artifact.get("path", "unknown"),
                description="Health check tidak ditemukan dalam konfigurasi",
                impact="Pod dapat dianggap healthy meskipun aplikasi gagal",
                confidence=0.8,
            ))
        return problems

    def _detect_missing_resource_limit(self, artifact: dict[str, Any]) -> list[Problem]:
        problems: list[Problem] = []
        content = artifact.get("content", "")
        if "resources:" not in content and "limits:" not in content:
            problems.append(Problem(
                id=f"devops-missing-resource-limit-{len(problems)+1}",
                type=ProblemType.MISSING_RESOURCE_LIMIT.value,
                severity="medium",
                location=artifact.get("path", "unknown"),
                description="Resource limit tidak ditemukan",
                impact="Pod dapat mengonsumsi sumber daya tanpa batas",
                confidence=0.85,
            ))
        return problems

    def _detect_missing_rollback(self, artifact: dict[str, Any]) -> list[Problem]:
        problems: list[Problem] = []
        content = artifact.get("content", "")
        if "rollback" not in content.lower() and "revisionHistoryLimit" not in content:
            problems.append(Problem(
                id=f"devops-missing-rollback-{len(problems)+1}",
                type=ProblemType.MISSING_ROLLBACK.value,
                severity="medium",
                location=artifact.get("path", "unknown"),
                description="Rollback strategy tidak ditemukan",
                impact="Deployment gagal tanpa cara kembali ke versi sebelumnya",
                confidence=0.8,
            ))
        return problems

    def _detect_outdated_image(self, artifact: dict[str, Any]) -> list[Problem]:
        problems: list[Problem] = []
        content = artifact.get("content", "")
        outdated_patterns = [r":latest", r":alpine-\d+\.\d+", r":\d+\.\d+\.\d+-(old|legacy)"]
        for pattern in outdated_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                problems.append(Problem(
                    id=f"devops-outdated-image-{len(problems)+1}",
                    type=ProblemType.OUTDATED_IMAGE.value,
                    severity="low",
                    location=artifact.get("path", "unknown"),
                    description="Gambar container yang sudah outdated digunakan",
                    impact="Vulnerabilitas keamanan dan masalah kompatibilitas",
                    confidence=0.7,
                ))
                break
        return problems

    def _detect_insecure_config(self, artifact: dict[str, Any]) -> list[Problem]:
        problems: list[Problem] = []
        content = artifact.get("content", "")
        insecure_patterns = [
            (r"privileged:\s*true", "Container running in privileged mode"),
            (r"runAsUser:\s*0", "Container running as root"),
            (r"NET_ADMIN", "Container has NET_ADMIN capability"),
        ]
        for pattern, description in insecure_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                problems.append(Problem(
                    id=f"devops-insecure-config-{len(problems)+1}",
                    type=ProblemType.INSECURE_CONFIG.value,
                    severity="high",
                    location=artifact.get("path", "unknown"),
                    description=description,
                    impact="Increased attack surface",
                    confidence=0.85,
                ))
        return problems

    def _detect_missing_monitoring(self, artifact: dict[str, Any]) -> list[Problem]:
        problems: list[Problem] = []
        content = artifact.get("content", "")
        if "prometheus" not in content.lower() and "metrics" not in content.lower() and "monitoring" not in content.lower():
            problems.append(Problem(
                id=f"devops-missing-monitoring-{len(problems)+1}",
                type=ProblemType.MISSING_MONITORING.value,
                severity="low",
                location=artifact.get("path", "unknown"),
                description="Monitoring tidak dikonfigurasi",
                impact="Tidak ada visibilitas terhadap kesehatan layanan",
                confidence=0.75,
            ))
        return problems

    def _detect_pipeline_break(self, artifact: dict[str, Any]) -> list[Problem]:
        problems: list[Problem] = []
        content = artifact.get("content", "")
        if "on:" not in content and "trigger" not in content.lower():
            problems.append(Problem(
                id=f"devops-pipeline-break-{len(problems)+1}",
                type=ProblemType.PIPELINE_BREAK.value,
                severity="high",
                location=artifact.get("path", "unknown"),
                description="Pipeline trigger tidak ditemukan",
                impact="CI/CD pipeline tidak akan berjalan otomatis",
                confidence=0.8,
            ))
        return problems

    def _detect_missing_backup(self, artifact: dict[str, Any]) -> list[Problem]:
        problems: list[Problem] = []
        content = artifact.get("content", "")
        if "backup" not in content.lower() and "snapshot" not in content.lower():
            problems.append(Problem(
                id=f"devops-missing-backup-{len(problems)+1}",
                type=ProblemType.MISSING_BACKUP.value,
                severity="medium",
                location=artifact.get("path", "unknown"),
                description="Backup strategy tidak ditemukan",
                impact="Data loss in case of failure",
                confidence=0.7,
            ))
        return problems

    def _detect_policy_violation(self, artifact: dict[str, Any]) -> list[Problem]:
        problems: list[Problem] = []
        content = artifact.get("content", "")
        if "policy" not in content.lower() and "opa" not in content.lower():
            problems.append(Problem(
                id=f"devops-policy-violation-{len(problems)+1}",
                type=ProblemType.POLICY_VIOLATION.value,
                severity="low",
                location=artifact.get("path", "unknown"),
                description="Policy-as-code tidak diimplementasikan",
                impact="Tidak ada enforcement terhadap kebijakan organisasi",
                confidence=0.6,
            ))
        return problems
