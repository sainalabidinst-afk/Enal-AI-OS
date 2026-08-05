"use client";

import { useEffect } from "react";
import { Button } from "@/components/design-system/primitives/button";
import { useMarketStore } from "../stores/market-store";
import { useChartEngineStore } from "../chart-engine/stores/chart-engine-store";
import { ChartCanvas } from "../chart-engine/renderer/chart-canvas";
import { ReplayControls } from "../chart-engine/replay/replay-controls";
import { useTimeframeEngine } from "../chart-engine/hooks/use-timeframe-engine";
import { sma, ema } from "../chart-engine/models/indicators";

export function ChartPlaceholder() {
  const symbol = useMarketStore((s) => s.symbol);
  const ohlcv = useMarketStore((s) => s.ohlcv);
  const fetchOHLCV = useMarketStore((s) => s.fetchOHLCV);
  const setCandles = useChartEngineStore((s) => s.setCandles);
  const setReplayState = useChartEngineStore((s) => s.setReplayState);
  const addIndicator = useChartEngineStore((s) => s.addIndicator);
  const indicators = useChartEngineStore((s) => s.indicators);
  const { timeframe, handleTimeframeChange, timeframes } = useTimeframeEngine();

  useEffect(() => {
    fetchOHLCV();
  }, [fetchOHLCV]);

  useEffect(() => {
    if (ohlcv.length > 0) {
      setCandles(ohlcv);
      setReplayState({ totalCandles: ohlcv.length, currentIndex: 0 });
    }
  }, [ohlcv, setCandles, setReplayState]);

  const toggleSMA = () => {
    const exists = indicators.find((i) => i.id.startsWith("sma-"));
    if (exists) {
      useChartEngineStore.getState().removeIndicator(exists.id);
    } else {
      addIndicator(sma(20));
    }
  };

  const toggleEMA = () => {
    const exists = indicators.find((i) => i.id.startsWith("ema-"));
    if (exists) {
      useChartEngineStore.getState().removeIndicator(exists.id);
    } else {
      addIndicator(ema(20));
    }
  };

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b border-[var(--color-border)] px-4 py-2">
        <div className="flex items-center gap-4">
          <div>
            <h3 className="text-sm font-semibold">{symbol ?? "BTC/USDT"}</h3>
            <p className="text-xs text-[var(--color-secondary-500)]">
              {timeframe} • {ohlcv.length > 0 ? `${ohlcv.length} candles` : "Loading..."}
            </p>
          </div>
          {indicators.length > 0 && (
            <div className="flex gap-1">
              {indicators.map((ind) => (
                <span key={ind.id} className="text-xs px-2 py-0.5 rounded bg-[var(--color-primary-500)] text-white">
                  {ind.name}
                </span>
              ))}
            </div>
          )}
        </div>
        <div className="flex items-center gap-2">
          <select
            value={timeframe}
            onChange={(e) => handleTimeframeChange(e.target.value as any)}
            className="text-xs border border-[var(--color-border)] rounded px-2 py-1 bg-[var(--color-surface)]"
          >
            {timeframes.map((tf) => (
              <option key={tf.value} value={tf.value}>
                {tf.label}
              </option>
            ))}
          </select>
          <Button variant={indicators.some((i) => i.id.startsWith("sma-")) ? "primary" : "secondary"} size="sm" onClick={toggleSMA}>
            SMA
          </Button>
          <Button variant={indicators.some((i) => i.id.startsWith("ema-")) ? "primary" : "secondary"} size="sm" onClick={toggleEMA}>
            EMA
          </Button>
          <Button variant="secondary" size="sm">Drawing</Button>
          <ReplayControls />
        </div>
      </div>
      <div className="flex-1">
        <ChartCanvas />
      </div>
    </div>
  );
}
