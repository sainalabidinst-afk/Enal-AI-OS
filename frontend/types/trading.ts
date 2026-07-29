export interface TradingEvidence {
  id: string;
  type: string;
  description: string;
  timeframe: string;
  strength: number;
  direction: string;
  source: string;
  confidence: number;
}

export interface TradingAnalysisMetadata {
  symbol: string;
  exchange: string;
  timeframes: string[];
  generated_at: string;
  data_source: string;
  analysis_version: string;
  latency_ms: number;
  raw_data_points: number;
}

export interface TradingAnalysisResult {
  symbol: string;
  bias: "bullish" | "bearish" | "neutral";
  confidence: number;
  evidence: TradingEvidence[];
  risk_level: "low" | "medium" | "high";
  counter_scenario: string;
  suggested_strategy: string;
  summary: string;
  reasoning_steps: string[];
  metadata: TradingAnalysisMetadata;
  raw: {
    category_scores: Record<string, number>;
    top_evidence: Array<{
      id: string;
      description: string;
      strength: number;
      confidence: number;
    }>;
    timeframes_analyzed: string[];
  };
}

export interface TradingAnalyzeResponse {
  success: boolean;
  data?: TradingAnalysisResult;
  error?: string;
}
