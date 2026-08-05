import type { ToolDefinition } from "../tools/tool-types";
import { useMarketStore } from "../../../apps/trading/stores/market-store";
import { useWatchlistStore } from "../../../apps/trading/stores/watchlist-store";

export function createTradingTools(): ToolDefinition[] {
  return [
    {
      id: "trading-load-symbol",
      name: "Load Symbol",
      description: "Load a trading symbol into the chart",
      parameters: { symbol: "string" },
      execute: async (params) => {
        const symbol = params.symbol as string;
        useMarketStore.getState().setSymbol(symbol);
        return { success: true, data: { symbol } };
      },
    },
    {
      id: "trading-load-watchlist",
      name: "Load Watchlist",
      description: "Load the current watchlist",
      parameters: {},
      execute: async () => {
        await useWatchlistStore.getState().fetchWatchlist();
        return { success: true, data: useWatchlistStore.getState().items };
      },
    },
  ];
}

