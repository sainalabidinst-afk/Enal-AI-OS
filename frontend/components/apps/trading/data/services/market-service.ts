import type { MarketService, ServiceStatus } from "../providers/market-data-provider";
import { generateOHLCV, generateWatchlist, generateNews, generatePositions, generatePortfolio, generateFakeQuote } from "../mock/mock-data-engine";

class MockMarketService implements MarketService {
  private cache = new Map<string, unknown>();

  async getOHLCV(symbol: string, timeframe: string) {
    const key = `ohlcv-${symbol}-${timeframe}`;
    if (!this.cache.has(key)) {
      this.cache.set(key, generateOHLCV(symbol, timeframe));
    }
    return this.cache.get(key) as ReturnType<typeof generateOHLCV>;
  }

  async getQuote(symbol: string) {
    return generateFakeQuote(symbol);
  }

  async getWatchlist() {
    return generateWatchlist();
  }

  async getNews() {
    return generateNews();
  }

  async getPortfolio() {
    return generatePortfolio();
  }

  async getPositions() {
    return generatePositions();
  }
}

export const marketService = new MockMarketService();
