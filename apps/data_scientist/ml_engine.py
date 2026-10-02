"""
Data Scientist — ML Pipeline Engine.
"""

from __future__ import annotations

import hashlib
import logging
import time
from typing import Any

from apps.data_scientist.schemas import (
    BusinessContext,
    DataScienceConfig,
    FeatureEngineeringResult,
    HyperparameterResult,
    MLAlgorithm,
    MLTask,
    ModelConfig,
    ModelEvaluationResult,
    ModelTrainingResult,
)

logger = logging.getLogger(__name__)


class MLPipelineEngine:
    """
    Provides feature engineering, model training, evaluation, and hyperparameter
    tuning for advanced machine learning pipelines.
    """

    ALGORITHM_CHARACTERISTICS: dict[MLAlgorithm, dict[str, Any]] = {
        MLAlgorithm.random_forest: {
            "strengths": ["handles_nonlinearity", "robust_to_outliers"],
            "best_for": [MLTask.classification, MLTask.regression],
            "n_estimators_range": [50, 100, 200],
        },
        MLAlgorithm.gradient_boosting: {
            "strengths": ["high_accuracy", "handles_missing"],
            "best_for": [MLTask.classification, MLTask.regression],
            "n_estimators_range": [50, 100, 200],
        },
        MLAlgorithm.logistic_regression: {
            "strengths": ["interpretable", "fast"],
            "best_for": [MLTask.classification],
            "n_estimators_range": [1],
        },
        MLAlgorithm.neural_network: {
            "strengths": ["handles_complex_patterns"],
            "best_for": [MLTask.classification, MLTask.regression, MLTask.time_series_forecasting],
            "n_estimators_range": [1],
        },
        MLAlgorithm.kmeans: {
            "strengths": ["unsupervised", "fast_clustering"],
            "best_for": [MLTask.clustering],
            "n_estimators_range": [1],
        },
        MLAlgorithm.arima: {
            "strengths": ["time_series"],
            "best_for": [MLTask.time_series_forecasting],
            "n_estimators_range": [1],
        },
        MLAlgorithm.prophet: {
            "strengths": ["trend_decomposition", "handles_seasonality"],
            "best_for": [MLTask.time_series_forecasting],
            "n_estimators_range": [1],
        },
    }

    def engineer_features(self, config: DataScienceConfig) -> FeatureEngineeringResult:
        """Perform feature engineering on configured features."""
        transformations = []
        generated = []
        for feature in config.features:
            t = feature.transformation
            if t != "none":
                transformations.append(f"{feature.name}:{t}")
            if t in ("polynomial", "interaction"):
                generated.extend([
                    f"{feature.name}_squared",
                    f"{feature.name}_interaction",
                ])
            elif t == "binning":
                generated.append(f"{feature.name}_binned")
            elif t == "scaling":
                generated.append(f"{feature.name}_scaled")
            elif t == "encoding":
                generated.extend([
                    f"{feature.name}_encoded_0",
                    f"{feature.name}_encoded_1",
                ])

        original = len(config.features)
        engineered = len(generated)
        confidence = min(1.0, round(0.95 - original * 0.01, 2))

        return FeatureEngineeringResult(
            original_features=original,
            engineered_features=engineered,
            generated_features=generated,
            transformations_applied=transformations,
            confidence=confidence,
        )

    def train_model(
        self, config: DataScienceConfig, context: BusinessContext
    ) -> list[ModelTrainingResult]:
        """Train model(s) based on the configured algorithm and task."""
        results = []
        model = config.model or ModelConfig(
            algorithm=MLAlgorithm.random_forest,
            task=config.task,
        )

        total_samples = sum(d.n_samples for d in config.datasets)
        training_start = time.monotonic()

        # Simulate training time.
        training_time = round(
            1.5 + (total_samples / 10000.0) * 0.5 + len(config.features) * 0.1, 2
        )

        model_id = hashlib.md5(
            f"{model.algorithm.value}-{context.project_name}".encode()
        ).hexdigest()[:12]

        feature_importance = self._compute_feature_importance(model, config)

        results.append(ModelTrainingResult(
            algorithm=model.algorithm,
            model_id=model_id,
            training_samples=total_samples,
            training_time_seconds=round(time.monotonic() - training_start + training_time, 2),
            feature_importance=feature_importance,
            confidence=min(1.0, round(0.85 + training_time / 100.0, 2)),
        ))

        logger.info("Trained model %s with %d samples", model_id, total_samples)
        return results

    def evaluate_model(
        self, config: DataScienceConfig, training_results: list[ModelTrainingResult]
    ) -> list[ModelEvaluationResult]:
        """Evaluate trained models and compute metrics."""
        results = []
        for train_result in training_results:
            metrics = self._compute_metrics(train_result.algorithm, config.task)
            overfit_risk = self._assess_overfit(metrics, config.task)

            results.append(ModelEvaluationResult(
                model_id=train_result.model_id,
                task=config.task,
                metrics=metrics,
                confusion_matrix=(
                    self._build_confusion_matrix(metrics)
                    if config.task == MLTask.classification
                    else {}
                ),
                classification_report=(
                    self._build_classification_report(metrics)
                    if config.task == MLTask.classification
                    else {}
                ),
                overfit_risk=overfit_risk,
            ))
        return results

    def tune_hyperparameters(
        self, config: DataScienceConfig
    ) -> HyperparameterResult:
        """Perform hyperparameter tuning (grid search simulation)."""
        model = config.model or ModelConfig(
            algorithm=MLAlgorithm.random_forest,
            task=config.task,
        )
        search_space_size = 1
        for v in self.ALGORITHM_CHARACTERISTICS.get(model.algorithm, {}).get(
            "n_estimators_range", [100]
        ):
            if isinstance(v, list):
                search_space_size *= len(v)

        best_params = dict(model.hyperparameters) or {"n_estimators": 100, "max_depth": 10}
        best_score = round(0.88 - search_space_size * 0.01, 3)
        if best_score < 0.7:
            best_score = 0.7

        return HyperparameterResult(
            model_id=hashlib.md5(
                f"{model.algorithm.value}-tuned".encode()
            ).hexdigest()[:12],
            best_params=best_params,
            best_score=best_score,
            search_space_size=search_space_size,
            iterations=search_space_size,
        )

    def _compute_feature_importance(
        self, model: ModelConfig, config: DataScienceConfig
    ) -> dict[str, float]:
        """Compute deterministic feature importance scores."""
        importance = {}
        base = 1.0 / max(len(config.features), 1)
        for i, feature in enumerate(config.features):
            importance[feature.name] = round(base + (i * 0.05) % 0.3, 3)
        return importance

    def _compute_metrics(self, algorithm: MLAlgorithm, task: MLTask) -> dict[str, float]:
        """Compute synthetic metrics for evaluation."""
        base = {
            MLTask.classification: {"accuracy": 0.91, "precision": 0.89, "recall": 0.88, "f1": 0.88},  # noqa: E501
            MLTask.regression: {"r2": 0.85, "mae": 2.3, "rmse": 3.7, "mape": 0.12},  # noqa: E501
            MLTask.clustering: {"silhouette": 0.62, "inertia": 142.5, "calinski_harabasz": 320.0},  # noqa: E501
            MLTask.time_series_forecasting: {"mape": 0.08, "smape": 0.09, "rmse": 1.2, "mae": 0.8},
        }
        return dict(base.get(task, {"score": 0.85}))

    def _assess_overfit(self, metrics: dict[str, float], task: MLTask) -> str:
        """Assess overfitting risk from metrics."""
        if task == MLTask.classification:
            score_key = "f1"
        elif task == MLTask.regression:
            score_key = "r2"
        else:
            score_key = "silhouette"
        score = metrics.get(score_key, 0.85)
        if score < 0.7:
            return "high"
        if score < 0.85:
            return "medium"
        return "low"

    def _build_confusion_matrix(self, metrics: dict[str, float]) -> dict[str, Any]:
        """Build a synthetic confusion matrix for classification."""
        correct = int(metrics.get("accuracy", 0.9) * 100)
        return {
            "true_positive": correct * 50 // 100,
            "false_positive": 100 - correct * 50 // 100,
            "true_negative": correct * 50 // 100,
            "false_negative": 100 - correct * 50 // 100,
        }

    def _build_classification_report(self, metrics: dict[str, float]) -> dict[str, Any]:
        """Build a synthetic classification report."""
        return {
            "macro_avg": {
                "precision": metrics.get("precision", 0.89),
                "recall": metrics.get("recall", 0.88),
            },
            "weighted_avg": {"f1-score": metrics.get("f1", 0.88)},
        }


__all__ = ["MLPipelineEngine"]
