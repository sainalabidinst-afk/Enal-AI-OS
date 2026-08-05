"use client";

import { useTradingUIStore } from "../stores/ui-store";
import { useConnectionStore } from "../connectivity/manager/connection-store";
import { Tabs, TabPanel } from "@/components/design-system/navigation/tabs";
import { Badge } from "@/components/design-system/primitives/badge";
import { TradingHeader } from "./trading-header";
import { TradingSidebar } from "./trading-sidebar";
import { AIWorkspacePanel } from "@/components/workspace/ai/ai-workspace-panel";
import { TradingBottomPanel } from "./trading-bottom-panel";

const STATUS_COLORS: Record<string, "success" | "warning" | "danger" | "secondary"> = {
  connected: "success",
  connecting: "warning",
  reconnecting: "warning",
  disconnected: "danger",
  error: "danger",
  idle: "secondary",
};

export function TradingLayout({ children }: { children: React.ReactNode }) {
  const activeTab = useTradingUIStore((s) => s.activeTab);
  const setActiveTab = useTradingUIStore((s) => s.setActiveTab);
  const status = useConnectionStore((s) => s.status);
  const providerName = useConnectionStore((s) => s.providerName);

  const tabs = [
    { id: "dashboard" as const, label: "Dashboard" },
    { id: "watchlist" as const, label: "Watchlist" },
    { id: "portfolio" as const, label: "Portfolio" },
    { id: "scanner" as const, label: "Scanner" },
    { id: "alerts" as const, label: "Alerts" },
    { id: "news" as const, label: "News" },
    { id: "research" as const, label: "Research" },
    { id: "settings" as const, label: "Settings" },
  ];

  return (
    <div className="flex h-full flex-col">
      <TradingHeader />
      <div className="flex flex-1 overflow-hidden">
        <TradingSidebar />
        <div className="flex flex-1 flex-col overflow-hidden">
          <div className="flex flex-1 overflow-hidden">
            <div className="flex flex-1 flex-col overflow-hidden">
              <Tabs tabs={tabs} activeTab={activeTab} onChange={(id) => setActiveTab(id as any)} />
              <TabPanel>
                <div className="flex-1 overflow-y-auto p-4">
                  {children}
                </div>
              </TabPanel>
            </div>
            <AIWorkspacePanel capabilityId="trading" />
          </div>
          <TradingBottomPanel />
        </div>
      </div>
      <div className="flex h-6 shrink-0 items-center justify-between border-t border-[var(--color-border)] bg-[var(--color-surface)] px-3">
        <div className="flex items-center gap-2">
          <Badge variant={STATUS_COLORS[status] ?? "secondary"}>{status}</Badge>
          {providerName && (
            <span className="text-xs text-[var(--color-secondary-500)]">{providerName}</span>
          )}
        </div>
        <div className="text-xs text-[var(--color-secondary-500)]">Enal AI OS • Trading Terminal</div>
      </div>
    </div>
  );
}
