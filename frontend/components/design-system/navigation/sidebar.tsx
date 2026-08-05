"use client";

import { type ReactNode } from "react";
import { cn } from "@/lib/utils";

interface SidebarProps {
  children: ReactNode;
  collapsed?: boolean;
  className?: string;
}

export function Sidebar({ children, collapsed, className }: SidebarProps) {
  return (
    <aside
      className={cn(
        "flex flex-col border-r border-[var(--color-border)] bg-[var(--color-surface)] transition-all duration-200",
        collapsed ? "w-14" : "w-56",
        className
      )}
    >
      {children}
    </aside>
  );
}

interface SidebarItemProps {
  icon?: ReactNode;
  label: string;
  active?: boolean;
  disabled?: boolean;
  onClick?: () => void;
  className?: string;
}

export function SidebarItem({ icon, label, active, disabled, onClick, className }: SidebarItemProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={cn(
        "flex items-center gap-3 w-full px-3 py-2 text-sm rounded-lg transition-colors",
        active
          ? "bg-[var(--color-primary-500)] text-white"
          : "text-[var(--color-secondary-600)] hover:text-[var(--color-foreground)] hover:bg-[var(--color-secondary-100)]",
        disabled && "opacity-50 pointer-events-none",
        className
      )}
    >
      {icon && <span className="h-4 w-4">{icon}</span>}
      <span className={cn(active ? "font-medium" : "")}>{label}</span>
    </button>
  );
}
