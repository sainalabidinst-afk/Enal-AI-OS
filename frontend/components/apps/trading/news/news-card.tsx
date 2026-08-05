"use client";

import { Card, CardHeader, CardTitle } from "@/components/design-system/layout/card";

const NEWS = [
  { title: "Fed signals rate pause in upcoming meeting", time: "2h ago", source: "Reuters" },
  { title: "BTC ETF inflows hit record weekly high", time: "4h ago", source: "Bloomberg" },
  { title: "Tech earnings beat analyst estimates", time: "6h ago", source: "CNBC" },
];

export function NewsCard() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>News</CardTitle>
      </CardHeader>
      <div className="space-y-2">
        {NEWS.map((item, idx) => (
          <div key={idx} className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-3">
            <p className="text-sm font-medium">{item.title}</p>
            <div className="flex items-center gap-2 mt-1">
              <span className="text-xs text-[var(--color-secondary-500)]">{item.source}</span>
              <span className="text-xs text-[var(--color-secondary-500)]">•</span>
              <span className="text-xs text-[var(--color-secondary-500)]">{item.time}</span>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}
