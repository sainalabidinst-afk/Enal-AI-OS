"use client";

import { Card, CardHeader, CardTitle, CardDescription } from "@/components/design-system/layout/card";
import { Badge } from "@/components/design-system/primitives/badge";
import { Sparkles, TrendingUp, AlertTriangle, CheckCircle } from "lucide-react";
import { useMarketStore } from "../stores/market-store";

export function AIPanel() {
  const symbol = useMarketStore((s) => s.symbol);

  return (
    <aside className="flex w-80 flex-col border-l border-[var(--color-border)] bg-[var(--color-surface)]" aria-label="AI Insight panel">
      <div className="border-b border-[var(--color-border)] px-4 py-3">
        <h2 className="text-sm font-semibold">AI Insight {symbol ? `• ${symbol}` : ""}</h2>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-[var(--color-primary-500)]" />
              <CardTitle>AI Summary</CardTitle>
            </div>
            <CardDescription>
              Bullish momentum detected on the 4H timeframe. Key resistance at $52,400.
            </CardDescription>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <TrendingUp className="h-4 w-4 text-[var(--color-primary-500)]" />
              <CardTitle>Recommendation</CardTitle>
            </div>
            <CardDescription>
              Wait for breakout confirmation above resistance before entering long position.
            </CardDescription>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <AlertTriangle className="h-4 w-4 text-[var(--color-warning-500)]" />
                <CardTitle>Risk</CardTitle>
              </div>
              <Badge variant="warning">Medium</Badge>
            </div>
            <CardDescription>
              Elevated IV percentile suggests upcoming volatility event.
            </CardDescription>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-[var(--color-success-500)]" />
                <CardTitle>Confidence</CardTitle>
              </div>
              <Badge variant="success">85%</Badge>
            </div>
            <CardDescription>
              Based on 7 knowledge domains: Wyckoff, SMC, Elliott, Volume Profile, Psychology, Macro, Derivatives.
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    </aside>
  );
}
