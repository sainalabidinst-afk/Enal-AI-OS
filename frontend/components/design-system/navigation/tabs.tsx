"use client";

import { type ReactNode, type ReactElement, useState } from "react";
import { cn } from "@/lib/utils";

interface TabsProps {
  tabs: { id: string; label: string; icon?: ReactElement }[];
  activeTab: string;
  onChange: (id: string) => void;
  className?: string;
}

export function Tabs({ tabs, activeTab, onChange, className }: TabsProps) {
  return (
    <div className={cn("flex items-center gap-1 border-b border-[var(--color-border)]", className)}>
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onChange(tab.id)}
          className={cn(
            "flex items-center gap-1.5 px-4 py-2.5 text-sm transition-colors",
            activeTab === tab.id
              ? "text-[var(--color-foreground)] border-b-2 border-[var(--color-primary-500)]"
              : "text-[var(--color-secondary-500)] hover:text-[var(--color-foreground)]"
          )}
        >
          {tab.icon && <span className="h-4 w-4">{tab.icon}</span>}
          {tab.label}
        </button>
      ))}
    </div>
  );
}

interface TabPanelProps {
  children: ReactNode;
  className?: string;
}

export function TabPanel({ children, className }: TabPanelProps) {
  return <div className={cn("flex-1 overflow-y-auto", className)}>{children}</div>;
}
