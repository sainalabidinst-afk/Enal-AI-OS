import type { Candle } from "../../chart-engine/models/chart-models";
import type { MarketStructureResult, TrendDirection } from "../models/analysis-models";

export class MarketStructureEngine {
  analyze(candles: Candle[]): MarketStructureResult {
    if (candles.length < 20) {
      return {
        structure: "trend",
        trend: "neutral",
        confidence: 0,
        reasoning: "Insufficient data for market structure analysis.",
      };
    }

    const highs = candles.slice(-20).map((c) => c.high);
    const lows = candles.slice(-20).map((c) => c.low);
    const closes = candles.slice(-20).map((c) => c.close);

    const higherHighs = this.countHigherHighs(highs);
    const higherLows = this.countHigherLows(lows);
    const lowerHighs = this.countLowerHighs(highs);
    const lowerLows = this.countLowerLows(lows);

    const trend = this.determineTrend(higherHighs, higherLows, lowerHighs, lowerLows);
    const structure = this.determineStructure(candles, trend);
    const confidence = this.calculateConfidence(candles, trend);

    return {
      structure,
      trend,
      confidence,
      reasoning: this.buildReasoning(trend, structure, higherHighs, higherLows, lowerHighs, lowerLows),
    };
  }

  private countHigherHighs(highs: number[]): number {
    let count = 0;
    for (let i = 1; i < highs.length; i++) {
      if (highs[i] > highs[i - 1]) count++;
    }
    return count;
  }

  private countHigherLows(lows: number[]): number {
    let count = 0;
    for (let i = 1; i < lows.length; i++) {
      if (lows[i] > lows[i - 1]) count++;
    }
    return count;
  }

  private countLowerHighs(highs: number[]): number {
    let count = 0;
    for (let i = 1; i < highs.length; i++) {
      if (highs[i] < highs[i - 1]) count++;
    }
    return count;
  }

  private countLowerLows(lows: number[]): number {
    let count = 0;
    for (let i = 1; i < lows.length; i++) {
      if (lows[i] < lows[i - 1]) count++;
    }
    return count;
  }

  private determineTrend(higherHighs: number, higherLows: number, lowerHighs: number, lowerLows: number): TrendDirection {
    if (higherHighs > lowerHighs && higherLows > lowerLows) return "bullish";
    if (lowerHighs > higherHighs && lowerLows > higherLows) return "bearish";
    return "sideways";
  }

  private determineStructure(candles: Candle[], trend: TrendDirection): MarketStructureResult["structure"] {
    const lastCandle = candles[candles.length - 1];
    const prevCandle = candles[candles.length - 2];
    const recentHigh = Math.max(...candles.slice(-10).map((c) => c.high));
    const recentLow = Math.min(...candles.slice(-10).map((c) => c.low));
    const range = recentHigh - recentLow;
    const currentPosition = (lastCandle.close - recentLow) / range;

    if (trend === "bullish") {
      if (lastCandle.close < prevCandle.close && currentPosition < 0.3) return "pullback";
      if (lastCandle.close > recentHigh * 0.99) return "breakout";
      return "trend";
    }
    if (trend === "bearish") {
      if (lastCandle.close > prevCandle.close && currentPosition > 0.7) return "pullback";
      if (lastCandle.close < recentLow * 1.01) return "breakout";
      return "trend";
    }
    return "range";
  }

  private calculateConfidence(candles: Candle[], trend: TrendDirection): number {
    const closes = candles.slice(-10).map((c) => c.close);
    const volatility = this.calculateVolatility(closes);
    if (volatility > 0.05) return 40;
    if (trend === "sideways") return 50;
    return 75;
  }

  private calculateVolatility(values: number[]): number {
    if (values.length < 2) return 0;
    const mean = values.reduce((a, b) => a + b) / values.length;
    const squaredDiffs = values.map((v) => (v - mean) ** 2);
    const avgSquaredDiff = squaredDiffs.reduce((a, b) => a + b) / squaredDiffs.length;
    return Math.sqrt(avgSquaredDiff) / mean;
  }

  private buildReasoning(
    trend: TrendDirection,
    structure: MarketStructureResult["structure"],
    higherHighs: number,
    higherLows: number,
    lowerHighs: number,
    lowerLows: number
  ): string {
    const trendDesc = trend === "bullish" ? "bullish" : trend === "bearish" ? "bearish" : "sideways";
    const structureDesc = structure === "trend" ? "trending" : structure === "range" ? "ranging" : structure === "breakout" ? "breaking out" : structure === "pullback" ? "pulling back" : "reversing";

    return `Market is ${structureDesc} with ${trendDesc} bias. Higher highs: ${higherHighs}, Higher lows: ${higherLows}, Lower highs: ${lowerHighs}, Lower lows: ${lowerLows}.`;
  }
}

export const marketStructureEngine = new MarketStructureEngine();

