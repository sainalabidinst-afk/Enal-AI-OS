import type { ConnectionStatus, HistoricalLoadRequest, HistoricalLoadResult, ProviderHealth, Quote, SymbolInfo } from "../providers/market-provider.types";
import { providerRegistry } from "../registry/provider-registry";

export class ProviderManager {
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelayMs = 1000;
  private healthCheckInterval: ReturnType<typeof setInterval> | null = null;

  async connect(providerId?: string) {
    if (providerId) {
      providerRegistry.setActive(providerId);
    }

    const provider = providerRegistry.getActive();
    if (!provider) {
      throw new Error("No active provider selected");
    }

    try {
      await provider.connect();
      this.reconnectAttempts = 0;
      this.startHealthCheck();
    } catch (error) {
      this.handleReconnect();
      throw error;
    }
  }

  disconnect() {
    this.stopHealthCheck();
    const provider = providerRegistry.getActive();
    if (provider) {
      provider.disconnect();
    }
  }

  async reconnect() {
    this.disconnect();
    await this.connect();
  }

  switchProvider(providerId: string) {
    this.disconnect();
    providerRegistry.setActive(providerId);
    this.connect(providerId);
  }

  subscribeQuote(symbol: string) {
    const provider = providerRegistry.getActive();
    if (provider) {
      provider.subscribeQuote(symbol);
    }
  }

  unsubscribeQuote(symbol: string) {
    const provider = providerRegistry.getActive();
    if (provider) {
      provider.unsubscribeQuote(symbol);
    }
  }

  subscribeCandles(symbol: string, timeframe: string) {
    const provider = providerRegistry.getActive();
    if (provider) {
      provider.subscribeCandles(symbol, timeframe);
    }
  }

  unsubscribeCandles(symbol: string, timeframe: string) {
    const provider = providerRegistry.getActive();
    if (provider) {
      provider.unsubscribeCandles(symbol, timeframe);
    }
  }

  async loadHistory(request: HistoricalLoadRequest): Promise<HistoricalLoadResult> {
    const provider = providerRegistry.getActive();
    if (!provider) {
      throw new Error("No active provider");
    }
    return provider.loadHistory(request);
  }

  getHealth(): ProviderHealth | undefined {
    return providerRegistry.getActive()?.getHealth();
  }

  getSupportedSymbols(): SymbolInfo[] {
    return providerRegistry.getActive()?.getSupportedSymbols() ?? [];
  }

  getStatus(): ConnectionStatus {
    return providerRegistry.getActive()?.status ?? "idle";
  }

  private startHealthCheck() {
    this.healthCheckInterval = setInterval(() => {
      const health = this.getHealth();
      if (health?.status === "error" || health?.status === "disconnected") {
        this.handleReconnect();
      }
    }, 5000);
  }

  private stopHealthCheck() {
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
      this.healthCheckInterval = null;
    }
  }

  private async handleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error("Max reconnect attempts reached");
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelayMs * this.reconnectAttempts;

    setTimeout(async () => {
      try {
        await this.reconnect();
      } catch (error) {
        console.error("Reconnect failed:", error);
      }
    }, delay);
  }
}

export const providerManager = new ProviderManager();
