"use client";

import { useState } from "react";
import { Network, Settings, ShieldCheck, Rocket, FileSearch } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

type Tab = "topology" | "config" | "analyzer" | "deploy" | "audit";

const TABS = [
  { id: "topology" as Tab, label: "Topology", icon: Network },
  { id: "config" as Tab, label: "Configuration", icon: Settings },
  { id: "analyzer" as Tab, label: "Analyzer", icon: ShieldCheck },
  { id: "deploy" as Tab, label: "Deploy", icon: Rocket },
  { id: "audit" as Tab, label: "Audit Logs", icon: FileSearch },
];

export function NetworkWorkspace() {
  const [tab, setTab] = useState<Tab>("topology");

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center gap-2 border-b border-[var(--color-border)] px-4 py-2">
        <h2 className="text-sm font-semibold">Network Workspace</h2>
        <div className="ml-auto flex items-center gap-1">
          {TABS.map((item) => {
            const Icon = item.icon;
            return (
              <Button
                key={item.id}
                variant={tab === item.id ? "primary" : "ghost"}
                size="sm"
                onClick={() => setTab(item.id)}
              >
                <Icon className="h-3.5 w-3.5" />
                {item.label}
              </Button>
            );
          })}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        <Card>
          <CardHeader>
            <CardTitle>{TABS.find((t) => t.id === tab)?.label}</CardTitle>
            <CardDescription>
              {tab === "topology" && "Network topology visualization will render here."}
              {tab === "config" && "Configuration editor for network devices."}
              {tab === "analyzer" && "Security and performance analyzer results."}
              {tab === "deploy" && "Deployment pipeline for network changes."}
              {tab === "audit" && "Audit trail and change history."}
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    </div>
  );
}
