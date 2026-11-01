"""
REA bridging service for the Reverse Engineer Capability Pack.

Wraps the morluto/rea CLI and MCP server so the ECP cognitive pipeline can
invoke reverse-engineering analysis through a stable, async interface.
"""

from __future__ import annotations

import asyncio
import json
import logging
import shutil
from pathlib import Path
from typing import Any

from apps.reverse_engineer.models import (
    REAAnalysisResult,
    REAArtifactInspection,
    REAEvidence,
    REATargetType,
)

logger = logging.getLogger(__name__)


class REAService:
    """Service that talks to the REA CLI / MCP server.

    The service is intentionally resilient: if the REA CLI is not installed
    on the host it degrades gracefully instead of crashing the pack.
    """

    def __init__(self, cli_path: str | None = None) -> None:
        self.cli_path = cli_path or self._detect_cli()
        self._available: bool | None = None

    # ------------------------------------------------------------------
    # CLI detection
    # ------------------------------------------------------------------
    def _detect_cli(self) -> str:
        """Locate the REA CLI binary on PATH."""
        for candidate in ("rea", "rea-agents", "npx"):
            if shutil.which(candidate):
                return candidate
        return "rea"  # fall back; errors will surface at call time

    @property
    def available(self) -> bool:
        """Whether the REA CLI appears usable on this host."""
        if self._available is None:
            self._available = bool(shutil.which(self.cli_path))
        return self._available

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    async def analyze_target(self, target_path: str, deep: bool = False) -> REAAnalysisResult:
        """Run a full reverse-engineering analysis against *target_path*.

        Dispatches to the appropriate REA sub-command based on file
        extension when *deep* is False, otherwise attempts a generic
        evidence-based inspection.
        """
        path = Path(target_path)
        if not path.exists():
            return REAAnalysisResult(
                target_path=target_path,
                target_type=REATargetType.UNKNOWN,
                summary=f"Target not found: {target_path}",
                findings=[f"File does not exist: {target_path}"],
                recommendations=["Provide a valid executable/archive path"],
            )

        target_type = self._guess_type(path)

        if target_type == REATargetType.ELECTRON_JS:
            return await self._analyze_javascript_app(path, deep=deep)
        return await self._inspect_binary_evidence(path, deep=deep)

    async def _analyze_javascript_app(
        self, app_path: Path, deep: bool = False
    ) -> REAAnalysisResult:
        """Analyse Electron / JavaScript packaged applications (ASAR, IPC)."""
        if not self.available:
            return self._unavailable_result(str(app_path), REATargetType.ELECTRON_JS)

        cmd = [
            self.cli_path,
            "-y",
            "rea-agents@latest",
            "analyze-javascript-application",
            str(app_path),
            "--json",
        ]
        if deep:
            cmd.append("--deep")

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            if proc.returncode != 0:
                err_text = stderr.decode("utf-8", errors="replace")
                logger.error("REA JavaScript analysis failed: %s", err_text)
                return REAAnalysisResult(
                    target_path=str(app_path),
                    target_type=REATargetType.ELECTRON_JS,
                    summary="REA JavaScript analysis returned non-zero exit code",
                    findings=[f"REA error: {err_text[:500]}"],
                    recommendations=["Verify REA CLI installation and target accessibility"],
                )

            payload = json.loads(stdout.decode("utf-8"))
            return self._parse_js_analysis(str(app_path), payload)
        except Exception as exc:  # pragma: no cover - defensive
            logger.exception("Unexpected error during JavaScript analysis")
            return REAAnalysisResult(
                target_path=str(app_path),
                target_type=REATargetType.ELECTRON_JS,
                summary=f"Unexpected error: {exc}",
                findings=[f"Exception: {exc}"],
                recommendations=["Check REA CLI and Node.js installation"],
            )

    async def _inspect_binary_evidence(
        self,
        target_binary: Path,
        deep: bool = False,
    ) -> REAAnalysisResult:
        """Inspect native binary evidence for a function or feature."""
        if not self.available:
            return self._unavailable_result(str(target_binary), REATargetType.NATIVE)

        cmd = [
            self.cli_path,
            "-y",
            "rea-agents@latest",
            "inspect-binary-evidence",
            str(target_binary),
            "--json",
        ]
        if deep:
            cmd.append("--deep")

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            if proc.returncode != 0:
                err_text = stderr.decode("utf-8", errors="replace")
                logger.error("REA binary inspection failed: %s", err_text)
                return REAAnalysisResult(
                    target_path=str(target_binary),
                    target_type=REATargetType.NATIVE,
                    summary="REA binary inspection returned non-zero exit code",
                    findings=[f"REA error: {err_text[:500]}"],
                    recommendations=["Verify REA CLI and native toolchain (Ghidra/Rizin/objdump)"],
                )

            payload = json.loads(stdout.decode("utf-8"))
            return self._parse_binary_inspection(str(target_binary), payload)
        except Exception as exc:  # pragma: no cover - defensive
            logger.exception("Unexpected error during binary inspection")
            return REAAnalysisResult(
                target_path=str(target_binary),
                target_type=REATargetType.NATIVE,
                summary=f"Unexpected error: {exc}",
                findings=[f"Exception: {exc}"],
                recommendations=["Check REA CLI installation"],
            )

    # ------------------------------------------------------------------
    # Parsers for REA JSON output
    # ------------------------------------------------------------------
    def _parse_js_analysis(self, target_path: str, payload: dict[str, Any]) -> REAAnalysisResult:
        """Map REA JavaScript JSON output into REAAnalysisResult."""
        evidence: list[REAEvidence] = []
        artifacts: list[REAArtifactInspection] = []
        findings: list[str] = []

        raw = payload.get("result", payload)

        for item in raw.get("evidence", []):
            evidence.append(
                REAEvidence(
                    evidence_id=item.get("evidence_id", f"EVID-{len(evidence) + 1}"),
                    target_type=REATargetType.ELECTRON_JS,
                    target_path=target_path,
                    summary=item.get("summary", ""),
                    observations=item.get("observations", []),
                    inferences=item.get("inferences", []),
                    unknowns=item.get("unknowns", []),
                    metadata=item.get("metadata", {}),
                )
            )
            findings.extend(item.get("inferences", []))

        for item in raw.get("artifacts", []):
            artifacts.append(
                REAArtifactInspection(
                    artifact_id=item.get("artifact_id", f"ART-{len(artifacts) + 1}"),
                    artifact_type=item.get("artifact_type", "unknown"),
                    path=item.get("path", target_path),
                    evidence_refs=item.get("evidence_refs", []),
                    confidence=item.get("confidence", 0.5),
                    details=item.get("details", {}),
                )
            )

        return REAAnalysisResult(
            target_path=target_path,
            target_type=REATargetType.ELECTRON_JS,
            summary=raw.get("summary", "JavaScript application analysed"),
            evidence=evidence,
            artifacts=artifacts,
            findings=findings,
            recommendations=raw.get("recommendations", []),
            metadata=raw.get("metadata", {}),
        )

    def _parse_binary_inspection(
        self,
        target_path: str,
        payload: dict[str, Any],
    ) -> REAAnalysisResult:
        """Map REA binary inspection JSON output into REAAnalysisResult."""
        evidence: list[REAEvidence] = []
        artifacts: list[REAArtifactInspection] = []
        findings: list[str] = []

        raw = payload.get("result", payload)

        evidence.append(
            REAEvidence(
                evidence_id=raw.get("evidence_id", f"EVID-{1}"),
                target_type=REATargetType.NATIVE,
                target_path=target_path,
                summary=raw.get("summary", ""),
                observations=raw.get("observations", []),
                inferences=raw.get("inferences", []),
                unknowns=raw.get("unknowns", []),
                metadata=raw.get("metadata", {}),
            )
        )
        findings.extend(raw.get("inferences", []))

        return REAAnalysisResult(
            target_path=target_path,
            target_type=REATargetType.NATIVE,
            summary=raw.get("summary", "Binary inspection completed"),
            evidence=evidence,
            artifacts=artifacts,
            findings=findings,
            recommendations=raw.get("recommendations", []),
            metadata=raw.get("metadata", {}),
        )

    def _unavailable_result(
        self, target_path: str, target_type: REATargetType
    ) -> REAAnalysisResult:
        """Return a graceful result when the REA CLI is not installed."""
        return REAAnalysisResult(
            target_path=target_path,
            target_type=target_type,
            summary="REA CLI not available on this host",
            findings=[
                "REA (morluto/rea) CLI or MCP server not detected on PATH",
                "Install with: npm install -g rea-agents",
            ],
            recommendations=[
                "Install rea-agents globally",
                "Run `npx rea-agents@latest setup` to verify dependencies",
            ],
        )

    @staticmethod
    def _guess_type(path: Path) -> REATargetType:
        """Heuristic target-type detection from file extension/name."""
        suffix = path.suffix.lower()
        name = path.name.lower()
        if suffix in {".asar", ".js", ".mjs", ".cjs", ".json"}:
            return REATargetType.ELECTRON_JS
        if suffix in {".exe", ".dll", ".so", ".dylib", ".bin"}:
            return REATargetType.NATIVE
        if suffix in {".net", ".dll"} and "dotnet" in name:
            return REATargetType.DOTNET
        return REATargetType.UNKNOWN
