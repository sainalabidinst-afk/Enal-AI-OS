import type { Candle } from "../../chart-engine/models/chart-models";
import { sma, ema } from "../../chart-engine/models/indicators";
import { rsi, macd } from "../indicators/analysis-indicators";
import { marketStructureEngine } from "../market-structure/market-structure-engine";
import type { SignalResult, SignalType } from "../models/analysis-models";

export class SignalEngine {
  generate(candles: Candle[]): SignalResult {
    if (candles.length < 50) {
      return {
        signal: "wait",
        confidence: 0,
        strength: 0,
        reasoning: "Insufficient data for signal generation.",
      };
    }

    const structure = marketStructureEngine.analyze(candles);
    const sma20 = sma(20).calculate(candles);
    const sma50 = sma(50).calculate(candles);
    const ema20 = ema(20).calculate(candles);
    const rsi14 = rsi(14).calculate(candles);
    const macdResult = macd().calculate(candles);

    const lastClose = candles[candles.length - 1].close;
    const lastSma20 = sma20.values[sma20.values.length - 1];
    const lastSma50 = sma50.values[sma50.values.length - 1];
    const lastEma20 = ema20.values[ema20.values.length - 1];
    const lastRsi = rsi14.values[rsi14.values.length - 1];
    const lastMacd = macdResult.values[macdResult.values.length - 1];

    let bullishSignals = 0;
    let bearishSignals = 0;

    if (!isNaN(lastSma20) && !isNaN(lastSma50) && lastClose > lastSma20 && lastSma20 > lastSma50) bullishSignals++;
    if (!isNaN(lastSma20) && !isNaN(lastSma50) && lastClose < lastSma20 && lastSma20 < lastSma50) bearishSignals++;
    if (!isNaN(lastEma20) && lastClose > lastEma20) bullishSignals++;
    if (!isNaN(lastEma20) && lastClose < lastEma20) bearishSignals++;
    if (!isNaN(lastRsi) && lastRsi < 30) bullishSignals++;
    if (!isNaN(lastRsi) && lastRsi > 70) bearishSignals++;
    if (!isNaN(lastMacd) && lastMacd > 0) bullishSignals++;
    if (!isNaN(lastMacd) && lastMacd < 0) bearishSignals++;
    if (structure.trend === "bullish") bullishSignals++;
    if (structure.trend === "bearish") bearishSignals++;

    const totalSignals = bullishSignals + bearishSignals;
    let signal: SignalType = "wait";
    let confidence = 0;

    if (totalSignals > 0) {
      const bullishRatio = bullishSignals / totalSignals;
      if (bullishRatio >= 0.7) {
        signal = "buy";
        confidence = Math.round(bullishRatio * 100);
      } else if (bullishRatio <= 0.3) {
        signal = "sell";
        confidence = Math.round((1 - bullishRatio) * 100);
      } else {
        signal = "wait";
        confidence = 50;
      }
    }

    const strength = Math.abs(bullishSignals - bearishSignals) / Math.max(totalSignals, 1);

    return {
      signal,
      confidence,
      strength: Math.round(strength * 100),
      reasoning: this.buildReasoning(signal, bullishSignals, bearishSignals, structure, lastRsi, lastMacd),
    };
  }

  private buildReasoning(
    signal: SignalType,
    bullish: number,
    bearish: number,
    structure: { trend: string },
    rsi?: number,
    macd?: number
  ): string {
    const parts = [`Signal: ${signal.toUpperCase()} (bullish: ${bullish}, bearish: ${bearish})`];
    parts.push(`Trend: ${structure.trend}`);
    if (typeof rsi === "number" && !isNaN(rsi)) parts.push(`RSI: ${rsi.toFixed(1)}`);
    if (typeof macd === "number" && !isNaN(macd)) parts.push(`MACD: ${macd.toFixed(2)}`);
    return parts.join(", ");
  }
}

export const signalEngine = new SignalEngine();

