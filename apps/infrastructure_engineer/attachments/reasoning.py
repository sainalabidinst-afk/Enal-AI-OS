from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from apps.infrastructure_engineer.attachments.compliance import (
    ComplianceCheck,
    ComplianceEngine,
    ComplianceFramework,
)
from apps.infrastructure_engineer.attachments.models import InfrastructureAST, InfrastructureFinding, Severity


@dataclass
class ReasoningChain:
    finding: InfrastructureFinding
    premises: list[str] = field(default_factory=list)
    conclusion: str = ""
    impact: str = ""
    confidence: float = 1.0
    remediation_steps: list[str] = field(default_factory=list)
    rollback_steps: list[str] = field(default_factory=list)
    reasoning_notes: list[str] = field(default_factory=list)


@dataclass
class RiskAssessment:
    risk_score: float = 0.0
    attack_surface: list[str] = field(default_factory=list)
    exposed_services: list[str] = field(default_factory=list)
    credential_exposure: list[str] = field(default_factory=list)
    lateral_movement_paths: list[str] = field(default_factory=list)
    privilege_escalation_risks: list[str] = field(default_factory=list)
    summary: str = ""


@dataclass
class InfrastructureReasoningResult:
    ast: InfrastructureAST
    reasoning_chains: list[ReasoningChain] = field(default_factory=list)
    risk_assessment: RiskAssessment | None = None
    recommendations: list[str] = field(default_factory=list)
    execution_plan: list[str] = field(default_factory=list)
    explainability: dict[str, Any] = field(default_factory=dict)
    executive_summary: str = ""
    quick_wins: list[str] = field(default_factory=list)
    plan_30d: list[str] = field(default_factory=list)
    plan_90d: list[str] = field(default_factory=list)
    compliance_checks: list[ComplianceCheck] = field(default_factory=list)
    compliance_score: float = 0.0
    diff_result: Any | None = None


