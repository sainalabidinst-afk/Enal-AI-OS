import logging
from backend.app.core.cognitive.planner import planner as planner_module

logger = logging.getLogger(__name__)


async def planner_node(state: dict) -> dict:
    plan = await planner_module.create_plan(state["messages"][-1].content)
    from langchain_core.messages import SystemMessage
    return {
        "messages": [SystemMessage(content=f"Plan: {plan['description']}")],
        "plan": plan,
        "current_agent": "executor",
    }
