"use client";

import { Card, CardHeader, CardTitle } from "@/components/ui/card";

export function TradingChart() {
  return (
    <div className="flex h-full flex-col">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Chart</CardTitle>
          <span className="text-xs text-[var(--color-text-secondary)]">Symbol: BTCUSDT</span>
        </div>
      </CardHeader>
      <div className="flex-1 rounded-xl border border-dashed border-[var(--color-border)] bg-[var(--color-bg-secondary)] m-4 flex items-center justify-center">
        <div className="text-center space-y-2">
          <p className="text-2xl">📈</p>
          <p className="text-sm text-[var(--color-text-secondary)]">TradingView-style chart will render here.</p>
        </div>
      </div>
    </div>
  );
}
