"""
Storage Designer
=================

Designs storage solutions: block (EBS, iSCSI), file (EFS, NFS),
object (S3, MinIO), and distributed (Ceph, GlusterFS) storage.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.infrastructure_engineer.schemas import (
    InfrastructureEngineerRequest,
    VolumeSpec,
    StorageClassSpec,
    StorageType,
    StorageTier,
)

logger = logging.getLogger(__name__)

STORAGE_TYPE_MAP: dict[str, StorageType] = {
    "block": StorageType.block,
    "file": StorageType.file,
    "object": StorageType.object,
    "distributed": StorageType.distributed,
}

TIER_MAP: dict[str, StorageTier] = {
    "hot": StorageTier.hot,
    "warm": StorageTier.warm,
    "cold": StorageTier.cold,
    "archive": StorageTier.archive,
}


class StorageDesigner:
    """Designs storage specifications for various workloads."""

    def design_storage(self, request: InfrastructureEngineerRequest) -> list[VolumeSpec | StorageClassSpec]:
        inputs = request.inputs
        storage_requests = inputs.get("storage_specs", [])
        result: list[VolumeSpec | StorageClassSpec] = []

        if not storage_requests:
            result.append(
                VolumeSpec(
                    name="default-data-volume",
                    size_gb=100,
                    storage_type=StorageType.block,
                    storage_tier=StorageTier.hot,
                    iops=3000,
                    throughput_mbps=125,
                    replicas=3,
                    encryption=True,
                    snapshot_enabled=True,
                )
            )
            result.append(
                StorageClassSpec(
                    name="standard-block",
                    storage_type=StorageType.block,
                    storage_tier=StorageTier.hot,
                    reclaim_policy="retain",
                    volume_expansion=True,
                )
            )
            return result

        for sr in storage_requests:
            vol = VolumeSpec(
                name=sr.get("name", f"vol-{len(result)+1}"),
                size_gb=sr.get("size_gb", 100),
                storage_type=STORAGE_TYPE_MAP.get(sr.get("type", "block"), StorageType.block),
                storage_tier=TIER_MAP.get(sr.get("tier", "hot"), StorageTier.hot),
                iops=sr.get("iops", 3000),
                throughput_mbps=sr.get("throughput_mbps", 125),
                replicas=sr.get("replicas", 3),
                encryption=sr.get("encryption", True),
                snapshot_enabled=sr.get("snapshot_enabled", True),
            )
            result.append(vol)

            if sr.get("create_storage_class"):
                result.append(
                    StorageClassSpec(
                        name=sr.get("name", "sc") + "-sc",
                        storage_type=vol.storage_type,
                        storage_tier=vol.storage_tier,
                        reclaim_policy=sr.get("reclaim_policy", "retain"),
                        volume_expansion=sr.get("volume_expansion", True),
                        allowed_topologies=sr.get("allowed_topologies", []),
                    )
                )

        return result

    def get_recommendations(self, specs: list[Any]) -> list[str]:
        recs: list[str] = []
        for spec in specs:
            if isinstance(spec, VolumeSpec):
                if not spec.encryption:
                    recs.append(f"Volume '{spec.name}': aktifkan encryption-at-rest")
                if spec.storage_tier == StorageTier.cold and spec.iops > 100:
                    recs.append(f"Volume '{spec.name}': turunkan IOPS untuk tier cold")
                if spec.replicas < 3:
                    recs.append(f"Volume '{spec.name}': tingkatkan jumlah replika ke ≥3")
                if not spec.snapshot_enabled:
                    recs.append(f"Volume '{spec.name}': aktifkan snapshot untuk backup")
        return recs

    def estimate_cost(self, specs: list[Any]) -> dict[str, float]:
        total_monthly = 0.0
        by_type: dict[str, float] = {}
        for spec in specs:
            if isinstance(spec, VolumeSpec):
                gb_cost = 0.10 if spec.storage_tier == StorageTier.hot else 0.03
                monthly = spec.size_gb * gb_cost
                if spec.iops > 3000:
                    monthly += (spec.iops - 3000) * 0.005
                by_type[spec.storage_type.value] = by_type.get(spec.storage_type.value, 0.0) + monthly
                total_monthly += monthly
        result = dict(by_type)
        result["total_monthly"] = total_monthly
        return result

    def get_security_hardening(self, specs: list[Any]) -> list[str]:
        return [
            "Semua volume dienkripsi menggunakan LUKS atau storage-level encryption",
            "Akses storage mengikuti principle of least privilege (IAM/ACL)",
            "Snapshot dienkripsi dan disimpan di lokasi terpisah dari data utama",
            "Access logging diaktifkan untuk object storage",
            "Data classification diterapkan — sensitif data di tier hot, cold untuk arsip",
        ]

    def score_quality(self, specs: list[Any]) -> float:
        if not specs:
            return 0.0
        score = 0.0
        for spec in specs:
            if isinstance(spec, VolumeSpec):
                s = 0.7
                if spec.encryption:
                    s += 0.05
                if spec.snapshot_enabled:
                    s += 0.05
                if spec.replicas >= 3:
                    s += 0.05
                if spec.iops > 0:
                    s += 0.05
                score = max(score, s)
        return min(score, 1.0)
