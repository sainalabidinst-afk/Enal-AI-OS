from __future__ import annotations


from backend.app.core.attachments.models import InfrastructureAST, InfrastructureFinding, Severity


class CrossFileReasoningEngine:
    def cross_reason(self, asts: list[InfrastructureAST]) -> InfrastructureAST:
        combined = InfrastructureAST()
        if not asts:
            return combined

        primary = asts[0]
        combined.vendor = primary.vendor
        combined.device_role = primary.device_role
        combined.format = primary.format
        combined.version = primary.version

        for ast in asts:
            combined.interfaces.extend(ast.interfaces)
            combined.vlans.extend(ast.vlans)
            combined.routing.extend(ast.routing)
            combined.firewall.extend(ast.firewall)
            combined.services.extend(ast.services)
            combined.security.extend(ast.security)
            combined.wireless.extend(ast.wireless)
            combined.ha.extend(ast.ha)
            combined.findings.extend(ast.findings)
combined.system["sources"] = combined.system.get("sources", []) + [ast.metadata.get("source")]
             for key, value in ast.system.items():
                 if isinstance(value, list):
                     combined.system.setdefault(key, []).extend(value)
                 else:
                     combined.system[key] = value
             for key, value in ast.metadata.items():
                 combined.metadata.setdefault(key, value)

        self._detect_vlan_gaps(combined)
        self._detect_unreachable_subnets(combined)
        self._detect_consistency_gaps(combined)
        return combined

    def _detect_vlan_gaps(self, combined: InfrastructureAST) -> None:
        switch_vlans = {str(item.get("id") or item.get("raw", "")).strip() for item in combined.vlans}
        router_vlans = {str(item.get("id") or item.get("name") or item.get("raw", "")).strip() for item in combined.routing}
        missing_vlans = sorted(switch_vlans - router_vlans)
        if missing_vlans:
            combined.findings.append(
                InfrastructureFinding(
                    severity=Severity.medium,
                    category="cross-file",
                    title="VLAN routing gap detected",
                    description=f"Switch VLANs {missing_vlans} were not detected in router configuration.",
                    confidence=0.7,
                    evidence=[f"Switch VLANs: {missing_vlans}"],
                )
            )

    def _detect_unreachable_subnets(self, combined: InfrastructureAST) -> None:
        firewall_entries = [str(item.get("raw", "")) for item in combined.firewall]
        routing_entries = [str(item.get("raw", "")) for item in combined.routing]
        if firewall_entries and routing_entries:
            combined.findings.append(
                InfrastructureFinding(
                    severity=Severity.medium,
                    category="cross-file",
                    title="Firewall/routing consistency review needed",
                    description="Verify that firewall rules and routing entries cover the same address space.",
                    confidence=0.6,
                    evidence=firewall_entries[:3] + routing_entries[:3],
                )
            )

    def _detect_consistency_gaps(self, combined: InfrastructureAST) -> None:
        routing_text = " ".join(str(item.get("raw", "")) for item in combined.routing).lower()
        if "ospf" in routing_text:
            combined.findings.append(
                InfrastructureFinding(
                    severity=Severity.low,
                    category="cross-file",
                    title="Routing protocol requires validation",
                    description="Review if routing protocol configuration is present across all expected nodes.",
                    confidence=0.5,
                )
            )
