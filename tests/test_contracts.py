import asyncio
import pytest

from backend.app.core.contracts import (
    CapabilityContract,
    ToolContract,
    ArtifactContract,
    MemoryContract,
    WorkflowContract,
    WorldModelContract,
    LearningContract,
    ContractVersion,
)


class TestContractVersion:
    def test_version_string_format(self):
        assert ContractVersion.VERSION == "1.0.0"

    def test_version_constants(self):
        assert ContractVersion.MAJOR == 1
        assert ContractVersion.MINOR == 0
        assert ContractVersion.PATCH == 0


class TestCapabilityContract:
    def test_cannot_instantiate_abstract_class(self):
        with pytest.raises(TypeError):
            CapabilityContract()

    def test_subclass_must_implement_execute(self):
        class IncompleteCapability(CapabilityContract):
            def get_capabilities(self):
                return []

        with pytest.raises(TypeError):
            IncompleteCapability()

    def test_concrete_subclass_works(self):
        class ConcreteCapability(CapabilityContract):
            async def execute(self, context):
                return {"result": "ok"}

            def get_capabilities(self):
                return ["test"]

        cap = ConcreteCapability()
        assert cap.get_capabilities() == ["test"]


class TestToolContract:
    def test_cannot_instantiate_abstract_class(self):
        with pytest.raises(TypeError):
            ToolContract()

    def test_concrete_subclass_works(self):
        class ConcreteTool(ToolContract):
            async def invoke(self, parameters):
                return {"result": "ok"}

            def get_schema(self):
                return {"type": "object"}

        tool = ConcreteTool()
        assert tool.get_schema() == {"type": "object"}


class TestArtifactContract:
    def test_cannot_instantiate_abstract_class(self):
        with pytest.raises(TypeError):
            ArtifactContract()

    def test_concrete_subclass_works(self):
        class ConcreteArtifact(ArtifactContract):
            async def create(self, content, metadata):
                return "artifact-1"

            async def read(self, artifact_id):
                return {"id": artifact_id}

        artifact = ConcreteArtifact()
        assert asyncio.run(artifact.create("content", {})) == "artifact-1"


class TestMemoryContract:
    def test_cannot_instantiate_abstract_class(self):
        with pytest.raises(TypeError):
            MemoryContract()

    def test_concrete_subclass_works(self):
        class ConcreteMemory(MemoryContract):
            async def store(self, key, value, ttl=None):
                pass

            async def retrieve(self, key):
                return None

            async def search(self, query, limit=10):
                return []

        memory = ConcreteMemory()
        assert asyncio.run(memory.search("test")) == []


class TestWorkflowContract:
    def test_cannot_instantiate_abstract_class(self):
        with pytest.raises(TypeError):
            WorkflowContract()

    def test_concrete_subclass_works(self):
        class ConcreteWorkflow(WorkflowContract):
            async def execute(self, workflow_id, context):
                return {"status": "completed"}

            async def get_status(self, workflow_id):
                return {"status": "completed"}

        workflow = ConcreteWorkflow()
        assert asyncio.run(workflow.get_status("wf-1"))["status"] == "completed"


class TestWorldModelContract:
    def test_cannot_instantiate_abstract_class(self):
        with pytest.raises(TypeError):
            WorldModelContract()

    def test_concrete_subclass_works(self):
        class ConcreteWorldModel(WorldModelContract):
            async def query(self, query):
                return []

            async def infer(self, context):
                return {"inference": "ok"}

        wm = ConcreteWorldModel()
        assert asyncio.run(wm.infer("test"))["inference"] == "ok"


class TestLearningContract:
    def test_cannot_instantiate_abstract_class(self):
        with pytest.raises(TypeError):
            LearningContract()

    def test_concrete_subclass_works(self):
        class ConcreteLearning(LearningContract):
            async def record(self, experience):
                pass

            async def search(self, query, limit=5):
                return []

        learning = ConcreteLearning()
        assert asyncio.run(learning.search("test")) == []
