"use client";

import { useChartEngineStore } from "../../stores/chart-engine-store";
import { viewportEngine } from "../../viewport/viewport-engine";

export function CandleLayer() {
  const candles = useChartEngineStore((s) => s.candles);
  const viewport = useChartEngineStore((s) => s.viewport);
  const visibleRange = useChartEngineStore((s) => s.visibleRange);

  if (candles.length === 0) {
    return (
      <text x="50%" y="50%" textAnchor="middle" className="fill-[var(--color-secondary-500)] text-sm">
        No candle data
      </text>
    );
  }

  const visibleCandles = candles.slice(visibleRange.startIndex, visibleRange.endIndex);
  const prices = visibleCandles.flatMap((c) => [c.high, c.low]);
  const minPrice = Math.min(...prices);
  const maxPrice = Math.max(...prices);
  const priceRange = maxPrice - minPrice || 1;

  const chartHeight = 400;
  const volumeHeight = 80;
  const candleWidth = 8;
  const spacing = 2;

  return (
    <g>
      {visibleCandles.map((candle, i) => {
        const globalIndex = visibleRange.startIndex + i;
        const x = viewportEngine.getCandleX(globalIndex, viewport);
        const isGreen = candle.close >= candle.open;
        const color = isGreen ? "var(--color-success-500)" : "var(--color-danger-500)";

        const openY = chartHeight - ((candle.open - minPrice) / priceRange) * chartHeight;
        const closeY = chartHeight - ((candle.close - minPrice) / priceRange) * chartHeight;
        const highY = chartHeight - ((candle.high - minPrice) / priceRange) * chartHeight;
        const lowY = chartHeight - ((candle.low - minPrice) / priceRange) * chartHeight;

        return (
          <g key={candle.timestamp}>
            <line
              x1={x + candleWidth / 2}
              y1={highY}
              x2={x + candleWidth / 2}
              y2={lowY}
              stroke={color}
              strokeWidth="1"
            />
            <rect
              x={x}
              y={Math.min(openY, closeY)}
              width={candleWidth}
              height={Math.max(Math.abs(closeY - openY), 1)}
              fill={color}
            />
          </g>
        );
      })}
    </g>
  );
}


