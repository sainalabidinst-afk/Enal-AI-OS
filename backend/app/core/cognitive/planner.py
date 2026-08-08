import json
import logging

from backend.app.core.config import settings
from backend.app.core.model_router import model_router

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = (
    "You are an expert AI Planner. Your job is to analyze the user's request "
    "and create a structured plan.\n\n"
    "You have access to the following specialized agents:\n"
    "- planner: Breaks down complex tasks into subtasks\n"
    "- coding-agent: Writes and reviews code in multiple languages\n"
    "- research-agent: Gathers information from the web and documents\n"
    "- data-agent: Handles databases, data analysis, and migrations\n"
    "- ui-agent: Designs and builds user interfaces\n"
    "- trading-agent: Analyzes markets and executes trades\n"
    "- network-agent: Configures networking and security\n"
    "- writer-agent: Creates documentation and content\n"
    "- qa-agent: Tests and validates outputs\n"
    "- security-agent: Audits code and infrastructure\n"
    "- reviewer: Reviews and merges results\n\n"
    "For each request, output a JSON plan with:\n"
    "{\n"
    '  "description": "summary of the plan",\n'
    '  "agents": ["agent1", "agent2"],\n'
    '  "tasks": [\n'
    '    {"description": "task description", "agent": "agent_name"}\n'
    "  ]\n"
    "}\n\n"
    "Be thorough but concise. Only include necessary agents."
)


class Planner:
    async def create_plan(self, user_request: str) -> dict:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Create a plan for: {user_request}"},
        ]
        response = await model_router.acomplete(messages, model=settings.DEFAULT_REASONING_MODEL, temperature=0.3)
        content = response.choices[0].message.content
        try:
            plan = json.loads(content)
            return plan
        except json.JSONDecodeError:
            return {"description": "Direct response", "agents": ["planner"], "tasks": [{"description": user_request, "agent": "planner"}]}

    async def review_result(self, task_description: str, result: str) -> str:
        messages = [
            {"role": "system", "content": "You are a critical reviewer. Evaluate if the result adequately addresses the task. Output 'PASS' or 'FAIL' with brief reasoning."},
            {"role": "user", "content": f"Task: {task_description}\n\nResult:\n{result}"},
        ]
        response = await model_router.acomplete(messages, model=settings.DEFAULT_REASONING_MODEL, temperature=0.3)
        return response.choices[0].message.content


planner = Planner()
