"use client";

import { useChartEngineStore } from "../../stores/chart-engine-store";
import { viewportEngine } from "../../viewport/viewport-engine";

export function IndicatorLayer() {
  const indicators = useChartEngineStore((s) => s.indicators);
  const candles = useChartEngineStore((s) => s.candles);
  const viewport = useChartEngineStore((s) => s.viewport);
  const visibleRange = useChartEngineStore((s) => s.visibleRange);

  if (indicators.length === 0 || candles.length === 0) return null;

  const visibleCandles = candles.slice(visibleRange.startIndex, visibleRange.endIndex);
  const prices = visibleCandles.flatMap((c) => [c.high, c.low]);
  const minPrice = Math.min(...prices);
  const maxPrice = Math.max(...prices);
  const priceRange = maxPrice - minPrice || 1;
  const chartHeight = 400;

  return (
    <g>
      {indicators.map((indicator) => {
        const result = indicator.calculate(candles);
        const visibleValues = result.values.slice(visibleRange.startIndex, visibleRange.endIndex);

        return (
          <path
            key={indicator.id}
            d={visibleValues
              .map((val, i) => {
                const globalIndex = visibleRange.startIndex + i;
                const x = viewportEngine.getCandleX(globalIndex, viewport) + 4;
                const y = chartHeight - ((val - minPrice) / priceRange) * chartHeight;
                return `${i === 0 ? "M" : "L"} ${x} ${y}`;
              })
              .join(" ")}
            fill="none"
            stroke={result.color || "var(--color-primary-500)"}
            strokeWidth="2"
          />
        );
      })}
    </g>
  );
}


