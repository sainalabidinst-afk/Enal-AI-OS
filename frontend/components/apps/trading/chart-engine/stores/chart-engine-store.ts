import { create } from "zustand";
import type { Candle, Timeframe, ViewportState, VisibleRange, IndicatorPlugin, DrawingObject, OverlayObject, ReplayState } from "../models/chart-models";

interface ChartEngineState {
  candles: Candle[];
  timeframe: Timeframe;
  viewport: ViewportState;
  visibleRange: VisibleRange;
  indicators: IndicatorPlugin[];
  drawings: DrawingObject[];
  overlays: OverlayObject[];
  replay: ReplayState;
  activeDrawingTool: string;
  crosshair: { x: number; y: number; timestamp: number; price: number } | null;
  setCandles: (candles: Candle[]) => void;
  setTimeframe: (timeframe: Timeframe) => void;
  setViewport: (viewport: Partial<ViewportState>) => void;
  setVisibleRange: (range: Partial<VisibleRange>) => void;
  addIndicator: (indicator: IndicatorPlugin) => void;
  removeIndicator: (id: string) => void;
  addDrawing: (drawing: DrawingObject) => void;
  setActiveDrawingTool: (tool: string) => void;
  addOverlay: (overlay: OverlayObject) => void;
  setReplayState: (state: Partial<ReplayState>) => void;
  setCrosshair: (crosshair: { x: number; y: number; timestamp: number; price: number } | null) => void;
  resetView: () => void;
}

export const useChartEngineStore = create<ChartEngineState>((set, get) => ({
  candles: [],
  timeframe: "1h",
  viewport: { offset: 0, scale: 1, crosshair: null },
  visibleRange: { startIndex: 0, endIndex: 100 },
  indicators: [],
  drawings: [],
  overlays: [],
  replay: { isPlaying: false, speed: 1, currentIndex: 0, totalCandles: 0 },
  activeDrawingTool: "none",
  crosshair: null,

  setCandles: (candles) => set({ candles }),
  setTimeframe: (timeframe) => set({ timeframe, viewport: { offset: 0, scale: 1, crosshair: null } }),
  setViewport: (viewport) => set((state) => ({ viewport: { ...state.viewport, ...viewport } })),
  setVisibleRange: (visibleRange) => set((state) => ({ visibleRange: { ...state.visibleRange, ...visibleRange } })),
  addIndicator: (indicator) => set((state) => ({ indicators: [...state.indicators, indicator] })),
  removeIndicator: (id) => set((state) => ({ indicators: state.indicators.filter((i) => i.id !== id) })),
  addDrawing: (drawing) => set((state) => ({ drawings: [...state.drawings, drawing] })),
  setActiveDrawingTool: (activeDrawingTool) => set({ activeDrawingTool }),
  addOverlay: (overlay) => set((state) => ({ overlays: [...state.overlays, overlay] })),
  setReplayState: (replay) => set((state) => ({ replay: { ...state.replay, ...replay } })),
  setCrosshair: (crosshair) => set({ crosshair }),
  resetView: () => set({ viewport: { offset: 0, scale: 1, crosshair: null }, visibleRange: { startIndex: 0, endIndex: 100 } }),
}));


