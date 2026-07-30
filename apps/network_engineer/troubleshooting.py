"""
Troubleshooting Engine
=======================

Structured troubleshooting workflow that learns from network engineer patterns.
Input: symptom → evidence → hypothesis → verification → root cause.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class VerificationStatus(str, Enum):
    CONFIRMED = "confirmed"
    RULED_OUT = "ruled_out"
    PARTIAL = "partial"
    UNKNOWN = "unknown"


@dataclass
class EvidenceItem:
    source: str
    content: str
    timestamp: str = ""
    confidence: float = 1.0


@dataclass
class Hypothesis:
    id: str
    title: str
    description: str
    required_evidence: list[str] = field(default_factory=list)
    verification_steps: list[str] = field(default_factory=list)
    confidence: float = 0.0
    status: VerificationStatus = VerificationStatus.UNKNOWN


@dataclass
class TroubleshootingSession:
    session_id: str
    symptom: str
    evidence: list[EvidenceItem] = field(default_factory=list)
    hypotheses: list[Hypothesis] = field(default_factory=list)
    counter_hypotheses: list[Hypothesis] = field(default_factory=list)
    root_cause: Hypothesis | None = None
    resolution: str = ""
    confidence: float = 0.0
    status: str = "open"

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "symptom": self.symptom,
            "evidence": [
                {
                    "source": e.source,
                    "content": e.content,
                    "timestamp": e.timestamp,
                    "confidence": e.confidence,
                }
                for e in self.evidence
            ],
            "hypotheses": [
                {
                    "id": h.id,
                    "title": h.title,
                    "description": h.description,
                    "confidence": h.confidence,
                    "status": h.status.value,
                    "verification_steps": h.verification_steps,
                }
                for h in self.hypotheses
            ],
            "counter_hypotheses": [
                {
                    "id": h.id,
                    "title": h.title,
                    "description": h.description,
                    "confidence": h.confidence,
                    "status": h.status.value,
                }
                for h in self.counter_hypotheses
            ],
            "root_cause": {
                "id": self.root_cause.id,
                "title": self.root_cause.title,
                "description": self.root_cause.description,
                "confidence": self.root_cause.confidence,
                "status": self.root_cause.status.value,
            } if self.root_cause else None,
            "resolution": self.resolution,
            "confidence": self.confidence,
            "status": self.status,
        }


class TroubleshootingEngine:
    """Structured troubleshooting engine for network issues."""

    def __init__(self):
        self._symptom_patterns: dict[str, list[Hypothesis]] = self._build_patterns()

    def _build_patterns(self) -> dict[str, list[Hypothesis]]:
        return {
            "ping timeout": [
                Hypothesis(
                    id="TSH-001",
                    title="Downstream Device Unreachable",
                    description="The target device is powered off, disconnected, or has no IP reachability.",
                    required_evidence=["icmp_timeout", "device_status"],
                    verification_steps=[
                        "Ping the target IP directly.",
                        "Check physical link LEDs.",
                        "Verify interface status on upstream device.",
                    ],
                ),
                Hypothesis(
                    id="TSH-002",
                    title="Routing Blackhole",
                    description="A static or dynamic route is missing or incorrect toward the destination.",
                    required_evidence=["route_check", "traceroute"],
                    verification_steps=[
                        "Run traceroute to identify blackhole.",
                        "Check routing table for destination prefix.",
                        "Verify next-hop reachability.",
                    ],
                ),
                Hypothesis(
                    id="TSH-003",
                    title="Firewall Blocking ICMP",
                    description="Firewall or ACL is dropping ICMP echo requests.",
                    required_evidence=["firewall_log", "acl_check"],
                    verification_steps=[
                        "Review firewall logs for dropped packets.",
                        "Temporarily allow ICMP to test.",
                        "Check NAT and forwarding rules.",
                    ],
                ),
            ],
            "intermittent connectivity": [
                Hypothesis(
                    id="TSH-004",
                    title="Interface Flapping",
                    description="Physical interface is going up and down due to cabling, duplex, or SFP issues.",
                    required_evidence=["interface_status_history", "error_counts"],
                    verification_steps=[
                        "Check interface error counters (CRC, runts, giants).",
                        "Replace cable or SFP module.",
                        "Force duplex and speed settings.",
                    ],
                ),
                Hypothesis(
                    id="TSH-005",
                    title="Routing Instability",
                    description="Dynamic routing protocol is flapping routes due to unstable neighbors or MTU mismatch.",
                    required_evidence=["ospf_bdf", "bgp_state_changes"],
                    verification_steps=[
                        "Check routing protocol neighbor state.",
                        "Verify MTU consistency across links.",
                        "Review interface dampening settings.",
                    ],
                ),
            ],
            "slow network": [
                Hypothesis(
                    id="TSH-006",
                    title="Bandwidth Saturation",
                    description="Link utilization is near capacity, causing queuing delays.",
                    required_evidence=["interface_utilization", "qos_policy"],
                    verification_steps=[
                        "Check interface utilization via SNMP.",
                        "Identify top talkers.",
                        "Implement QoS or increase bandwidth.",
                    ],
                ),
                Hypothesis(
                    id="TSH-007",
                    title="DNS Latency",
                    description="DNS resolution is slow, delaying application responses.",
                    required_evidence=["dns_query_time", "dns_log"],
                    verification_steps=[
                        "Measure DNS query response time.",
                        "Check DNS server health.",
                        "Configure local DNS cache.",
                    ],
                ),
            ],
        }

    def create_session(self, symptom: str) -> TroubleshootingSession:
        import uuid
        return TroubleshootingSession(session_id=str(uuid.uuid4())[:8], symptom=symptom)

    def add_evidence(self, session: TroubleshootingSession, source: str, content: str, confidence: float = 1.0) -> None:
        from datetime import datetime, timezone
        session.evidence.append(EvidenceItem(
            source=source,
            content=content,
            timestamp=datetime.now(timezone.utc).isoformat() + "Z",
            confidence=confidence,
        ))

    def generate_hypotheses(self, session: TroubleshootingSession) -> list[Hypothesis]:
        symptom_key = session.symptom.lower()
        matched = []
        for key, hypotheses in self._symptom_patterns.items():
            if key in symptom_key:
                matched.extend(hypotheses)
        session.hypotheses = matched
        return matched

    def add_counter_hypothesis(self, session: TroubleshootingSession, hypothesis: Hypothesis) -> None:
        session.counter_hypotheses.append(hypothesis)

    def verify_hypothesis(self, session: TroubleshootingSession, hypothesis_id: str, status: VerificationStatus) -> None:
        for h in session.hypotheses:
            if h.id == hypothesis_id:
                h.status = status
                if status == VerificationStatus.CONFIRMED:
                    session.root_cause = h
                break

    def conclude(self, session: TroubleshootingSession, resolution: str, confidence: float) -> None:
        session.resolution = resolution
        session.confidence = confidence
        session.status = "resolved" if session.root_cause else "investigating"


troubleshooting_engine = TroubleshootingEngine()
