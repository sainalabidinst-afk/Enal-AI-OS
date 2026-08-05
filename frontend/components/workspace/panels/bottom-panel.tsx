"use client";

import { useState } from "react";
import { Tabs, TabPanel } from "@/components/design-system/navigation/tabs";

const TABS = ["Logs", "Problems", "Output", "Debug Console"] as const;

export function BottomPanel() {
  const [activeTab, setActiveTab] = useState<(typeof TABS)[number]>("Logs");

  return (
    <div className="flex h-48 flex-col border-t border-[var(--color-border)] bg-[var(--color-surface)]" aria-label="Bottom panel">
      <Tabs
        tabs={TABS.map((tab) => ({ id: tab, label: tab }))}
        activeTab={activeTab}
        onChange={(id) => setActiveTab(id as (typeof TABS)[number])}
      />
      <TabPanel>
        <pre className="text-xs text-[var(--color-secondary-500)] whitespace-pre-wrap">
          {activeTab === "Logs" && "[workspace] Workspace engine initialized.\n[workspace] Ready."}
          {activeTab === "Problems" && "No problems detected."}
          {activeTab === "Output" && "Workspace output will appear here."}
          {activeTab === "Debug Console" && "> _"}
        </pre>
      </TabPanel>
    </div>
  );
}
