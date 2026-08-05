import type { MarketProvider } from "../providers/market-provider.interface";
import type { ConnectionStatus, ProviderHealth, Quote, Candle, HistoricalLoadRequest, HistoricalLoadResult, SymbolInfo } from "../providers/market-provider.types";
import { marketStream } from "../websocket/market-stream";
import { historicalLoader } from "../services/historical-loader";
import { symbolRegistry } from "../registry/symbol-registry";
import { connectionRecovery } from "../websocket/connection-recovery";
import { diagnosticsMonitor } from "../diagnostics/diagnostics-monitor";

export class ReplayMarketProvider implements MarketProvider {
  id = "replay";
  name = "Replay Provider";
  type: MarketProvider["type"] = "replay";
  status: ConnectionStatus = "idle";

  private candles: Candle[] = [];
  private currentIndex = 0;
  private interval: ReturnType<typeof setInterval> | null = null;

  async connect() {
    this.status = "connecting";
    await new Promise((resolve) => void setTimeout(resolve, 300));
    this.status = "connected";
    this.startReplay();
  }

  disconnect() {
    if (this.interval) {
      clearInterval(this.interval);
      this.interval = null;
    }
    this.status = "disconnected";
    connectionRecovery.clear();
  }

  subscribeQuote(_symbol: string) {
    connectionRecovery.saveState(_symbol, true);
  }

  unsubscribeQuote(symbol: string) {
    connectionRecovery.saveState(symbol, false);
  }

  subscribeCandles(symbol: string, timeframe: string) {
    connectionRecovery.saveState(symbol, true, timeframe);
  }

  unsubscribeCandles(symbol: string, timeframe: string) {
    connectionRecovery.saveState(symbol, false, timeframe);
  }

  async loadHistory(request: HistoricalLoadRequest): Promise<HistoricalLoadResult> {
    return historicalLoader.load(request);
  }

  getHealth(): ProviderHealth {
    return {
      providerId: this.id,
      status: this.status,
      latencyMs: 0,
      packetsReceived: 0,
      reconnectCount: 0,
      lastConnectedAt: this.status === "connected" ? Date.now() : null,
      lastError: null,
    };
  }

  getSupportedSymbols(): SymbolInfo[] {
    return symbolRegistry.getAll();
  }

  private startReplay() {
    this.interval = setInterval(() => {
      const quote: Quote = {
        symbol: "BTCUSDT",
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
  }
}
