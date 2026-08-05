"use client";

import { useTradingUIStore } from "../stores/ui-store";
import { Tabs, TabPanel } from "@/components/design-system/navigation/tabs";
import { TradingHeader } from "./trading-header";
import { TradingSidebar } from "./trading-sidebar";
import { AIPanel } from "../ai/ai-panel";
import { TradingBottomPanel } from "./trading-bottom-panel";

export function TradingLayout({ children }: { children: React.ReactNode }) {
  const activeTab = useTradingUIStore((s) => s.activeTab);
  const setActiveTab = useTradingUIStore((s) => s.setActiveTab);

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
            <AIPanel />
          </div>
          <TradingBottomPanel />
        </div>
      </div>
    </div>
  );
