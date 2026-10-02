"""
Data Scientist Schemas
=======================

Typed contracts for the Data Scientist capability pack.
Defines input/output contracts for ML pipelines and model evaluation.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class DataScientistOperation(StrEnum):
    feature_engineering = "feature_engineering"
    model_training = "model_training"
    model_evaluation = "model_evaluation"
    pipeline_execution = "pipeline_execution"


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=5, ge=1)
    budget_monthly_usd: float = Field(default=10000, ge=0)


class DataScientistInputs(BaseModel):
    operation: DataScientistOperation
    dataset_description: str = ""
    features: list[str] = Field(default_factory=list)
    target: str = ""
    model_type: str = ""
    sample_size: int = Field(default=1000, ge=1)
    test_split: float = Field(default=0.2, ge=0, le=1)
    metrics: list[str] = Field(default_factory=list)
    hyperparameters: dict[str, Any] = Field(default_factory=dict)


class TrainingSummary(BaseModel):
    model_type: str
    training_time_seconds: float
    training_samples: int
    feature_count: int
    convergence_info: str = ""


class ModelEvaluation(BaseModel):
    metric_name: str
    value: float
    threshold: float = 0.8
    passes: bool = True
    description: str = ""


class FeatureImportance(BaseModel):
    feature_name: str
    importance_score: float
    rank: int
    description: str = ""


class PipelineResult(BaseModel):
    step_name: str
    status: str
    output_description: str = ""
    artifacts: list[str] = Field(default_factory=list)


class DataScientistReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    training_summary: TrainingSummary | None = None
    evaluations: list[ModelEvaluation] = Field(default_factory=list)
    feature_importance: list[FeatureImportance] = Field(default_factory=list)
    pipeline_results: list[PipelineResult] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    quality_score: float = Field(default=0.90, ge=0, le=1)
    model_version: str = "1.0.0"


class DataScientistRecord(BaseModel):
    pack_id: str = "data-scientist"
    version: str = "2.7.0"
    capabilities: list[str] = Field(default_factory=lambda: [
        "feature_engineering",
        "model_training",
        "model_evaluation",
        "pipeline_execution",
    ])


class DataScientistRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    business_context: BusinessContext
    inputs: DataScientistInputs
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


__all__ = [
    "DataScientistInputs",
    "DataScientistOperation",
    "DataScientistRequest",
    "DataScientistReport",
    "DataScientistRecord",
    "TrainingSummary",
    "ModelEvaluation",
    "FeatureImportance",
    "PipelineResult",
    "BusinessContext",
]
