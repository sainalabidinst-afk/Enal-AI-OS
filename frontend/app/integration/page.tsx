"use client";

import { useState } from "react";
import { TradingAnalysisIntegration } from "@/components/integration/trading-analysis";
import { NetworkDesignReviewIntegration } from "@/components/integration/network-design-review";
import { SelfImprovementIntegration } from "@/components/integration/self-improvement";

type TabId = "trading" | "network" | "self-improvement";

const tabs: { id: TabId; label: string; description: string }[] = [
  {
    id: "trading",
    label: "Trading + Knowledge",
    description: "Integrated market analysis with knowledge base and reasoning",
  },
  {
    id: "network",
    label: "Network + Knowledge",
    description: "Network design review with knowledge graph and reasoning",
  },
  {
    id: "self-improvement",
    label: "Self Improvement",
    description: "Execution history → Knowledge update → Improvement proposal",
  },
];

export default function IntegrationPage() {
  const [activeTab, setActiveTab] = useState<TabId>("trading");

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
          Capability Integration
        </h1>
        <p className="mt-1 text-sm text-[var(--color-text-secondary)]">
          Cross-capability workflows that combine Trading, Network, Knowledge,
          and Self-Improvement capabilities.
        </p>
      </div>

      <div className="border-b border-[var(--color-border)]">
        <nav className="flex gap-4" aria-label="Integration workflows">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`border-b-2 px-1 py-2 text-sm font-medium transition-colors ${
                activeTab === tab.id
                  ? "border-[var(--color-accent)] text-[var(--color-text-primary)]"
                  : "border-transparent text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4">
        <p className="text-sm text-[var(--color-text-secondary)]">
          {tabs.find((t) => t.id === activeTab)?.description}
        </p>
      </div>

      <div>
        {activeTab === "trading" && <TradingAnalysisIntegration />}
        {activeTab === "network" && <NetworkDesignReviewIntegration />}
        {activeTab === "self-improvement" && <SelfImprovementIntegration />}
      </div>
    </div>
  );
}
