"""
Proposal Repository
===================

Persists capability proposals and improvement proposals
for the Self Development capability pack.

Storage: in-memory with optional JSON file persistence.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from apps.self_development.schemas import CapabilityProposal, ImprovementProposal

logger = logging.getLogger(__name__)


class ProposalRepository:
    """In-memory repository for proposals with optional file persistence."""

    def __init__(self, storage_path: Path | None = None) -> None:
        self._capabilities: dict[str, CapabilityProposal] = {}
        self._improvements: dict[str, ImprovementProposal] = {}
        self._storage_path = storage_path or Path("apps/self_development/proposals.json")
        self._load()

    def add_capability(self, proposal: CapabilityProposal) -> CapabilityProposal:
        self._capabilities[proposal.id] = proposal
        self._save()
        return proposal

    def get_capability(self, proposal_id: str) -> CapabilityProposal | None:
        return self._capabilities.get(proposal_id)

    def list_capabilities(self, status: str | None = None) -> list[CapabilityProposal]:
        proposals = list(self._capabilities.values())
        if status:
            proposals = [p for p in proposals if p.status == status]
        return sorted(proposals, key=lambda p: p.confidence, reverse=True)

    def update_capability_status(self, proposal_id: str, status: str) -> CapabilityProposal | None:
        proposal = self._capabilities.get(proposal_id)
        if proposal is None:
            return None
        proposal.status = status
        self._save()
        return proposal

    def add_improvement(self, proposal: ImprovementProposal) -> ImprovementProposal:
        self._improvements[proposal.id] = proposal
        self._save()
        return proposal

    def get_improvement(self, proposal_id: str) -> ImprovementProposal | None:
        return self._improvements.get(proposal_id)

    def list_improvements(
        self, status: str | None = None, target_type: str | None = None
    ) -> list[ImprovementProposal]:  # noqa: E501
        proposals = list(self._improvements.values())
        if status:
            proposals = [p for p in proposals if p.status == status]
        if target_type:
            proposals = [p for p in proposals if p.target_type == target_type]
        return sorted(proposals, key=lambda p: p.confidence, reverse=True)

    def update_improvement_status(
        self, proposal_id: str, status: str
    ) -> ImprovementProposal | None:  # noqa: E501
        proposal = self._improvements.get(proposal_id)
        if proposal is None:
            return None
        proposal.status = status
        self._save()
        return proposal

    def clear(self) -> None:
        self._capabilities.clear()
        self._improvements.clear()
        self._save()

    def _save(self) -> None:
        try:
            data = {
                "capabilities": [
                    {
                        "id": p.id,
                        "name": p.name,
                        "domain": p.domain,
                        "description": p.description,
                        "tier": p.tier,
                        "reuse_potential": p.reuse_potential,
                        "estimated_effort": p.estimated_effort,
                        "risk": p.risk,
                        "confidence": p.confidence,
                        "rationale": p.rationale,
                        "required_packs": p.required_packs,
                        "status": p.status,
                        "metadata": p.metadata,
                    }
                    for p in self._capabilities.values()
                ],
                "improvements": [
                    {
                        "id": p.id,
                        "target_type": p.target_type,
                        "target_id": p.target_id,
                        "improvement_type": p.improvement_type,
                        "description": p.description,
                        "estimated_effort": p.estimated_effort,
                        "risk": p.risk,
                        "confidence": p.confidence,
                        "expected_impact": p.expected_impact,
                        "status": p.status,
                        "metadata": p.metadata,
                    }
                    for p in self._improvements.values()
                ],
            }
            self._storage_path.parent.mkdir(parents=True, exist_ok=True)
            self._storage_path.write_text(json.dumps(data, indent=2))
        except Exception:
            logger.debug("Failed to save proposals", exc_info=True)

    def _load(self) -> None:
        if not self._storage_path.exists():
            return
        try:
            data = json.loads(self._storage_path.read_text())
            for item in data.get("capabilities", []):
                proposal = CapabilityProposal(
                    id=item["id"],
                    name=item["name"],
                    domain=item["domain"],
                    description=item["description"],
                    tier=item["tier"],
                    reuse_potential=item["reuse_potential"],
                    estimated_effort=item["estimated_effort"],
                    risk=item["risk"],
                    confidence=item["confidence"],
                    rationale=item["rationale"],
                    required_packs=item.get("required_packs", []),
                    status=item.get("status", "draft"),
                    metadata=item.get("metadata", {}),
                )
                self._capabilities[proposal.id] = proposal
            for item in data.get("improvements", []):
                proposal = ImprovementProposal(
                    id=item["id"],
                    target_type=item["target_type"],
                    target_id=item["target_id"],
                    improvement_type=item["improvement_type"],
                    description=item["description"],
                    estimated_effort=item["estimated_effort"],
                    risk=item["risk"],
                    confidence=item["confidence"],
                    expected_impact=item["expected_impact"],
                    status=item.get("status", "draft"),
                    metadata=item.get("metadata", {}),
                )
                self._improvements[proposal.id] = proposal
        except Exception:
            logger.debug("Failed to load proposals", exc_info=True)


proposal_repository = ProposalRepository()
