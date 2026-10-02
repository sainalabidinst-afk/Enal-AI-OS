"""
Data Scientist Engine.
"""

from __future__ import annotations

import logging

from apps.data_scientist.ml_engine import MLPipelineEngine
from apps.data_scientist.schemas import (
    DataScienceConfig,
    DataScienceReport,
    DataScienceRequest,
)

logger = logging.getLogger(__name__)


class DataScientistEngine:
    """
    Orchestrates the data science ML pipeline:
        1. Feature Engineering
        2. Model Training
        3. Model Evaluation
        4. Hyperparameter Tuning
    """

    def __init__(self) -> None:
        self.engine = MLPipelineEngine()

    def execute(self, request: DataScienceRequest) -> DataScienceReport:
        config: DataScienceConfig = request.inputs
        context = request.business_context

        feature_results = [self.engine.engineer_features(config)] if config.features else []

        training_results = self.engine.train_model(config, context)
        evaluation_results = self.engine.evaluate_model(config, training_results)

        hyperparameter_results = []
        if config.operation == "hyperparameter_tuning":
            hyperparameter_results.append(self.engine.tune_hyperparameters(config))

        # Aggregate quality score from evaluation metrics.
        score_keys = ["f1", "r2", "silhouette", "mape"]
        quality_scores: list[float] = []
        for ev in evaluation_results:
            metrics = ev.metrics
            for key in score_keys:
                if key in metrics:
                    val = metrics[key]
                    # mape is an error metric (lower is better); convert.
                    quality_scores.append(1.0 - val if key == "mape" else val)
                    break
        if quality_scores:
            quality_score = round(sum(quality_scores) / len(quality_scores), 3)
        else:
            quality_score = 0.75

        return DataScienceReport(
            request_id=request.request_id,
            operation=config.operation,
            feature_results=feature_results,
            training_results=training_results,
            evaluation_results=evaluation_results,
            hyperparameter_results=hyperparameter_results,
            quality_score=quality_score,
        )


__all__ = ["DataScientistEngine"]
