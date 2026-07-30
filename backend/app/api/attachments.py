from __future__ import annotations

import logging
import time
import uuid
from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile

from backend.app.core.attachments.analyzer import analyze_attachment, analyze_multi
from backend.app.core.attachments.diff_engine import ConfigurationDiffEngine
from backend.app.core.attachments.pipeline import validate_filename
from backend.app.core.telemetry.service import record_analysis_event
from backend.app.core.workspace_service import workspace_service

router = APIRouter()
logger = logging.getLogger(__name__)


def _safe_get(obj: Any, attr: str, default: Any = None) -> Any:
    if obj is None:
        return default
    return getattr(obj, attr, default)


@router.post("/attachments/upload")
async def upload_attachment(
    file: UploadFile = File(...),
    workspace_id: str | None = Form(None),
    conversation_id: str | None = Form(None),
    compliance_frameworks: list[str] | None = Query(default=None),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    validate_filename(file.filename)
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file upload")

    text = _decode(content)
    if not text:
        raise HTTPException(status_code=400, detail="Unsupported file content")

    started = time.perf_counter()
    status = "success"
    error = None
    analysis_id = str(uuid.uuid4())
    result = None

    try:
        meta = validate_filename(file.filename)
        result = analyze_attachment(meta, text, compliance_frameworks=compliance_frameworks)

        target_workspace = workspace_id or conversation_id
        if target_workspace:
            try:
                ws = await workspace_service.get_workspace(target_workspace)
                if ws:
                    await workspace_service.add_file(
                        target_workspace,
                        filename=file.filename,
                        path=f"/attachments/{file.filename}",
                        size=len(content),
                        metadata={
                            "attachment_type": _safe_get(_safe_get(result, "meta"), "attachment_type"),
                            "vendor": _safe_get(_safe_get(_safe_get(result, "meta"), "vendor"), "value"),
                            "device_role": _safe_get(_safe_get(_safe_get(result, "meta"), "device_role"), "value"),
                            "analysis": _safe_get(_safe_get(result, "ast"), "to_dict") and _safe_get(result, "ast", None).to_dict() or {},
                            "summary": _safe_get(result, "summary"),
                            "risk_score": _safe_get(result, "risk_score"),
                            "recommendations": _safe_get(result, "recommendations"),
                        },
                    )
            except Exception as exc:
                logger.warning("Attachment workspace attachment failed: %s", exc)
    except Exception as exc:
        status = "error"
        error = str(exc)
        logger.error("Attachment upload error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        total_ms = (time.perf_counter() - started) * 1000
        try:
            record_analysis_event(
                analysis_id=analysis_id,
                status=status,
                error=error,
                workspace_id=workspace_id or conversation_id or "",
                vendor=_safe_get(_safe_get(_safe_get(result, "meta"), "vendor"), "value") or "",
                device_type=_safe_get(_safe_get(_safe_get(result, "meta"), "device_role"), "value") or "",
                files=1,
                size_bytes=len(content),
                parser=_safe_get(_safe_get(result, "ast"), "format"),
                total_time_ms=round(total_ms, 2),
                findings=len(_safe_get(_safe_get(result, "ast"), "findings") or []),
                confidence=_safe_get(_safe_get(result, "meta"), "confidence"),
                compliance_score=_safe_get(result, "risk_score"),
                executive_report=bool(_safe_get(result, "summary")),
            )
        except Exception as telemetry_error:
            logger.debug("Analysis telemetry recording failed: %s", telemetry_error)

    payload: dict[str, Any] = {
        "filename": _safe_get(_safe_get(result, "meta"), "filename"),
        "attachment_type": _safe_get(_safe_get(_safe_get(result, "meta"), "attachment_type"), "value"),
        "vendor": _safe_get(_safe_get(_safe_get(result, "meta"), "vendor"), "value"),
        "device_role": _safe_get(_safe_get(_safe_get(result, "meta"), "device_role"), "value"),
        "format": _safe_get(_safe_get(result, "meta"), "detected_format"),
        "version": _safe_get(_safe_get(result, "meta"), "detected_version"),
        "confidence": _safe_get(_safe_get(result, "meta"), "confidence"),
        "summary": _safe_get(result, "summary"),
        "risk_score": _safe_get(result, "risk_score"),
        "recommendations": _safe_get(result, "recommendations"),
        "ast": _safe_get(_safe_get(result, "ast"), "to_dict") and _safe_get(_safe_get(result, "ast"), "to_dict")() or {},
    }
    if _safe_get(result, "analysis_error"):
        payload["analysis_error"] = _safe_get(result, "analysis_error")
    return payload


@router.post("/attachments/analyze")
async def analyze_attachments(
    files: list[UploadFile] = File(...),
    compliance_frameworks: list[str] | None = Query(default=None),
):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    items: list[tuple[str, bytes]] = []
    for upload in files:
        content_bytes = await upload.read()
        items.append((upload.filename or "unknown", content_bytes))

    started = time.perf_counter()
    status = "success"
    error = None
    analysis_id = str(uuid.uuid4())
    result = None

    try:
        result = analyze_multi(items, compliance_frameworks=compliance_frameworks)
        return {
            "count": len(items),
            "summary": _safe_get(result, "summary"),
            "risk_score": _safe_get(result, "risk_score"),
            "recommendations": _safe_get(result, "recommendations"),
            "ast": _safe_get(_safe_get(result, "ast"), "to_dict") and _safe_get(result, "ast").to_dict() or {},
            "analysis_error": _safe_get(result, "analysis_error"),
        }
    except Exception as exc:
        status = "error"
        error = str(exc)
        logger.error("Attachment analyze error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        total_ms = (time.perf_counter() - started) * 1000
        try:
            record_analysis_event(
                analysis_id=analysis_id,
                status=status,
                error=error,
                files=len(items),
                size_bytes=sum(len(item[1]) for item in items),
                total_time_ms=round(total_ms, 2),
                findings=len(_safe_get(_safe_get(result, "ast"), "findings") or []),
                confidence=_safe_get(_safe_get(result, "meta"), "confidence"),
                executive_report=bool(_safe_get(result, "summary")),
            )
        except Exception as telemetry_error:
            logger.debug("Analysis telemetry recording failed: %s", telemetry_error)


@router.post("/attachments/diff")
async def diff_attachments(
    before: UploadFile = File(...),
    after: UploadFile = File(...),
):
    before_content = await before.read()
    after_content = await after.read()
    before_text = _decode(before_content)
    after_text = _decode(after_content)
    if not before_text or not after_text:
        raise HTTPException(status_code=400, detail="Both files must be readable text")

    started = time.perf_counter()
    status = "success"
    error = None
    analysis_id = str(uuid.uuid4())

    try:
        diff_result = ConfigurationDiffEngine().diff(before_text, after_text)
        return {
            "summary": diff_result.summary,
            "overall_risk": diff_result.overall_risk,
            "rollback_available": diff_result.rollback_available,
            "diffs": [
                {
                    "section": item.section,
                    "change_type": item.change_type,
                    "before": item.before,
                    "after": item.after,
                    "risk": item.risk,
                    "risk_score": item.risk_score,
                    "recommendation": item.recommendation,
                    "rollback": item.rollback,
                    "evidence": item.evidence,
                }
                for item in diff_result.diffs
            ],
        }
    except Exception as exc:
        status = "error"
        error = str(exc)
        logger.error("Attachment diff error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        total_ms = (time.perf_counter() - started) * 1000
        try:
            record_analysis_event(
                analysis_id=analysis_id,
                status=status,
                error=error,
                total_time_ms=round(total_ms, 2),
                files=2,
            )
        except Exception as telemetry_error:
            logger.debug("Analysis telemetry recording failed: %s", telemetry_error)


def _decode(content: bytes) -> str:
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return content.decode("latin-1")
        except UnicodeDecodeError:
            return ""
