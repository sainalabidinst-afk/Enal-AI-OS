"use client";

import { useState } from "react";
import { FileCode, Terminal, GitBranch, Bot, Bug } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

type Tab = "explorer" | "editor" | "ai" | "terminal" | "git";

const TABS = [
  { id: "explorer" as Tab, label: "Explorer", icon: FileCode },
  { id: "editor" as Tab, label: "Editor", icon: FileCode },
  { id: "ai" as Tab, label: "AI", icon: Bot },
  { id: "terminal" as Tab, label: "Terminal", icon: Terminal },
  { id: "git" as Tab, label: "Git", icon: GitBranch },
];

export function CodeWorkspace() {
  const [tab, setTab] = useState<Tab>("editor");

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center gap-2 border-b border-[var(--color-border)] px-4 py-2">
        <h2 className="text-sm font-semibold">Code Workspace</h2>
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
              {tab === "explorer" && "File explorer with project tree."}
              {tab === "editor" && "Code editor with syntax highlighting and AI assistance."}
              {tab === "ai" && "AI-powered code review and suggestions."}
              {tab === "terminal" && "Integrated terminal for command-line operations."}
              {tab === "git" && "Git integration for version control."}
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    </div>
  );
}
