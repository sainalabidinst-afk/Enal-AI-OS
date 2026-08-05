import type { Candle, IndicatorPlugin, IndicatorResult } from "../models/chart-models";

export function sma(period: number = 20): IndicatorPlugin {
  return {
    id: `sma-${period}`,
    name: `SMA ${period}`,
    calculate(candles: Candle[]): IndicatorResult {
      const values: number[] = [];

      for (let i = 0; i < candles.length; i++) {
        if (i < period - 1) {
          values.push(NaN);
          continue;
        }

        let sum = 0;
        for (let j = i - period + 1; j <= i; j++) {
          sum += candles[j].close;
        }
        values.push(sum / period);
      }

      return { values, color: "var(--color-primary-500)" };
    },
  };
}

export function ema(period: number = 20): IndicatorPlugin {
  return {
    id: `ema-${period}`,
    name: `EMA ${period}`,
    calculate(candles: Candle[]): IndicatorResult {
      const values: number[] = [];
      const k = 2 / (period + 1);

      for (let i = 0; i < candles.length; i++) {
        if (i === 0) {
          values.push(candles[i].close);
          continue;
        }

        const prevEma = values[i - 1];
        if (isNaN(prevEma)) {
          values.push(candles[i].close);
          continue;
        }

        values.push(candles[i].close * k + prevEma * (1 - k));
      }

      return { values, color: "var(--color-accent-500)" };
    },
  };
}


