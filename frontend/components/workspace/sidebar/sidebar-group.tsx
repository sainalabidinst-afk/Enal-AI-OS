"use client";

import { type ReactNode } from "react";
import { cn } from "@/lib/utils";

interface SidebarGroupProps {
  label?: string;
  children: ReactNode;
  className?: string;
}

export function SidebarGroup({ label, children, className }: SidebarGroupProps) {
  return (
    <div className={cn("flex flex-col items-center gap-1", className)}>
      {label && (
        <span className="text-[10px] uppercase tracking-wide text-[var(--color-text-secondary)] mb-1">
          {label}
        </span>
      )}
      {children}
    </div>
  );
}
