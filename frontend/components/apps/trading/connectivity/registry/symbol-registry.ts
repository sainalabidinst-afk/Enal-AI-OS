import type { SymbolInfo } from "../providers/market-provider.types";

const BUILTIN_SYMBOLS: SymbolInfo[] = [
  { symbol: "BTCUSDT", name: "Bitcoin", exchange: "Binance", type: "crypto", baseCurrency: "BTC", quoteCurrency: "USDT", active: true },
  { symbol: "ETHUSDT", name: "Ethereum", exchange: "Binance", type: "crypto", baseCurrency: "ETH", quoteCurrency: "USDT", active: true },
  { symbol: "SOLUSDT", name: "Solana", exchange: "Binance", type: "crypto", baseCurrency: "SOL", quoteCurrency: "USDT", active: true },
  { symbol: "AAPL", name: "Apple Inc.", exchange: "NASDAQ", type: "stock", baseCurrency: "AAPL", quoteCurrency: "USD", active: true },
  { symbol: "MSFT", name: "Microsoft Corp.", exchange: "NASDAQ", type: "stock", baseCurrency: "MSFT", quoteCurrency: "USD", active: true },
  { symbol: "BBCA", name: "Bank Central Asia", exchange: "IDX", type: "stock", baseCurrency: "BBCA", quoteCurrency: "IDR", active: true },
  { symbol: "TLKM", name: "Telkomsel", exchange: "IDX", type: "stock", baseCurrency: "TLKM", quoteCurrency: "IDR", active: true },
];

class SymbolRegistryImpl {
  private symbols = new Map<string, SymbolInfo>();

  constructor() {
    BUILTIN_SYMBOLS.forEach((s) => this.symbols.set(s.symbol, s));
  }

  register(symbol: SymbolInfo) {
    this.symbols.set(symbol.symbol, symbol);
  }

  unregister(symbol: string) {
    this.symbols.delete(symbol);
  }

  get(symbol: string) {
    return this.symbols.get(symbol);
  }

  getAll() {
    return Array.from(this.symbols.values());
  }

  search(query: string) {
    const q = query.toLowerCase();
    return this.getAll().filter(
      (s) =>
        s.symbol.toLowerCase().includes(q) ||
        s.name.toLowerCase().includes(q) ||
        s.exchange.toLowerCase().includes(q)
    );
  }
}

export const symbolRegistry = new SymbolRegistryImpl();
