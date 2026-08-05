import { create } from "zustand";
import type { OHLCV } from "../models/trading-models";
import { marketService } from "../services/market-service";

interface MarketState {
  symbol: string | null;
  timeframe: string;
  ohlcv: OHLCV[];
  status: "idle" | "loading" | "success" | "error";
  error: string | null;
  setSymbol: (symbol: string) => void;
  setTimeframe: (timeframe: string) => void;
  fetchOHLCV: () => Promise<void>;
  fetchQuote: (symbol: string) => Promise<{ price: number; change: number }>;
}

export const useMarketStore = create<MarketState>((set, get) => ({
  symbol: "BTCUSDT",
  timeframe: "1h",
  ohlcv: [],
  status: "idle",
  error: null,

  setSymbol: (symbol) => set({ symbol, status: "idle", error: null }),
  setTimeframe: (timeframe) => set({ timeframe, status: "idle", error: null }),

  fetchOHLCV: async () => {
    const { symbol, timeframe } = get();
    if (!symbol) return;

    set({ status: "loading", error: null });
    try {
      const data = await marketService.getOHLCV(symbol, timeframe);
      set({ ohlcv: data, status: "success" });
    } catch (error) {
      set({ status: "error", error: "Failed to fetch chart data" });
    }
  },

  fetchQuote: async (symbol) => {
    try {
      return await marketService.getQuote(symbol);
    } catch {
      return { price: 0, change: 0 };
    }
  },
}));
