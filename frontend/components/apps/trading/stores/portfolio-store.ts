import { create } from "zustand";
import type { Portfolio, Position } from "../data/models/trading-models";
import { marketConnectivityService } from "../services/market-connectivity-service";

interface PortfolioState {
  portfolio: Portfolio | null;
  positions: Position[];
  status: "idle" | "loading" | "success" | "error";
  error: string | null;
  fetchPortfolio: () => Promise<void>;
  fetchPositions: () => Promise<void>;
}

export const usePortfolioStore = create<PortfolioState>((set) => ({
  portfolio: null,
  positions: [],
  status: "idle",
  error: null,

  fetchPortfolio: async () => {
    set({ status: "loading", error: null });
    try {
      const portfolio = await marketConnectivityService.getPortfolio();
      set({ portfolio, status: "success" });
    } catch {
      set({ status: "error", error: "Failed to load portfolio" });
    }
  },

  fetchPositions: async () => {
    try {
      const positions = await marketConnectivityService.getPositions();
      set({ positions });
    } catch {
      // silently fail
    }
  },
}));
