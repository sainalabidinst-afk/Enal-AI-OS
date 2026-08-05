"use client";

import { Card, CardHeader, CardTitle, CardDescription } from "@/components/design-system/layout/card";

export function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-20 px-4 text-center">
      <div className="text-6xl mb-4">📈</div>
      <Card>
        <CardHeader>
          <CardTitle>No Symbol Selected</CardTitle>
          <CardDescription>Choose a symbol from the watchlist to begin analysis.</CardDescription>
        </CardHeader>
      </Card>
    </div>
  );
}
