"use client";

import { memo, useEffect } from "react";
import { Card, CardHeader, CardTitle } from "@/components/design-system/layout/card";
import { useWatchlistStore } from "../stores/watchlist-store";

const WatchlistWidgetInner = () => {
  const items = useWatchlistStore((s) => s.items);
  const status = useWatchlistStore((s) => s.status);
  const fetchWatchlist = useWatchlistStore((s) => s.fetchWatchlist);

  useEffect(() => {
    fetchWatchlist();
  }, [fetchWatchlist]);

  if (status === "loading") {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Watchlist</CardTitle>
        </CardHeader>
        <div className="p-4 space-y-2">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="h-12 rounded-lg bg-[var(--color-bg-secondary)] animate-pulse" />
          ))}
        </div>
      </Card>
    );
  }

  if (status === "error" || items.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Watchlist</CardTitle>
        </CardHeader>
        <div className="p-4 text-sm text-[var(--color-secondary-500)]">
          No watchlist data available.
        </div>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Watchlist</CardTitle>
      </CardHeader>
      <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] divide-y divide-[var(--color-border)]">
        {items.map((item) => (
          <div key={item.symbol} className="flex items-center justify-between px-4 py-3">
            <div>
              <p className="text-sm font-medium">{item.symbol}</p>
              <p className="text-xs text-[var(--color-secondary-500)]">{item.name}</p>
            </div>
            <div className="text-right">
              <p className="text-sm font-medium">${item.price.toLocaleString()}</p>
              <p className={`text-xs ${item.change >= 0 ? "text-green-400" : "text-red-400"}`}>
                {item.change >= 0 ? "+" : ""}{item.changePercent.toFixed(2)}%
              </p>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};

export const WatchlistWidget = memo(WatchlistWidgetInner);
WatchlistWidget.displayName = "WatchlistWidget";
