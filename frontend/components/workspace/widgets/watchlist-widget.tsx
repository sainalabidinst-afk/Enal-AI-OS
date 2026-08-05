"use client";

import { Card, CardHeader, CardTitle } from "@/components/ui/card";

export function WatchlistWidget() {
  return (
    <div className="space-y-3">
      <Card>
        <CardHeader>
          <CardTitle>Watchlist</CardTitle>
        </CardHeader>
        <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] divide-y divide-[var(--color-border)]">
          {["BTCUSDT", "ETHUSDT", "SOLUSDT", "ADAUSDT"].map((symbol) => (
            <div key={symbol} className="flex items-center justify-between px-4 py-3">
              <div>
                <p className="text-sm font-medium">{symbol}</p>
                <p className="text-xs text-[var(--color-text-secondary)]">Crypto</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-medium">{(Math.random() * 1000).toFixed(2)}</p>
                <p className={`text-xs ${Math.random() > 0.5 ? "text-green-400" : "text-red-400"}`}>
                  {(Math.random() * 5 - 2.5).toFixed(2)}%
                </p>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
