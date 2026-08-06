export type DecisionAction = "buy" | "sell" | "hold" | "wait" | "reduce" | "increase";
export type DecisionConfidence = "very_low" | "low" | "medium" | "high" | "very_high";

export interface EvidenceItem {
  label: string;
  value: string | number | boolean;
  source?: string;
  weight?: number;
}

export interface AlternativeOption {
  id: string;
  label: string;
  description: string;
  confidence: number;
  risk: number;
  tradeOff: string;
}

export interface DecisionRequest {
  capabilityId: string;
  context: Record<string, unknown>;
  evidence: EvidenceItem[];
  signal: {
    action: string;
    confidence: number;
    strength: number;
  };
  risk: {
    level: string;
    volatility: number;
    confidence: number;
  };
  alternatives?: AlternativeOption[];
  constraints?: Record<string, unknown>;
}

export interface TradeOffAnalysis {
  benefit: string;
  cost: string;
  net: string;
}

export interface DecisionReasoning {
  primary: string;
  tradeOffs: TradeOffAnalysis;
  evidenceChain: string[];
  alternativeReasoning: Record<string, string>;
}

export interface DecisionOutcome {
  decisionId: string;
  action: DecisionAction;
  confidence: number;
  confidenceLevel: DecisionConfidence;
  reasoning: DecisionReasoning;
  alternatives: AlternativeOption[];
  riskAssessment: {
    level: string;
    volatility: number;
    mitigation: string;
  };
  nextAction: string;
  timestamp: number;
  capabilityId: string;
}

export interface DecisionHistoryEntry {
  decisionId: string;
  capabilityId: string;
  action: DecisionAction;
  confidence: number;
  evidence: EvidenceItem[];
  outcome?: {
    success: boolean;
    actualResult?: unknown;
    feedback?: string;
  };
  timestamp: number;
  resolvedAt?: number;
}

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
