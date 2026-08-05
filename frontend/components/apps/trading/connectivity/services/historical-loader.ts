import type { Candle, HistoricalLoadRequest, HistoricalLoadResult } from "../providers/market-provider.types";

export class HistoricalLoader {
  async load(request: HistoricalLoadRequest): Promise<HistoricalLoadResult> {
    await new Promise((resolve) => setTimeout(resolve, 300));

    const candles: Candle[] = [];
    const now = Date.now();
    const intervalMs = this.getIntervalMs(request.timeframe);

    for (let i = request.limit - 1; i >= 0; i--) {
      const basePrice = 50000 + Math.random() * 50000;
      const volatility = 0.01;
      const change = basePrice * (Math.random() - 0.5) * volatility;
      const open = basePrice;
      const close = basePrice + change;
      const high = Math.max(open, close) + Math.abs(change) * Math.random();
      const low = Math.min(open, close) - Math.abs(change) * Math.random();
      const volume = Math.random() * 10000;

      candles.push({
        timestamp: now - i * intervalMs,
        open,
        high,
        low,
        close,
        volume,
      });
    }

    return {
      symbol: request.symbol,
      timeframe: request.timeframe,
      candles,
      loadedAt: Date.now(),
    };
  }

  private getIntervalMs(timeframe: string): number {
    const map: Record<string, number> = {
      "1m": 60000,
      "5m": 300000,
      "15m": 900000,
      "1h": 3600000,
      "4h": 14400000,
      "1d": 86400000,
      "1w": 604800000,
    };
    return map[timeframe] ?? 3600000;
  }
}

export const historicalLoader = new HistoricalLoader();
