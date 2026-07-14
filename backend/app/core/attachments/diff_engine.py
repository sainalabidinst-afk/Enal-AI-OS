from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from backend.app.core.attachments.models import InfrastructureAST


@dataclass
class ConfigDiffItem:
    section: str
    before: str
    after: str
    change_type: str
    risk: str
    risk_score: float = 0.0
    recommendation: str | None = None
    rollback: str | None = None
    evidence: list[str] = field(default_factory=list)


@dataclass
class ConfigurationDiffResult:
    before_ast: InfrastructureAST
    after_ast: InfrastructureAST
    diffs: list[ConfigDiffItem] = field(default_factory=list)
    overall_risk: float = 0.0
    rollback_available: bool = False
    summary: str = ""


class ConfigurationDiffEngine:
    def diff(self, before: str, after: str) -> ConfigurationDiffResult:
        from backend.app.core.attachments.parsers.registry import parser_registry
        from backend.app.core.attachments.detector import detect_from_content

        before_meta = detect_from_content("before", before)
        after_meta = detect_from_content("after", after)
        before_ast = parser_registry.parse(before_meta, before)
        after_ast = parser_registry.parse(after_meta, after)

        diffs = self._diff_sections(before_ast, after_ast)
        overall_risk = self._calculate_risk(diffs)
        rollback_available = True
        summary = self._summarize(diffs, overall_risk)

        return ConfigurationDiffResult(
            before_ast=before_ast,
            after_ast=after_ast,
            diffs=diffs,
            overall_risk=overall_risk,
            rollback_available=rollback_available,
            summary=summary,
        )

    def _diff_sections(self, before: InfrastructureAST, after: InfrastructureAST) -> list[ConfigDiffItem]:
        diffs: list[ConfigDiffItem] = []
        self._compare_list(before.firewall, after.firewall, "firewall", diffs)
        self._compare_list(before.interfaces, after.interfaces, "interface", diffs)
        self._compare_list(before.routing, after.routing, "routing", diffs)
        self._compare_list(before.vlans, after.vlans, "vlan", diffs)
        self._compare_list(before.wireless, after.wireless, "wireless", diffs)
        self._compare_list(before.ha, after.ha, "ha", diffs)
        return diffs

    def _compare_list(self, before_items: list[dict[str, Any]], after_items: list[dict[str, Any]], section: str, diffs: list[ConfigDiffItem]) -> None:
        before_texts = {str(item.get("raw", "")): item for item in before_items if item.get("raw")}
        after_texts = {str(item.get("raw", "")): item for item in after_items if item.get("raw")}

        for text, item in after_texts.items():
            if text not in before_texts:
                diffs.append(self._added(section, "", text, item))
        for text, item in before_texts.items():
            if text not in after_texts:
                diffs.append(self._removed(section, text, "", item))

        common = set(before_texts.keys()) & set(after_texts.keys())
        for text in common:
            diffs.extend(self._compare_detail(section, before_texts[text], after_texts[text]))

    def _compare_detail(self, section: str, before_item: dict[str, Any], after_item: dict[str, Any]) -> list[ConfigDiffItem]:
        diffs: list[ConfigDiffItem] = []
        before_raw = str(before_item.get("raw", ""))
        after_raw = str(after_item.get("raw", ""))
        if before_raw != after_raw:
            risk = self._estimate_change_risk(section, before_raw, after_raw)
            diffs.append(ConfigDiffItem(
                section=section,
                before=before_raw,
                after=after_raw,
                change_type="modified",
                risk=risk,
                risk_score=self._risk_to_score(risk),
                recommendation=self._recommendation_for_change(section, after_raw),
                rollback=f"Restore previous {section} configuration from backup.",
                evidence=[before_raw, after_raw],
            ))
        return diffs

    def _added(self, section: str, before: str, after: str, item: dict[str, Any]) -> ConfigDiffItem:
        risk = self._estimate_change_risk(section, before, after)
        return ConfigDiffItem(
            section=section,
            before=before,
            after=after,
            change_type="added",
            risk=risk,
            risk_score=self._risk_to_score(risk),
            recommendation=self._recommendation_for_change(section, after),
            rollback=f"Remove added {section} configuration from current config.",
            evidence=[after],
        )

    def _removed(self, section: str, before: str, after: str, item: dict[str, Any]) -> ConfigDiffItem:
        risk = self._estimate_change_risk(section, before, after)
        return ConfigDiffItem(
            section=section,
            before=before,
            after=after,
            change_type="removed",
            risk=risk,
            risk_score=self._risk_to_score(risk),
            recommendation=f"Verify removal of {section} entry does not impact existing traffic or operation.",
            rollback=f"Restore removed {section} configuration from backup.",
            evidence=[before],
        )

    def _estimate_change_risk(self, section: str, before: str, after: str) -> str:
        lowered = f"{before} {after}".lower()
        if any(key in lowered for key in ["vpn", "firewall", "acl", "access-list", "policy", "nat"]):
            return "high"
        if any(key in lowered for key in ["routing", "ospf", "bgp", "static", "route"]):
            return "medium"
        return "low"

    def _risk_to_score(self, risk: str) -> float:
        return {"high": 0.8, "medium": 0.5, "low": 0.2}.get(risk, 0.3)

    def _recommendation_for_change(self, section: str, after: str) -> str:
        lowered = after.lower()
        if "firewall" in lowered or "policy" in lowered:
            return "Review policy hit counts, source/destination zones, and service restrictions."
        if "vpn" in lowered:
            return "Verify VPN tunnel, encryption, and peer configuration; test failover if applicable."
        if "routing" in lowered or "ospf" in lowered or "bgp" in lowered:
            return "Validate routing new next-hop, area/peer stability, and convergence behavior."
        return f"Review {section} change against baseline policy and test in maintenance window."

    def _calculate_risk(self, diffs: list[ConfigDiffItem]) -> float:
        if not diffs:
            return 0.0
        return round(sum(item.risk_score for item in diffs) / len(diffs), 2)

    def _summarize(self, diffs: list[ConfigDiffItem], overall_risk: float) -> str:
        added = sum(1 for d in diffs if d.change_type == "added")
        removed = sum(1 for d in diffs if d.change_type == "removed")
        modified = sum(1 for d in diffs if d.change_type == "modified")
        return (
            f"Configuration diff completed. "
            f"Added: {added}, modified: {modified}, removed: {removed}. "
            f"Overall change risk: {overall_risk:.0%}."
        )
