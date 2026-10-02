"""
Data Scientist Capability Schemas
====================================

Typed contracts for the Data Scientist capability pack.
Defines input (DataScienceRequest) and output (DataScienceReport) contracts for
advanced ML pipelines, model training, evaluation, and feature engineering.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class MLTask(StrEnum):
    classification = "classification"
    regression = "regression"
    clustering = "clustering"
    time_series_forecasting = "time_series_forecasting"


class MLAlgorithm(StrEnum):
    random_forest = "random_forest"
    gradient_boosting = "gradient_boosting"
    logistic_regression = "logistic_regression"
    neural_network = "neural_network"
    kmeans = "kmeans"
    arima = "arima"
    prophet = "prophet"


class DataScienceOperation(StrEnum):
    feature_engineering = "feature_engineering"
    model_training = "model_training"
    model_evaluation = "model_evaluation"
    hyperparameter_tuning = "hyperparameter_tuning"


class Dataset(BaseModel):
    name: str
    path: str
    n_samples: int = 0
    n_features: int = 0
    target_column: str | None = None


class FeatureConfig(BaseModel):
    name: str
    type: str = "numerical"
    transformation: str = "none"


class ModelConfig(BaseModel):
    algorithm: MLAlgorithm
    hyperparameters: dict[str, Any] = Field(default_factory=dict)
    task: MLTask = MLTask.classification


class BusinessContext(BaseModel):
    project_name: str
    domain: str
    team_size: int = Field(default=8, ge=1)


class DataScienceConfig(BaseModel):
    operation: DataScienceOperation
    task: MLTask = MLTask.classification
    datasets: list[Dataset] = Field(default_factory=list)
    features: list[FeatureConfig] = Field(default_factory=list)
    model: ModelConfig | None = None
    metrics: list[str] = Field(default_factory=list)
    constraints: dict[str, Any] = Field(default_factory=dict)


class DataScienceRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    operation: str = "model_training"
    business_context: BusinessContext
    inputs: DataScienceConfig
    quality_attributes: dict[str, Any] = Field(default_factory=dict)


class FeatureEngineeringResult(BaseModel):
    original_features: int
    engineered_features: int
    generated_features: list[str] = Field(default_factory=list)
    transformations_applied: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class ModelTrainingResult(BaseModel):
    algorithm: MLAlgorithm
    model_id: str
    training_samples: int
    training_time_seconds: float
    feature_importance: dict[str, float] = Field(default_factory=dict)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class ModelEvaluationResult(BaseModel):
    model_id: str
    task: MLTask
    metrics: dict[str, float] = Field(default_factory=dict)
    confusion_matrix: dict[str, Any] = Field(default_factory=dict)
    classification_report: dict[str, Any] = Field(default_factory=dict)
    overfit_risk: str = "low"


class HyperparameterResult(BaseModel):
    model_id: str
    best_params: dict[str, Any] = Field(default_factory=dict)
    best_score: float = 0.0
    search_space_size: int = 0
    iterations: int = 0


class DataScienceReport(BaseModel):
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    operation: DataScienceOperation
    feature_results: list[FeatureEngineeringResult] = Field(default_factory=list)
    training_results: list[ModelTrainingResult] = Field(default_factory=list)
    evaluation_results: list[ModelEvaluationResult] = Field(default_factory=list)
    hyperparameter_results: list[HyperparameterResult] = Field(default_factory=list)
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0)
    model_version: str = "1.0.0"


class DataScientistPackRecord(BaseModel):
    pack_id: str = "data-scientist"
    version: str = "1.0.0"
    capabilities: list[str] = Field(default_factory=lambda: [
        "feature_engineering",
        "model_training",
        "model_evaluation",
        "hyperparameter_tuning",
    ])


__all__ = [
    "BusinessContext",
    "DataScienceConfig",
    "DataScienceOperation",
    "DataScienceReport",
    "DataScienceRequest",
    "DataScientistPackRecord",
    "Dataset",
    "FeatureConfig",
    "FeatureEngineeringResult",
    "HyperparameterResult",
    "MLAlgorithm",
    "MLTask",
    "ModelConfig",
    "ModelEvaluationResult",
    "ModelTrainingResult",
]
