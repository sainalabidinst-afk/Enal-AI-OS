import logging
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger(__name__)


class ContractVersion:
    MAJOR = 1
    MINOR = 0
    PATCH = 0
    VERSION = f"{MAJOR}.{MINOR}.{PATCH}"


class CapabilityContract(ABC):
    @abstractmethod
    async def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_capabilities(self) -> list[str]:
        raise NotImplementedError


class ToolContract(ABC):
    @abstractmethod
    async def invoke(self, parameters: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_schema(self) -> dict[str, Any]:
        raise NotImplementedError


class ArtifactContract(ABC):
    @abstractmethod
    async def create(self, content: str, metadata: dict[str, Any]) -> str:
        raise NotImplementedError

    @abstractmethod
    async def read(self, artifact_id: str) -> dict[str, Any]:
        raise NotImplementedError


class MemoryContract(ABC):
    @abstractmethod
    async def store(self, key: str, value: Any, ttl: int | None = None):
        raise NotImplementedError

    @abstractmethod
    async def retrieve(self, key: str) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    async def search(self, query: str, limit: int = 10) -> list[dict]:
        raise NotImplementedError


class WorkflowContract(ABC):
    @abstractmethod
    async def execute(self, workflow_id: str, context: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def get_status(self, workflow_id: str) -> dict[str, Any]:
        raise NotImplementedError


class WorldModelContract(ABC):
    @abstractmethod
    async def query(self, query: str) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def infer(self, context: str) -> dict[str, Any]:
        raise NotImplementedError


class LearningContract(ABC):
    @abstractmethod
    async def record(self, experience: dict[str, Any]):
        raise NotImplementedError

    @abstractmethod
    async def search(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        raise NotImplementedError


AGENT_CONTRACTS = {
    "capability": CapabilityContract,
    "tool": ToolContract,
    "artifact": ArtifactContract,
    "memory": MemoryContract,
    "workflow": WorkflowContract,
    "world_model": WorldModelContract,
    "learning": LearningContract,
}


class ContractRegistry:
    def __init__(self):
        self._contracts: dict[str, dict[str, Any]] = {}

    def register(self, name: str, contract: Any, version: str = ContractVersion.VERSION):
        self._contracts[name] = {"contract": contract, "version": version}
        logger.info(f"Contract registered: {name} v{version}")

    def get(self, name: str) -> Any | None:
        return self._contracts.get(name, {}).get("contract")

    def list_contracts(self) -> list[str]:
        return list(self._contracts.keys())


contract_registry = ContractRegistry()
