"use client";

import { type ReactNode } from "react";
import { cn } from "@/lib/utils";

export interface TabItem {
  id: string;
  label: string;
  icon?: ReactNode;
  badge?: ReactNode;
}

export function ConsoleTabs({
  tabs,
  active,
  onChange,
  className,
}: {
  tabs: TabItem[];
  active: string;
  onChange: (id: string) => void;
  className?: string;
}) {
  return (
    <div
      role="tablist"
      className={cn(
        "flex items-center gap-1 overflow-x-auto border-b border-[var(--ecp-border)]",
        className
      )}
    >
      {tabs.map((tab) => {
        const selected = tab.id === active;
        return (
          <button
            key={tab.id}
            role="tab"
            aria-selected={selected}
            type="button"
            onClick={() => onChange(tab.id)}
            className={cn(
              "flex shrink-0 items-center gap-1.5 border-b-2 px-3 py-2.5 text-xs font-medium transition-colors",
              selected
                ? "border-[var(--ecp-gov)] text-[var(--ecp-text)]"
                : "border-transparent text-[var(--ecp-text-muted)] hover:text-[var(--ecp-text)]"
            )}
          >
            {tab.icon}
            {tab.label}
            {tab.badge}
          </button>
        );
      })}
    </div>
  );
}