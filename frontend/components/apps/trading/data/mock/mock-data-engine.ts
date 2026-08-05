import type { OHLCV, WatchlistItem, NewsItem, Position, Portfolio } from "../models/trading-models";

const SYMBOLS = [
  { symbol: "BTCUSDT", name: "Bitcoin", basePrice: 104245 },
  { symbol: "ETHUSDT", name: "Ethereum", basePrice: 2512 },
  { symbol: "SOLUSDT", name: "Solana", basePrice: 178 },
  { symbol: "ADAUSDT", name: "Cardano", basePrice: 0.68 },
  { symbol: "XRPUSDT", name: "Ripple", basePrice: 2.14 },
];

const NEWS_SOURCES = ["Reuters", "Bloomberg", "CNBC", "CoinDesk", "The Block", "Cointelegraph"];
const NEWS_TITLES = [
  "Fed signals rate pause in upcoming meeting",
  "BTC ETF inflows hit record weekly high",
  "Tech earnings beat analyst estimates",
  "Ethereum upgrade successfully activated",
  "Institutional demand for crypto assets rises",
  "SEC approves new spot trading product",
  "Macro uncertainty drives safe-haven flows",
  "Derivatives positioning shifts ahead of expiry",
];

function random(min: number, max: number) {
  return Math.random() * (max - min) + min;
}

function generateOHLCV(symbol: string, timeframe: string, limit = 100): OHLCV[] {
  const item = SYMBOLS.find((s) => s.symbol === symbol) ?? SYMBOLS[0];
  const now = Date.now();
  const candles: OHLCV[] = [];
  let price = item.basePrice;

  for (let i = limit - 1; i >= 0; i--) {
    const volatility = timeframe === "1m" ? 0.001 : timeframe === "1h" ? 0.005 : 0.02;
    const change = price * random(-volatility, volatility);
    const open = price;
    const close = price + change;
    const high = Math.max(open, close) + Math.abs(change) * random(0, 1);
    const low = Math.min(open, close) - Math.abs(change) * random(0, 1);
    const volume = random(100, 10000);

    candles.push({
      timestamp: now - i * (timeframe === "1m" ? 60000 : timeframe === "1h" ? 3600000 : 86400000),
      open,
      high,
      low,
      close,
      volume,
    });

    price = close;
  }

  return candles;
}

export function generateWatchlist(): WatchlistItem[] {
  return SYMBOLS.map((item) => {
    const change = random(-5, 5);
    return {
      symbol: item.symbol,
      name: item.name,
      price: item.basePrice * (1 + change / 100),
      change,
      changePercent: change,
      volume: random(1000000, 500000000),
      favorite: Math.random() > 0.7,
      pinned: Math.random() > 0.8,
    };
  });
}

export function generateNews(): NewsItem[] {
  return NEWS_TITLES.map((title, idx) => ({
    id: `news-${idx}`,
    title,
    summary: `Latest update regarding ${title.toLowerCase()}. Market analysts are closely watching developments.`,
    source: NEWS_SOURCES[idx % NEWS_SOURCES.length],
    publishedAt: Date.now() - idx * 3600000 * random(1, 6),
    categories: ["markets", "crypto", "macro"].filter(() => Math.random() > 0.5),
    sentiment: ["bullish", "bearish", "neutral"][Math.floor(Math.random() * 3)] as NewsItem["sentiment"],
  }));
}

export function generatePositions(): Position[] {
  return SYMBOLS.slice(0, 4).map((item, idx) => {
    const entryPrice = item.basePrice * random(0.9, 1.1);
    const currentPrice = item.basePrice * random(0.95, 1.05);
    const side = Math.random() > 0.3 ? "long" : "short";
    const pnl = side === "long" ? currentPrice - entryPrice : entryPrice - currentPrice;
    return {
      id: `pos-${idx}`,
      symbol: item.symbol,
      side,
      size: random(0.1, 10),
      entryPrice,
      currentPrice,
      pnl,
      pnlPercent: (pnl / entryPrice) * 100,
      openedAt: Date.now() - idx * 86400000 * random(1, 30),
    };
  });
}

export function generatePortfolio(): Portfolio {
  const positionsValue = generatePositions().reduce((sum, pos) => sum + pos.currentPrice * pos.size, 0);
  const cash = random(10000, 50000);
  return {
    totalValue: positionsValue + cash,
    cash,
    positionsValue,
    dayChange: random(-2000, 2000),
    dayChangePercent: random(-3, 3),
    openPositions: generatePositions().length,
    winRate: random(55, 75),
  };
}

export function generateFakeQuote(symbol: string) {
  const item = SYMBOLS.find((s) => s.symbol === symbol) ?? SYMBOLS[0];
  const change = random(-2, 2);
  return {
    price: item.basePrice * (1 + change / 100),
    change,
  };
}
