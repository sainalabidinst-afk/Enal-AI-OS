from __future__ import annotations

from pathlib import Path

from backend.app.core.attachments.analyzer import analyze_attachment
from backend.app.core.attachments.detector import detect_from_content, detect_from_filename, summarize_archive
from backend.app.core.attachments.models import (
    AttachmentAnalysisResult,
    AttachmentMeta,
    AttachmentType,
)


MAX_ANALYSIS_TEXT = 1_000_000
MAX_ARCHIVE_MEMBERS = 200
ALLOWED_EXTENSIONS = {
    ".rsc", ".backup", ".export", ".cfg", ".conf", ".txt", ".cli", ".xml", ".json", ".yaml", ".yml",
    ".tf", ".ps1", ".sh", ".pdf", ".docx", ".xlsx", ".csv", ".pptx", ".drawio", ".vsdx", ".svg",
    ".png", ".jpg", ".jpeg", ".webp", ".bmp", ".zip", ".tar.gz", ".gz", ".log",
}


def validate_filename(filename: str) -> AttachmentMeta:
    meta = detect_from_filename(filename)
    ext = _extension_for(filename)
    if ext and ext not in ALLOWED_EXTENSIONS:
        meta.attachment_type = AttachmentType.unknown
        meta.parse_error = f"Unsupported extension: {ext}"
    return meta


def _make_infra(vendor, device_role, fmt, **kwargs):
    """Create InfrastructureAST inline to avoid import order issues."""
    import backend.app.core.attachments.models as m
    ast = m.InfrastructureAST(vendor=vendor, device_role=device_role, format=fmt)
    for k, v in kwargs.items():
        ast.metadata[k] = v
    return ast


def analyze_bytes(filename: str, content: bytes) -> AttachmentAnalysisResult:
    text = ""
    meta = validate_filename(filename)
    if meta.parse_error and meta.attachment_type == AttachmentType.unknown:
        try:
            text = content.decode("utf-8", errors="ignore")
            meta = detect_from_content(filename, text)
        except Exception as exc:
            ast = _make_infra(meta.vendor, meta.device_role, "")
            return AttachmentAnalysisResult(meta=meta, ast=ast, analysis_error=str(exc))
    else:
        text = _safe_decode(content)

    if meta.attachment_type in {AttachmentType.archive}:
        archive_summary = summarize_archive(content, filename)
        ast = _make_infra(meta.vendor, meta.device_role, "archive")
        ast.metadata.update(archive_summary)
        return AttachmentAnalysisResult(
            meta=meta,
            ast=ast,
            summary=f"Archive contains {archive_summary.get('member_count', 0)} items.",
            recommendations=["Extract archive before analysis if deeper inspection is needed."],
        )

    if meta.attachment_type == AttachmentType.image:
        ast = _make_infra(meta.vendor, meta.device_role, "image")
        return AttachmentAnalysisResult(
            meta=meta,
            ast=ast,
            summary="Image file detected. Screenshot/diagram analysis should be handled by image-capable models.",
            recommendations=["Route image to multimodal analysis if supported."],
        )

    if not text:
        ast = _make_infra(meta.vendor, meta.device_role, meta.detected_format)
        return AttachmentAnalysisResult(
            meta=meta,
            ast=ast,
            analysis_error="Unable to decode content for analysis.",
        )

    text = text[:MAX_ANALYSIS_TEXT]
    if meta.attachment_type == AttachmentType.document:
        ast = _make_infra(meta.vendor, meta.device_role, meta.detected_format, text_preview=text[:500])
        return AttachmentAnalysisResult(
            meta=meta,
            ast=ast,
            summary=f"Document detected ({filename}). Text extraction result may need document-aware parsing.",
            recommendations=["Use document-aware parsing for structured fields if needed."],
        )

    meta.text_preview = text[:1000]
    result = analyze_attachment(meta, text)
    return result


def analyze_multi(files: list[tuple[str, bytes]]) -> list[AttachmentAnalysisResult]:
    results: list[AttachmentAnalysisResult] = []
    for filename, content in files:
        results.append(analyze_bytes(filename, content))
    return results


def _extension_for(filename: str) -> str:
    lower = filename.lower()
    if lower.endswith(".tar.gz"):
        return ".tar.gz"
    return Path(filename).suffix.lower()


def _safe_decode(content: bytes) -> str:
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return content.decode("latin-1")
        except UnicodeDecodeError:
            return ""