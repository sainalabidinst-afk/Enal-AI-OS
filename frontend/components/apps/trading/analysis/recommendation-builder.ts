import type { SignalResult, RiskAssessment, MarketStructureResult } from "./models/analysis-models";

export interface Recommendation {
  action: "BUY" | "SELL" | "WAIT";
  reasoning: string;
  risk: "LOW" | "MEDIUM" | "HIGH" | "EXTREME";
  confidence: number;
  positionSize?: string;
  stopLoss?: number;
  takeProfit?: number;
}

export class RecommendationBuilder {
  static build(signal: SignalResult, risk: RiskAssessment, structure: MarketStructureResult): Recommendation {
    const action = signal.signal === "buy" ? "BUY" : signal.signal === "sell" ? "SELL" : "WAIT";

    let reasoning = `${structure.reasoning} `;
    reasoning += `Signal: ${signal.reasoning}. `;
    reasoning += `Risk: ${risk.reasoning}`;

    let positionSize = "1%";
    if (risk.level === "low") positionSize = "2-3%";
    else if (risk.level === "medium") positionSize = "1-2%";
    else if (risk.level === "high") positionSize = "0.5-1%";
    else positionSize = "Avoid";

    return {
      action,
      reasoning,
      risk: risk.level.toUpperCase() as Recommendation["risk"],
      confidence: signal.confidence,
      positionSize,
    };
  }
}

