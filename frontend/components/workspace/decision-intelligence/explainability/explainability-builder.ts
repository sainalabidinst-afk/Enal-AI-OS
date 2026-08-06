import type { DecisionOutcome, EvidenceItem } from "../models/decision-models";

export interface ExplainabilityChain {
  summary: string;
  evidence: EvidenceItem[];
  reasoning: string;
  tradeOffs: {
    benefit: string;
    cost: string;
    net: string;
  };
  alternatives: {
    label: string;
    description: string;
    confidence: number;
    reason: string;
  }[];
  risk: {
    level: string;
    volatility: number;
    mitigation: string;
  };
  confidence: number;
  confidenceLevel: string;
  nextAction: string;
}

export class ExplainabilityBuilder {
  static build(outcome: DecisionOutcome): ExplainabilityChain {
    return {
      summary: outcome.reasoning.primary,
      evidence: [],
      reasoning: outcome.reasoning.evidenceChain.join("\n"),
      tradeOffs: outcome.reasoning.tradeOffs,
      alternatives: outcome.alternatives.map((alt) => ({
        label: alt.label,
        description: alt.description,
        confidence: alt.confidence,
        reason: alt.tradeOff,
      })),
      risk: outcome.riskAssessment,
      confidence: outcome.confidence,
      confidenceLevel: outcome.confidenceLevel,
      nextAction: outcome.nextAction,
    };
  }

  static formatChain(chain: ExplainabilityChain): string {
    const lines = [
      `## Decision: ${chain.confidenceLevel.toUpperCase()} CONFIDENCE`,
      ``,
      `### Summary`,
      chain.summary,
      ``,
      `### Evidence`,
      ...chain.evidence.map((e) => `- ${e.label}: ${e.value}`),
      ``,
      `### Reasoning`,
      chain.reasoning,
      ``,
      `### Trade-offs`,
      `- **Benefit**: ${chain.tradeOffs.benefit}`,
      `- **Cost**: ${chain.tradeOffs.cost}`,
      `- **Net**: ${chain.tradeOffs.net}`,
      ``,
      `### Risk`,
      `- Level: ${chain.risk.level}`,
      `- Volatility: ${chain.risk.volatility}%`,
      `- Mitigation: ${chain.risk.mitigation}`,
      ``,
      `### Confidence`,
      `${chain.confidence}% (${chain.confidenceLevel})`,
      ``,
      `### Next Action`,
      chain.nextAction,
    ];

    return lines.join("\n");
  }
}
