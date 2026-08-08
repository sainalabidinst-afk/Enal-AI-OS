import pytest

from backend.app.core.contracts import (
    AGENT_CONTRACTS,
    ArtifactContract,
    CapabilityContract,
    ContractRegistry,
    ContractVersion,
    LearningContract,
    MemoryContract,
    ToolContract,
    WorldModelContract,
    WorkflowContract,
)


class ConcreteCapability(CapabilityContract):
    async def execute(self, context: dict[str, object]) -> dict[str, object]:
        return {"result": "ok"}

    def get_capabilities(self) -> list[str]:
        return ["cap1"]


class TestContractVersion:
    def test_version_format(self):
        assert ContractVersion.VERSION == "1.0.0"

    def test_constants(self):
        assert ContractVersion.MAJOR == 1
        assert ContractVersion.MINOR == 0
        assert ContractVersion.PATCH == 0


class TestCapabilityContract:
    async def test_execute(self):
        impl = ConcreteCapability()
        result = await impl.execute({})
        assert result == {"result": "ok"}

    def test_get_capabilities(self):
        impl = ConcreteCapability()
        assert impl.get_capabilities() == ["cap1"]


class TestContractRegistry:
    def test_register_and_get(self):
        registry = ContractRegistry()
        contract = ConcreteCapability()
        registry.register("cap", contract, version="1.1.0")
        assert registry.get("cap") is contract

    def test_get_missing_returns_none(self):
        registry = ContractRegistry()
        assert registry.get("missing") is None

    def test_list_contracts(self):
        registry = ContractRegistry()
        registry.register("a", object(), version="1.0.0")
        registry.register("b", object(), version="2.0.0")
        assert set(registry.list_contracts()) == {"a", "b"}


class TestAgentContracts:
    def test_contains_expected_contracts(self):
        assert "capability" in AGENT_CONTRACTS
        assert "tool" in AGENT_CONTRACTS
        assert "artifact" in AGENT_CONTRACTS
        assert "memory" in AGENT_CONTRACTS
        assert "workflow" in AGENT_CONTRACTS
        assert "world_model" in AGENT_CONTRACTS
        assert "learning" in AGENT_CONTRACTS
