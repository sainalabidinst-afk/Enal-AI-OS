from __future__ import annotations

from backend.app.core.attachments.models import (
    AttachmentAnalysisResult,
    AttachmentMeta,
    InfrastructureAST,
    AttachmentType,
)
from backend.app.core.attachments.parsers.registry import parser_registry
from backend.app.core.attachments.reasoning import InfrastructureReasoningEngine
from backend.app.core.attachments.report import ExecutiveReportGenerator


def analyze_attachment(meta: AttachmentMeta, content: str, compliance_frameworks: list[str] | None = None) -> AttachmentAnalysisResult:
    try:
        ast = parser_registry.parse(meta, content)
        ast.metadata["detected_filename"] = meta.filename
        ast.metadata["detected_type"] = meta.attachment_type.value
        ast.metadata["content_length"] = len(content)
    except Exception as exc:
        return AttachmentAnalysisResult(meta=meta, ast=InfrastructureAST(), analysis_error=str(exc))

    frameworks = None
    if compliance_frameworks:
        from backend.app.core.attachments.compliance import ComplianceFramework
        frameworks = [ComplianceFramework(value) for value in compliance_frameworks if value in ComplianceFramework.__members__]

    reasoning_result = InfrastructureReasoningEngine().reason(ast, compliance_frameworks=frameworks)
    ExecutiveReportGenerator().generate(reasoning_result)

    return AttachmentAnalysisResult(
        meta=meta,
        ast=reasoning_result.ast,
        summary=reasoning_result.executive_summary,
        risk_score=reasoning_result.risk_assessment.risk_score if reasoning_result.risk_assessment else 0.0,
        recommendations=reasoning_result.recommendations,
    )


def analyze_multi(files: list[tuple[str, bytes]], compliance_frameworks: list[str] | None = None) -> AttachmentAnalysisResult:
    from backend.app.core.attachments.cross_file import CrossFileReasoningEngine

    all_results: list[AttachmentAnalysisResult] = []
    for filename, content in files:
        text = _safe_decode(content)
        if not text:
            continue
        meta = _detect_meta(filename, text)
        result = analyze_attachment(meta, text, compliance_frameworks=compliance_frameworks)
        all_results.append(result)

    if not all_results:
        return AttachmentAnalysisResult(meta=AttachmentMeta(filename="multi-file", attachment_type=AttachmentType.unknown), ast=InfrastructureAST(), analysis_error="No readable files")

    combined_ast = CrossFileReasoningEngine().cross_reason([r.ast for r in all_results])
    
    frameworks = None
    if compliance_frameworks:
        from backend.app.core.attachments.compliance import ComplianceFramework
        frameworks = [ComplianceFramework(value) for value in compliance_frameworks if value in ComplianceFramework.__members__]
    
    reasoning_result = InfrastructureReasoningEngine().reason(combined_ast, compliance_frameworks=frameworks)

    return AttachmentAnalysisResult(
        meta=all_results[0].meta,
        ast=reasoning_result.ast,
        summary=reasoning_result.executive_summary or "Multi-file analysis completed.",
        risk_score=reasoning_result.risk_assessment.risk_score if reasoning_result.risk_assessment else 0.0,
        recommendations=reasoning_result.recommendations,
    )


def _detect_meta(filename: str, text: str) -> AttachmentMeta:
    from backend.app.core.attachments.detector import detect_from_content
    return detect_from_content(filename, text)


def _safe_decode(content: bytes) -> str:
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return content.decode("latin-1")
        except UnicodeDecodeError:
            return ""


def _summarize(ast: InfrastructureAST) -> str:
    return (
        f"Detected {ast.vendor.value} {ast.format or 'configuration'} "
        f"with {len(ast.interfaces)} interface entries, "
        f"{len(ast.firewall)} firewall entries, "
        f"{len(ast.routing)} routing entries, "
        f"and {len(ast.findings)} findings."
    )
