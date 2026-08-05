"use client";

import { Card, CardHeader, CardTitle } from "@/components/ui/card";

export function PortfolioWidget() {
  return (
    <div className="space-y-3">
      <Card>
        <CardHeader>
          <CardTitle>Portfolio</CardTitle>
        </CardHeader>
        <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-xs text-[var(--color-text-secondary)]">Total Value</p>
              <p className="text-lg font-semibold">$124,593.00</p>
            </div>
            <div>
              <p className="text-xs text-[var(--color-text-secondary)]">24h Change</p>
              <p className="text-lg font-semibold text-green-400">+$2,341.50</p>
            </div>
            <div>
              <p className="text-xs text-[var(--color-text-secondary)]">Open Positions</p>
              <p className="text-lg font-semibold">12</p>
            </div>
            <div>
              <p className="text-xs text-[var(--color-text-secondary)]">Win Rate</p>
              <p className="text-lg font-semibold">68%</p>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}
