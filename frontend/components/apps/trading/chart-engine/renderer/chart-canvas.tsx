"use client";

import { useRef, useEffect } from "react";
import { useChartEngineStore } from "../stores/chart-engine-store";
import { viewportEngine } from "../viewport/viewport-engine";
import { CandleLayer } from "../layers/candle/candle-layer";
import { VolumeLayer } from "../layers/volume/volume-layer";
import { CrosshairLayer } from "../layers/overlay/crosshair-layer";
import { IndicatorLayer } from "../layers/indicator/indicator-layer";
import { DrawingLayer } from "../layers/drawing/drawing-layer";

export function ChartCanvas() {
  const containerRef = useRef<HTMLDivElement>(null);
  const candles = useChartEngineStore((s) => s.candles);
  const viewport = useChartEngineStore((s) => s.viewport);
  const setViewport = useChartEngineStore((s) => s.setViewport);
  const setVisibleRange = useChartEngineStore((s) => s.setVisibleRange);
  const resetView = useChartEngineStore((s) => s.resetView);

  useEffect(() => {
    viewportEngine.setTotalCandles(candles.length);
    if (containerRef.current) {
      const range = viewportEngine.getVisibleRange(viewport, containerRef.current.clientWidth);
      setVisibleRange(range);
    }
  }, [candles.length, viewport, setVisibleRange]);

  const handleWheel = (e: React.WheelEvent) => {
    e.preventDefault();
    if (containerRef.current) {
      const newViewport = viewportEngine.zoom(e.deltaY, viewport, containerRef.current.clientWidth);
      setViewport(newViewport);
    }
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    if (e.button === 1 || (e.button === 0 && e.shiftKey)) {
      const startX = e.clientX;
      const startOffset = viewport.offset;

      const handleMouseMove = (moveEvent: MouseEvent) => {
        const deltaX = startX - moveEvent.clientX;
        if (containerRef.current) {
          const newViewport = viewportEngine.pan(deltaX, { ...viewport, offset: startOffset }, containerRef.current.clientWidth);
          setViewport(newViewport);
        }
      };

      const handleMouseUp = () => {
        document.removeEventListener("mousemove", handleMouseMove);
        document.removeEventListener("mouseup", handleMouseUp);
      };

      document.addEventListener("mousemove", handleMouseMove);
      document.addEventListener("mouseup", handleMouseUp);
    }
  };

  const handleDoubleClick = () => {
    if (containerRef.current) {
      const newViewport = viewportEngine.fitToScreen(containerRef.current.clientWidth);
      setViewport(newViewport);
    }
  };

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
              const newViewport = viewportEngine.zoom(-100, viewport, containerRef.current.clientWidth);
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
              const newViewport = viewportEngine.zoom(100, viewport, containerRef.current.clientWidth);
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
}


