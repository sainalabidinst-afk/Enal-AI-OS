import logging

from backend.app.core.cognitive.planner import planner

logger = logging.getLogger(__name__)


async def reviewer_node(state: dict) -> dict:
    task_results = state.get("task_results", [])
    if not task_results:
        return state

    last_result = task_results[-1]
    review = await planner.review_result(last_result["task"], last_result["result"])

    from langchain_core.messages import SystemMessage
    return {
        "messages": [SystemMessage(content=f"Review: {review}")],
        "final_result": last_result["result"],
        "current_agent": "reviewer",
    }
