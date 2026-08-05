import { create } from "zustand";

export type Timeframe = "1m" | "5m" | "15m" | "1h" | "4h" | "1d" | "1w";

interface ChartState {
  timeframe: Timeframe;
  indicators: string[];
  drawings: unknown[];
  crosshair: { x: number; y: number } | null;
  setTimeframe: (timeframe: Timeframe) => void;
  toggleIndicator: (indicator: string) => void;
  clearDrawings: () => void;
  setCrosshair: (pos: { x: number; y: number } | null) => void;
}

export const useChartStore = create<ChartState>((set) => ({
  timeframe: "1h",
  indicators: [],
  drawings: [],
  crosshair: null,

  setTimeframe: (timeframe) => set({ timeframe }),
  toggleIndicator: (indicator) =>
    set((state) => ({
      indicators: state.indicators.includes(indicator)
        ? state.indicators.filter((i) => i !== indicator)
        : [...state.indicators, indicator],
    })),
  clearDrawings: () => set({ drawings: [] }),
  setCrosshair: (crosshair) => set({ crosshair }),
}));
