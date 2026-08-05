import { create } from "zustand";
import type { NewsItem } from "../data/models/trading-models";
import { marketConnectivityService } from "../services/market-connectivity-service";

type NewsFilter = "all" | "bullish" | "bearish" | "neutral";

interface NewsState {
  items: NewsItem[];
  filter: NewsFilter;
  status: "idle" | "loading" | "success" | "error";
  error: string | null;
  setFilter: (filter: NewsFilter) => void;
  fetchNews: () => Promise<void>;
}

export const useNewsStore = create<NewsState>((set) => ({
  items: [],
  filter: "all",
  status: "idle",
  error: null,

  setFilter: (filter) => set({ filter }),

  fetchNews: async () => {
    set({ status: "loading", error: null });
    try {
      const items = await marketConnectivityService.getNews();
      set({ items, status: "success" });
    } catch {
      set({ status: "error", error: "Failed to load news" });
    }
  },
}));
