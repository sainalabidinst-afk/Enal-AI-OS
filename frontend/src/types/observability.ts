export interface MetricsResponse {
  analysis: Record<string, unknown>;
  chat: Record<string, unknown>;
  parser: Record<string, unknown>;
  reasoning: Record<string, unknown>;
  trading: Record<string, unknown>;
  cross_pack: Record<string, unknown>;
}

export interface AlertFeedResponse {
  trading_regime: Array<{
    event_id: string;
    symbol: string;
    timeframe: string;
    regime: string;
    confidence: number;
    status: string;
    timestamp: string;
  }>;
  cross_pack_correlations: Array<{
    event_id: string;
    source_pack: string;
    target_pack: string;
    correlation_type: string;
    confidence: number;
    status: string;
    timestamp: string;
  }>;
  growth_alerts: Array<{
    event_id: string;
    alert_type: string;
    severity: string;
    subject: string;
    message: string;
    status: string;
    timestamp: string;
  }>;
}
