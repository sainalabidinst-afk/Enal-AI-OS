import logging
from typing import Any
from backend.app.core.background_tasks import background_task_manager
from backend.app.core.workspace_service import workspace_service
from backend.app.core.observability import observability
from backend.app.core.state_recovery import state_recovery

logger = logging.getLogger(__name__)


class AIOrchestrator:
    def __init__(self):
        self.orchestrator = "ai-orchestrator"

    async def process_request(self, user_message: str, project_id: str | None = None) -> dict[str, Any]:
        project_id = project_id or "default"
        await workspace_service.add_memory(project_id, "last_user_message", {"message": user_message, "timestamp": str(__import__("datetime").datetime.utcnow())})
        trace_id = observability.start_trace(f"request-{project_id}")
        task_id = await background_task_manager.submit(
            name=f"process-{__import__('uuid').uuid4().hex[:8]}",
            agent="orchestrator",
            payload={"message": user_message, "project_id": project_id},
        )
        await state_recovery.save(project_id, "started", {"task_id": task_id, "message": user_message})
        return {"task_id": task_id, "status": "processing", "trace_id": trace_id, "message": "Request is being processed by AI agents."}

    async def get_result(self, task_id: str) -> dict[str, Any] | None:
        status = await background_task_manager.get_status(task_id)
        return status


ai_orchestrator = AIOrchestrator()
