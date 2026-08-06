import type { DecisionRequest } from "../models/decision-models";
import { useMarketStore } from "../../../apps/trading/stores/market-store";
import { useChartEngineStore } from "../../../apps/trading/chart-engine/stores/chart-engine-store";

export function createTradingDecisionRequest(
  signal: { action: string; confidence: number; strength: number },
  risk: { level: string; volatility: number; confidence: number },
  evidence: { label: string; value: string | number | boolean }[]
): DecisionRequest {
  const symbol = useMarketStore.getState().symbol;
  const timeframe = useChartEngineStore.getState().timeframe;

  return {
    capabilityId: "trading",
    context: {
      symbol,
      timeframe,
    },
    evidence,
    signal: {
      action: signal.action,
      confidence: signal.confidence,
      strength: signal.strength,
    },
    risk: {
      level: risk.level,
      volatility: risk.volatility,
      confidence: risk.confidence,
    },
    constraints: {
      maxPositionSize: "2%",
      minConfidence: 60,
    },
  };
}
