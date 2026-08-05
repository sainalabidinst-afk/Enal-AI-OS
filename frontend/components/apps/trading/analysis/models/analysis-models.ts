export type TrendDirection = "bullish" | "bearish" | "sideways" | "neutral";
export type MarketStructure = "trend" | "range" | "breakout" | "pullback" | "reversal";
export type SignalType = "buy" | "sell" | "wait";
export type RiskLevel = "low" | "medium" | "high" | "extreme";

export interface MarketStructureResult {
  structure: MarketStructure;
  trend: TrendDirection;
  confidence: number;
  reasoning: string;
}

export interface SignalResult {
  signal: SignalType;
  confidence: number;
  strength: number;
  reasoning: string;
}

export interface MultiTimeframeResult {
  timeframe: string;
  trend: TrendDirection;
  signal: SignalType;
  confidence: number;
}

export interface AnalysisEvidence {
  summary: string;
  items: { label: string; value: string | number | boolean }[];
  reasoning: string;
  confidence: number;
  alternative?: string;
  nextAction?: string;
}

export interface Recommendation {
  action: SignalType;
  reasoning: string;
  risk: RiskLevel;
  confidence: number;
  positionSize?: string;
  stopLoss?: number;
  takeProfit?: number;
}

export interface RiskAssessment {
  level: RiskLevel;
  volatility: number;
  confidence: number;
  reasoning: string;
}
