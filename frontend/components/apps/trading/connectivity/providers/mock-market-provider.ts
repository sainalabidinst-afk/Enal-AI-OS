import type { MarketProvider } from "./market-provider.interface";
import type { ConnectionStatus, ProviderHealth, Quote, Candle, NewsArticle, HistoricalLoadRequest, HistoricalLoadResult, SymbolInfo } from "./market-provider.types";
import { marketStream } from "../websocket/market-stream";
import { newsProvider } from "../providers/news-provider";
import { historicalLoader } from "../services/historical-loader";
import { symbolRegistry } from "../registry/symbol-registry";
import { connectionRecovery } from "../websocket/connection-recovery";
import { diagnosticsMonitor } from "../diagnostics/diagnostics-monitor";

export class MockMarketProvider implements MarketProvider {
  id = "mock";
  name = "Mock Provider";
  type: MarketProvider["type"] = "websocket";
  status: ConnectionStatus = "idle";

  private intervals: ReturnType<typeof setInterval>[] = [];

  async connect() {
    this.status = "connecting";

    await new Promise((resolve) => void setTimeout(resolve, 500));

    this.status = "connected";

    this.startMockStreams();
    this.publishHealth();
  }

  disconnect() {
    this.intervals.forEach(clearInterval);
    this.intervals = [];
    this.status = "disconnected";
    connectionRecovery.clear();
  }

  subscribeQuote(symbol: string) {
    connectionRecovery.saveState(symbol, true);
    const interval = setInterval(() => {
      const quote: Quote = {
        symbol,
        bid: 100 + Math.random() * 10,
        ask: 100 + Math.random() * 10 + 0.5,
        last: 100 + Math.random() * 10,
        change: (Math.random() - 0.5) * 2,
        changePercent: (Math.random() - 0.5) * 2,
        volume: Math.random() * 1000,
        timestamp: Date.now(),
      };
      diagnosticsMonitor.recordPacket();
      marketStream.publishQuote(quote);
    }, 1000);

    this.intervals.push(interval);
  }

  unsubscribeQuote(symbol: string) {
    connectionRecovery.saveState(symbol, false);
  }

  subscribeCandles(symbol: string, timeframe: string) {
    connectionRecovery.saveState(symbol, true, timeframe);
    const interval = setInterval(() => {
      const candle: Candle = {
        timestamp: Date.now(),
        open: 100 + Math.random() * 10,
        high: 100 + Math.random() * 10 + 1,
        low: 100 + Math.random() * 10 - 1,
        close: 100 + Math.random() * 10,
        volume: Math.random() * 1000,
      };
      diagnosticsMonitor.recordPacket();
      marketStream.publishCandle(`${symbol}:${timeframe}`, candle);
    }, 2000);

    this.intervals.push(interval);
  }

  unsubscribeCandles(symbol: string, timeframe: string) {
    const key = `${symbol}:${timeframe}`;
    connectionRecovery.saveState(symbol, false, timeframe);
  }

  async loadHistory(request: HistoricalLoadRequest): Promise<HistoricalLoadResult> {
    return historicalLoader.load(request);
  }

  getHealth(): ProviderHealth {
    return {
      providerId: this.id,
      status: this.status,
      latencyMs: Math.random() * 50,
      packetsReceived: diagnosticsMonitor.getPacketCount(),
      reconnectCount: 0,
      lastConnectedAt: this.status === "connected" ? Date.now() : null,
      lastError: null,
    };
  }

  getSupportedSymbols(): SymbolInfo[] {
    return symbolRegistry.getAll();
  }

  private startMockStreams() {
    const news: NewsArticle[] = [
      {
        id: "news-1",
        title: "Fed signals rate pause in upcoming meeting",
        summary: "Market analysts expect stable rates.",
        source: "Reuters",
        publishedAt: Date.now(),
        categories: ["markets"],
        sentiment: "neutral",
      },
    ];
    newsProvider.publish(news);
  }

  private publishHealth() {
    const health = this.getHealth();
    diagnosticsMonitor.publish(health);
  }
}
