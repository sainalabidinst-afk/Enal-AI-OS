import logging
from abc import ABC, abstractmethod
from typing import Any
from backend.app.core.memory_layer import memory_manager
from backend.app.core.cognitive.world_model import world_model

logger = logging.getLogger(__name__)


class CognitiveService(ABC):
    @abstractmethod
    async def process(self, context: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


class PerceptionService(CognitiveService):
    async def process(self, context: dict[str, Any]) -> dict[str, Any]:
        user_input = context.get("input", "")
        project_id = context.get("project_id")
        memories = []
        if project_id:
            try:
                memories = await memory_manager.search("working", user_input, limit=3)
            except Exception:
                pass
        world_entities = await world_model.query(user_input)
        return {
            "input": user_input,
            "memories": memories,
            "world_entities": world_entities,
            "context": context,
        }


class MemoryService(CognitiveService):
    async def process(self, context: dict[str, Any]) -> dict[str, Any]:
        perception = context.get("perception", {})
        user_input = perception.get("input", "")
        project_id = context.get("project_id")
        relevant_memories = []
        if project_id:
            try:
                relevant_memories = await memory_manager.search("knowledge", user_input, limit=5)
            except Exception:
                pass
        return {"relevant_memories": relevant_memories, "working_memory": perception.get("memories", [])}


class ReasoningService(CognitiveService):
    async def process(self, context: dict[str, Any]) -> dict[str, Any]:
        from backend.app.core.cognitive.reasoning_engine import reasoning_engine
        perception = context.get("perception", {})
        problem = perception.get("input", "")
        hypotheses = await reasoning_engine.generate_hypotheses(problem)
        chain = await reasoning_engine.reason(problem, hypotheses)
        decision = await reasoning_engine.decide(chain)
        return {"hypotheses": hypotheses, "chain": chain, "decision": decision}


class PlanningService(CognitiveService):
    async def process(self, context: dict[str, Any]) -> dict[str, Any]:
        from backend.app.core.cognitive.strategic_planner import strategic_planner
        perception = context.get("perception", {})
        problem = perception.get("input", "")
        roadmap = await strategic_planner.create_strategy(problem, context)
        return {"roadmap": roadmap}


class DecisionService(CognitiveService):
    async def process(self, context: dict[str, Any]) -> dict[str, Any]:
        from backend.app.core.decision_engine import decision_engine
        options = context.get("options", [])
        if not options:
            return {"decision": context.get("perception", {}).get("input", ""), "confidence": 0.0}
        return await decision_engine.decide(options, context)


class ActionService(CognitiveService):
    async def process(self, context: dict[str, Any]) -> dict[str, Any]:
        decision = context.get("decision", {})
        return {"action": decision.get("decision", ""), "parameters": decision.get("parameters", {}), "executed": False}


class ReflectionService(CognitiveService):
    async def process(self, context: dict[str, Any]) -> dict[str, Any]:
        from backend.app.core.reflection import self_reflection
        decision = context.get("decision", {})
        task = context.get("perception", {}).get("input", "")
        result = decision.get("decision", "")
        review = await self_reflection.review(task, result)
        return {"review": review, "score": review.get("score", 0), "passed": review.get("passed", False)}


class LearningService(CognitiveService):
    async def process(self, context: dict[str, Any]) -> dict[str, Any]:
        reflection = context.get("reflection", {})
        review = reflection.get("review", {})
        score = review.get("score", 0)
        return {"learned": score >= 7, "quality_score": score, "suggestions": review.get("suggestions", [])}


class CognitiveKernel:
    def __init__(self):
        self.services: dict[str, CognitiveService] = {
            "perception": PerceptionService(),
            "memory": MemoryService(),
            "reasoning": ReasoningService(),
            "planning": PlanningService(),
            "decision": DecisionService(),
            "action": ActionService(),
            "reflection": ReflectionService(),
            "learning": LearningService(),
        }
        self._initialized = True

    async def execute_service(self, service_name: str, context: dict[str, Any]) -> dict[str, Any]:
        service = self.services.get(service_name)
        if not service:
            raise ValueError(f"Unknown cognitive service: {service_name}")
        return await service.process(context)

    def list_services(self) -> list[str]:
        return list(self.services.keys())

    async def execute_pipeline(self, pipeline: list[str], context: dict[str, Any]) -> dict[str, Any]:
        result = context
        for service_name in pipeline:
            if service_name not in self.services:
                continue
            result = await self.execute_service(service_name, result)
            result[f"{service_name}_result"] = result
        return result


cognitive_kernel = CognitiveKernel()
