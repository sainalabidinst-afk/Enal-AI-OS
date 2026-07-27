from fastapi import APIRouter, HTTPException
from backend.app.models.schemas import ChatRequest
from backend.app.agents.orchestrator_v2 import ai_orchestrator

router = APIRouter()


@router.post("/v2/chat")
async def chat_v2(request: ChatRequest):
    try:
        result = await ai_orchestrator.orchestrate_goal(
            goal=request.message,
            context={"conversation_id": request.conversation_id},
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/v2/tasks/{task_id}")
async def get_task_status(task_id: str):
    session = ai_orchestrator._active_sessions.get(task_id)
    if not session:
        raise HTTPException(status_code=404, detail="Task not found")
    return session
