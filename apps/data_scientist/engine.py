"""
Data Scientist Engine.
"""

from __future__ import annotations

import logging

from apps.data_scientist.data_science_engine import DataScienceEngine
from apps.data_scientist.schemas import (
    DataScientistInputs,
    DataScientistOperation,
    DataScientistReport,
    DataScientistRequest,
    FeatureImportance,
    ModelEvaluation,
    PipelineResult,
    TrainingSummary,
)

logger = logging.getLogger(__name__)


class DataScientistEngine:
    """
    Orchestrates data science pipeline:
        1. Input Validation
        2. Feature Engineering / Model Training / Model Evaluation / Pipeline Execution
        3. Result Generation
    """

    def __init__(self) -> None:
        self.engine = DataScienceEngine()

    def analyze(self, request: DataScientistRequest) -> DataScientistReport:
        inputs: DataScientistInputs = request.inputs
        validation = self.engine.check_input_validation(inputs)

        if not validation["valid"]:
            logger.warning("Data Scientist validation failed: %s", validation["errors"])
            return DataScientistReport(
                request_id=request.request_id,
                training_summary=None,
                evaluations=[],
                feature_importance=[],
                pipeline_results=[],
                recommendations=validation["errors"],
                quality_score=0.0,
            )

        training_summary: TrainingSummary | None = None
        evaluations: list[ModelEvaluation] = []
        feature_importance: list[FeatureImportance] = []
        pipeline_results: list[PipelineResult] = []
        recommendations: list[str] = []

        if inputs.operation == DataScientistOperation.feature_engineering:
            pipeline_results = self.engine.engineer_features(inputs)
        elif inputs.operation == DataScientistOperation.model_training:
            training_summary = self.engine.train_model(inputs)
        elif inputs.operation == DataScientistOperation.model_evaluation:
            evaluations = self.engine.evaluate_model(inputs)
        elif inputs.operation == DataScientistOperation.pipeline_execution:
            pipeline_results = self.engine.engineer_features(inputs)
            training_summary = self.engine.train_model(inputs)
            evaluations = self.engine.evaluate_model(inputs)
            feature_importance = self.engine.compute_feature_importance(inputs)

        recommendations.extend(self.engine.safety_boundary_check())

        quality_score = self.engine.compute_quality_score(
            training_summary=training_summary,
            evaluations=evaluations,
            feature_importance=feature_importance,
            pipeline_results=pipeline_results,
        )

        return DataScientistReport(
            request_id=request.request_id,
            training_summary=training_summary,
            evaluations=evaluations,
            feature_importance=feature_importance,
            pipeline_results=pipeline_results,
            recommendations=recommendations,
            quality_score=quality_score,
        )
