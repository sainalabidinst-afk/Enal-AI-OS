"use client";

import { type ReactNode } from "react";
import { cn } from "@/lib/utils";

interface TopbarProps {
  children: ReactNode;
  className?: string;
}

export function Topbar({ children, className }: TopbarProps) {
  return (
    <header
      className={cn(
        "flex h-12 shrink-0 items-center justify-between border-b border-[var(--color-border)] bg-[var(--color-surface)] px-4",
        className
      )}
    >
      {children}
    </header>
  );
}

interface TopbarLeftProps {
  children: ReactNode;
  className?: string;
}

export function TopbarLeft({ children, className }: TopbarLeftProps) {
  return <div className={cn("flex items-center gap-4", className)}>{children}</div>;
}

interface TopbarRightProps {
  children: ReactNode;
  className?: string;
}

export function TopbarRight({ children, className }: TopbarRightProps) {
  return <div className={cn("flex items-center gap-2", className)}>{children}</div>;
}
