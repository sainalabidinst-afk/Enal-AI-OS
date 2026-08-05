"use client";

import { useState } from "react";
import { Search, Bell, Settings, Sun, Moon } from "lucide-react";
import { Button } from "@/components/design-system/primitives/button";
import { Input } from "@/components/design-system/primitives/input";

export function TradingHeader() {
  const [query, setQuery] = useState("");

  return (
    <header className="flex h-12 shrink-0 items-center justify-between border-b border-[var(--color-border)] bg-[var(--color-surface)] px-4">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <span className="text-lg">📈</span>
          <span className="text-sm font-semibold">Trading Terminal</span>
        </div>
        <div className="h-4 w-px bg-[var(--color-border)]" />
        <div className="flex items-center gap-2">
          <span className="text-xs text-[var(--color-secondary-500)]">Market:</span>
          <select className="text-xs border border-[var(--color-border)] rounded px-2 py-1 bg-[var(--color-surface)]">
            <option>Crypto</option>
            <option>Stocks</option>
            <option>Forex</option>
          </select>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[var(--color-secondary-500)]" />
          <Input
            type="text"
            placeholder="Symbol search..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="pl-9 h-8 w-64 text-xs"
          />
        </div>
        <div className="flex items-center gap-1">
          <Button variant="ghost" size="icon" className="h-8 w-8">
            <Bell className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="icon" className="h-8 w-8">
            <Sun className="h-4 w-4 hidden dark:block" />
            <Moon className="h-4 w-4 block dark:hidden" />
          </Button>
          <Button variant="ghost" size="icon" className="h-8 w-8">
            <Settings className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </header>
  );
}
