"use client";

import { type ReactNode } from "react";
import { cn } from "@/lib/utils";

export function Panel({
  children,
  className,
  bodyClassName,
}: {
  children: ReactNode;
  className?: string;
  bodyClassName?: string;
}) {
  return (
    <section
      className={cn(
        "flex min-w-0 flex-col rounded-xl border border-[var(--ecp-border)] bg-[var(--ecp-surface)]",
        className
      )}
    >
      {children}
    </section>
  );
}

export function PanelHeader({
  title,
  subtitle,
  actions,
  className,
}: {
  title: ReactNode;
  subtitle?: ReactNode;
  actions?: ReactNode;
  className?: string;
}) {
  return (
    <header
      className={cn(
        "flex items-center gap-3 border-b border-[var(--ecp-border)] px-4 py-3",
        className
      )}
    >
      <div className="min-w-0 flex-1">
        <h2 className="truncate text-sm font-semibold">{title}</h2>
        {subtitle && (
          <p className="mt-0.5 truncate text-[11px] text-[var(--ecp-text-dim)]">{subtitle}</p>
        )}
      </div>
      {actions && <div className="flex shrink-0 items-center gap-2">{actions}</div>}
    </header>
  );
}

export function PanelBody({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("min-w-0 flex-1 overflow-auto p-4", className)}>{children}</div>
  );
}

export function PageHeader({
  title,
  description,
  actions,
}: {
  title: string;
  description?: string;
  actions?: ReactNode;
}) {
  return (
    <div className="mb-4 flex flex-wrap items-end justify-between gap-3">
      <div>
        <h1 className="text-lg font-bold tracking-tight">{title}</h1>
        {description && (
          <p className="mt-1 text-xs text-[var(--ecp-text-muted)]">{description}</p>
        )}
      </div>
      {actions && <div className="flex items-center gap-2">{actions}</div>}
    </div>
  );
}