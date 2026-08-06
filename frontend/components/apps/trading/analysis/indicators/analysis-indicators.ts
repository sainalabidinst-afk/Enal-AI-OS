import type { Candle } from "../../chart-engine/models/chart-models";
import type { IndicatorPlugin, IndicatorResult } from "../../chart-engine/models/chart-models";

function calculateEMA(values: number[], period: number): number[] {
  const k = 2 / (period + 1);
  const result: number[] = [];
  let ema = values[0];

  for (let i = 0; i < values.length; i++) {
    if (isNaN(values[i])) {
      result.push(NaN);
      continue;
    }
    ema = values[i] * k + ema * (1 - k);
    result.push(ema);
  }

  return result;
}

export function rsi(period = 14): IndicatorPlugin {
  return {
    id: `rsi-${period}`,
    name: `RSI ${period}`,
    calculate(candles: Candle[]): IndicatorResult {
      const values: number[] = [];

      for (let i = 0; i < candles.length; i++) {
        if (i < period) {
          values.push(NaN);
          continue;
        }

        const slice = candles.slice(i - period, i + 1);
        let gains = 0;
        let losses = 0;

        for (let j = 1; j < slice.length; j++) {
          const change = slice[j].close - slice[j - 1].close;
          if (change > 0) gains += change;
          else losses += Math.abs(change);
        }

        const avgGain = gains / period;
        const avgLoss = losses / period;
        const rs = avgLoss === 0 ? 100 : avgGain / avgLoss;
        const rsi = 100 - 100 / (1 + rs);

        values.push(rsi);
      }

      return { values, color: "var(--color-primary-500)" };
    },
  };
}

export function macd(fast = 12, slow = 26, signal = 9): IndicatorPlugin {
  return {
    id: `macd-${fast}-${slow}`,
    name: `MACD ${fast},${slow}`,
    calculate(candles: Candle[]): IndicatorResult {
      const closes = candles.map((c) => c.close);
      const emaFast = calculateEMA(closes, fast);
      const emaSlow = calculateEMA(closes, slow);
      const macdLine = emaFast.map((v, i) => v - emaSlow[i]);

      return { values: macdLine, color: "var(--color-primary-500)" };
    },
  };
}

export function bollingerBands(period = 20, stdDev = 2): IndicatorPlugin {
  return {
    id: `bb-${period}`,
    name: `Bollinger Bands ${period}`,
    calculate(candles: Candle[]): IndicatorResult {
      const values: number[] = [];
      const closes = candles.map((c) => c.close);

      for (let i = 0; i < candles.length; i++) {
        if (i < period - 1) {
          values.push(NaN);
          continue;
        }

        const slice = closes.slice(i - period + 1, i + 1);
        const mean = slice.reduce((a, b) => a + b) / period;
        const variance = slice.reduce((sum, val) => sum + (val - mean) ** 2, 0) / period;
        const std = Math.sqrt(variance);
        const upper = mean + stdDev * std;

        values.push(upper);
      }

      return { values, color: "var(--color-primary-500)" };
    },
  };
}

export function atr(period = 14): IndicatorPlugin {
  return {
    id: `atr-${period}`,
    name: `ATR ${period}`,
    calculate(candles: Candle[]): IndicatorResult {
      const values: number[] = [];

      for (let i = 0; i < candles.length; i++) {
        if (i === 0) {
          values.push(candles[i].high - candles[i].low);
          continue;
        }

        const tr = Math.max(
          candles[i].high - candles[i].low,
          Math.abs(candles[i].high - candles[i - 1].close),
          Math.abs(candles[i].low - candles[i - 1].close)
        );

        if (i < period) {
          values.push(NaN);
          continue;
        }

        let sum = 0;
        for (let j = i - period + 1; j <= i; j++) {
          sum += values[j] || 0;
        }
        values.push(sum / period);
      }

      return { values, color: "var(--color-primary-500)" };
    },
  };
}

export function vwap(candles: Candle[]): IndicatorPlugin {
  return {
    id: "vwap",
    name: "VWAP",
    calculate(candles: Candle[]): IndicatorResult {
      const values: number[] = [];
      let cumulativeTPV = 0;
      let cumulativeVolume = 0;

      for (const candle of candles) {
        const typicalPrice = (candle.high + candle.low + candle.close) / 3;
        cumulativeTPV += typicalPrice * candle.volume;
        cumulativeVolume += candle.volume;
        const vwap = cumulativeVolume === 0 ? 0 : cumulativeTPV / cumulativeVolume;
        values.push(vwap);
      }

      return { values, color: "var(--color-primary-500)" };
    },
  };
}

