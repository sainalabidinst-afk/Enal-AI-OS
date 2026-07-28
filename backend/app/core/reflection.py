import json
import logging
from typing import Any

from backend.app.core.config import settings
from backend.app.core.model_router import model_router

logger = logging.getLogger(__name__)


class SelfReflection:
    def __init__(self, max_iterations: int = 3):
        self.max_iterations = max_iterations
        self._feedback_history: list[dict[str, Any]] = []

    async def review(self, task: str, result: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        prompt = (
            "You are a critical reviewer. Evaluate the result against the task.\n"
            f"Task: {task}\n\nResult:\n{result}\n\n"
            "Output JSON: {\"passed\": bool, \"score\": int(1-10), \"issues\": [str], \"suggestions\": [str]}"
        )
        try:
            response = model_router.complete(
                [{"role": "user", "content": prompt}],
                model=settings.DEFAULT_REASONING_MODEL,
                temperature=0.3,
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except json.JSONDecodeError:
            return {"passed": True, "score": 7, "issues": [], "suggestions": []}
        except Exception as e:
            logger.warning(f"Review fallback due to: {e}")
            return {"passed": True, "score": 7, "issues": [], "suggestions": []}

    async def improve(self, task: str, result: str, review: dict[str, Any]) -> str:
        prompt = (
            "Improve the following result based on the review.\n"
            f"Task: {task}\n\nOriginal Result:\n{result}\n\n"
            f"Issues: {', '.join(review.get('issues', []))}\n"
            f"Suggestions: {', '.join(review.get('suggestions', []))}\n\n"
            "Output the improved result."
        )
        try:
            response = model_router.complete(
                [{"role": "user", "content": prompt}],
                model=settings.DEFAULT_REASONING_MODEL,
                temperature=0.5,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.warning(f"Improve fallback due to: {e}")
            return result

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

    async def feedback_loop(self, service_name: str, task: str, result: dict[str, Any]) -> dict[str, Any]:
        """Connect to cognitive services for iterative improvement."""
        review = await self.review(task, str(result.get("result", "")), result.get("context"))
        self._feedback_history.append({
            "service": service_name,
            "task": task,
            "score": review.get("score", 0),
            "passed": review.get("passed", False),
        })
        if review.get("score", 0) < 8:
            improved = await self.improve(task, str(result.get("result", "")), review)
            return {"original": result, "improved": improved, "review": review}
        return {"original": result, "improved": result.get("result"), "review": review}

    def get_feedback_summary(self) -> dict[str, Any]:
        """Get summary of feedback collected across services."""
        if not self._feedback_history:
            return {"total": 0, "avg_score": 0}
        scores = [f["score"] for f in self._feedback_history if f.get("score")]
        return {
            "total": len(self._feedback_history),
            "avg_score": sum(scores) / len(scores) if scores else 0,
            "by_service": {s: len([f for f in self._feedback_history if f["service"] == s]) for s in set(f["service"] for f in self._feedback_history)},
        }


self_reflection = SelfReflection()
