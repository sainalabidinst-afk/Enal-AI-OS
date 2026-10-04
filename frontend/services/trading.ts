import { api } from "./api";
import type { TradingAnalyzeResponse } from "../types/trading";

export interface MarketRegimeLive {
  symbol: string;
  regime: string;
  confidence: number;
  volatility: string;
  trend_strength: number;
  source: string;
  timestamp?: number;
}

export interface FeedStatusResponse {
  running: boolean;
  symbol: string | null;
  timeframes: string[];
  last_update: number;
  error_count: number;
  fallback_active: boolean;
}

export interface TradingFeedOptions {
  symbol: string;
  timeframes?: string[];
  pollInterval?: number;
  onRegimeUpdate?: (regime: MarketRegimeLive) => void;
  onError?: (error: Error) => void;
  onStatusChange?: (status: FeedStatusResponse) => void;
  signal?: AbortSignal;
}

export async function analyzeMarket(
  symbol: string,
  timeframes?: string[]
): Promise<TradingAnalyzeResponse> {
  return api.post<TradingAnalyzeResponse>("/api/v1/trading/analyze", {
    symbol: symbol.toUpperCase().trim(),
    timeframes: timeframes,
  });
}

export async function startLiveFeed(options: TradingFeedOptions): Promise<void> {
  const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const response = await api.post<{ success: boolean; data: Record<string, unknown> }>(
    "/api/v1/trading/feed/start",
    {
      symbol: options.symbol.toUpperCase().trim(),
      timeframes: options.timeframes,
      poll_interval: options.pollInterval ?? 5,
    }
  );

  if (!response.data?.success) {
    throw new Error("Failed to start live feed");
  }
}

export async function stopLiveFeed(): Promise<void> {
  const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  await api.post(`${base}/api/v1/trading/feed/stop`, {});
}

export async function getFeedStatus(): Promise<FeedStatusResponse> {
  const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const response = await api.get<{ success: boolean; data: { data: FeedStatusResponse } }>(
    "/api/v1/trading/feed/status"
  );
  return response.data.data;
}

export async function getLiveRegime(symbol: string, lookback = 20): Promise<MarketRegimeLive> {
  const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const response = await api.get<{ success: boolean; data: { data: MarketRegimeLive } }>(
    `/api/v1/trading/regime/live?symbol=${encodeURIComponent(symbol.toUpperCase().trim())}&lookback=${lookback}`
  );
  return response.data.data;
}
