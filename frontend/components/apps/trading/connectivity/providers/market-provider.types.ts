export type ConnectionStatus = "idle" | "connecting" | "connected" | "disconnected" | "reconnecting" | "error";

export interface ProviderHealth {
  providerId: string;
  status: ConnectionStatus;
  latencyMs: number | null;
  packetsReceived: number;
  reconnectCount: number;
  lastConnectedAt: number | null;
  lastError: string | null;
}

export interface SymbolInfo {
  symbol: string;
  name: string;
  exchange: string;
  type: "crypto" | "stock" | "forex" | "commodity";
  baseCurrency: string;
  quoteCurrency: string;
  active: boolean;
}

export interface Quote {
  symbol: string;
  bid: number;
  ask: number;
  last: number;
  change: number;
  changePercent: number;
  volume: number;
  timestamp: number;
}

export interface Candle {
  timestamp: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface NewsArticle {
  id: string;
  title: string;
  summary: string;
  source: string;
  publishedAt: number;
  categories: string[];
  sentiment: "bullish" | "bearish" | "neutral";
}

export interface HistoricalLoadRequest {
  symbol: string;
  timeframe: string;
  limit: number;
}

export interface HistoricalLoadResult {
  symbol: string;
  timeframe: string;
  candles: Candle[];
  loadedAt: number;
}
