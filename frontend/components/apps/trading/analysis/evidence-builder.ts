import type { AnalysisEvidence, MarketStructureResult, SignalResult, RiskAssessment, MultiTimeframeResult } from "./models/analysis-models";

export class AnalysisEvidenceBuilder {
  static build(
    structure: MarketStructureResult,
    signal: SignalResult,
    risk: RiskAssessment,
    multiTimeframe: MultiTimeframeResult[]
  ): AnalysisEvidence {
    const items = [
      { label: "Market Structure", value: structure.structure },
      { label: "Trend", value: structure.trend },
      { label: "Signal", value: signal.signal },
      { label: "Confidence", value: `${signal.confidence}%` },
      { label: "Risk Level", value: risk.level },
      { label: "Volatility", value: `${risk.volatility.toFixed(2)}%` },
      ...multiTimeframe.map((tf) => ({
        label: `Timeframe ${tf.timeframe}`,
        value: `${tf.trend} / ${tf.signal} (${tf.confidence}%)`,
      })),
    ];

    const multiTimeframeConsensus = multiTimeframe.map((tf) => `${tf.timeframe}: ${tf.trend}`).join(", ");

    return {
      summary: signal.signal === "wait" ? "No clear signal at this time." : `${signal.signal.toUpperCase()} signal detected with ${signal.confidence}% confidence.`,
      items,
      reasoning: `${structure.reasoning} ${signal.reasoning} ${risk.reasoning} Multi-timeframe: ${multiTimeframeConsensus}.`,
      confidence: Math.round((structure.confidence + signal.confidence + risk.confidence) / 3),
      alternative: signal.signal === "buy" ? "Wait for pullback to enter at better price." : signal.signal === "sell" ? "Wait for bounce to enter short at better price." : "Wait for clearer signal before entering.",
      nextAction: "Monitor price action at key levels and confirm signal with additional data.",
    };
  }
}

