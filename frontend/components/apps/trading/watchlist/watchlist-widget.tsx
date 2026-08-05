"use client";

import { Card, CardHeader, CardTitle } from "@/components/design-system/layout/card";

const WATCHLIST = [
  { symbol: "BTCUSDT", price: 104_245.30, change: 2.34 },
  { symbol: "ETHUSDT", price: 2_512.18, change: -0.87 },
  { symbol: "SOLUSDT", price: 178.42, change: 5.12 },
  { symbol: "ADAUSDT", price: 0.68, change: -1.24 },
  { symbol: "XRPUSDT", price: 2.14, change: 1.05 },
];

export function WatchlistWidget() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Watchlist</CardTitle>
      </CardHeader>
      <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] divide-y divide-[var(--color-border)]">
        {WATCHLIST.map((item) => (
          <div key={item.symbol} className="flex items-center justify-between px-4 py-3">
            <div>
              <p className="text-sm font-medium">{item.symbol}</p>
              <p className="text-xs text-[var(--color-secondary-500)]">Crypto</p>
            </div>
            <div className="text-right">
              <p className="text-sm font-medium">${item.price.toLocaleString()}</p>
              <p className={`text-xs ${item.change >= 0 ? "text-green-400" : "text-red-400"}`}>
                {item.change >= 0 ? "+" : ""}{item.change}%
              </p>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}
