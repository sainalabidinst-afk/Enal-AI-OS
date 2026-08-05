"use client";

import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

export function AIInsightWidget() {
  return (
    <div className="space-y-3">
      <Card>
        <CardHeader>
          <CardTitle>AI Insight</CardTitle>
        </CardHeader>
        <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4 space-y-3">
          <div className="flex items-start gap-2">
            <span className="text-lg">🧠</span>
            <div>
              <p className="text-sm font-medium">Market Sentiment</p>
              <p className="text-xs text-[var(--color-text-secondary)] mt-1">
                Bullish momentum detected on the 4H timeframe. Key resistance at $52,400.
              </p>
            </div>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-lg">⚠️</span>
            <div>
              <p className="text-sm font-medium">Risk Alert</p>
              <p className="text-xs text-[var(--color-text-secondary)] mt-1">
                Elevated IV percentile suggests upcoming volatility event.
              </p>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}
