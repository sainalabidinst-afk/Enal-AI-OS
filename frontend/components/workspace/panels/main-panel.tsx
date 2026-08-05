"use client";

import { type ReactNode } from "react";
import { cn } from "@/lib/utils";

interface MainPanelProps {
  app?: string;
  children: ReactNode;
  className?: string;
}

export function MainPanel({ app, children, className }: MainPanelProps) {
  return (
    <main className={cn("flex-1 overflow-hidden bg-[var(--color-bg-primary)]", className)}>
      {children}
    </main>
  );
}
