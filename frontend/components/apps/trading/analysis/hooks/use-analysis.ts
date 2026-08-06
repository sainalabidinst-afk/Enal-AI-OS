import { useMemo } from "react";
import { useMarketStore } from "../../stores/market-store";
import { useChartEngineStore } from "../../chart-engine/stores/chart-engine-store";
import { marketStructureEngine } from "../market-structure/market-structure-engine";
import { signalEngine } from "../signal/signal-engine";
import { multiTimeframeAnalyzer } from "../multi-timeframe/multi-timeframe-analyzer";
import { riskEngine } from "../risk/risk-engine";
import { AnalysisEvidenceBuilder } from "../evidence-builder";
import { RecommendationBuilder } from "../recommendation-builder";
import type { AnalysisEvidence, Recommendation, MultiTimeframeResult } from "../models/analysis-models";

export function useAnalysis() {
  const candles = useMarketStore((s) => s.ohlcv);
  const chartCandles = useChartEngineStore((s) => s.candles);
  const timeframe = useChartEngineStore((s) => s.timeframe);

  const analysis = useMemo(() => {
    const data = chartCandles.length > 0 ? chartCandles : candles;
    if (data.length < 20) return null;

    const structure = marketStructureEngine.analyze(data);
    const signal = signalEngine.generate(data);
    const risk = riskEngine.assess(data, signal);
    const multiTimeframe = multiTimeframeAnalyzer.analyze({ [timeframe]: data });
    const evidence = AnalysisEvidenceBuilder.build(structure, signal, risk, multiTimeframe);
    const recommendation = RecommendationBuilder.build(signal, risk, structure);

    return {
      structure,
      signal,
      risk,
      multiTimeframe,
      evidence,
      recommendation,
    };
  }, [candles, chartCandles, timeframe]);

  return analysis;
}

