import type { CapabilityAdapter, CapabilityContext } from "./capability-adapter.interface";
import type { ToolDefinition } from "../tools/tool-types";
import type { EvidencePayload } from "../evidence/evidence-types";
import { toolRegistry } from "../tools/tool-registry";
import { EvidenceBuilder } from "../evidence/evidence-builder";
import { useMarketStore } from "../../../apps/trading/stores/market-store";
import { useWatchlistStore } from "../../../apps/trading/stores/watchlist-store";
import { usePortfolioStore } from "../../../apps/trading/stores/portfolio-store";

export class TradingCapabilityAdapter implements CapabilityAdapter {
  capabilityId = "trading";

  async provideContext(): Promise<CapabilityContext> {
    const symbol = useMarketStore.getState().symbol;
    const timeframe = useMarketStore.getState().timeframe;
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

    const items = [
      EvidenceBuilder.fromData("Symbol", symbol ?? "Unknown"),
      EvidenceBuilder.fromData("Query", query),
    ];

    return EvidenceBuilder.build({
      summary: `Trading knowledge for: ${query}`,
      items,
      reasoning: "Based on current trading context and available data.",
      confidence: 50,
      alternative: "Check additional data sources.",
    });
  }
}

export const tradingCapabilityAdapter = new TradingCapabilityAdapter();

