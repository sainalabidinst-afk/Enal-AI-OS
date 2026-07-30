import { api } from "./api";
import type {
  IntegrationResponse,
  TradingIntegrationRequest,
  NetworkDesignReviewRequest,
  SelfImprovementRequest,
} from "../types/integration";

export async function analyzeTradingWithKnowledge(
  req: TradingIntegrationRequest,
): Promise<IntegrationResponse> {
  return api.post<IntegrationResponse>("/api/v1/integration/trading-analysis", {
    symbol: req.symbol,
    timeframes: req.timeframes,
    exchange: req.exchange || "binance",
  });
}

export async function reviewNetworkDesignWithKnowledge(
  req: NetworkDesignReviewRequest,
): Promise<IntegrationResponse> {
  return api.post<IntegrationResponse>("/api/v1/integration/network-design-review", {
    topology_description: req.topology_description,
    requirements: req.requirements,
  });
}

export async function runSelfImprovementCycle(
  req: SelfImprovementRequest,
): Promise<IntegrationResponse> {
  return api.post<IntegrationResponse>("/api/v1/integration/self-improvement", {
    project_path: req.project_path,
    analysis_type: req.analysis_type || "full",
  });
}
