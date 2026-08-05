import { create } from "zustand";

interface TradingUIState {
  activeTab: string;
  sidebarCollapsed: boolean;
  bottomPanelTab: string;
  isLoading: boolean;
  error: string | null;
  setActiveTab: (tab: string) => void;
  toggleSidebar: () => void;
  setBottomPanelTab: (tab: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useTradingUIStore = create<TradingUIState>((set) => ({
  activeTab: "dashboard",
  sidebarCollapsed: false,
  bottomPanelTab: "orders",
  isLoading: false,
  error: null,

  setActiveTab: (activeTab) => set({ activeTab }),
  toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
  setBottomPanelTab: (bottomPanelTab) => set({ bottomPanelTab }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
}));
