"use client";

import { useRef, useEffect, memo, useCallback } from "react";
import { useChartEngineStore } from "../stores/chart-engine-store";
import { viewportEngine } from "../viewport/viewport-engine";
import { CandleLayer } from "../layers/candle/candle-layer";
import { VolumeLayer } from "../layers/volume/volume-layer";
import { CrosshairLayer } from "../layers/overlay/crosshair-layer";
import { IndicatorLayer } from "../layers/indicator/indicator-layer";
import { DrawingLayer } from "../layers/drawing/drawing-layer";

export const ChartCanvas = memo(function ChartCanvas() {
  const containerRef = useRef<HTMLDivElement>(null);
  const candles = useChartEngineStore((s) => s.candles);
  const viewport = useChartEngineStore((s) => s.viewport);
  const setViewport = useChartEngineStore((s) => s.setViewport);
  const setVisibleRange = useChartEngineStore((s) => s.setVisibleRange);
  const resetView = useChartEngineStore((s) => s.resetView);
  const viewportRef = useRef(viewport);
  viewportRef.current = viewport;

  useEffect(() => {
    viewportEngine.setTotalCandles(candles.length);
    if (containerRef.current) {
      const range = viewportEngine.getVisibleRange(viewport, containerRef.current.clientWidth);
      setVisibleRange(range);
    }
  }, [candles.length, viewport, setVisibleRange]);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleMouseMove = (moveEvent: MouseEvent) => {
      const startX = (moveEvent as MouseEvent & { startX?: number }).startX || 0;
      const startOffset = (moveEvent as MouseEvent & { startOffset?: number }).startOffset || 0;
      const deltaX = startX - moveEvent.clientX;
      const currentViewport = viewportEngine.pan(deltaX, { ...viewportRef.current, offset: startOffset }, container.clientWidth);
      setViewport(currentViewport);
    };

    const handleMouseUp = () => {
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
    };

    return () => {
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
    };
  }, [setViewport]);

  const handleWheel = useCallback(
    (e: React.WheelEvent) => {
      e.preventDefault();
      if (containerRef.current) {
        const newViewport = viewportEngine.zoom(e.deltaY, viewportRef.current, containerRef.current.clientWidth);
        setViewport(newViewport);
      }
    },
    [setViewport]
  );

  const handleMouseDown = useCallback(
    (e: React.MouseEvent) => {
      if (e.button === 1 || (e.button === 0 && e.shiftKey)) {
        const startX = e.clientX;
        const startOffset = viewportRef.current.offset;

        const moveEvent = e.nativeEvent as MouseEvent & { startX?: number; startOffset?: number };
        moveEvent.startX = startX;
        moveEvent.startOffset = startOffset;

        const handleMouseMove = (moveEvent: MouseEvent) => {
          const startX = (moveEvent as MouseEvent & { startX?: number }).startX || 0;
          const startOffset = (moveEvent as MouseEvent & { startOffset?: number }).startOffset || 0;
          const deltaX = startX - moveEvent.clientX;
          const currentViewport = viewportEngine.pan(deltaX, { ...viewportRef.current, offset: startOffset }, containerRef.current!.clientWidth);
          setViewport(currentViewport);
        };

        const handleMouseUp = () => {
          document.removeEventListener("mousemove", handleMouseMove);
          document.removeEventListener("mouseup", handleMouseUp);
        };

        document.addEventListener("mousemove", handleMouseMove);
        document.addEventListener("mouseup", handleMouseUp);
      }
    },
    [setViewport]
  );

  const handleDoubleClick = useCallback(() => {
    if (containerRef.current) {
      const newViewport = viewportEngine.fitToScreen(containerRef.current.clientWidth);
      setViewport(newViewport);
    }
  }, [setViewport]);

  return (
    <div
      ref={containerRef}
      className="relative h-full w-full overflow-hidden bg-[var(--color-bg-secondary)]"
      onWheel={handleWheel}
      onMouseDown={handleMouseDown}
      onDoubleClick={handleDoubleClick}
    >
      <svg className="absolute inset-0 h-full w-full">
        <IndicatorLayer />
        <CandleLayer />
        <VolumeLayer />
        <CrosshairLayer />
        <DrawingLayer />
      </svg>
      <div className="absolute bottom-2 right-2 flex gap-2">
        <button
          onClick={() => {
            if (containerRef.current) {
              const newViewport = viewportEngine.zoom(-100, viewportRef.current, containerRef.current.clientWidth);
              setViewport(newViewport);
            }
          }}
          className="px-2 py-1 text-xs bg-[var(--color-surface)] border border-[var(--color-border)] rounded"
        >
          Zoom +
        </button>
        <button
          onClick={() => {
            if (containerRef.current) {
              const newViewport = viewportEngine.zoom(100, viewportRef.current, containerRef.current.clientWidth);
              setViewport(newViewport);
            }
          }}
          className="px-2 py-1 text-xs bg-[var(--color-surface)] border border-[var(--color-border)] rounded"
        >
          Zoom -
        </button>
        <button
          onClick={() => resetView()}
          className="px-2 py-1 text-xs bg-[var(--color-surface)] border border-[var(--color-border)] rounded"
        >
          Fit
        </button>
      </div>
    </div>
  );
});
