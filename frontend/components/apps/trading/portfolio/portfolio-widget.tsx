"use client";

import { useEffect } from "react";
import { Card, CardHeader, CardTitle } from "@/components/design-system/layout/card";
import { usePortfolioStore } from "../stores/portfolio-store";

export function PortfolioWidget() {
  const portfolio = usePortfolioStore((s) => s.portfolio);
  const status = usePortfolioStore((s) => s.status);
  const fetchPortfolio = usePortfolioStore((s) => s.fetchPortfolio);

  useEffect(() => {
    fetchPortfolio();
  }, [fetchPortfolio]);

  if (status === "loading") {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Portfolio</CardTitle>
        </CardHeader>
        <div className="p-4 grid grid-cols-2 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-16 rounded-lg bg-[var(--color-bg-secondary)] animate-pulse" />
          ))}
        </div>
      </Card>
    );
  }

  if (status === "error" || !portfolio) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Portfolio</CardTitle>
        </CardHeader>
        <div className="p-4 text-sm text-[var(--color-secondary-500)]">
          No portfolio data available.
        </div>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Portfolio</CardTitle>
      </CardHeader>
      <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-xs text-[var(--color-secondary-500)]">Total Value</p>
            <p className="text-lg font-semibold">${portfolio.totalValue.toLocaleString()}</p>
          </div>
          <div>
            <p className="text-xs text-[var(--color-secondary-500)]">24h Change</p>
            <p className={`text-lg font-semibold ${portfolio.dayChange >= 0 ? "text-green-400" : "text-red-400"}`}>
              {portfolio.dayChange >= 0 ? "+" : ""}${portfolio.dayChange.toLocaleString()}
            </p>
          </div>
          <div>
            <p className="text-xs text-[var(--color-secondary-500)]">Open Positions</p>
            <p className="text-lg font-semibold">{portfolio.openPositions}</p>
          </div>
          <div>
            <p className="text-xs text-[var(--color-secondary-500)]">Win Rate</p>
            <p className="text-lg font-semibold">{portfolio.winRate.toFixed(1)}%</p>
          </div>
        </div>
      </div>
    </Card>
  );
}
