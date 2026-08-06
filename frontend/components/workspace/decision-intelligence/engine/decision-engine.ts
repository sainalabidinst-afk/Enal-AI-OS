import type { DecisionRequest, DecisionOutcome, DecisionConfidence, TradeOffAnalysis, DecisionReasoning } from "../models/decision-models";

export class DecisionEngine {
  evaluate(request: DecisionRequest): DecisionOutcome {
    const confidence = this.recalculateConfidence(request);
    const confidenceLevel = this.mapConfidenceLevel(confidence);
    const action = this.determineAction(request, confidence);
    const reasoning = this.buildReasoning(request, action);
    const alternatives = this.rankAlternatives(request, action);
    const riskAssessment = this.assessRisk(request, action);

    return {
      decisionId: `decision-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`,
      action,
      confidence,
      confidenceLevel,
      reasoning,
      alternatives,
      riskAssessment,
      nextAction: this.buildNextAction(action, confidence, riskAssessment.level),
      timestamp: Date.now(),
      capabilityId: request.capabilityId,
    };
  }

  private recalculateConfidence(request: DecisionRequest): number {
    let baseConfidence = request.signal.confidence;
    const riskPenalty = request.risk.volatility * 2;
    const evidenceBonus = Math.min(request.evidence.length * 2, 10);
    const adjustedConfidence = baseConfidence - riskPenalty + evidenceBonus;
    return Math.min(Math.max(Math.round(adjustedConfidence), 0), 100);
  }

  private mapConfidenceLevel(confidence: number): DecisionConfidence {
    if (confidence >= 90) return "very_high";
    if (confidence >= 75) return "high";
    if (confidence >= 60) return "medium";
    if (confidence >= 40) return "low";
    return "very_low";
  }

  private determineAction(request: DecisionRequest, confidence: number): DecisionOutcome["action"] {
    const signalAction = request.signal.action.toLowerCase() as DecisionOutcome["action"];

    if (confidence < 30) return "wait";
    if (request.risk.level === "extreme") return "wait";
    if (request.risk.level === "high" && confidence < 60) return "wait";

    return signalAction;
  }

  private buildReasoning(request: DecisionRequest, action: DecisionOutcome["action"]): DecisionReasoning {
    const evidenceChain = request.evidence.map((e) => `${e.label}: ${e.value}`);

    const tradeOffs: TradeOffAnalysis = {
      benefit: `Strong ${request.signal.action} signal with ${request.signal.confidence}% confidence`,
      cost: `Market volatility at ${request.risk.volatility.toFixed(2)}%`,
      net: action === "wait" ? "Risk exceeds opportunity" : "Opportunity outweighs risk",
    };

    const primary = `Decision: ${action.toUpperCase()}. ` +
      `Signal confidence: ${request.signal.confidence}%. ` +
      `Risk level: ${request.risk.level}. ` +
      `Final confidence: ${this.recalculateConfidence(request)}%.`;

    return {
      primary,
      tradeOffs,
      evidenceChain,
      alternativeReasoning: {},
    };
  }

  private rankAlternatives(request: DecisionRequest, selectedAction: DecisionOutcome["action"]): DecisionOutcome["alternatives"] {
    const alternatives: DecisionOutcome["alternatives"] = [];

    const actions: DecisionOutcome["action"][] = ["buy", "sell", "hold", "wait", "reduce", "increase"];
    for (const action of actions) {
      if (action === selectedAction) continue;

      const confidence = request.signal.confidence + (Math.random() - 0.5) * 20;
      alternatives.push({
        id: `alt-${action}`,
        label: action.toUpperCase(),
        description: `Alternative ${action.toUpperCase()} based on current market conditions`,
        confidence: Math.round(Math.max(0, Math.min(100, confidence))),
        risk: Math.round(request.risk.volatility * 10),
        tradeOff: `Lower confidence than primary decision but viable under different conditions`,
      });
    }

    return alternatives.sort((a, b) => b.confidence - a.confidence).slice(0, 3);
  }

  private assessRisk(request: DecisionRequest, action: DecisionOutcome["action"]) {
    const mitigation = action === "wait" ? "Wait for better entry" : "Use stop loss";

    return {
      level: request.risk.level,
      volatility: request.risk.volatility,
      mitigation,
    };
  }

  private buildNextAction(action: DecisionOutcome["action"], confidence: number, riskLevel: string): string {
    if (action === "wait") return "Monitor market for clearer signal";
    if (riskLevel === "extreme" || riskLevel === "high") return "Reduce position size or wait for confirmation";
    return `Proceed with ${action.toUpperCase()} with defined risk parameters`;
  }
}

export const decisionEngine = new DecisionEngine();
