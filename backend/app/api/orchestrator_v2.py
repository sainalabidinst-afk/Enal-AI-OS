from fastapi import APIRouter, HTTPException
from backend.app.models.schemas import ChatRequest
from backend.app.agents.orchestrator_v2 import ai_orchestrator

router = APIRouter()


@router.post("/v2/chat")
async def chat_v2(request: ChatRequest):
    try:
        result = await ai_orchestrator.process_request(request.message, request.conversation_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/v2/tasks/{task_id}")
async def get_task_status(task_id: str):
    result = await ai_orchestrator.get_result(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result
