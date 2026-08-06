import type { Candle } from "../../chart-engine/models/chart-models";
import { signalEngine } from "../signal/signal-engine";
import { marketStructureEngine } from "../market-structure/market-structure-engine";
import type { MultiTimeframeResult, TrendDirection, SignalType } from "../models/analysis-models";

export class MultiTimeframeAnalyzer {
  analyze(candlesByTimeframe: Record<string, Candle[]>): MultiTimeframeResult[] {
    const results: MultiTimeframeResult[] = [];

    for (const [timeframe, candles] of Object.entries(candlesByTimeframe)) {
      const structure = marketStructureEngine.analyze(candles);
      const signal = signalEngine.generate(candles);

      results.push({
        timeframe,
        trend: structure.trend,
        signal: signal.signal,
        confidence: signal.confidence,
      });
    }

    return results;
  }

  getConsensus(results: MultiTimeframeResult[]): { trend: TrendDirection; signal: SignalType; confidence: number } {
    if (results.length === 0) {
      return { trend: "neutral", signal: "wait", confidence: 0 };
    }

    const bullishTrends = results.filter((r) => r.trend === "bullish").length;
    const bearishTrends = results.filter((r) => r.trend === "bearish").length;
    const buySignals = results.filter((r) => r.signal === "buy").length;
    const sellSignals = results.filter((r) => r.signal === "sell").length;

    const trend: TrendDirection = bullishTrends > bearishTrends ? "bullish" : bearishTrends > bullishTrends ? "bearish" : "sideways";
    const signal: SignalType = buySignals > sellSignals ? "buy" : sellSignals > buySignals ? "sell" : "wait";
    const confidence = Math.round(((bullishTrends + bearishTrends) / results.length) * 100);

    return { trend, signal, confidence };
  }
}

export const multiTimeframeAnalyzer = new MultiTimeframeAnalyzer();

