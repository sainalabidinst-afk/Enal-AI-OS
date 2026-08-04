"""
AI Engineer Schemas
====================

Typed contracts for the AI Engineer capability pack.
Defines the input (AIEngineerRequest) and output (AIEngineerReport)
contracts, plus all supporting types.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class OperationType(str, Enum):
    agent_design = "agent_design"
    rag_engine_design = "rag_engine_design"
    prompt_engineering = "prompt_engineering"
    llmops_setup = "llmops_setup"
    ai_assessment = "ai_assessment"


class AgentArchitectureType(str, Enum):
    single_agent = "single_agent"
    multi_agent = "multi_agent"
    hierarchical = "hierarchical"
    swarm = "swarm"
    pipeline = "pipeline"


class OrchestrationPattern(str, Enum):
    sequential = "sequential"
    concurrent = "concurrent"
    conditional = "conditional"
    human_in_loop = "human_in_loop"
    reflection = "reflection"


class RAGStrategy(str, Enum):
    naive = "naive"
    chunked = "chunked"
    hybrid = "hybrid"
    graph = "graph"
    agentic = "agentic"


class EvaluationMetric(str, Enum):
    accuracy = "accuracy"
    f1_score = "f1_score"
    bleu = "bleu"
    rouge = "rouge"
    faithfulness = "faithfulness"
    hallucination_rate = "hallucination_rate"
    latency_p95 = "latency_p95"
    throughput = "throughput"


class LLMProvider(str, Enum):
    openai = "openai"
    anthropic = "anthropic"
    google = "google"
    mistral = "mistral"
    local = "local"
    custom = "custom"


class DeploymentEnvironment(str, Enum):
    development = "development"
    staging = "staging"
    production = "production"


class BusinessContext(BaseModel):
    domain: str = Field(default="", description="Business domain")
    project_name: str = Field(default="", description="Project name")
    description: str = Field(default="", description="Project overview")


class QualityAttributes(BaseModel):
    accuracy_target: str = Field(default="95%", description="Target accuracy")
    latency_target: str = Field(default="< 500ms", description="Latency target")
    availability_target: str = Field(default="99.9%", description="Availability SLA")
    cost_per_1k_tokens: float = Field(default=0.01, description="Target cost per 1k tokens")


class ToolSpec(BaseModel):
    name: str = Field(default="", description="Tool name")
    description: str = Field(default="", description="Tool description")
    parameters: dict[str, Any] = Field(default_factory=dict, description="Tool parameters schema")
    required: list[str] = Field(default_factory=list, description="Required parameters")


class AgentSpec(BaseModel):
    name: str = Field(default="", description="Agent name")
    role: str = Field(default="", description="Agent role/purpose")
    architecture: AgentArchitectureType = Field(default=AgentArchitectureType.single_agent)
    orchestration: OrchestrationPattern = Field(default=OrchestrationPattern.sequential)
    llm_provider: LLMProvider = Field(default=LLMProvider.openai)
    model: str = Field(default="gpt-4o", description="LLM model identifier")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="LLM temperature")
    max_tokens: int = Field(default=4096, description="Max output tokens")
    tools: list[ToolSpec] = Field(default_factory=list, description="Available tools")
    system_prompt: str = Field(default="", description="System prompt")
    guardrails: list[str] = Field(default_factory=list, description="Guardrail rules")
    memory_enabled: bool = Field(default=True, description="Enable conversation memory")
    context_window: int = Field(default=128000, description="Context window in tokens")


class RAGConfig(BaseModel):
    strategy: RAGStrategy = Field(default=RAGStrategy.chunked)
    chunk_size: int = Field(default=512, description="Chunk size in tokens")
    chunk_overlap: int = Field(default=50, description="Chunk overlap in tokens")
    embedding_model: str = Field(default="text-embedding-3-small", description="Embedding model")
    vector_store: str = Field(default="pinecone", description="Vector store")
    top_k: int = Field(default=5, description="Top K retrieval")
    rerank_enabled: bool = Field(default=False, description="Enable reranking")
    rerank_model: str = Field(default="", description="Rerank model")
    retrieval_metrics: list[EvaluationMetric] = Field(
        default_factory=lambda: [EvaluationMetric.faithfulness, EvaluationMetric.hallucination_rate]
    )


class PromptTemplate(BaseModel):
    name: str = Field(default="", description="Template name")
    template: str = Field(default="", description="Prompt template string")
    variables: list[str] = Field(default_factory=list, description="Template variables")
    version: str = Field(default="1.0", description="Template version")
    description: str = Field(default="", description="Template description")
    expected_output_format: str = Field(default="json", description="Expected output format")


class FineTuningConfig(BaseModel):
    base_model: str = Field(default="gpt-4o-mini", description="Base model to fine-tune")
    training_data_path: str = Field(default="", description="Path to training data")
    validation_data_path: str = Field(default="", description="Path to validation data")
    epochs: int = Field(default=3, description="Training epochs")
    learning_rate: float = Field(default=0.0001, description="Learning rate")
    batch_size: int = Field(default=8, description="Batch size")
    evaluation_metrics: list[EvaluationMetric] = Field(
        default_factory=lambda: [EvaluationMetric.accuracy, EvaluationMetric.f1_score]
    )
    target_metric_threshold: float = Field(default=0.9, description="Target metric threshold")


class DeploymentConfig(BaseModel):
    environment: DeploymentEnvironment = Field(default=DeploymentEnvironment.production)
    scaling_min: int = Field(default=1, description="Minimum replicas")
    scaling_max: int = Field(default=10, description="Maximum replicas")
    cpu_request: str = Field(default="500m", description="CPU request")
    memory_request: str = Field(default="1Gi", description="Memory request")
    gpu_enabled: bool = Field(default=False, description="Enable GPU")
    gpu_count: int = Field(default=0, description="Number of GPUs")
    rate_limit_rpm: int = Field(default=100, description="Rate limit requests per minute")
    timeout_seconds: int = Field(default=60, description="Request timeout")


class MonitoringConfig(BaseModel):
    metrics_enabled: bool = Field(default=True, description="Enable metrics collection")
    logging_level: str = Field(default="INFO", description="Logging level")
    tracing_enabled: bool = Field(default=True, description="Enable distributed tracing")
    alert_on_latency_p95: str = Field(default="1000ms", description="Alert threshold for P95 latency")
    alert_on_error_rate: str = Field(default="1%", description="Alert threshold for error rate")
    dashboard_url: str = Field(default="", description="Monitoring dashboard URL")


class AIEngineerRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: OperationType = Field(default=OperationType.agent_design)
    business_context: BusinessContext = Field(default_factory=BusinessContext)
    quality_attributes: QualityAttributes = Field(default_factory=QualityAttributes)
    output_format: str = Field(default="json")
    inputs: dict[str, Any] = Field(default_factory=dict, description="Operation-specific inputs")


class AIEngineerReport(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: str = Field(default="")
    agent_spec: AgentSpec | None = Field(default=None, description="Agent architecture design")
    rag_config: RAGConfig | None = Field(default=None, description="RAG configuration")
    prompt_templates: list[PromptTemplate] = Field(default_factory=list, description="Prompt templates")
    fine_tuning_config: FineTuningConfig | None = Field(default=None, description="Fine-tuning configuration")
    deployment_config: DeploymentConfig | None = Field(default=None, description="Deployment configuration")
    monitoring_config: MonitoringConfig | None = Field(default=None, description="Monitoring configuration")
    evaluation_results: dict[str, float] = Field(default_factory=dict, description="Evaluation metrics")
    cost_estimate: dict[str, float] = Field(default_factory=dict, description="Cost estimate")
    recommendations: list[str] = Field(default_factory=list, description="Improvement recommendations")
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0)
    explanation: str = Field(default="")
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        data = self.model_dump()
        data["generated_at"] = self.generated_at.isoformat()
        return data


class AIEngineerRecord(BaseModel):
    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str = Field(default="")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    operation: str = Field(default="")
    agent_type: str = Field(default="")
    accuracy_achieved: float = Field(default=0.0)
    latency_p95_ms: int = Field(default=0)
    cost_monthly_usd: float = Field(default=0.0)
    outcome: str = Field(default="accepted")
