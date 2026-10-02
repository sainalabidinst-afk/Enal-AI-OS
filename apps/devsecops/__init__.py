"""
DevSecOps Capability Pack — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.devsecops.engine import DevSecOpsEngine
from apps.devsecops.schemas import (
    BusinessContext,
    DevSecOpsInputs,
    DevSecOpsOperation,
    DevSecOpsRecord,
    DevSecOpsReport,
    DevSecOpsRequest,
    PipelineSecurityGate,
    SecurityFinding,
    VulnerableDependency,
)
from apps.devsecops.worker import DevSecOpsWorker


class DevSecOpsApp(BaseReferenceApp):
    name = "devsecops"
    version = "3.0.0"
    description = (
        "CI/CD security gates, dependency vulnerability scanning, "
        "runtime policy enforcement, and compliance as code"
    )
    category = "security"
    pipeline = ["perception", "memory", "reasoning", "planning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = DevSecOpsWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return self.worker.execute(task)


def get_app() -> DevSecOpsApp:
    return DevSecOpsApp()


__all__ = [
    "DevSecOpsApp",
    "get_app",
    "DevSecOpsEngine",
    "DevSecOpsWorker",
    "DevSecOpsRequest",
    "DevSecOpsReport",
    "DevSecOpsOperation",
    "DevSecOpsInputs",
    "DevSecOpsRecord",
    "PipelineSecurityGate",
    "SecurityFinding",
    "VulnerableDependency",
    "BusinessContext",
]
