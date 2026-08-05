"use client";

import { useChartEngineStore } from "../../stores/chart-engine-store";
import { viewportEngine } from "../../viewport/viewport-engine";

export function VolumeLayer() {
  const candles = useChartEngineStore((s) => s.candles);
  const visibleRange = useChartEngineStore((s) => s.visibleRange);
  const viewport = useChartEngineStore((s) => s.viewport);

  if (candles.length === 0) return null;

  const visibleCandles = candles.slice(visibleRange.startIndex, visibleRange.endIndex);
  const volumes = visibleCandles.map((c) => c.volume);
  const maxVolume = Math.max(...volumes, 1);

  const chartHeight = 400;
  const volumeHeight = 80;
  const volumeTop = chartHeight + 10;
  const candleWidth = 8;

  return (
    <g>
      {visibleCandles.map((candle, i) => {
        const globalIndex = visibleRange.startIndex + i;
        const x = viewportEngine.getCandleX(globalIndex, viewport);
        const isGreen = candle.close >= candle.open;
        const color = isGreen ? "var(--color-success-500)" : "var(--color-danger-500)";
        const barHeight = (candle.volume / maxVolume) * volumeHeight;

        return (
          <rect
            key={candle.timestamp}
            x={x}
            y={volumeTop + volumeHeight - barHeight}
            width={candleWidth}
            height={barHeight}
            fill={color}
            opacity="0.6"
          />
        );
      })}
    </g>
  );
}


