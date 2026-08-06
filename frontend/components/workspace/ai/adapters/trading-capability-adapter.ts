import type { CapabilityAdapter, CapabilityContext } from "./capability-adapter.interface";
import type { ToolDefinition } from "../tools/tool-types";
import type { EvidencePayload } from "../evidence/evidence-types";
import { toolRegistry } from "../tools/tool-registry";
import { EvidenceBuilder } from "../evidence/evidence-builder";
import { useMarketStore } from "../../../apps/trading/stores/market-store";
import { useWatchlistStore } from "../../../apps/trading/stores/watchlist-store";
import { usePortfolioStore } from "../../../apps/trading/stores/portfolio-store";
import { useChartEngineStore } from "../../../apps/trading/chart-engine/stores/chart-engine-store";
import { marketStructureEngine } from "../../../apps/trading/analysis/market-structure/market-structure-engine";
import { signalEngine } from "../../../apps/trading/analysis/signal/signal-engine";
import { riskEngine } from "../../../apps/trading/analysis/risk/risk-engine";
import { AnalysisEvidenceBuilder } from "../../../apps/trading/analysis/evidence-builder";
import { RecommendationBuilder } from "../../../apps/trading/analysis/recommendation-builder";

export class TradingCapabilityAdapter implements CapabilityAdapter {
  capabilityId = "trading";

  async provideContext(): Promise<CapabilityContext> {
    const symbol = useMarketStore.getState().symbol;
    const timeframe = useChartEngineStore.getState().timeframe;
    const watchlist = useWatchlistStore.getState().items;
    const portfolio = usePortfolioStore.getState().portfolio;

    return {
      capabilityId: this.capabilityId,
      workspaceId: "trading",
      symbol: symbol ?? undefined,
      timeframe: timeframe ?? undefined,
      state: {
        watchlist,
        portfolio,
      },
    };
  }

  async provideTools(): Promise<ToolDefinition[]> {
    return toolRegistry.getAll().filter((t) => t.id.startsWith("trading-"));
  }

  async provideKnowledge(query: string): Promise<EvidencePayload> {
    const symbol = useMarketStore.getState().symbol;
    const ohlcv = useMarketStore.getState().ohlcv;
    const chartCandles = useChartEngineStore.getState().candles;
    const timeframe = useChartEngineStore.getState().timeframe;

    const candles = chartCandles.length > 0 ? chartCandles : ohlcv;

    if (candles.length < 20) {
      return EvidenceBuilder.build({
        summary: `Insufficient data for analysis of ${symbol ?? "Unknown"}.`,
        items: [EvidenceBuilder.fromData("Symbol", symbol ?? "Unknown")],
        reasoning: "Need at least 20 candles to perform technical analysis.",
        confidence: 0,
        alternative: "Wait for more data to load.",
        nextAction: "Ensure market data is connected and candles are loading.",
      });
    }

    const structure = marketStructureEngine.analyze(candles);
    const signal = signalEngine.generate(candles);
    const risk = riskEngine.assess(candles, signal);
    const multiTimeframe = [{ timeframe, trend: structure.trend, signal: signal.signal, confidence: signal.confidence }];
    const evidence = AnalysisEvidenceBuilder.build(structure, signal, risk, multiTimeframe);
    const recommendation = RecommendationBuilder.build(signal, risk, structure);

    const items = [
      EvidenceBuilder.fromData("Symbol", symbol ?? "Unknown"),
      EvidenceBuilder.fromData("Timeframe", timeframe),
      EvidenceBuilder.fromData("Trend", structure.trend),
      EvidenceBuilder.fromData("Structure", structure.structure),
      EvidenceBuilder.fromData("Signal", signal.signal.toUpperCase()),
      EvidenceBuilder.fromData("Confidence", `${signal.confidence}%`),
      EvidenceBuilder.fromData("Risk", risk.level.toUpperCase()),
      EvidenceBuilder.fromData("Volatility", `${risk.volatility.toFixed(2)}%`),
      EvidenceBuilder.fromData("Recommendation", recommendation.action),
      EvidenceBuilder.fromData("Position Size", recommendation.positionSize ?? "N/A"),
    ];

    return EvidenceBuilder.build({
      summary: evidence.summary,
      items,
      reasoning: evidence.reasoning,
      confidence: evidence.confidence,
      alternative: evidence.alternative,
      nextAction: evidence.nextAction,
    });
  }
}

export const tradingCapabilityAdapter = new TradingCapabilityAdapter();
