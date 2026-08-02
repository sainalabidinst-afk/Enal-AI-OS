"""
Data Engineer — Domain Engine orchestrator.

Orchestrates the full data engineering pipeline:
    1. ETL/ELT Pipeline (source ingestion + transformation + loading)
    2. Data Cleaning (missing values, duplicates, outliers, format issues)
    3. Dataset Validation (schema, integrity, quality checks)
    4. Schema Evolution (drift detection, migration plan)
    5. Feature Engineering (derived features with lineage)
    6. Time Series Handling (interpolation, resampling, alignment)
    7. Data Quality Assurance (completeness, uniqueness, validity, freshness, consistency)

All business logic resides here (per ADR-004). The Worker is a thin
adapter (per ADR-003).
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any

from apps.data_engineer.schemas import (
    DataEngineeringRequest,
    DataEngineeringReport,
    DataQualityRecord,
    DatasetSummary,
    QualityReport,
    QualityIssue,
    IssueSeverity,
    SchemaDriftReport,
    SchemaChange,
    ChangeType,
    TimeSeriesReport,
    DataLineage,
    JobStatus,
    IssueType,
    JobType,
)
from apps.data_engineer.etl_pipeline import ETLPipeline
from apps.data_engineer.cleaner import DataCleaner
from apps.data_engineer.validator import DatasetValidator
from apps.data_engineer.schema_evolver import SchemaEvolver
from apps.data_engineer.feature_store import FeatureStore
from apps.data_engineer.time_series import TimeSeriesHandler
from apps.data_engineer.quality_assurance import DataQualityAssurance

logger = logging.getLogger(__name__)


class DataEngineerEngine:
    """
    Orchestrates the full data engineering pipeline.

    Public API::

        engine = DataEngineerEngine()
        report = engine.process(request)
    """

    def __init__(self) -> None:
        self.etl = ETLPipeline()
        self.cleaner = DataCleaner()
        self.validator = DatasetValidator()
        self.schema_evolver = SchemaEvolver()
        self.feature_store = FeatureStore()
        self.time_series = TimeSeriesHandler()
        self.quality = DataQualityAssurance()

    def process(self, request: DataEngineeringRequest) -> DataEngineeringReport:
        """
        Run the data engineering pipeline based on job_type.

        Args:
            request: DataEngineeringRequest with source, operations, quality rules.

        Returns:
            DataEngineeringReport with dataset summary, quality report, features, etc.
        """
        started = time.monotonic()
        source = request.source
        source_data = self.etl.extract(source)

        # Apply ETL or ELT.
        if request.job_type in (JobType.etl, JobType.elt):
            transformed = self.etl.transform(source_data, request.operations)
            loaded = self.etl.load(transformed, request.target_schema)
            working_data = loaded
        else:
            working_data = source_data

        # Cleaning.
        cleaned_data, cleaning_issues = self.cleaner.clean(working_data, request.operations)

        # Dataset Validation.
        validation_result = self.validator.validate(
            cleaned_data, request.source.schema_definition, request.quality_rules
        )

        # Schema Evolution (if schema_evolve job).
        schema_drift = SchemaDriftReport()
        if request.job_type == JobType.schema_evolve:
            schema_drift = self.schema_evolver.detect_drift(
                cleaned_data, request.source.schema_definition, request.target_schema
            )

        # Feature Engineering.
        features = self.feature_store.generate(
            cleaned_data, request.feature_definitions
        )

        # Time Series Handling.
        ts_report = TimeSeriesReport()
        if request.job_type == JobType.time_series and request.time_series_config:
            ts_report = self.time_series.handle(
                cleaned_data, request.time_series_config
            )

        # Data Quality Assurance.
        quality_report = self.quality.assess(
            cleaned_data, validation_result, cleaning_issues, request.quality_rules
        )

        # Build dataset summary.
        dataset_summary = DatasetSummary(
            row_count=len(cleaned_data) if isinstance(cleaned_data, list) else 1,
            column_count=len(cleaned_data[0].keys()) if isinstance(cleaned_data, list) and cleaned_data else 0,
            schema_definition=request.source.schema_definition or {},
            quality_score=quality_report.overall_score,
        )

        # Build lineage.
        lineage = DataLineage(
            source=source.location,
            transforms=[op.operation.value for op in request.operations],
            target=f"output_{request.job_id[:8]}",
        )

        # Determine status.
        status = JobStatus.success
        if quality_report.issues and any(i.severity in (IssueSeverity.critical, IssueSeverity.high) for i in quality_report.issues):
            status = JobStatus.partial
        if not cleaned_data or (isinstance(cleaned_data, list) and len(cleaned_data) == 0):
            status = JobStatus.failed

        report = DataEngineeringReport(
            job_id=request.job_id,
            job_type=request.job_type.value,
            status=status,
            dataset=dataset_summary,
            quality_report=quality_report,
            schema_drift=schema_drift,
            features=features,
            time_series=ts_report,
            lineage=lineage,
            execution_time_ms=int((time.monotonic() - started) * 1000),
            explanation=f"Processed {request.job_type.value} job. "
                        f"Quality score: {quality_report.overall_score:.0%}. "
                        f"Issues: {len(quality_report.issues)}.",
            raw={
                "issues_found": len(quality_report.issues),
                "features_created": len(features),
                "cleaning_issues_count": len(cleaning_issues),
            },
        )

        # Record to Experience Memory.
        record = DataQualityRecord(
            job_id=request.job_id,
            job_type=request.job_type.value,
            quality_score=quality_report.overall_score,
            issues_found=len(quality_report.issues),
            issues_resolved=len([i for i in quality_report.issues if i.count == 0 or i.severity == IssueSeverity.low]),
            schema_drift_detected=schema_drift.detected,
            features_created=len(features),
            time_series_gaps_filled=ts_report.interpolated_count,
            outcome=status.value,
        )
        self._record(record)

        return report

    def _record(self, record: DataQualityRecord) -> str:
        """Record to in-memory store (Experience Memory interface)."""
        try:
            base = Path("artifacts/data_quality_history")
            base.mkdir(parents=True, exist_ok=True)
            path = base / f"{record.record_id}.json"
            path.write_text(
                json.dumps(record.model_dump(), indent=2, default=str),
                encoding="utf-8",
            )
        except OSError:
            logger.warning("Failed to persist data quality record %s", record.record_id)
        return record.record_id


# Fix import.