class InfrastructureReasoningEngine:
    def reason(self, ast: InfrastructureAST, compliance_frameworks: list[ComplianceFramework] | None = None, diff_result: Any | None = None) -> InfrastructureReasoningResult:
        chains = self._build_chains(ast)
        risk = self._assess_risk(ast, chains)
        recommendations = self._generate_recommendations(ast, chains)
        execution_plan = self._plan_execution(ast, chains)
        explainability = self._build_explainability(ast, chains)
        executive_summary = self._generate_executive_summary(ast, chains, risk)
        quick_wins, plan_30d, plan_90d = self._build_roadmap(ast, chains, risk)

        compliance_checks = ComplianceEngine().evaluate(ast, compliance_frameworks)
        compliance_score = self._compute_compliance_score(compliance_checks)

        return InfrastructureReasoningResult(
            ast=ast,
            reasoning_chains=chains,
            risk_assessment=risk,
            recommendations=recommendations,
            execution_plan=execution_plan,
            explainability=explainability,
            executive_summary=executive_summary,
            quick_wins=quick_wins,
            plan_30d=plan_30d,
            plan_90d=plan_90d,
            compliance_checks=compliance_checks,
            compliance_score=compliance_score,
            diff_result=diff_result,
        )

    def _build_chains(self, ast: InfrastructureAST) -> list[ReasoningChain]:
        chains: list[ReasoningChain] = []
        for finding in ast.findings:
            chain = self._chain_for_finding(ast, finding)
            chains.append(chain)
        return chains

    def _chain_for_finding(self, ast: InfrastructureAST, finding: InfrastructureFinding) -> ReasoningChain:
        category = finding.category.lower()
        premises = list(finding.evidence or [])
        conclusion = finding.description
        impact = finding.description
        remediation = [finding.recommendation] if finding.recommendation else []
        rollback: list[str] = []
        notes: list[str] = []

        if category == "firewall":
            if ast.firewall:
                notes.append("Firewall configuration present but may not cover all interfaces or directions.")
            if not ast.firewall:
                notes.append("No explicit firewall rules detected.")
                conclusion = "Network may be exposed because no firewall rules were detected."
                impact = "Increased brute-force, DoS, and lateral movement risk."
                remediation = [
                    "Add an explicit default-drop firewall policy on all interfaces.",
                    "Whitelist only required services and sources.",
                    "Log dropped traffic for visibility.",
                ]
                rollback = [
                    "Remove the added default-drop policy if legitimate traffic is blocked.",
                    "Restore previous firewall backup.",
                ]
                premises = premises or ["No firewall rules detected."]

        elif category == "switch":
            if "trunk" in finding.title.lower():
                notes.append("Trunk interfaces carry multiple VLANs and require strict allowed-list validation.")
                impact = impact or "VLAN hopping or unauthorized VLAN access risk."
                remediation = remediation or [
                    "Validate allowed VLAN list on trunk interfaces.",
                    "Disable unused VLANs.",
                    "Enable BPDU guard and root guard where appropriate.",
                ]
                rollback = rollback or ["Revert trunk allowed-VLAN changes if connectivity breaks.", "Restore previous interface configuration."]
            elif "poe" in finding.title.lower():
                notes.append("PoE increases power and availability requirements.")
                impact = impact or "Power budget exhaustion or unplanned device behavior."
                remediation = remediation or ["Review PoE allocation versus power budget.", "Verify redundant PSUs if supported."]
                rollback = rollback or ["Disable PoE on unused ports.", "Restore previous PoE configuration."]
            elif "stp" in finding.title.lower() or "spanning-tree" in finding.title.lower():
                notes.append("STP protects against loops but needs consistent configuration.")
                impact = impact or "Broadcast storm if misconfigured."
                remediation = remediation or ["Enable RSTP/MSTP if supported.", "Document root bridge and port roles."]
                rollback = rollback or ["Restore previous STP configuration.", "Clear port roles if confusion occurs."]

        elif category == "wireless":
            notes.append("Wireless configuration affects confidentiality, availability, and compliance.")
            impact = impact or "Weak Wi-Fi security may lead to unauthorized access."
            remediation = remediation or [
                "Enforce WPA3 or WPA2-AES.",
                "Segment wireless traffic from wired infrastructure.",
                "Review roaming and DFS settings.",
            ]
            rollback = rollback or ["Revert SSID security settings to previous state.", "Restore previous controller configuration."]

        elif category == "ha":
            notes.append("High availability depends on consistent configuration and reachable heartbeats.")
            impact = impact or "Split-brain or failover failure risk."
            remediation = remediation or [
                "Verify HA heartbeat interfaces are on a dedicated VLAN.",
                "Align priorities and preempt settings.",
                "Validate failover in a maintenance window.",
            ]
            rollback = rollback or ["Restore original HA priority and mode.", "Verify controller synchronization."]

        elif category == "security":
            notes.append("Security gaps increase likelihood of compromise.")
            impact = impact or "Potential breach or unauthorized access path."
            remediation = remediation or [
                "Tighten access control and authentication.",
                "Enable encryption and logging.",
                "Review exposure on management interfaces.",
            ]
            rollback = rollback or ["Restore previous access control entries.", "Enable previous authentication methods if breakage occurs."]

        elif category == "bridge":
            notes.append("Bridges can expand attack surface if ports are not secured.")
            impact = impact or "Unintended network access through bridge ports."
            remediation = remediation or [
                "Enable port security where supported.",
                "Restrict bridge participation to required interfaces only.",
            ]
            rollback = rollback or ["Remove bridge port restrictions.", "Restore original bridge configuration."]

        if not notes:
            notes.append("Evidence-based reasoning applied from available configuration artifacts.")
        if not impact:
            impact = finding.description
        if not remediation:
            remediation = [finding.recommendation] if finding.recommendation else ["Review the finding and apply vendor best practice."]
        if not rollback:
            rollback = ["Restore the configuration from backup if needed."]

        return ReasoningChain(
            finding=finding,
            premises=premises,
            conclusion=conclusion,
            impact=impact,
            confidence=finding.confidence,
            remediation_steps=remediation,
            rollback_steps=rollback,
            reasoning_notes=notes,
        )

    def _assess_risk(self, ast: InfrastructureAST, chains: list[ReasoningChain]) -> RiskAssessment:
        score = 0.0
        attack_surface: list[str] = []
        exposed_services: list[str] = []
        credential_exposure: list[str] = []
        lateral_movement_paths: list[str] = []
        privilege_escalation_risks: list[str] = []

        for chain in chains:
            if "management" in chain.finding.category.lower() or "firewall" in chain.finding.category.lower():
                score += 0.15
            if "wireless" in chain.finding.category.lower():
                exposed_services.append("Wireless")
            if "telnet" in (chain.finding.title or "").lower():
                exposed_services.append("Telnet")
            if "ftp" in (chain.finding.title or "").lower():
                credential_exposure.append("FTP")
            if "root" in (chain.finding.title or "").lower() or "ssh" in (chain.finding.title or "").lower():
                credential_exposure.append("SSH")
            if "bridge" in chain.finding.category.lower():
                lateral_movement_paths.append("Bridge segments")
            if "ha" in chain.finding.category.lower():
                lateral_movement_paths.append("HA failure domain")
            if "password" in (chain.finding.title or "").lower():
                privilege_escalation_risks.append("Password exposure")
            if "privileged" in (chain.finding.title or "").lower():
                privilege_escalation_risks.append("Privileged container/role")

        score = min(score, 1.0)
        summary = f"Calculated risk score: {score:.0%}. "
        if exposed_services:
            summary += f"Exposed services: {', '.join(exposed_services)}. "
        if credential_exposure:
            summary += f"Credential exposure vectors: {', '.join(credential_exposure)}."
        return RiskAssessment(
            risk_score=round(score, 2),
            attack_surface=attack_surface,
            exposed_services=exposed_services,
            credential_exposure=credential_exposure,
            lateral_movement_paths=lateral_movement_paths,
            privilege_escalation_risks=privilege_escalation_risks,
            summary=summary.strip(),
        )

    def _generate_recommendations(self, ast: InfrastructureAST, chains: list[ReasoningChain]) -> list[str]:
        recs: list[str] = []
        seen: set[str] = set()
        for chain in chains:
            for step in chain.remediation_steps:
                if step not in seen:
                    seen.add(step)
                    recs.append(step)
        if not recs:
            recs.append("Review the detected configuration against vendor best practices and internal policy.")
        return recs[:10]

    def _plan_execution(self, ast: InfrastructureAST, chains: list[ReasoningChain]) -> list[str]:
        plan: list[str] = []
        for chain in chains:
            if chain.finding.severity in {Severity.high, Severity.critical}:
                plan.append(f"[{chain.finding.severity.value.upper()}] {chain.finding.title}: {'; '.join(chain.remediation_steps[:2])}")
        return plan

    def _build_explainability(self, ast: InfrastructureAST, chains: list[ReasoningChain]) -> dict[str, Any]:
        return {
            "vendor": ast.vendor.value,
            "format": ast.format,
            "finding_count": len(ast.findings),
            "reasoning_chains": [
                {
                    "finding": c.finding.title,
                    "premises": c.premises,
                    "conclusion": c.conclusion,
                    "impact": c.impact,
                    "confidence": c.confidence,
                    "remediation": c.remediation_steps,
                    "rollback": c.rollback_steps,
                    "notes": c.reasoning_notes,
                }
                for c in chains
            ],
        }

    def _generate_executive_summary(self, ast: InfrastructureAST, chains: list[ReasoningChain], risk: RiskAssessment) -> str:
        critical = sum(1 for c in chains if c.finding.severity == Severity.critical)
        high = sum(1 for c in chains if c.finding.severity == Severity.high)
        medium = sum(1 for c in chains if c.finding.severity == Severity.medium)
        low = sum(1 for c in chains if c.finding.severity == Severity.low)

        lines = [
            f"Detected {ast.vendor.value} {ast.format or 'configuration'}.",
            f"Findings: {critical} critical, {high} high, {medium} medium, {low} low.",
            f"Risk score: {risk.risk_score:.0%}.",
        ]
        if risk.exposed_services:
            lines.append(f"Exposed services: {', '.join(risk.exposed_services)}.")
        if risk.credential_exposure:
            lines.append(f"Credential exposure vectors: {', '.join(risk.credential_exposure)}.")
        if risk.lateral_movement_paths:
            lines.append(f"Lateral movement concerns: {', '.join(risk.lateral_movement_paths)}.")
        return " ".join(lines)

    def _build_roadmap(self, ast: InfrastructureAST, chains: list[ReasoningChain], risk: RiskAssessment) -> tuple[list[str], list[str], list[str]]:
        quick_wins: list[str] = []
        plan_30d: list[str] = []
        plan_90d: list[str] = []

        for chain in chains:
            title = chain.finding.title
            if chain.finding.severity in {Severity.high, Severity.critical}:
                plan_30d.append(f"Address {title}: {'; '.join(chain.remediation_steps[:2])}")
            elif chain.finding.severity == Severity.medium:
                quick_wins.append(f"Review {title}: {'; '.join(chain.remediation_steps[:2])}")
            else:
                plan_90d.append(f"Monitor {title} and validate baseline.")

        if not quick_wins:
            quick_wins.append("Review manager/alert rules for quick visibility improvements.")
        if not plan_30d:
            plan_30d.append("Validate management-plane access controls.")
        if not plan_90d:
            plan_90d.append("Schedule architecture review and baseline update.")

        return quick_wins[:5], plan_30d[:5], plan_90d[:5]

    def _compute_compliance_score(self, checks: list[ComplianceCheck]) -> float:
        if not checks:
            return 0.0
        passed = sum(1 for check in checks if check.passed)
        return round(passed / len(checks), 2)
