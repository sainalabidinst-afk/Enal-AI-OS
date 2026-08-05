import { useEffect } from "react";
import { useMarketStore } from "../stores/market-store";
import { useWatchlistStore } from "../stores/watchlist-store";
import { usePortfolioStore } from "../stores/portfolio-store";
import { useNewsStore } from "../stores/news-store";
import { eventBus } from "../events/event-bus";
import { generateFakeQuote } from "../mock/mock-data-engine";

export function useMarketData() {
  const symbol = useMarketStore((s) => s.symbol);
  const setSymbol = useMarketStore((s) => s.setSymbol);
  const fetchQuote = useMarketStore((s) => s.fetchQuote);
  const watchlistItems = useWatchlistStore((s) => s.items);

  useEffect(() => {
    if (!symbol) return;

    fetchQuote(symbol);

    const interval = setInterval(() => {
      const quote = generateFakeQuote(symbol);
      eventBus.publish({
        type: "market:updated",
        payload: { symbol, quote },
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [symbol, fetchQuote]);

  return {
    symbol,
    setSymbol,
    watchlistItems,
  };
}

export function useTradingRealtime() {
  useEffect(() => {
    const intervals: ReturnType<typeof setInterval>[] = [];

    const refreshWatchlist = setInterval(() => {
      eventBus.publish({ type: "watchlist:updated" });
    }, 3000);

    const refreshNews = setInterval(() => {
      eventBus.publish({ type: "news:updated" });
    }, 10000);

    const refreshPortfolio = setInterval(() => {
      eventBus.publish({ type: "portfolio:updated" });
    }, 5000);

    intervals.push(refreshWatchlist, refreshNews, refreshPortfolio);

    return () => intervals.forEach(clearInterval);
  }, []);
}
