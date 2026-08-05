"use client";

import { useState } from "react";
import { LineChart, BarChart3, Wallet, Sparkles, Newspaper, TrendingUp, TrendingDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Tabs, TabPanel } from "@/components/ui/tabs";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

type Tab = "chart" | "watchlist" | "portfolio" | "ai" | "news";

const TABS = [
  { id: "chart" as Tab, label: "Chart", icon: <LineChart className="h-3.5 w-3.5" /> },
  { id: "watchlist" as Tab, label: "Watchlist", icon: <BarChart3 className="h-3.5 w-3.5" /> },
  { id: "portfolio" as Tab, label: "Portfolio", icon: <Wallet className="h-3.5 w-3.5" /> },
  { id: "ai" as Tab, label: "AI Insight", icon: <Sparkles className="h-3.5 w-3.5" /> },
  { id: "news" as Tab, label: "News", icon: <Newspaper className="h-3.5 w-3.5" /> },
];

const WATCHLIST = [
  { symbol: "BTCUSDT", price: 104_245.30, change: 2.34 },
  { symbol: "ETHUSDT", price: 2_512.18, change: -0.87 },
  { symbol: "SOLUSDT", price: 178.42, change: 5.12 },
  { symbol: "ADAUSDT", price: 0.68, change: -1.24 },
  { symbol: "XRPUSDT", price: 2.14, change: 1.05 },
];

const NEWS = [
  { title: "Fed signals rate pause in upcoming meeting", time: "2h ago", source: "Reuters" },
  { title: "BTC ETF inflows hit record weekly high", time: "4h ago", source: "Bloomberg" },
  { title: "Tech earnings beat analyst estimates", time: "6h ago", source: "CNBC" },
  { title: "Ethereum upgrade successfully activated", time: "8h ago", source: "CoinDesk" },
];

export function TradingWorkspace() {
  const [tab, setTab] = useState<Tab>("chart");

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b border-[var(--color-border)] px-4 py-2">
        <h2 className="text-sm font-semibold">Trading Workspace</h2>
        <Tabs
          tabs={TABS}
          activeTab={tab}
          onChange={(id) => setTab(id as Tab)}
        />
      </div>

      <TabPanel>
        {tab === "chart" && (
          <div className="h-full flex flex-col">
            <div className="flex items-center justify-between px-4 py-2">
              <div>
                <h3 className="text-sm font-semibold">BTC/USDT</h3>
                <p className="text-xs text-[var(--color-text-secondary)]">1H • Binance</p>
              </div>
              <div className="text-right">
                <p className="text-lg font-semibold">104,245.30</p>
                <div className="flex items-center gap-1 text-green-400 text-xs">
                  <TrendingUp className="h-3 w-3" />
                  +2.34%
                </div>
              </div>
            </div>
            <div className="flex-1 rounded-xl border border-dashed border-[var(--color-border)] bg-[var(--color-bg-secondary)] m-4 flex items-center justify-center">
              <div className="text-center space-y-2">
                <p className="text-4xl">📈</p>
                <p className="text-sm text-[var(--color-text-secondary)]">TradingView-style chart will render here.</p>
                <p className="text-xs text-[var(--color-text-secondary)]">Wyckoff, SMC, Elliott, Volume Profile, Macro, Derivatives</p>
              </div>
            </div>
          </div>
        )}

        {tab === "watchlist" && (
          <div className="space-y-3">
            <div className="grid gap-2">
              {WATCHLIST.map((item) => (
                <Card key={item.symbol} padding={false}>
                  <div className="flex items-center justify-between px-4 py-3">
                    <div>
                      <p className="text-sm font-medium">{item.symbol}</p>
                      <p className="text-xs text-[var(--color-text-secondary)]">Crypto</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium">${item.price.toLocaleString()}</p>
                      <div className={`flex items-center gap-1 text-xs ${item.change >= 0 ? "text-green-400" : "text-red-400"}`}>
                        {item.change >= 0 ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                        {item.change >= 0 ? "+" : ""}{item.change}%
                      </div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {tab === "portfolio" && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <Card>
                <CardHeader>
                  <CardTitle>Total Value</CardTitle>
                </CardHeader>
                <p className="text-2xl font-bold">$124,593.00</p>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>24h Change</CardTitle>
                </CardHeader>
                <p className="text-2xl font-bold text-green-400">+$2,341.50</p>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Open Positions</CardTitle>
                </CardHeader>
                <p className="text-2xl font-bold">12</p>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Win Rate</CardTitle>
                </CardHeader>
                <p className="text-2xl font-bold">68%</p>
              </Card>
            </div>
          </div>
        )}

        {tab === "ai" && (
          <div className="space-y-4">
            <Card>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <Sparkles className="h-4 w-4 text-[var(--color-accent)]" />
                  <CardTitle>Market Sentiment</CardTitle>
                </div>
                <CardDescription>
                  Bullish momentum detected on the 4H timeframe. Key resistance at $52,400.
                </CardDescription>
              </CardHeader>
            </Card>
            <Card>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <TrendingUp className="h-4 w-4 text-[var(--color-accent)]" />
                  <CardTitle>Risk Alert</CardTitle>
                </div>
                <CardDescription>
                  Elevated IV percentile suggests upcoming volatility event.
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        )}

        {tab === "news" && (
          <div className="space-y-3">
            {NEWS.map((item, idx) => (
              <Card key={idx}>
                <div className="px-4 py-3">
                  <p className="text-sm font-medium">{item.title}</p>
                  <div className="flex items-center gap-2 mt-1">
                    <span className="text-xs text-[var(--color-text-secondary)]">{item.source}</span>
                    <span className="text-xs text-[var(--color-text-secondary)]">•</span>
                    <span className="text-xs text-[var(--color-text-secondary)]">{item.time}</span>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </TabPanel>
    </div>
  );
}
