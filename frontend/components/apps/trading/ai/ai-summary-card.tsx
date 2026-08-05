"use client";

import { Card, CardHeader, CardTitle, CardDescription } from "@/components/design-system/layout/card";
import { Badge } from "@/components/design-system/primitives/badge";
import { Sparkles, CheckCircle, AlertTriangle } from "lucide-react";

export function AISummaryCard() {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="h-4 w-4 text-[var(--color-primary-500)]" />
            <CardTitle>AI Summary</CardTitle>
          </div>
          <Badge variant="success">85%</Badge>
        </div>
        <CardDescription>
          Bullish momentum detected on the 4H timeframe. Key resistance at $52,400.
        </CardDescription>
      </CardHeader>
      <div className="px-4 pb-4 space-y-2">
        <div className="flex items-start gap-2">
          <CheckCircle className="h-4 w-4 text-green-400 mt-0.5" />
          <div>
            <p className="text-sm font-medium">Recommendation</p>
            <p className="text-xs text-[var(--color-secondary-500)]">Wait for breakout confirmation above resistance.</p>
          </div>
        </div>
        <div className="flex items-start gap-2">
          <AlertTriangle className="h-4 w-4 text-yellow-400 mt-0.5" />
          <div>
            <p className="text-sm font-medium">Risk</p>
            <p className="text-xs text-[var(--color-secondary-500)]">Elevated IV percentile suggests upcoming volatility.</p>
          </div>
        </div>
      </div>
    </Card>
  );
}
