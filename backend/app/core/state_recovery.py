import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class Checkpoint:
    def __init__(self, workflow_id: str, step_id: str, state: dict[str, Any]):
        self.workflow_id = workflow_id
        self.step_id = step_id
        self.state = state
        self.timestamp = datetime.utcnow()


class StateRecovery:
    def __init__(self, base_path: str = "./workspace/checkpoints"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def save(self, workflow_id: str, step_id: str, state: dict[str, Any]):
        checkpoint = Checkpoint(workflow_id=workflow_id, step_id=step_id, state=state)
        path = self.base_path / f"{workflow_id}.json"
        data = {
            "workflow_id": workflow_id,
            "step_id": step_id,
            "state": state,
            "timestamp": checkpoint.timestamp.isoformat(),
        }
        path.write_text(json.dumps(data, indent=2))
        logger.info(f"Checkpoint saved: {workflow_id} @ {step_id}")

    async def load(self, workflow_id: str) -> dict[str, Any] | None:
        path = self.base_path / f"{workflow_id}.json"
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text())
            return data
        except Exception as e:
            logger.error(f"Failed to load checkpoint {workflow_id}: {e}")
            return None

    async def list_checkpoints(self) -> list[dict[str, Any]]:
        checkpoints = []
        for path in self.base_path.glob("*.json"):
            try:
                data = json.loads(path.read_text())
                checkpoints.append(data)
            except Exception:
                continue
        return sorted(checkpoints, key=lambda x: x.get("timestamp", ""), reverse=True)

    async def delete(self, workflow_id: str):
        path = self.base_path / f"{workflow_id}.json"
        if path.exists():
            path.unlink()


state_recovery = StateRecovery()
