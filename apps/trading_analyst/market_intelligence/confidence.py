"""
Confidence Scorer
=================

Computes final confidence score using weighted scoring model:

- Market Structure: 35%
- Trend: 25%
- Volume: 20%
- Volatility: 10%
- Session: 10%

Pure function: input Evidence list → output confidence score.
"""

from apps.trading_analyst.market_intelligence.models import Evidence, Bias

WEIGHTS = {
    "market_structure": 0.35,
    "trend": 0.25,
    "volume": 0.20,
    "volatility": 0.10,
    "session": 0.10,
}


def compute_weighted_score(evidence: list[Evidence]) -> tuple[Bias, float, dict[str, float]]:
    """
    Compute weighted confidence score from evidence.

    Args:
        evidence: List of Evidence items

    Returns:
        (bias, overall_confidence, category_scores)
    """
    by_category: dict[str, list[Evidence]] = {}
    for ev in evidence:
        cat = ev.type
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(ev)

    category_scores: dict[str, float] = {}
    total_weighted = 0.0
    total_weight = 0.0

    for category, weight in WEIGHTS.items():
        ev_list = by_category.get(category, [])
        if not ev_list:
            category_scores[category] = 0.0
            continue

        # Score: sum of (strength * confidence * direction_sign) / count
        cat_score = 0.0
        for ev in ev_list:
            sign = 1.0 if ev.direction == "bullish" else (-1.0 if ev.direction == "bearish" else 0.0)
            cat_score += sign * ev.strength * ev.confidence

        cat_score = cat_score / len(ev_list) if ev_list else 0.0
        category_scores[category] = cat_score
        total_weighted += cat_score * weight
        total_weight += weight

    if total_weight == 0:
        return Bias.NEUTRAL, 0.0, category_scores

    overall = total_weighted / total_weight

    # Determine bias based on overall score threshold
    if overall > 0.15:
        bias = Bias.BULLISH
    elif overall < -0.15:
        bias = Bias.BEARISH
    else:
        bias = Bias.NEUTRAL

    # Convert to 0-1 confidence scale
    confidence = min(1.0, abs(overall) * 2.0)

    return bias, confidence, category_scores


def compute_risk_level(bias: Bias, confidence: float, evidence: list[Evidence]) -> str:
    """
    Compute risk level based on bias confidence and evidence contradictions.

    Returns: "low", "medium", or "high"
    """
    # Count contradictory evidence
    bullish_count = sum(1 for e in evidence if e.direction == "bullish")
    bearish_count = sum(1 for e in evidence if e.direction == "bearish")
    total = max(bullish_count + bearish_count, 1)

    # Contradiction ratio
    if bias == Bias.BULLISH:
        contradiction_ratio = bearish_count / total
    elif bias == Bias.BEARISH:
        contradiction_ratio = bullish_count / total
    else:
        contradiction_ratio = min(bullish_count, bearish_count) / total

    # Low confidence + high contradiction = high risk
    if confidence < 0.3 and contradiction_ratio > 0.4:
        return "high"
    elif confidence < 0.5 or contradiction_ratio > 0.3:
        return "medium"
    else:
        return "low"
