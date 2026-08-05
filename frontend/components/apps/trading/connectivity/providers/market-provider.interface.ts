import type { ConnectionStatus, ProviderHealth, Quote, Candle, NewsArticle, HistoricalLoadRequest, HistoricalLoadResult, SymbolInfo } from "./market-provider.types";

export interface MarketProvider {
  id: string;
  name: string;
  type: "websocket" | "rest" | "replay";
  status: ConnectionStatus;

  connect(): Promise<void>;
  disconnect(): void;

  subscribeQuote(symbol: string): void;
  unsubscribeQuote(symbol: string): void;

  subscribeCandles(symbol: string, timeframe: string): void;
  unsubscribeCandles(symbol: string, timeframe: string): void;

  loadHistory(request: HistoricalLoadRequest): Promise<HistoricalLoadResult>;

  getHealth(): ProviderHealth;
  getSupportedSymbols(): SymbolInfo[];
}

export interface MarketProviderRegistry {
  register(provider: MarketProvider): void;
  unregister(providerId: string): void;
  get(providerId: string): MarketProvider | undefined;
  getAll(): Map<string, MarketProvider>;
  getActive(): MarketProvider | undefined;
  setActive(providerId: string): void;
}
