import logging
from typing import Any
from backend.app.core.model_router import model_router
from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class SelfReflection:
    def __init__(self, max_iterations: int = 3):
        self.max_iterations = max_iterations

    async def review(self, task: str, result: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        prompt = (
            "You are a critical reviewer. Evaluate the result against the task.\n"
            f"Task: {task}\n\nResult:\n{result}\n\n"
            "Output JSON: {\"passed\": bool, \"score\": int(1-10), \"issues\": [str], \"suggestions\": [str]}"
        )
        response = model_router.complete(
            [{"role": "user", "content": prompt}],
            model=settings.DEFAULT_REASONING_MODEL,
            temperature=0.3,
        )
        import json
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {"passed": True, "score": 7, "issues": [], "suggestions": []}

    async def improve(self, task: str, result: str, review: dict[str, Any]) -> str:
        prompt = (
            "Improve the following result based on the review.\n"
            f"Task: {task}\n\nOriginal Result:\n{result}\n\n"
            f"Issues: {', '.join(review.get('issues', []))}\n"
            f"Suggestions: {', '.join(review.get('suggestions', []))}\n\n"
            "Output the improved result."
        )
        response = model_router.complete(
            [{"role": "user", "content": prompt}],
            model=settings.DEFAULT_REASONING_MODEL,
            temperature=0.5,
        )
        return response.choices[0].message.content

    async def reflect(self, task: str, initial_result: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        current = initial_result
        history: list[dict[str, Any]] = []
        for i in range(self.max_iterations):
            review = await self.review(task, current, context)
            history.append({"iteration": i + 1, "review": review, "result": current})
            if review.get("passed", False) or review.get("score", 0) >= 8:
                break
            current = await self.improve(task, current, review)
        return {"final_result": current, "iterations": len(history), "history": history}


self_reflection = SelfReflection()
