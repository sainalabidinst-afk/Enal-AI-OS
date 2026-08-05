"use client";

import { useTradingUIStore } from "../stores/ui-store";
import { Button } from "@/components/design-system/primitives/button";
import { cn } from "@/lib/utils";

const MENU_ITEMS = [
  { id: "dashboard" as const, label: "Dashboard", icon: "📊" },
  { id: "watchlist" as const, label: "Watchlist", icon: "👁️" },
  { id: "portfolio" as const, label: "Portfolio", icon: "💼" },
  { id: "scanner" as const, label: "Scanner", icon: "🔍" },
  { id: "alerts" as const, label: "Alerts", icon: "🔔" },
  { id: "news" as const, label: "News", icon: "📰" },
  { id: "research" as const, label: "Research", icon: "📑" },
  { id: "settings" as const, label: "Settings", icon: "⚙️" },
];

export function TradingSidebar() {
  const activeTab = useTradingUIStore((s) => s.activeTab);
  const setActiveTab = useTradingUIStore((s) => s.setActiveTab);

  return (
    <aside className="flex w-48 flex-col border-r border-[var(--color-border)] bg-[var(--color-surface)]" aria-label="Trading sidebar">
      <div className="p-2 border-b border-[var(--color-border)]">
        <span className="text-xs font-medium text-[var(--color-secondary-500)] uppercase tracking-wide">
          Trading
        </span>
      </div>
      <nav className="flex-1 overflow-y-auto p-2 space-y-1">
        {MENU_ITEMS.map((item) => {
          const isActive = activeTab === item.id;
          return (
            <Button
              key={item.id}
              variant="ghost"
              onClick={() => setActiveTab(item.id)}
              className={cn(
                "w-full justify-start gap-2",
                isActive
                  ? "bg-[var(--color-primary-500)] text-white hover:bg-[var(--color-primary-500)] hover:text-white"
                  : "text-[var(--color-secondary-600)] hover:text-[var(--color-foreground)] hover:bg-[var(--color-secondary-100)]"
              )}
            >
              <span>{item.icon}</span>
              <span className="text-sm">{item.label}</span>
            </Button>
          );
        })}
      </nav>
    </aside>
  );
}
