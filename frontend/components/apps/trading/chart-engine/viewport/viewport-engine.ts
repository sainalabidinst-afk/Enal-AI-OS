import type { VisibleRange, ViewportState } from "../models/chart-models";

export class ViewportEngine {
  private candleWidth = 8;
  private spacing = 2;
  private totalCandles = 0;

  setTotalCandles(count: number) {
    this.totalCandles = count;
  }

  getVisibleRange(state: ViewportState, containerWidth: number): VisibleRange {
    const totalWidth = this.totalCandles * (this.candleWidth + this.spacing);
    const maxOffset = Math.max(0, totalWidth - containerWidth);
    const clampedOffset = Math.min(state.offset, maxOffset);

    const visibleCount = Math.floor(containerWidth / (this.candleWidth + this.spacing)) + 1;
    const startIndex = Math.floor(clampedOffset / (this.candleWidth + this.spacing));
    const endIndex = Math.min(startIndex + visibleCount, this.totalCandles);

    return {
      startIndex: Math.max(0, startIndex),
      endIndex: Math.max(0, endIndex),
    };
  }

  getCandleX(index: number, state: ViewportState): number {
    return index * (this.candleWidth + this.spacing) - state.offset;
  }

  zoom(delta: number, state: ViewportState, containerWidth: number): ViewportState {
    const zoomFactor = delta > 0 ? 0.9 : 1.1;
    const newScale = Math.min(Math.max(state.scale * zoomFactor, 0.1), 5);

    return {
      ...state,
      scale: newScale,
    };
  }

  pan(deltaX: number, state: ViewportState, containerWidth: number): ViewportState {
    const totalWidth = this.totalCandles * (this.candleWidth + this.spacing) * state.scale;
    const maxOffset = Math.max(0, totalWidth - containerWidth);
    const newOffset = Math.min(Math.max(state.offset + deltaX, 0), maxOffset);

    return {
      ...state,
      offset: newOffset,
    };
  }

  fitToScreen(containerWidth: number): ViewportState {
    if (this.totalCandles === 0) return { offset: 0, scale: 1, crosshair: null };

    const totalWidth = this.totalCandles * (this.candleWidth + this.spacing);
    const scale = containerWidth / totalWidth;

    return {
      offset: 0,
      scale: Math.min(scale, 1),
      crosshair: null,
    };
  }
}

export const viewportEngine = new ViewportEngine();


