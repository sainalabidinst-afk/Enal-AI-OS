"""
Capability Gap Detector
=======================

Detects whether a user query can be handled by existing ECP capability packs.
If not, flags the query as a capability gap and suggests a new domain/pack.

Algorithm:
    1. Route user query through IntentRouter.
    2. If best domain is GENERAL and confidence is below threshold → potential gap.
    3. Extract topics from query via keyword/entity matching.
    4. Check existing pack capability descriptions for topic coverage.
    5. If no existing pack covers the topics → flag as capability gap.
    6. Return structured GapDetectionResult.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from apps.self_development.schemas import CapabilityProposal, ProposalStatus
from apps.society.intent_router import IntentDomain, IntentRouter, intent_router

logger = logging.getLogger(__name__)

CONFIDENCE_THRESHOLD = 0.55

TOPIC_KEYWORDS: dict[str, list[str]] = {
    "observability": [
        "metrics",
        "tracing",
        "logging",
        "monitoring",
        "anomaly-detection",
        "alert",
        "dashboard",
        "prometheus",
        "grafana",
        "observabilitas",
        "monitor",
        "logging",
        "tracing",
    ],
    "cybersecurity": [
        "threat",
        "vulnerability",
        "penetration",
        "incident",
        "compliance",
        "security-audit",
        "cve",
        "exploit",
        "firewall",
        "siem",
        "keamanan",
        "serangan",
        "malware",
        "ransomware",
        "audit-keamanan",
    ],
    "ai-ethics": [
        "bias",
        "fairness",
        "explainability",
        "responsible-ai",
        "ethics",
        "governance",
        "regulatory",
        "model-card",
        "etika",
        " fairness",
        "penjelasan",
        "regulasi",
    ],
    "supply-chain": [
        "logistics",
        "warehouse",
        "shipping",
        "demand-forecast",
        "inventory",
        "procurement",
        "supplier",
        "route-optimization",
        "supply-chain",
        "gudang",
        "pengiriman",
        "permintaan",
        "stok",
        "pemasok",
    ],
    "data-science": [
        "machine-learning",
        "ml",
        "feature-engineering",
        "model-training",
        "evaluation",
        "pipeline",
        "experiment",
        "jupyter",
        "data-science",
        "pelatihan-model",
        "eksperimen",
        "data",
    ],
    "business-intelligence": [
        "dashboard",
        "kpi",
        "reporting",
        "visualization",
        "power-bi",
        "looker",
        "metabase",
        "analytics",
        "business-intelligence",
        "laporan",
        "visualisasi",
        "metrik",
        "kpi",
    ],
    "innovation": [
        "trend-analysis",
        "foresight",
        "rd-portfolio",
        "technology-radar",
        "emerging-tech",
        "roadmap",
        "inovasi",
        "tren",
        "teknologi-masa-depan",
        "portfolio",
        "penelitian",
    ],
    "devsecops": [
        "shift-left",
        "security-by-design",
        "dependency-scan",
        "policy-as-code",
        "opa",
        "trivy",
        "sast",
        "dast",
        "devsecops",
        "ci-cd",
        "pipeline",
        "otomatisasi",
    ],
    "translator": [
        "translation",
        "multilingual",
        "localization",
        "glossary",
        "language-detection",
        "i18n",
        "l10n",
        "translator",
        "penerjemahan",
        "terjemahan",
        "bahasa",
        "lokalisasi",
        "glosarium",
    ],
    "document-processing": [
        "pdf",
        "docx",
        "xlsx",
        "pptx",
        "ocr",
        "document-parse",
        "extract-text",
        "reportlab",
        "document-processing",
        "dokumen",
        "pdf",
        "word",
        "excel",
        "powerpoint",
        "ekstraksi",
    ],
    "voice-interaction": [
        "stt",
        "tts",
        "speech-to-text",
        "text-to-speech",
        "voice-command",
        "telephony",
        "twilio",
        "wake-word",
        "voice",
        "suara",
        "percakapan",
        "telepon",
    ],
    "robotics": [
        "ros2",
        "robot",
        "edge",
        "iot",
        "mqtt",
        "camera",
        "vision",
        "yolo",
        "tensorrt",
        "jetson",
        "robotika",
        "otomatisasi",
        "pertanian",
        "smart-agri",
    ],
    "decision-intelligence": [
        "digital-twin",
        "simulation",
        "scenario",
        "monte-carlo",
        "causal",
        "counterfactual",
        "red-team",
        "adversarial",
        "decision",
        "keputusan",
        "simulasi",
        "analisis-keputusan",
    ],
    "self-evolving": [
        "autonomous",
        "self-healing",
        "capability-synthesis",
        "pack-generator",
        "federated",
        "consent-gate",
        "governance-sandbox",
        "self-evolving",
        "mandiri",
        "otomatis",
        "sintesis",
        "federasi",
    ],
    "visual-builder": [
        "reactflow",
        "canvas",
        "blueprint",
        "node-editor",
        "visual-builder",
        "agent-builder",
        "tool-builder",
        "visual",
        "builder",
        "blueprint",
        "node",
        "editor",
    ],
}


@dataclass
class GapDetectionResult:
    is_gap: bool
    suggested_domain: str
    confidence: float
    matched_capabilities: list[str]
    gap_reason: str
    proposed_pack: CapabilityProposal | None = None


class CapabilityGapDetector:
    """Detects capability gaps from user queries."""

    def __init__(self, router: IntentRouter | None = None) -> None:
        self.router = router or intent_router

    def detect(self, user_query: str) -> GapDetectionResult:
        lowered = user_query.lower()
        intent = self.router.route(user_query)

        matched_capabilities = self._collect_matched_capabilities(lowered)
        topic_coverage = self._check_topic_coverage(lowered)

        if intent.confidence >= CONFIDENCE_THRESHOLD and intent.domain != IntentDomain.GENERAL:
            return GapDetectionResult(
                is_gap=False,
                suggested_domain=intent.domain.value,
                confidence=intent.confidence,
                matched_capabilities=matched_capabilities,
                gap_reason="Query covered by existing capability pack.",
            )

        if topic_coverage:
            return GapDetectionResult(
                is_gap=False,
                suggested_domain=intent.domain.value,
                confidence=max(intent.confidence, topic_coverage["confidence"]),
                matched_capabilities=matched_capabilities,
                gap_reason="Query partially covered by existing pack topics.",
            )

        best_topic = self._best_topic_match(lowered)
        if best_topic:
            return GapDetectionResult(
                is_gap=True,
                suggested_domain=best_topic,
                confidence=0.6,
                matched_capabilities=matched_capabilities,
                gap_reason=f"No existing pack covers topic: {best_topic}.",
                proposed_pack=self._build_proposal(best_topic, user_query),
            )

        return GapDetectionResult(
            is_gap=True,
            suggested_domain="unknown",
            confidence=0.4,
            matched_capabilities=matched_capabilities,
            gap_reason="Query intent unclear; no matching domain or topic found.",
        )

    def _collect_matched_capabilities(self, lowered_query: str) -> list[str]:
        matched: list[str] = []
        for domain, pack in self.router._capability_packs.items():
            for capability in pack.capabilities:
                if capability.replace("-", " ") in lowered_query or capability in lowered_query:
                    matched.append(f"{domain.value}:{capability}")
        return matched

    def _check_topic_coverage(self, lowered_query: str) -> dict[str, Any] | None:
        best_domain = None
        best_score = 0
        for domain, keywords in TOPIC_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in lowered_query)
            if score > best_score:
                best_score = score
                best_domain = domain

        if best_domain and best_score >= 2:
            pack_name_map = {
                "observability": "Observability Engineer",
                "cybersecurity": "Cybersecurity Analyst",
                "ai-ethics": "AI Ethics & Governance",
                "supply-chain": "Supply Chain Analyst",
                "data-science": "Data Scientist",
                "business-intelligence": "Business Intelligence",
                "innovation": "Innovation Strategist",
                "devsecops": "DevSecOps",
                "translator": "Translator Expert",
                "document-processing": "Document Processing",
                "voice-interaction": "Voice Interaction",
                "robotics": "Robotics & Edge AI",
                "decision-intelligence": "Decision Intelligence",
                "self-evolving": "Self-Evolving Platform",
                "visual-builder": "Visual Builder",
            }
            return {
                "domain": best_domain,
                "score": best_score,
                "pack": pack_name_map.get(best_domain, best_domain),
                "confidence": min(1.0, 0.4 + 0.1 * best_score),
            }
        return None

    def _best_topic_match(self, lowered_query: str) -> str | None:
        best_domain = None
        best_score = 0
        for domain, keywords in TOPIC_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in lowered_query)
            if score > best_score:
                best_score = score
                best_domain = domain
        return best_domain if best_score > 0 else None

    def _build_proposal(self, domain: str, user_query: str) -> CapabilityProposal:
        pack_name_map = {
            "observability": "Observability Engineer",
            "cybersecurity": "Cybersecurity Analyst",
            "ai-ethics": "AI Ethics & Governance",
            "supply-chain": "Supply Chain Analyst",
            "data-science": "Data Scientist",
            "business-intelligence": "Business Intelligence",
            "innovation": "Innovation Strategist",
            "devsecops": "DevSecOps",
            "translator": "Translator Expert",
            "document-processing": "Document Processing",
            "voice-interaction": "Voice Interaction",
            "robotics": "Robotics & Edge AI",
            "decision-intelligence": "Decision Intelligence",
            "self-evolving": "Self-Evolving Platform",
            "visual-builder": "Visual Builder",
        }
        description_map = {
            "observability": "Metrics, tracing, logging, anomaly detection",
            "cybersecurity": "Threat modeling, incident detection, compliance mapping",
            "ai-ethics": "Fairness, bias detection, explainability, regulatory compliance",
            "supply-chain": "Logistics optimization, demand forecasting, risk management",
            "data-science": "Advanced ML pipelines, feature engineering, model evaluation",
            "business-intelligence": "Dashboarding, KPI tracking, scenario planning",
            "innovation": "Trend analysis, foresight modeling, R&D portfolio",
            "devsecops": "Security-by-design, shift-left, compliance-as-code",
            "translator": "Document translation, multilingual support, localization",
            "document-processing": "PDF, DOCX, CSV parsing, extraction, OCR",
            "voice-interaction": "STT, TTS, voice commands, telephony",
            "robotics": "ROS2, edge inference, computer vision, IoT automation",
            "decision-intelligence": "Digital twin, simulation, causal reasoning, red teaming",
            "self-evolving": "Autonomous pack synthesis, self-healing, federated memory",
            "visual-builder": "ReactFlow canvas, agent/tool builder, blueprints",
        }
        name = pack_name_map.get(domain, domain)
        description = description_map.get(domain, user_query)
        return CapabilityProposal(
            id=f"cap-{domain}-gap",
            name=name,
            domain=domain,
            description=description,
            tier="tier_b",
            reuse_potential=0,
            estimated_effort="medium",
            risk="medium",
            confidence=0.6,
            rationale=f"Capability gap detected from user query: {user_query}",
            required_packs=[],
            status=ProposalStatus.DRAFT.value,
        )
