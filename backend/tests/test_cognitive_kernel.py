import pytest

from backend.app.core.cognitive_kernel import (
    ActionService,
    CognitiveKernel,
    DecisionService,
    LearningService,
    MemoryService,
    PerceptionService,
    PlanningService,
    ReasoningService,
    ReflectionService,
)


class FakeMemoryManager:
    async def search(self, *args, **kwargs):
        return []


class TestCognitiveServices:
    @pytest.mark.asyncio
    async def test_perception_service(self, monkeypatch):
        import backend.app.core.cognitive_kernel as ck_module
        monkeypatch.setattr(ck_module, "memory_manager", FakeMemoryManager())

        class FakeWorldModel:
            @staticmethod
            async def query(user_input):
                return []

        monkeypatch.setattr("backend.app.core.cognitive.world_model.world_model", FakeWorldModel())
        service = PerceptionService()
        result = await service.process({"input": "hello", "project_id": "p1"})
        assert result["input"] == "hello"
        assert "memories" in result
        assert "world_entities" in result

    @pytest.mark.asyncio
    async def test_memory_service(self, monkeypatch):
        import backend.app.core.cognitive_kernel as ck_module
        monkeypatch.setattr(ck_module, "memory_manager", FakeMemoryManager())
        service = MemoryService()
        result = await service.process({"perception": {"input": "hello"}, "project_id": "p1"})
        assert "relevant_memories" in result
        assert result["relevant_memories"] == []

    @pytest.mark.asyncio
    async def test_reasoning_service(self, monkeypatch):
        import backend.app.core.cognitive_kernel as ck_module

        class FakeReasoningEngine:
            @staticmethod
            async def generate_hypotheses(problem):
                return []

            @staticmethod
            async def reason(problem, hypotheses):
                return type("Chain", (), {"__dict__": {"steps": []}})()

            @staticmethod
            async def decide(chain):
                return type("Decision", (), {"__dict__": {}})()

        monkeypatch.setattr("backend.app.core.cognitive.reasoning_engine.reasoning_engine", FakeReasoningEngine)
        service = ReasoningService()
        result = await service.process({"perception": {"input": "problem"}})
        assert "hypotheses" in result
        assert "chain" in result
        assert "decision" in result

    @pytest.mark.asyncio
    async def test_planning_service(self, monkeypatch):
        import backend.app.core.cognitive_kernel as ck_module

        class FakeStrategicPlanner:
            @staticmethod
            async def create_strategy(problem, context):
                return type("Roadmap", (), {"__dict__": {"steps": []}})()

        monkeypatch.setattr("backend.app.core.cognitive.strategic_planner.strategic_planner", FakeStrategicPlanner)
        service = PlanningService()
        result = await service.process({"perception": {"input": "problem"}})
        assert "roadmap" in result

    @pytest.mark.asyncio
    async def test_decision_service_empty_options(self, monkeypatch):
        service = DecisionService()
        result = await service.process({})
        assert result["confidence"] == 0.0

    @pytest.mark.asyncio
    async def test_action_service(self):
        service = ActionService()
        result = await service.process({"decision": {"decision": "do it", "parameters": {}}})
        assert result["action"] == "do it"
        assert result["executed"] is False

    @pytest.mark.asyncio
    async def test_reflection_service(self, monkeypatch):
        import backend.app.core.cognitive_kernel as ck_module

        class FakeSelfReflection:
            @staticmethod
            async def review(task, result):
                return {"score": 8, "passed": True, "suggestions": []}

        monkeypatch.setattr("backend.app.core.reflection.self_reflection", FakeSelfReflection)
        service = ReflectionService()
        result = await service.process({"decision": {"decision": "done"}, "perception": {"input": "task"}})
        assert result["score"] == 8
        assert result["passed"] is True

    async def test_learning_service(self):
        service = LearningService()
        result = await service.process({"reflection": {"review": {"score": 8}}})
        assert result["learned"] is True
        assert result["quality_score"] == 8

    async def test_learning_service_low_score(self):
        service = LearningService()
        result = await service.process({"reflection": {"review": {"score": 3}}})
        assert result["learned"] is False


class TestCognitiveKernel:
    def test_list_services_returns_all(self):
        kernel = CognitiveKernel()
        services = kernel.list_services()
        assert "perception" in services
        assert "memory" in services
        assert "reasoning" in services
        assert "planning" in services
        assert "decision" in services
        assert "action" in services
        assert "reflection" in services
        assert "learning" in services

    async def test_execute_service_unknown_raises(self):
        kernel = CognitiveKernel()
        with pytest.raises(ValueError):
            await kernel.execute_service("unknown", {})

    async def test_execute_pipeline_runs_services(self, monkeypatch):
        import backend.app.core.cognitive_kernel as ck_module
        monkeypatch.setattr(ck_module, "memory_manager", FakeMemoryManager())

        class FakeWorldModel:
            @staticmethod
            async def query(user_input):
                return []

        monkeypatch.setattr("backend.app.core.cognitive.world_model.world_model", FakeWorldModel())
        monkeypatch.setattr("backend.app.core.cognitive.strategic_planner.strategic_planner.create_strategy", lambda *a, **k: type("R", (), {"__dict__": {}})())
        monkeypatch.setattr("backend.app.core.reflection.self_reflection.review", lambda *a, **k: {"score": 8, "passed": True, "suggestions": []})

        class FakeReasoningEngine:
            @staticmethod
            async def generate_hypotheses(problem):
                return []

            @staticmethod
            async def reason(problem, hypotheses):
                return type("Chain", (), {"__dict__": {"steps": []}})()

            @staticmethod
            async def decide(chain):
                return type("Decision", (), {"__dict__": {}})()

        monkeypatch.setattr("backend.app.core.cognitive.reasoning_engine.reasoning_engine", FakeReasoningEngine)

        kernel = CognitiveKernel()
        result = await kernel.execute_pipeline(["perception", "memory", "reasoning"], {"input": "test"})
        assert "_pipeline_results" in result
        assert "perception" in result["_pipeline_results"]
