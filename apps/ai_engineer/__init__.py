"""
AI Engineer — __init__.py
"""

from typing import Any

from apps.base import BaseReferenceApp
from apps.ai_engineer.engine import AIEngineerEngine
from apps.ai_engineer.worker import AIEngineerWorker
from apps.ai_engineer.schemas import (
    AIEngineerRequest,
    AIEngineerReport,
    OperationType,
    AgentArchitectureType,
    OrchestrationPattern,
    RAGStrategy,
    EvaluationMetric,
    LLMProvider,
    DeploymentEnvironment,
    BusinessContext,
    QualityAttributes,
    AgentSpec,
    ToolSpec,
    RAGConfig,
    PromptTemplate,
    FineTuningConfig,
    DeploymentConfig,
    MonitoringConfig,
    AIEngineerRecord,
)


class AIEngineerApp(BaseReferenceApp):
    name = "ai-engineer"
    version = "1.0.0"
    description = "AI architecture, agent design, RAG, and LLMOps planning"
    category = "ai"
    pipeline = ["perception", "memory", "reasoning", "decision", "action"]

    def __init__(self) -> None:
        self.worker = AIEngineerWorker()

    async def run(
        self, user_input: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        task = dict(context or {})
        task.setdefault("user_input", user_input)
        return await self.worker.execute(task)


def get_app() -> AIEngineerApp:
    return AIEngineerApp()

__all__ = [
    "AIEngineerApp",
    "get_app",
    "AIEngineerEngine",
    "AIEngineerWorker",
    "AIEngineerRequest",
    "AIEngineerReport",
    "OperationType",
    "AgentArchitectureType",
    "OrchestrationPattern",
    "RAGStrategy",
    "EvaluationMetric",
    "LLMProvider",
    "DeploymentEnvironment",
    "BusinessContext",
    "QualityAttributes",
    "AgentSpec",
    "ToolSpec",
    "RAGConfig",
    "PromptTemplate",
    "FineTuningConfig",
    "DeploymentConfig",
    "MonitoringConfig",
    "AIEngineerRecord",
]
