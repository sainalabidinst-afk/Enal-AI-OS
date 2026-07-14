"""
Inference Engine
=================

Reasoning engine for network configurations.
Derives conclusions from evidence using network ontology.

Example reasoning:
  No VRRP + Single WAN + No Backup Route → Single Point of Failure
"""

from dataclasses import dataclass, field
from typing import Any

from apps.network_engineer.nic.knowledge.ontology import UniversalConcept


@dataclass
class Evidence:
    concept: UniversalConcept
    present: bool
    details: str = ""
    confidence: float = 1.0


@dataclass
class Hypothesis:
    id: str
    name: str
    description: str
    required_evidence: list[tuple[UniversalConcept, bool]]
    min_confidence: float = 0.7
    severity: str = "warning"
    recommendation: str = ""


@dataclass
class ReasoningChain:
    hypothesis_id: str
    evidence_found: list[Evidence]
    confidence: float
    conclusion: str
    recommendation: str


class InferenceEngine:
    """Reasoning engine for network configurations."""

    def __init__(self):
        self._hypotheses: list[Hypothesis] = []
        self._register_default_hypotheses()

    def _register_default_hypotheses(self):
        self._hypotheses = [
            Hypothesis(
                id="HYP-001",
                name="Single Point of Failure",
                description="Network has single point of failure due to lack of redundancy",
                required_evidence=[
                    (UniversalConcept.HIGH_AVAILABILITY, False),
                    (UniversalConcept.ROUTING, True),
                ],
                min_confidence=0.7,
                severity="critical",
                recommendation="Implement VRRP/HSRP/HA, add secondary WAN link, configure backup routes",
            ),
            Hypothesis(
                id="HYP-002",
                name="Security Risk - Open Management",
                description="Management services are exposed to the internet",
                required_evidence=[
                    (UniversalConcept.TRAFFIC_FILTERING, True),
                    (UniversalConcept.AUTHENTICATION, True),
                ],
                min_confidence=0.6,
                severity="critical",
                recommendation="Restrict management access to trusted networks, enable strong authentication",
            ),
            Hypothesis(
                id="HYP-003",
                name="Performance Risk - No QoS",
                description="Network lacks Quality of Service configuration",
                required_evidence=[
                    (UniversalConcept.QOS, False),
                    (UniversalConcept.ROUTING, True),
                ],
                min_confidence=0.6,
                severity="warning",
                recommendation="Implement QoS policies for critical traffic prioritization",
            ),
            Hypothesis(
                id="HYP-004",
                name="Compliance Risk - No Monitoring",
                description="Network lacks monitoring and logging",
                required_evidence=[
                    (UniversalConcept.MONITORING, False),
                    (UniversalConcept.LOGGING, False),
                ],
                min_confidence=0.7,
                severity="warning",
                recommendation="Enable SNMP monitoring and centralized logging",
            ),
            Hypothesis(
                id="HYP-005",
                name="Operational Risk - No Backup",
                description="Network has no backup configuration",
                required_evidence=[
                    (UniversalConcept.BACKUP, False),
                ],
                min_confidence=0.8,
                severity="warning",
                recommendation="Configure automated configuration backups",
            ),
            Hypothesis(
                id="HYP-006",
                name="DNS Risk - No Redundant DNS",
                description="Network has single DNS server",
                required_evidence=[
                    (UniversalConcept.DNS_RESOLUTION, True),
                ],
                min_confidence=0.5,
                severity="info",
                recommendation="Configure secondary DNS server for redundancy",
            ),
            Hypothesis(
                id="HYP-007",
                name="Time Risk - No NTP",
                description="Network lacks time synchronization",
                required_evidence=[
                    (UniversalConcept.TIME_SYNCHRONIZATION, False),
                ],
                min_confidence=0.8,
                severity="warning",
                recommendation="Configure NTP for accurate timekeeping across devices",
            ),
            Hypothesis(
                id="HYP-008",
                name="Segmentation Risk - Flat Network",
                description="Network lacks VLAN segmentation",
                required_evidence=[
                    (UniversalConcept.VLAN, False),
                    (UniversalConcept.TRAFFIC_FILTERING, True),
                ],
                min_confidence=0.6,
                severity="warning",
                recommendation="Implement VLANs to segment network traffic",
            ),
        ]

    def reason(self, evidence_list: list[Evidence]) -> list[ReasoningChain]:
        chains = []
        for hypothesis in self._hypotheses:
            matched = []
            for concept, expected in hypothesis.required_evidence:
                for ev in evidence_list:
                    if ev.concept == concept:
                        matched.append(ev)
                        break

            if len(matched) < len(hypothesis.required_evidence):
                continue

            all_match = all(
                ev.present == expected
                for ev, (_, expected) in zip(matched, hypothesis.required_evidence)
            )
            if not all_match:
                continue

            confidence = min(ev.confidence for ev in matched)
            if confidence < hypothesis.min_confidence:
                continue

            chains.append(ReasoningChain(
                hypothesis_id=hypothesis.id,
                evidence_found=matched,
                confidence=confidence,
                conclusion=hypothesis.description,
                recommendation=hypothesis.recommendation,
            ))

        chains.sort(key=lambda c: c.confidence, reverse=True)
        return chains

    def add_hypothesis(self, hypothesis: Hypothesis) -> None:
        self._hypotheses.append(hypothesis)

    def get_hypotheses(self) -> list[Hypothesis]:
        return list(self._hypotheses)


inference_engine = InferenceEngine()
