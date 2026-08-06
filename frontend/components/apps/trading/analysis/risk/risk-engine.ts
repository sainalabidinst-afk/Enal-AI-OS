import type { Candle } from "../../chart-engine/models/chart-models";
import { atr } from "../indicators/analysis-indicators";
import type { RiskAssessment, RiskLevel } from "../models/analysis-models";

export class RiskEngine {
  assess(candles: Candle[], signal: { confidence: number; signal: string }): RiskAssessment {
    if (candles.length < 14) {
      return {
        level: "medium",
        volatility: 0,
        confidence: 0,
        reasoning: "Insufficient data for risk assessment.",
      };
    }

    const atrResult = atr(14).calculate(candles);
    const lastAtr = atrResult.values[atrResult.values.length - 1];
    const lastClose = candles[candles.length - 1].close;
    const volatility = lastClose > 0 ? (lastAtr / lastClose) * 100 : 0;

    const level = this.determineRiskLevel(volatility, signal.confidence);
    const reasoning = this.buildReasoning(level, volatility, signal.confidence);

    return {
      level,
      volatility,
      confidence: signal.confidence,
      reasoning,
    };
  }

  private determineRiskLevel(volatility: number, confidence: number): RiskLevel {
    if (volatility > 5 || confidence < 40) return "extreme";
    if (volatility > 3 || confidence < 60) return "high";
    if (volatility > 1.5 || confidence < 75) return "medium";
    return "low";
  }

  private buildReasoning(level: RiskLevel, volatility: number, confidence: number): string {
    return `Risk level: ${level}. Volatility: ${volatility.toFixed(2)}%. AI confidence: ${confidence}%.`;
  }
}

export const riskEngine = new RiskEngine();

