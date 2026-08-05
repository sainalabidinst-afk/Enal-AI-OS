"use client";

import { create } from "zustand";

export type TradingTab = "dashboard" | "watchlist" | "portfolio" | "scanner" | "alerts" | "news" | "research" | "settings";

export interface TradingState {
  activeTab: TradingTab;
  symbol: string | null;
  timeframe: string;
  setActiveTab: (tab: TradingTab) => void;
  setSymbol: (symbol: string) => void;
  setTimeframe: (timeframe: string) => void;
}

export const useTradingStore = create<TradingState>((set) => ({
  activeTab: "dashboard",
  symbol: null,
  timeframe: "1h",
  setActiveTab: (activeTab) => set({ activeTab }),
  setSymbol: (symbol) => set({ symbol }),
  setTimeframe: (timeframe) => set({ timeframe }),
}));
