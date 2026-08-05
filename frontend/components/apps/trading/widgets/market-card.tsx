"use client";

import { Card, CardHeader, CardTitle, CardDescription } from "@/components/design-system/layout/card";
import { Badge } from "@/components/design-system/primitives/badge";

export function MarketCard() {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>BTC/USDT</CardTitle>
          <Badge variant="success">Live</Badge>
        </div>
        <CardDescription>Binance • 1H</CardDescription>
      </CardHeader>
      <div className="px-4 pb-4">
        <p className="text-2xl font-bold">$104,245.30</p>
        <p className="text-xs text-green-400 mt-1">+2.34% (24h)</p>
      </div>
    </Card>
  );
}
