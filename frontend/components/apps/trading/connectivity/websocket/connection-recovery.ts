import type { ConnectionStatus, Quote, Candle, SymbolInfo } from "../providers/market-provider.types";
import { symbolRegistry } from "../registry/symbol-registry";

export class ConnectionRecovery {
  private state: Map<string, { subscribed: boolean; timeframe?: string }> = new Map();

  saveState(symbol: string, subscribed: boolean, timeframe?: string) {
    this.state.set(symbol, { subscribed, timeframe });
  }

  getState(symbol: string) {
    return this.state.get(symbol);
  }

  async recover(provider: {
    subscribeQuote: (s: string) => void;
    subscribeCandles: (s: string, tf: string) => void;
  }) {
    const symbols = symbolRegistry.getAll();

    for (const symbol of symbols) {
      const state = this.state.get(symbol.symbol);
      if (state?.subscribed) {
        provider.subscribeQuote(symbol.symbol);
        if (state.timeframe) {
          provider.subscribeCandles(symbol.symbol, state.timeframe);
        }
      }
    }
  }

  clear() {
    this.state.clear();
  }
}

export const connectionRecovery = new ConnectionRecovery();
