import logging

from backend.app.core.config import settings
from backend.app.core.model_router import model_router
from backend.app.core.tool_registry import tool_registry
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


async def executor_node(state: dict) -> dict:
    plan = state.get("plan", {})
    tasks = plan.get("tasks", [])
    if not tasks:
        from langchain_core.messages import HumanMessage
        messages = state.get("messages", [])
        last_msg = messages[-1].content if messages else ""
        response = model_router.complete(messages + [HumanMessage(content=f"Execute: {last_msg}")])
        return {
            "messages": [response.choices[0].message],
            "final_result": response.choices[0].message.content,
            "task_results": [{"task": last_msg, "result": response.choices[0].message.content}],
            "current_agent": "executor",
        }

    agent_tools = tool_registry.get_tools(tasks[0].get("agent", "planner"))
    llm = ChatOpenAI(model=settings.DEFAULT_MODEL, temperature=settings.TEMPERATURE).bind_tools(agent_tools)

    from langchain_core.messages import HumanMessage
    messages = state.get("messages", [])
    prompt = f"You are the executor. Complete this task: {tasks[0]['description']}"
    response = llm.invoke([HumanMessage(content=prompt)] + list(messages))

    return {
        "messages": [response],
        "task_results": state.get("task_results", []) + [{"task": tasks[0]["description"], "result": response.content}],
        "current_agent": "executor",
    }
