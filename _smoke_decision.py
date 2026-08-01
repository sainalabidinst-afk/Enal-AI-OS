"""
Smoke test for Decision Intelligence pipeline (RFC-0007).
Run: python _smoke_decision.py
"""

from apps.decision_intelligence.engine import DecisionIntelligenceEngine
from apps.decision_intelligence.schemas import (
    DecisionRequest,
    EvidenceSource,
    Objective,
)


def main():
    engine = DecisionIntelligenceEngine()

    # Simulate a Trading Analyst decision: 'Should I enter a long position on BTC?'
    request = DecisionRequest(
        context="Should I enter a long position on BTCUSDT?",
        evidence_sources=[
            EvidenceSource(
                source_id="trading_analyst",
                evidence_type="analysis",
                payload={"sentiment": "bullish", "confidence": 0.85, "risk": 0.3},
                quality_score=0.85,
                weight=1.5,
            ),
            EvidenceSource(
                source_id="macro_economic",
                evidence_type="data",
                payload={"sentiment": "positive", "gdp_growth": 2.2, "cpi": 2.8},
                quality_score=0.7,
                weight=1.0,
            ),
            EvidenceSource(
                source_id="technical_analysis",
                evidence_type="analysis",
                payload={"bias": "bullish", "score": 0.78, "rsi": 55},
                quality_score=0.75,
                weight=1.2,
            ),
            EvidenceSource(
                source_id="risk_management",
                evidence_type="recommendation",
                payload={"recommendation": "proceed_with_caution", "max_risk": 0.05},
                quality_score=0.9,
                weight=1.0,
            ),
        ],
        constraints=["no leverage above 2x", "must have stop loss"],
        objectives=[
            Objective(name="Accuracy", weight=0.35, goal="maximize"),
            Objective(name="Risk", weight=0.30, goal="minimize"),
            Objective(name="Cost", weight=0.20, goal="minimize"),
            Objective(name="Latency", weight=0.15, goal="minimize"),
        ],
        risk_tolerance="medium",
        max_alternatives=5,
        include_explanation=True,
    )

    result = engine.evaluate(request)
    d = result.to_dict()

    print("=== SMOKE TEST: DECISION INTELLIGENCE ===")
    print("Decision ID:", d["decision_id"])
    print("Recommended:", d["recommended_decision"])
    print("Confidence:", d["confidence_score"])
    print("Confidence explanation:", d["confidence_explanation"])
    print("Alternatives:", len(d["alternatives"]))
    for i, alt in enumerate(d["alternatives"]):
        desc = alt["description"]
        score = alt["score"]
        risk = alt["risk_profile"]["overall_risk"]
        print(f"  #{i+1}: {desc}  score={score:.2f}  risk={risk:.2f}")

    print()
    print("Explanation chain:")
    print("  Evidence:", d["explanation"]["evidence_summary"][:150])
    print("  Reasoning steps:", len(d["explanation"]["reasoning_chain"]))
    for step in d["explanation"]["reasoning_chain"][:4]:
        print("   -", step)
    print("  Risk:", d["explanation"]["risk_assessment"][:150])
    print("  Rationale:", d["explanation"]["final_rationale"][:200])
    print()
    print("Raw metrics:", d["raw"])
    print("History ref:", d["decision_history_ref"])
    print("ALL OK")


if __name__ == "__main__":
    main()

