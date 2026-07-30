import logging
from typing import Any

logger = logging.getLogger(__name__)


class CognitiveOrchestrator:
    def __init__(self):
        from backend.app.core.adaptive_runtime import adaptive_runtime
        from backend.app.core.meta_cognition import meta_cognition
        self.runtime = adaptive_runtime
        self.meta = meta_cognition

    async def process(self, user_input: str, project_id: str | None = None) -> dict[str, Any]:
        pipeline_selection = await self.meta.choose_pipeline(user_input)
        pipeline = pipeline_selection.get("pipeline")
        model = pipeline_selection.get("model")
        result = await self.runtime.execute(user_input, project_id, force_pipeline=pipeline)
        result["selected_model"] = model
        result["pipeline_selection_reason"] = pipeline_selection.get("reason")
        optimization = await self.meta.evaluate_and_optimize(user_input, result)
        result["meta_cognition"] = optimization
        return result


cognitive_orchestrator = CognitiveOrchestrator()
