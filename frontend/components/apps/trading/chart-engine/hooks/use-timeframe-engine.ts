"use client";

import { useCallback } from "react";
import { useChartEngineStore } from "../stores/chart-engine-store";
import type { Timeframe } from "../models/chart-models";

export const TIMEFRAMES: { value: Timeframe; label: string }[] = [
  { value: "1m", label: "1m" },
  { value: "3m", label: "3m" },
  { value: "5m", label: "5m" },
  { value: "15m", label: "15m" },
  { value: "30m", label: "30m" },
  { value: "1h", label: "1H" },
  { value: "4h", label: "4H" },
  { value: "1d", label: "1D" },
  { value: "1w", label: "1W" },
  { value: "1M", label: "1M" },
];

export function useTimeframeEngine() {
  const timeframe = useChartEngineStore((s) => s.timeframe);
  const setTimeframe = useChartEngineStore((s) => s.setTimeframe);

  const handleTimeframeChange = useCallback(
    (newTimeframe: Timeframe) => {
      setTimeframe(newTimeframe);
    },
    [setTimeframe]
  );

  return {
    timeframe,
    timeframes: TIMEFRAMES,
    handleTimeframeChange,
  };
}


