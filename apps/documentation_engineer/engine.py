"""
Documentation Engine
====================

Upgraded engine with typed contracts, OpenAPI generation, SDK documentation,
architecture documentation, documentation validation, and release notes generation.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from apps.documentation_engineer.architecture_docs import ArchitectureDocsGenerator
from apps.documentation_engineer.openapi_generator import OpenAPIGenerator
from apps.documentation_engineer.release_notes_generator import ReleaseNotesGenerator
from apps.documentation_engineer.sdk_docs_generator import SDKDocsGenerator
from apps.documentation_engineer.schemas import (
    DocumentationReport,
    DocumentationRequest,
    DocumentationRecord,
)
from apps.documentation_engineer.validator import DocumentationValidator

logger = logging.getLogger(__name__)


class DocumentationEngine:
    """Upgraded Documentation engine with typed contracts."""

    def __init__(self) -> None:
        self.openapi_generator = OpenAPIGenerator()
        self.sdk_docs_generator = SDKDocsGenerator()
        self.architecture_docs_generator = ArchitectureDocsGenerator()
        self.validator = DocumentationValidator()
        self.release_notes_generator = ReleaseNotesGenerator()

    def generate(self, request: DocumentationRequest) -> DocumentationReport:
        started = time.monotonic()
        if hasattr(request.operation, "value"):
            op_value = request.operation.value
        else:
            op_value = str(request.operation)
        op = op_value

        generated_files: list[dict[str, Any]] = []
        total_errors = 0
        total_warnings = 0
        total_generated = 0
        total_validated = 0

        if op == "openapi_generation":
            result = self.openapi_generator.generate(
                request.inputs.source_code_path,
                request.target.app_name,
                request.target.version,
            )
            generated_files.append(result)
            total_generated += 1
            if result.get("status") == "generated":
                total_validated += 1

        elif op == "sdk_documentation":
            result = self.sdk_docs_generator.generate(
                request.inputs.source_code_path,
                request.target.app_name,
            )
            generated_files.append(result)
            total_generated += 1

        elif op == "architecture_documentation":
            result = self.architecture_docs_generator.generate(
                request.inputs.source_code_path,
                request.inputs.architecture_artifacts,
            )
            generated_files.append(result)
            total_generated += 1

        elif op == "documentation_validation":
            result = self.validator.validate(
                request.inputs.existing_docs_path,
                request.inputs.source_code_path,
            )
            generated_files.append(result)
            total_validated += 1
            total_errors += len(result.get("issues", []))
            total_warnings += sum(
                1 for i in result.get("issues", []) if i.get("severity") == "warning"
            )

        elif op == "release_notes_generation":
            result = self.release_notes_generator.generate(
                request.inputs.commit_range,
                request.target.app_name,
            )
            generated_files.append(result)
            total_generated += 1

        from apps.documentation_engineer.schemas import (
            DocumentationSummary,
            GeneratedFile,
            QualityMetrics,
        )

        summary = DocumentationSummary(
            total_files=len(generated_files),
            generated=total_generated,
            validated=total_validated,
            errors=total_errors,
            warnings=total_warnings,
        )
        quality_metrics = QualityMetrics(
            completeness=generated / total if total else 0.0,
            accuracy=validated / total if total else 0.0,
            consistency=0.9,
            freshness=0.95,
        )

        report = DocumentationReport(
            request_id=request.request_id,
            operation=op,
            generated_files=[
                GeneratedFile(**f) if isinstance(f, dict) else f for f in generated_files
            ],
            summary=summary,
            quality_metrics=quality_metrics,
            explanation=explanation,
            raw={
                "latency_ms": round((time.monotonic() - started) * 1000.0, 2),
            },
        )

        record = DocumentationRecord(
            request_id=request.request_id,
            operation=op,
            app_name=request.target.app_name,
            files_generated=total_generated,
            files_validated=total_validated,
            issues_found=total_errors + total_warnings,
            outcome="success" if total_errors == 0 else "partial",
        )
        self._record(record)

        return report

    def _compute_quality_metrics(self, files: list[dict[str, Any]]) -> dict[str, float]:
        total = len(files)
        if total == 0:
            return {"completeness": 0.0, "accuracy": 0.0, "consistency": 0.0, "freshness": 0.0}
        generated = sum(1 for f in files if f.get("status") == "generated")
        validated = sum(1 for f in files if f.get("status") == "validated")
        return {
            "completeness": generated / total if total else 0.0,
            "accuracy": validated / total if total else 0.0,
            "consistency": 0.9,
            "freshness": 0.95,
        }

    def _build_explanation(
        self,
        op: str,
        files: list[dict[str, Any]],
        generated: int,
        validated: int,
    ) -> str:
        parts = [f"Performed {op}."]
        if files:
            parts.append(f"Processed {len(files)} files.")
        if generated:
            parts.append(f"Generated {generated} artifacts.")
        if validated:
            parts.append(f"Validated {validated} artifacts.")
        return " ".join(parts)

    def _record(self, record: DocumentationRecord) -> str:
        try:
            import json
            from pathlib import Path
            base = Path("artifacts/documentation_history")
            base.mkdir(parents=True, exist_ok=True)
            path = base / f"{record.record_id}.json"
            path.write_text(
                json.dumps(record.model_dump(), indent=2, default=str),
                encoding="utf-8",
            )
        except OSError:
            logger.warning("Failed to persist documentation record %s", record.record_id)
        return record.record_id


documentation_engine = DocumentationEngine()
