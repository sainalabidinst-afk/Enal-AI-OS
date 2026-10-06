'use client';

import { create } from 'zustand';

interface TradingState {
  symbol: string;
  timeframe: string;
  regime: string | null;
  feedStatus: 'running' | 'stopped' | 'error';
  setSymbol: (symbol: string) => void;
  setTimeframe: (timeframe: string) => void;
  setRegime: (regime: string | null) => void;
  setFeedStatus: (feedStatus: 'running' | 'stopped' | 'error') => void;
}

export const useTradingStore = create<TradingState>((set) => ({
  symbol: 'BTCUSDT',
  timeframe: '1h',
  regime: null,
  feedStatus: 'stopped',
  setSymbol: (symbol) => set({ symbol }),
  setTimeframe: (timeframe) => set({ timeframe }),
  setRegime: (regime) => set({ regime }),
  setFeedStatus: (feedStatus) => set({ feedStatus }),
}));
