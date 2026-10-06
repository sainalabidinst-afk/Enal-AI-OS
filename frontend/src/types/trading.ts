export interface MarketAnalysisResponse {
  success: boolean;
  data?: {
    symbol: string;
    exchange: string;
    confidence: number;
    timeframes: string[];
    regimes: Record<string, { regime: string; confidence: number }>;
    summary: string;
    latency_ms: number;
  };
  error?: string;
}

export interface TradingRegimeResponse {
  success: boolean;
  data?: {
    symbol: string;
    regime: string;
    confidence: number;
    timestamp: string;
  };
}

export interface FeedStatusResponse {
  success: boolean;
  data?: {
    running: boolean;
    symbol: string;
    timeframes: string[];
    last_update: number;
    error_count: number;
  };
}
