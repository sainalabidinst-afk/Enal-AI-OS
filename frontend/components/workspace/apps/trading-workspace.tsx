"use client";

import { useEffect } from "react";
import { TradingLayout } from "@/components/apps/trading/layout/trading-layout";
import { ChartPlaceholder } from "@/components/apps/trading/chart/chart-placeholder";
import { WatchlistWidget } from "@/components/apps/trading/watchlist/watchlist-widget";
import { PortfolioWidget } from "@/components/apps/trading/portfolio/portfolio-widget";
import { MarketCard } from "@/components/apps/trading/widgets/market-card";
import { NewsCard } from "@/components/apps/trading/news/news-card";
import { AISummaryCard } from "@/components/apps/trading/ai/ai-summary-card";
import { EmptyState } from "@/components/apps/trading/widgets/empty-state";
import { useTradingRealtime } from "@/components/apps/trading/hooks/use-market-data";
import { useProviderInitialization } from "@/components/apps/trading/hooks/use-provider-init";

export function TradingWorkspace() {
  useProviderInitialization();
  useTradingRealtime();

  return (
    <TradingLayout>
      <div className="space-y-4">
        <MarketCard />
        <ChartPlaceholder />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <WatchlistWidget />
          <PortfolioWidget />
          <div className="space-y-4">
            <AISummaryCard />
            <NewsCard />
          </div>
        </div>
        <EmptyState />
      </div>
    </TradingLayout>
  );
}
