from __future__ import annotations

import json
import logging
import time
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from backend.app.core.execution_integration import execution_integration
from backend.app.core.telemetry.service import record_chat_event
from backend.app.core.workspace_service import workspace_service

from ..models.schemas import ChatRequest, ChatResponse
from ..models.schemas_execution import ExecutionSession

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    started = time.perf_counter()
    chat_id = str(uuid.uuid4())
    conversation_id = request.conversation_id or str(uuid.uuid4())
    workspace_id = request.workspace_id or conversation_id
    status = "success"
    error = None

    try:
        ws = await workspace_service.get_workspace(workspace_id)
        if not ws:
            ws = await workspace_service.create_workspace(name=f"Chat {conversation_id[:8]}")

        from apps.society.conversation_manager import conversation_manager

        analysis_payload: dict[str, Any] | None = None
        try:
            response = await conversation_manager.send_message(
                conversation_id=conversation_id,
                user_message=request.message,
            )
            execution: ExecutionSession | None = None
            if response.get("execution"):
                execution = response["execution"]
            elif _looks_like_goal(request.message):
                execution = await execution_integration.execute(
                    goal=request.message,
                    workspace_id=workspace_id,
                    conversation_id=conversation_id,
                )

            message = response.get("message", "")
            tasks_completed = 0
            if execution:
                tasks_completed = len(getattr(execution, "phases", []) or [])
                ws = await workspace_service.get_workspace(workspace_id)
                if ws:
                    ws.execution_ids.append(execution.id)

            metadata = {
                "domain": response.get("domain"),
                "events": response.get("events", []),
                "intent": response.get("metadata", {}).get("intent"),
                "workspace_id": workspace_id,
                "execution_id": getattr(execution, "id", None),
            }
            if response.get("analysis"):
                analysis_payload = response["analysis"]
            return ChatResponse(
                message=message,
                conversation_id=response["conversation_id"],
                agent="ecp",
                tasks_completed=tasks_completed,
                metadata=metadata,
                analysis=analysis_payload,
            )
        except Exception as e:
            status = "error"
            error = str(e)
            logger.error(f"Chat error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    finally:
        total_ms = (time.perf_counter() - started) * 1000
        try:
            record_chat_event(
                chat_id=chat_id,
                conversation_id=conversation_id,
                workspace_id=workspace_id,
                status=status,
                error=error,
                message_length=len(request.message or ""),
                total_time_ms=round(total_ms, 2),
            )
        except Exception as telemetry_error:
            logger.debug("Chat telemetry recording failed: %s", telemetry_error)


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str) -> dict[str, Any]:
    from apps.society.conversation_manager import conversation_manager
    messages = await conversation_manager.get_history(conversation_id)
    return {"conversation_id": conversation_id, "messages": messages}


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str) -> dict[str, Any]:
    from apps.society.conversation_manager import conversation_manager
    await conversation_manager.clear_history(conversation_id)
    return {"deleted": True}


@router.get("/chat/stream")
async def chat_stream(
    message: str = Query(...),
    conversation_id: str | None = None,
    workspace_id: str | None = None,
):
    from apps.society.conversation_manager import conversation_manager

    conversation_id = conversation_id or str(uuid.uuid4())
    workspace_id = workspace_id or conversation_id

    ws = await workspace_service.get_workspace(workspace_id)
    if not ws:
        ws = await workspace_service.create_workspace(name=f"Chat {conversation_id[:8]}")

    async def event_generator():
        try:
            execution_promise = None
            async for event in conversation_manager.stream_message(
                conversation_id=conversation_id,
                user_message=message,
            ):
                yield f"data: {json.dumps(event)}\n\n"
                if event.get("type") == "final":
                    if _looks_like_goal(message) and execution_promise is None:
                        execution_promise = execution_integration.execute(
                            goal=message,
                            workspace_id=workspace_id,
                            conversation_id=conversation_id,
                        )

            if execution_promise is not None:
                try:
                    execution = await execution_promise
                    yield f"data: {json.dumps({'type': 'execution_started', 'execution_id': execution.id, 'goal': execution.goal})}\n\n"
                    ws = await workspace_service.get_workspace(workspace_id)
                    if ws:
                        ws.execution_ids.append(execution.id)
                    for phase in execution.phases:
                        yield f"data: {json.dumps({'type': 'phase', 'phase_id': phase.get('id'), 'name': phase.get('name'), 'status': phase.get('status')})}\n\n"
                    for log in getattr(execution, "logs", []) or []:
                        yield f"data: {json.dumps({'type': 'log', 'level': log.get('level'), 'message': log.get('message')})}\n\n"
                    for artifact_id in getattr(execution, "artifacts", []) or []:
                        art = await __import__('backend.app.core.artifact_service', fromlist=['artifact_service']).artifact_service.get_artifact(artifact_id)
                        if art:
                            yield f"data: {json.dumps({'type': 'artifact', 'artifact_id': art.id, 'name': art.name, 'artifact_type': art.type})}\n\n"
                    yield f"data: {json.dumps({'type': 'execution_complete', 'execution_id': execution.id, 'progress': getattr(execution, 'progress', 100.0)})}\n\n"
                except Exception as exc:
                    yield f"data: {json.dumps({'type': 'error', 'message': str(exc)})}\n\n"
        except Exception as exc:
            yield f"data: {json.dumps({'type': 'error', 'message': str(exc)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


def _looks_like_goal(message: str) -> bool:
    goal_keywords = [
        "bangun", "build", "audit", "review", "scan", "create", "generate",
        "deploy", "setup", "install", "configure", "analisa", "analysis",
    ]
    lowered = message.lower()
    return any(keyword in lowered for keyword in goal_keywords)
