import { type ReactNode } from "react";
import { cn } from "@/lib/utils";

interface PanelProps {
  children: ReactNode;
  className?: string;
  collapsible?: boolean;
  collapsed?: boolean;
  onToggle?: () => void;
}

export function Panel({ children, className, collapsible, collapsed, onToggle }: PanelProps) {
  return (
    <div className={cn("rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)]", className)}>
      {collapsible && (
        <button
          onClick={onToggle}
          className="w-full px-4 py-2 text-xs font-medium text-[var(--color-secondary-500)] hover:text-[var(--color-foreground)] transition-colors"
        >
          {collapsed ? "Expand" : "Collapse"}
        </button>
      )}
      {!collapsed && <div className="p-4">{children}</div>}
    </div>
  );
}
