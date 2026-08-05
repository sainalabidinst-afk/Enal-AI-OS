import type { OHLCV, WatchlistItem, NewsItem, Position, Portfolio } from "../models/trading-models";

export interface MarketDataProvider {
  connect(): Promise<void>;
  disconnect(): void;
  subscribe(symbol: string): void;
  unsubscribe(symbol: string): void;
  getOHLCV(symbol: string, timeframe: string, limit?: number): Promise<OHLCV[]>;
  getQuote(symbol: string): Promise<{ price: number; change: number }>;
}

export interface MarketService {
  getOHLCV(symbol: string, timeframe: string): Promise<OHLCV[]>;
  getQuote(symbol: string): Promise<{ price: number; change: number }>;
  getWatchlist(): Promise<WatchlistItem[]>;
  getNews(): Promise<NewsItem[]>;
  getPortfolio(): Promise<Portfolio>;
  getPositions(): Promise<Position[]>;
}

export type ServiceStatus = "idle" | "loading" | "success" | "error";
