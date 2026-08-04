"""
Data Engineer Worker — thin adapter (per ADR-003).

Routes task requests to the Data Engineer Domain Engine.
Does not own business logic; delegates to DataEngineerEngine.
"""

from __future__ import annotations

from typing import Any

from apps.data_engineer.engine import DataEngineerEngine
from apps.data_engineer.schemas import (
    DataEngineeringRequest,
    DataSource,
    TransformOperation,
    QualityRuleSpec,
    FeatureSpec,
    JobType,
)


class DataEngineerWorker:
    """
    Thin Worker adapter for the Data Engineer Capability Pack.

    Responsibilities:
        - Parse incoming task into DataEngineeringRequest
        - Delegate to DataEngineerEngine.process()
        - Return DataEngineeringReport as dict

    Usage::

        worker = DataEngineerWorker()
        report = await worker.execute(task)
    """

    def __init__(self, engine: DataEngineerEngine | None = None) -> None:
        self._engine = engine or DataEngineerEngine()

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a data engineering task.

        Expected task format::

            {
                "job_type": "etl",
                "source": {"type": "csv", "location": "data/input.csv", "schema": {...}},
                "operations": [{"operation": "drop_duplicates", "parameters": {}}],
                "quality_rules": [{"rule": "completeness", "thresholds": {"min": 0.8}}],
                "feature_definitions": [...]
            }

        Returns:
            DataEngineeringReport as a JSON-serializable dict.
        """
        source_dict = task.get("source", {})
        source = DataSource(
            type=source_dict.get("type", "csv"),
            location=source_dict.get("location", ""),
            schema_definition=source_dict.get("schema_definition") or source_dict.get("schema"),
        )

        job_type_raw = task.get("job_type", "etl")
        try:
            job_type = JobType(job_type_raw)
        except ValueError:
            job_type = JobType.etl

        operations = [
            TransformOperation(
                operation=op.get("operation", "fill_missing"),
                parameters=op.get("parameters", {}),
            )
            for op in task.get("operations", [])
        ]

        quality_rules = [
            QualityRuleSpec(
                rule=qr.get("rule", "completeness"),
                thresholds=qr.get("thresholds", {}),
            )
            for qr in task.get("quality_rules", [])
        ]

        feature_defs = [
            FeatureSpec(**fd) for fd in task.get("feature_definitions", [])
        ]

        request = DataEngineeringRequest(
            job_type=job_type,
            source=source,
            operations=operations,
            quality_rules=quality_rules,
            target_schema=task.get("target_schema"),
            time_series_config=task.get("time_series_config"),
            feature_definitions=feature_defs,
        )

        report = self._engine.process(request)
        return report.to_dict()
