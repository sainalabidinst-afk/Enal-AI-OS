import { type ReactNode } from "react";
import { cn } from "@/lib/utils";

interface EmptyStateProps {
  icon?: ReactNode;
  title: string;
  description?: string;
  action?: ReactNode;
  className?: string;
}

export function EmptyState({ icon, title, description, action, className }: EmptyStateProps) {
  return (
    <div className={cn("flex flex-col items-center justify-center py-12 px-4 text-center", className)}>
      {icon && <div className="mb-4 text-4xl text-[var(--color-secondary-400)]">{icon}</div>}
      <h3 className="text-sm font-medium text-[var(--color-foreground)] mb-1">{title}</h3>
      {description && <p className="text-xs text-[var(--color-secondary-500)] mb-4">{description}</p>}
      {action}
    </div>
  );
}
