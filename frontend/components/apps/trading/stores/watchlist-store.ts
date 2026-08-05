import { create } from "zustand";
import type { WatchlistItem } from "../data/models/trading-models";
import { marketConnectivityService } from "../services/market-connectivity-service";

interface WatchlistState {
  items: WatchlistItem[];
  search: string;
  status: "idle" | "loading" | "success" | "error";
  error: string | null;
  setSearch: (search: string) => void;
  fetchWatchlist: () => Promise<void>;
  toggleFavorite: (symbol: string) => void;
  togglePin: (symbol: string) => void;
}

export const useWatchlistStore = create<WatchlistState>((set, get) => ({
  items: [],
  search: "",
  status: "idle",
  error: null,

  setSearch: (search) => set({ search }),

  fetchWatchlist: async () => {
    set({ status: "loading", error: null });
    try {
      const items = await marketConnectivityService.getWatchlist();
      set({ items, status: "success" });
    } catch {
      set({ status: "error", error: "Failed to load watchlist" });
    }
  },

  toggleFavorite: (symbol) =>
    set((state) => ({
      items: state.items.map((item) =>
        item.symbol === symbol ? { ...item, favorite: !item.favorite } : item
      ),
    })),

  togglePin: (symbol) =>
    set((state) => ({
      items: state.items.map((item) =>
        item.symbol === symbol ? { ...item, pinned: !item.pinned } : item
      ),
    })),
}));
