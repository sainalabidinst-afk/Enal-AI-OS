"""
Backup Manager
===============

Manages configuration backups before deployment.
Export → Hash → Timestamp → Artifact Store
"""

import hashlib
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class BackupRecord:
    backup_id: str
    device_id: str
    config_hash: str
    timestamp: str
    size_bytes: int
    artifact_path: str
    metadata: dict[str, Any] = field(default_factory=dict)


class BackupManager:
    """Manages configuration backups."""

    def __init__(self, store_dir: str = "artifacts/backups"):
        self.store_dir = Path(store_dir)
        self.store_dir.mkdir(parents=True, exist_ok=True)
        self._backups: dict[str, BackupRecord] = {}

    def create_backup(self, device_id: str, config_content: str, metadata: dict[str, Any] | None = None) -> BackupRecord:
        """Create a backup of the current configuration."""
        backup_id = f"bkp-{int(time.time() * 1000)}"
        config_hash = hashlib.sha256(config_content.encode()).hexdigest()[:16]
        timestamp = datetime.utcnow().isoformat()

        artifact_path = self.store_dir / f"{device_id}-{backup_id}.rsc"
        artifact_path.write_text(config_content, encoding="utf-8")

        record = BackupRecord(
            backup_id=backup_id,
            device_id=device_id,
            config_hash=config_hash,
            timestamp=timestamp,
            size_bytes=len(config_content.encode()),
            artifact_path=str(artifact_path),
            metadata=metadata or {},
        )

        self._backups[backup_id] = record
        logger.info(f"Backup created: {backup_id} for {device_id} (hash={config_hash})")
        return record

    def get_backup(self, backup_id: str) -> BackupRecord | None:
        """Get a backup record by ID."""
        return self._backups.get(backup_id)

    def list_backups(self, device_id: str | None = None) -> list[BackupRecord]:
        """List backups, optionally filtered by device."""
        if device_id:
            return [b for b in self._backups.values() if b.device_id == device_id]
        return list(self._backups.values())

    def restore_backup(self, backup_id: str) -> str:
        """Restore a backup and return its config content."""
        record = self._backups.get(backup_id)
        if not record:
            raise ValueError(f"Backup {backup_id} not found")
        path = Path(record.artifact_path)
        if not path.exists():
            raise FileNotFoundError(f"Backup artifact not found: {path}")
        return path.read_text(encoding="utf-8")

    def verify_integrity(self, backup_id: str) -> bool:
        """Verify backup integrity by re-hashing."""
        record = self._backups.get(backup_id)
        if not record:
            return False
        path = Path(record.artifact_path)
        if not path.exists():
            return False
        content = path.read_text(encoding="utf-8")
        actual_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        return actual_hash == record.config_hash


backup_manager = BackupManager()
