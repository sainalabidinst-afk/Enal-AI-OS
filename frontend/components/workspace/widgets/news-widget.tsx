"use client";

import { Card, CardHeader, CardTitle } from "@/components/ui/card";

export function NewsWidget() {
  return (
    <div className="space-y-3">
      <Card>
        <CardHeader>
          <CardTitle>News</CardTitle>
        </CardHeader>
        <div className="space-y-2">
          {[
            { title: "Fed signals rate pause", time: "2h ago", source: "Reuters" },
            { title: "BTC ETF inflows hit record", time: "4h ago", source: "Bloomberg" },
            { title: "Tech earnings beat estimates", time: "6h ago", source: "CNBC" },
          ].map((item, idx) => (
            <div key={idx} className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-3">
              <p className="text-sm font-medium">{item.title}</p>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-xs text-[var(--color-text-secondary)]">{item.source}</span>
                <span className="text-xs text-[var(--color-text-secondary)]">•</span>
                <span className="text-xs text-[var(--color-text-secondary)]">{item.time}</span>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
