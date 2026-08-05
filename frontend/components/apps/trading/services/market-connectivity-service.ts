import type { OHLCV, WatchlistItem, NewsItem, Position, Portfolio } from "../data/models/trading-models";
import { providerManager } from "../connectivity/manager/provider-manager";
import { marketStream } from "../connectivity/websocket/market-stream";
import { newsProvider } from "../connectivity/providers/news-provider";

export class MarketConnectivityService {
  async getOHLCV(symbol: string, timeframe: string): Promise<OHLCV[]> {
    const result = await providerManager.loadHistory({
      symbol,
      timeframe,
      limit: 100,
    });
    return result.candles;
  }

  async getQuote(symbol: string): Promise<{ price: number; change: number }> {
    return new Promise((resolve) => {
      const unsubscribe = marketStream.subscribeQuote((quote) => {
        if (quote.symbol === symbol) {
          unsubscribe();
          resolve({ price: quote.last, change: quote.change });
        }
      });
    });
  }

  async getWatchlist(): Promise<WatchlistItem[]> {
    const symbols = providerManager.getSupportedSymbols();
    return symbols.slice(0, 10).map((s) => ({
      symbol: s.symbol,
      name: s.name,
      price: 100 + Math.random() * 50,
      change: (Math.random() - 0.5) * 5,
      changePercent: (Math.random() - 0.5) * 5,
      volume: Math.random() * 1000000,
      favorite: false,
      pinned: false,
    }));
  }

  async getNews(): Promise<NewsItem[]> {
    return new Promise((resolve) => {
      const unsubscribe = newsProvider.subscribe((articles) => {
        unsubscribe();
        resolve(
          articles.map((a) => ({
            id: a.id,
            title: a.title,
            summary: a.summary,
            source: a.source,
            publishedAt: a.publishedAt,
            categories: a.categories,
            sentiment: a.sentiment,
          }))
        );
      });
    });
  }

  async getPortfolio(): Promise<Portfolio> {
    return {
      totalValue: 124593,
      cash: 50000,
      positionsValue: 74593,
      dayChange: 2341.5,
      dayChangePercent: 1.92,
      openPositions: 8,
      winRate: 67.5,
    };
  }

  async getPositions(): Promise<Position[]> {
    return [];
  }

  subscribeRealtime(symbol: string) {
    providerManager.subscribeQuote(symbol);
    providerManager.subscribeCandles(symbol, "1h");
  }
}

export const marketConnectivityService = new MarketConnectivityService();
