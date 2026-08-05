"use client";

import { Card, CardHeader, CardTitle } from "@/components/design-system/layout/card";

export function PortfolioWidget() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Portfolio</CardTitle>
      </CardHeader>
      <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-xs text-[var(--color-secondary-500)]">Total Value</p>
            <p className="text-lg font-semibold">$124,593.00</p>
          </div>
          <div>
            <p className="text-xs text-[var(--color-secondary-500)]">24h Change</p>
            <p className="text-lg font-semibold text-green-400">+$2,341.50</p>
          </div>
          <div>
            <p className="text-xs text-[var(--color-secondary-500)]">Open Positions</p>
            <p className="text-lg font-semibold">12</p>
          </div>
          <div>
            <p className="text-xs text-[var(--color-secondary-500)]">Win Rate</p>
            <p className="text-lg font-semibold">68%</p>
          </div>
        </div>
      </div>
    </Card>
  );
}
