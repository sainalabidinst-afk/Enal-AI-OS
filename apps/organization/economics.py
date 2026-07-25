"""
Organizational Economics
=========================

Cost/benefit/ROI analysis for organizational decisions.
Helps the CEO make informed decisions about team formation, model selection, and resource allocation.
"""

import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class CostEstimate:
    item: str
    estimated_cost: float
    cost_type: str = "token"
    confidence: float = 0.8
    breakdown: dict[str, float] = field(default_factory=dict)


@dataclass
class BenefitEstimate:
    item: str
    estimated_value: float
    benefit_type: str = "quality"
    confidence: float = 0.8
    description: str = ""


@dataclass
class ROIAnalysis:
    decision: str
    costs: list[CostEstimate] = field(default_factory=list)
    benefits: list[BenefitEstimate] = field(default_factory=list)
    net_value: float = 0.0
    roi: float = 0.0
    recommendation: str = ""
    confidence: float = 0.0


class OrganizationalEconomics:
    """Analyzes cost, benefit, and ROI for organizational decisions."""

    def __init__(self):
        self._analyses: dict[str, ROIAnalysis] = {}

    def analyze_team_formation(self, team_size: int, avg_cost_per_worker: float, estimated_duration_hours: float, expected_quality: float) -> ROIAnalysis:
        decision = f"team_formation_{team_size}_workers"
        token_cost = team_size * avg_cost_per_worker * estimated_duration_hours
        communication_cost = team_size * (team_size - 1) * 0.5 * estimated_duration_hours * 0.1
        meeting_cost = (team_size / 3) * estimated_duration_hours * 0.05
        total_cost = token_cost + communication_cost + meeting_cost

        quality_benefit = expected_quality * 100
        speed_benefit = (1.0 / team_size) * 50 if team_size > 0 else 0

        net_value = quality_benefit + speed_benefit - total_cost
        roi = (net_value / total_cost * 100) if total_cost > 0 else 0

        recommendation = "Proceed" if roi > 50 else "Consider reducing team size" if team_size > 5 else "Consider alternative approach"

        analysis = ROIAnalysis(
            decision=decision,
            costs=[
                CostEstimate(item="token_cost", estimated_cost=token_cost, breakdown={"per_worker": avg_cost_per_worker, "hours": estimated_duration_hours}),
                CostEstimate(item="communication_cost", estimated_cost=communication_cost, cost_type="overhead"),
                CostEstimate(item="meeting_cost", estimated_cost=meeting_cost, cost_type="overhead"),
            ],
            benefits=[
                BenefitEstimate(item="quality", estimated_value=quality_benefit, benefit_type="quality"),
                BenefitEstimate(item="speed", estimated_value=speed_benefit, benefit_type="speed"),
            ],
            net_value=net_value,
            roi=roi,
            recommendation=recommendation,
            confidence=0.7,
        )
        self._analyses[decision] = analysis
        logger.info("Team formation ROI: %.2f%% for %d workers", roi, team_size)
        return analysis

    def analyze_model_selection(self, model_cost_per_1k: float, estimated_tokens: int, quality_score: float, latency_ms: float, max_acceptable_latency: float = 2000.0) -> ROIAnalysis:
        decision = f"model_selection_cost_{model_cost_per_1k}_latency_{latency_ms}"
        total_cost = (estimated_tokens / 1000) * model_cost_per_1k
        latency_penalty = max(0, latency_ms - max_acceptable_latency) / 1000 * 0.1
        quality_benefit = quality_score * 100
        net_value = quality_benefit - total_cost - latency_penalty
        roi = (net_value / total_cost * 100) if total_cost > 0 else 0

        recommendation = "Selected model is cost-effective" if roi > 50 else "Consider cheaper model" if model_cost_per_1k > 0.001 else "Consider faster model" if latency_ms > max_acceptable_latency else "Model selection is acceptable"

        analysis = ROIAnalysis(
            decision=decision,
            costs=[CostEstimate(item="model_cost", estimated_cost=total_cost, cost_type="token", breakdown={"cost_per_1k": model_cost_per_1k, "tokens": estimated_tokens})],
            benefits=[BenefitEstimate(item="quality", estimated_value=quality_benefit, benefit_type="quality", description=f"Quality score: {quality_score}")],
            net_value=net_value,
            roi=roi,
            recommendation=recommendation,
            confidence=0.8,
        )
        self._analyses[decision] = analysis
        logger.info("Model selection ROI: %.2f%%", roi)
        return analysis

    def analyze_meeting_cost(self, participants: int, duration_minutes: int, avg_cost_per_participant_per_minute: float = 0.01) -> ROIAnalysis:
        decision = f"meeting_{participants}_participants_{duration_minutes}_minutes"
        total_cost = participants * duration_minutes * avg_cost_per_participant_per_minute
        benefit_value = participants * 10
        net_value = benefit_value - total_cost
        roi = (net_value / total_cost * 100) if total_cost > 0 else 0

        recommendation = "Meeting is worthwhile" if roi > 100 else "Consider async communication via Blackboard" if participants > 5 else "Meeting is acceptable"

        analysis = ROIAnalysis(
            decision=decision,
            costs=[CostEstimate(item="meeting_cost", estimated_cost=total_cost, cost_type="time", breakdown={"participants": participants, "minutes": duration_minutes})],
            benefits=[BenefitEstimate(item="synchronization", estimated_value=benefit_value, benefit_type="coordination")],
            net_value=net_value,
            roi=roi,
            recommendation=recommendation,
            confidence=0.6,
        )
        self._analyses[decision] = analysis
        logger.info("Meeting ROI: %.2f%% for %d participants, %d minutes", roi, participants, duration_minutes)
        return analysis

    def get_analysis(self, decision: str) -> ROIAnalysis | None:
        return self._analyses.get(decision)


organizational_economics = OrganizationalEconomics()
