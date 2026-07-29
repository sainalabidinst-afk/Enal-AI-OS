import { api } from "./api";
import type { TradingAnalyzeResponse } from "../types/trading";

export async function analyzeMarket(
  symbol: string,
  timeframes?: string[]
): Promise<TradingAnalyzeResponse> {
  return api.post<TradingAnalyzeResponse>("/api/v1/trading/analyze", {
    symbol: symbol.toUpperCase().trim(),
    timeframes: timeframes,
  });
}
