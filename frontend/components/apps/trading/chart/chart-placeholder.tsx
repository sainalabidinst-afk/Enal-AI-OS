"use client";

import { Button } from "@/components/design-system/primitives/button";

export function ChartPlaceholder() {
  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b border-[var(--color-border)] px-4 py-2">
        <div className="flex items-center gap-4">
          <div>
            <h3 className="text-sm font-semibold">BTC/USDT</h3>
            <p className="text-xs text-[var(--color-secondary-500)]">1H • Binance</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="secondary" size="sm">Timeframe</Button>
          <Button variant="secondary" size="sm">Indicators</Button>
          <Button variant="secondary" size="sm">Drawing</Button>
        </div>
      </div>
      <div className="flex-1 rounded-xl border border-dashed border-[var(--color-border)] bg-[var(--color-bg-secondary)] m-4 flex items-center justify-center">
        <div className="text-center space-y-2">
          <p className="text-4xl">📈</p>
          <p className="text-sm text-[var(--color-text-secondary)]">TradingView-style chart will render here.</p>
          <p className="text-xs text-[var(--color-text-secondary)]">Wyckoff, SMC, Elliott, Volume Profile, Macro, Derivatives</p>
        </div>
      </div>
    </div>
  );
}
