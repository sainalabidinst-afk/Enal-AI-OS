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

from apps.self_development.schemas import (
    CapabilityProposal,
    ImprovementProposal,
    ProposalStatus,
)

logger = logging.getLogger(__name__)

MAX_CAPABILITIES = 100
MAX_IMPROVEMENTS = 200


class ProposalRepository:
    """In-memory repository for proposals with optional file persistence.

    Proposals are deduplicated by their natural key (domain for capability
    proposals, target_type + target_id + improvement_type for improvement
    proposals) so repeated analysis runs update existing entries instead of
    growing the store without bound.
    """

    def __init__(self, storage_path: Path | None = None) -> None:
        self._capabilities: dict[str, CapabilityProposal] = {}
        self._improvements: dict[str, ImprovementProposal] = {}
        self._storage_path = storage_path or Path("apps/self_development/proposals.json")
        self._load()

    def add_capability(self, proposal: CapabilityProposal) -> CapabilityProposal:
        existing = self._find_capability_by_domain(proposal.domain)
        if existing is not None and existing.id != proposal.id:
            self._merge_capability(existing, proposal)
            self._save()
            return existing
        self._capabilities[proposal.id] = proposal
        self._prune_capabilities()
        self._save()
        return proposal

    def _find_capability_by_domain(self, domain: str) -> CapabilityProposal | None:
        for stored in self._capabilities.values():
            if stored.domain == domain:
                return stored
        return None

    @staticmethod
    def _merge_capability(
        existing: CapabilityProposal, incoming: CapabilityProposal
    ) -> None:
        existing.name = incoming.name
        existing.description = incoming.description
        existing.tier = incoming.tier
        existing.reuse_potential = incoming.reuse_potential
        existing.estimated_effort = incoming.estimated_effort
        existing.risk = incoming.risk
        existing.confidence = incoming.confidence
        existing.rationale = incoming.rationale
        existing.required_packs = incoming.required_packs
        existing.metadata = incoming.metadata

    def _prune_capabilities(self) -> None:
        if len(self._capabilities) <= MAX_CAPABILITIES:
            return
        overflow = len(self._capabilities) - MAX_CAPABILITIES
        ranked = sorted(
            self._capabilities.values(),
            key=lambda p: (p.status != ProposalStatus.REJECTED.value, p.confidence),
        )
        for proposal in ranked[:overflow]:
            self._capabilities.pop(proposal.id, None)

    def _prune_improvements(self) -> None:
        if len(self._improvements) <= MAX_IMPROVEMENTS:
            return
        overflow = len(self._improvements) - MAX_IMPROVEMENTS
        ranked = sorted(
            self._improvements.values(),
            key=lambda p: (p.status != ProposalStatus.REJECTED.value, p.confidence),
        )
        for proposal in ranked[:overflow]:
            self._improvements.pop(proposal.id, None)

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
        existing = self._find_improvement_by_key(
            proposal.target_type, proposal.target_id, proposal.improvement_type
        )
        if existing is not None and existing.id != proposal.id:
            self._merge_improvement(existing, proposal)
            self._save()
            return existing
        self._improvements[proposal.id] = proposal
        self._prune_improvements()
        self._save()
        return proposal

    def _find_improvement_by_key(
        self, target_type: str, target_id: str, improvement_type: str
    ) -> ImprovementProposal | None:
        for stored in self._improvements.values():
            if (
                stored.target_type == target_type
                and stored.target_id == target_id
                and stored.improvement_type == improvement_type
            ):
                return stored
        return None

    @staticmethod
    def _merge_improvement(
        existing: ImprovementProposal, incoming: ImprovementProposal
    ) -> None:
        existing.description = incoming.description
        existing.estimated_effort = incoming.estimated_effort
        existing.risk = incoming.risk
        existing.confidence = incoming.confidence
        existing.expected_impact = incoming.expected_impact
        existing.metadata = incoming.metadata

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

    def dedupe(self) -> dict[str, int]:
        """Collapse duplicates by natural key; returns removed counts."""
        before_caps = len(self._capabilities)
        before_imps = len(self._improvements)
        self._capabilities = {
            p.domain: p for p in self._capabilities.values()
        }
        self._capabilities = {
            p.id: p for p in self._capabilities.values()
        }
        improvements: dict[str, ImprovementProposal] = {}
        for proposal in self._improvements.values():
            key = (proposal.target_type, proposal.target_id, proposal.improvement_type)
            improvements[key] = proposal
        self._improvements = {p.id: p for p in improvements.values()}
        removed = {
            "capabilities": before_caps - len(self._capabilities),
            "improvements": before_imps - len(self._improvements),
        }
        if removed["capabilities"] or removed["improvements"]:
            self._save()
        return removed

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
                self._capabilities[proposal.domain] = proposal
            self._capabilities = {
                p.id: p for p in self._capabilities.values()
            }
            improvements: dict[tuple[str, str, str], ImprovementProposal] = {}
            for item in data.get("improvements", []):
                improvement = ImprovementProposal(
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
                key = (
                    improvement.target_type,
                    improvement.target_id,
                    improvement.improvement_type,
                )
                improvements[key] = improvement
            self._improvements = {p.id: p for p in improvements.values()}
        except Exception:
            logger.debug("Failed to load proposals", exc_info=True)


proposal_repository = ProposalRepository()
