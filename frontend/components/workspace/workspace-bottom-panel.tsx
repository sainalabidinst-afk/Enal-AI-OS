"use client";

import { useState } from "react";
import { ChevronUp } from "lucide-react";
import { Tabs, TabPanel } from "@/components/ui/tabs";

const TABS = ["Logs", "Problems", "Output", "Debug Console"] as const;

export function WorkspaceBottomPanel() {
  const [activeTab, setActiveTab] = useState<(typeof TABS)[number]>("Logs");

  return (
    <div className="flex h-48 flex-col border-t border-[var(--color-border)] bg-[var(--color-bg-secondary)]">
      <Tabs
        tabs={TABS.map((tab) => ({ id: tab, label: tab }))}
        activeTab={activeTab}
        onChange={(id) => setActiveTab(id as (typeof TABS)[number])}
      />
      <TabPanel>
        <pre className="text-xs text-[var(--color-text-secondary)] whitespace-pre-wrap">
          {activeTab === "Logs" && "[workspace] Workspace engine initialized.\n[workspace] Ready."}
          {activeTab === "Problems" && "No problems detected."}
          {activeTab === "Output" && "Workspace output will appear here."}
          {activeTab === "Debug Console" && "> _"}
        </pre>
      </TabPanel>
    </div>
  );
}
