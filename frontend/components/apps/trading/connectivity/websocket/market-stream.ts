import type { Quote, Candle } from "../providers/market-provider.types";

type QuoteListener = (quote: Quote) => void;
type CandleListener = (candle: Candle) => void;

class MarketStreamImpl {
  private quoteListeners = new Set<QuoteListener>();
  private candleListeners = new Map<string, Set<CandleListener>>();

  subscribeQuote(listener: QuoteListener) {
    this.quoteListeners.add(listener);
    return () => this.quoteListeners.delete(listener);
  }

  publishQuote(quote: Quote) {
    this.quoteListeners.forEach((listener) => listener(quote));
  }

  subscribeCandles(key: string, listener: CandleListener) {
    if (!this.candleListeners.has(key)) {
      this.candleListeners.set(key, new Set());
    }
    this.candleListeners.get(key)!.add(listener);
    return () => this.candleListeners.get(key)?.delete(listener);
  }

  publishCandle(key: string, candle: Candle) {
    const listeners = this.candleListeners.get(key);
    if (listeners) {
      listeners.forEach((listener) => listener(candle));
    }
  }
}

export const marketStream = new MarketStreamImpl();
