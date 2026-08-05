"use client";

import { useEffect } from "react";
import { Card, CardHeader, CardTitle } from "@/components/design-system/layout/card";
import { useNewsStore } from "../stores/news-store";

export function NewsCard() {
  const items = useNewsStore((s) => s.items);
  const status = useNewsStore((s) => s.status);
  const fetchNews = useNewsStore((s) => s.fetchNews);

  useEffect(() => {
    fetchNews();
  }, [fetchNews]);

  if (status === "loading") {
    return (
      <Card>
        <CardHeader>
          <CardTitle>News</CardTitle>
        </CardHeader>
        <div className="p-4 space-y-2">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-16 rounded-lg bg-[var(--color-bg-secondary)] animate-pulse" />
          ))}
        </div>
      </Card>
    );
  }

  if (status === "error" || items.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>News</CardTitle>
        </CardHeader>
        <div className="p-4 text-sm text-[var(--color-secondary-500)]">
          No news available.
        </div>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>News</CardTitle>
      </CardHeader>
      <div className="space-y-2">
        {items.slice(0, 5).map((item) => (
          <div key={item.id} className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-3">
            <p className="text-sm font-medium">{item.title}</p>
            <div className="flex items-center gap-2 mt-1">
              <span className="text-xs text-[var(--color-secondary-500)]">{item.source}</span>
              <span className="text-xs text-[var(--color-secondary-500)]">•</span>
              <span className="text-xs text-[var(--color-secondary-500)]">
                {new Date(item.publishedAt).toLocaleTimeString()}
              </span>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}
