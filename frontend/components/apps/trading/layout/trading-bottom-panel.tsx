"use client";

import { useState } from "react";
import { Tabs, TabPanel } from "@/components/design-system/navigation/tabs";

const TABS = ["Orders", "Positions", "History", "Logs"] as const;

export function TradingBottomPanel() {
  const [activeTab, setActiveTab] = useState<(typeof TABS)[number]>("Orders");

  return (
    <div className="flex h-48 flex-col border-t border-[var(--color-border)] bg-[var(--color-surface)]" aria-label="Trading bottom panel">
      <Tabs
        tabs={TABS.map((tab) => ({ id: tab, label: tab }))}
        activeTab={activeTab}
        onChange={(id) => setActiveTab(id as (typeof TABS)[number])}
      />
      <TabPanel>
        <div className="flex items-center justify-center h-full text-sm text-[var(--color-secondary-500)]">
          {activeTab} will appear here.
        </div>
      </TabPanel>
    </div>
  );
}
