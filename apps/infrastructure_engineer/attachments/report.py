from __future__ import annotations

from typing import Any

from apps.infrastructure_engineer.attachments.reasoning import InfrastructureReasoningEngine, ReasoningChain


class ExecutiveReportGenerator:
    def generate(self, result: Any) -> str:
        ast = result.ast
        chains = result.reasoning_chains
        risk = result.risk_assessment
        engine = InfrastructureReasoningEngine()

        lines: list[str] = []
        lines.append("# Infrastructure Analysis Report")
        lines.append("")
        lines.append("## Executive Summary")
        lines.append("")
        lines.append(result.executive_summary or engine._generate_executive_summary(ast, chains, risk))
        lines.append("")
        lines.append("## Detected Environment")
        lines.append("")
        lines.append(f"- Vendor: {ast.vendor.value}")
        lines.append(f"- Format: {ast.format or 'unknown'}")
        lines.append(f"- Device Role: {ast.device_role.value}")
        lines.append(f"- Interfaces: {len(ast.interfaces)}")
        lines.append(f"- VLANs: {len(ast.vlans)}")
        lines.append(f"- Routing entries: {len(ast.routing)}")
        lines.append(f"- Firewall entries: {len(ast.firewall)}")
        lines.append("")
        lines.append("## Current Risk")
        lines.append("")
        if risk:
            lines.append(f"- Risk Score: {risk.risk_score:.0%}")
            if risk.exposed_services:
                lines.append(f"- Exposed Services: {', '.join(risk.exposed_services)}")
            if risk.credential_exposure:
                lines.append(f"- Credential Exposure: {', '.join(risk.credential_exposure)}")
            if risk.lateral_movement_paths:
                lines.append(f"- Lateral Movement: {', '.join(risk.lateral_movement_paths)}")
            if risk.privilege_escalation_risks:
                lines.append(f"- Privilege Escalation: {', '.join(risk.privilege_escalation_risks)}")
        lines.append("")
        lines.append("## Critical Findings")
        lines.append("")
        critical_chains = [c for c in chains if c.finding.severity.value == "critical"]
        high_chains = [c for c in chains if c.finding.severity.value == "high"]
        medium_chains = [c for c in chains if c.finding.severity.value == "medium"]

        if critical_chains:
            for chain in critical_chains:
                lines.extend(self._format_chain(chain))
        if high_chains:
            lines.append("### High")
            lines.append("")
            for chain in high_chains:
                lines.extend(self._format_chain(chain))
        if medium_chains:
            lines.append("### Medium")
            lines.append("")
            for chain in medium_chains[:8]:
                lines.extend(self._format_chain(chain))
        if not critical_chains and not high_chains and not medium_chains:
            lines.append("No significant findings detected.")
            lines.append("")

        lines.append("## Quick Wins")
        lines.append("")
        for item in result.quick_wins:
            lines.append(f"- {item}")
        lines.append("")

        lines.append("## 30-Day Plan")
        lines.append("")
        for item in result.plan_30d:
            lines.append(f"- {item}")
        lines.append("")

        lines.append("## 90-Day Plan")
        lines.append("")
        for item in result.plan_90d:
            lines.append(f"- {item}")
        lines.append("")

        lines.append("## Recommendations")
        lines.append("")
        for rec in result.recommendations:
            lines.append(f"- {rec}")
        lines.append("")

        lines.append("## Execution Plan")
        lines.append("")
        for step in result.execution_plan:
            lines.append(f"- {step}")
        lines.append("")

        lines.append("## Explainability")
        lines.append("")
        for chain in chains[:10]:
            lines.append(f"### {chain.finding.title}")
            lines.append("")
            if chain.premises:
                lines.append("**Evidence:**")
                for premise in chain.premises[:3]:
                    lines.append(f"- `{premise}`")
                lines.append("")
            lines.append(f"**Reasoning:** {chain.conclusion}")
            lines.append("")
            lines.append(f"**Impact:** {chain.impact}")
            lines.append("")
            lines.append(f"**Confidence:** {chain.confidence:.0%}")
            lines.append("")
            if chain.remediation_steps:
                lines.append("**Remediation:**")
                for step in chain.remediation_steps:
                    lines.append(f"- {step}")
                lines.append("")
            if chain.rollback_steps:
                lines.append("**Rollback:**")
                for step in chain.rollback_steps:
                    lines.append(f"- {step}")
                lines.append("")
        return "\n".join(lines)

    def _format_chain(self, chain: ReasoningChain) -> list[str]:
        lines: list[str] = []
        lines.append(f"### {chain.finding.title}")
        lines.append("")
        lines.append(f"- Severity: {chain.finding.severity.value}")
        lines.append(f"- Category: {chain.finding.category}")
        lines.append(f"- Description: {chain.finding.description}")
        if chain.premises:
            lines.append("- Evidence:")
            for premise in chain.premises[:3]:
                lines.append(f"  - `{premise}`")
        lines.append(f"- Reasoning: {chain.conclusion}")
        lines.append(f"- Impact: {chain.impact}")
        lines.append(f"- Confidence: {chain.confidence:.0%}")
        if chain.finding.recommendation:
            lines.append(f"- Recommendation: {chain.finding.recommendation}")
        lines.append("")
        return lines
