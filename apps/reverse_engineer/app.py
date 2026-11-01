"""
REA Capability Pack entrypoint.

Implements :class:`apps.base.BaseApp` so the Reverse Engineer pack can be
discovered and executed by the ECP Cognitive Pipeline and FactoryRegistry.
"""

from __future__ import annotations

from typing import Any

from apps.base import BaseApp
from apps.reverse_engineer.models import REAAnalysisResult, REAResponse
from apps.reverse_engineer.rea_service import REAService


class ReverseEngineerCapabilityPack(BaseApp):
    """Reverse Engineer Capability Pack powered by morluto/rea.

    Provides evidence-based reverse engineering for:
        * Native binaries (C/C++, Rust, Go) via Ghidra / Rizin / objdump
        * Electron / JavaScript apps via ASAR / IPC decompilation
        * .NET assemblies
        * Web applications
    """

    name: str = "reverse-engineer"
    version: str = "1.0.0"
    description: str = (
        "Evidence-based reverse engineering pack for native, managed, "
        "Electron/JavaScript, and web applications using morluto/rea."
    )
    category: str = "security"
    pipeline: list[str] = ["parse", "inspect", "evidence", "output"]

    def __init__(self) -> None:
        super().__init__()
        self._service = REAService()

    async def run(
        self,
        user_input: str,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Execute the REA capability pack.

        Parameters
        ----------
        user_input : str
            Natural-language analysis request.
        context : dict | None
            Optional execution context. May contain ``target_path`` and
            ``deep_analysis`` keys.

        Returns
        -------
        dict[str, Any]
            Serialized :class:`REAResponse`.
        """
        ctx = context or {}
        target_path = ctx.get("target_path")
        deep = bool(ctx.get("deep_analysis", False))

        if not target_path:
            response = REAResponse(
                status="info",
                message="Reverse engineering request received. No target artifact provided.",
            )
            return response.model_dump()

        result: REAAnalysisResult = await self._service.analyze_target(target_path, deep=deep)

        response = REAResponse(
            status="success",
            result=result,
            message=f"Analysed {target_path} ({result.target_type.value})",
        )
        return response.model_dump()

    def to_dict(self) -> dict[str, Any]:
        """Return pack metadata including REA availability."""
        base = super().to_dict()
        base["rea_available"] = self._service.available
        return base
