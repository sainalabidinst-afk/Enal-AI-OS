export interface Candle {
  timestamp: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface VisibleRange {
  startIndex: number;
  endIndex: number;
}

export interface ViewportState {
  offset: number;
  scale: number;
  crosshair: { x: number; y: number } | null;
}

export interface ChartDimensions {
  width: number;
  height: number;
  candleWidth: number;
  spacing: number;
  volumeHeight: number;
  padding: { top: number; right: number; bottom: number; left: number };
}

export type Timeframe = "1m" | "3m" | "5m" | "15m" | "30m" | "1h" | "4h" | "1d" | "1w" | "1M";

export interface IndicatorResult {
  values: number[];
  color?: string;
}

export interface IndicatorPlugin {
  id: string;
  name: string;
  calculate(candles: Candle[]): IndicatorResult;
}

export type DrawingTool = "none" | "trendline" | "horizontal" | "vertical" | "rectangle" | "fibonacci";

export interface DrawingObject {
  id: string;
  type: DrawingTool;
  points: { x: number; y: number }[];
}

export type OverlayType = "buy" | "sell" | "ai-signal" | "news" | "earnings";

export interface OverlayObject {
  id: string;
  type: OverlayType;
  timestamp: number;
  price: number;
  label?: string;
}

export interface ReplayState {
  isPlaying: boolean;
  speed: number;
  currentIndex: number;
  totalCandles: number;
}


