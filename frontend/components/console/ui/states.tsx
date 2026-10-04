"use client";

import { type ReactNode } from "react";
import { AlertTriangle, Inbox, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

export function LoadingBlock({ label = "Loading" }: { label?: string }) {
  return (
    <div className="grid min-h-[140px] place-items-center gap-2 text-[var(--ecp-text-dim)]">
      <Loader2 className="h-4 w-4 animate-spin" />
      <span className="text-xs">{label}…</span>
    </div>
  );
}

export function ErrorBlock({
  message,
  onRetry,
}: {
  message: string;
  onRetry?: () => void;
}) {
  return (
    <div className="flex min-h-[140px] flex-col items-center justify-center gap-2 rounded-lg border border-[var(--ecp-danger)]/40 bg-[var(--ecp-danger-soft)] px-4 py-6 text-center">
      <AlertTriangle className="h-5 w-5 text-[var(--ecp-danger)]" />
      <p className="text-xs text-[var(--ecp-danger)]">{message}</p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="rounded-md border border-[var(--ecp-danger)]/50 px-2.5 py-1 text-[11px] text-[var(--ecp-danger)] transition-colors hover:bg-[var(--ecp-danger-soft)]"
        >
          Retry
        </button>
      )}
    </div>
  );
}

export function EmptyBlock({
  title,
  hint,
  action,
}: {
  title: string;
  hint?: string;
  action?: ReactNode;
}) {
  return (
    <div className="flex min-h-[140px] flex-col items-center justify-center gap-2 rounded-lg border border-dashed border-[var(--ecp-border)] px-4 py-8 text-center">
      <Inbox className="h-5 w-5 text-[var(--ecp-text-dim)]" />
      <p className="text-sm text-[var(--ecp-text-muted)]">{title}</p>
      {hint && <p className="max-w-sm text-[11px] text-[var(--ecp-text-dim)]">{hint}</p>}
      {action}
    </div>
  );
}

export type ResourceViewProps<T> = {
  status: "idle" | "loading" | "success" | "error";
  error: string | null;
  data: T | null;
  isEmpty?: (data: T) => boolean;
  loadingLabel?: string;
  emptyTitle?: string;
  emptyHint?: string;
  onRetry?: () => void;
  children: (data: T) => ReactNode;
};

export function ResourceView<T>({
  status,
  error,
  data,
  isEmpty,
  loadingLabel,
  emptyTitle = "No data yet",
  emptyHint,
  onRetry,
  children,
}: ResourceViewProps<T>) {
  if (status === "error" && error) {
    return <ErrorBlock message={error} onRetry={onRetry} />;
  }
  if (!data || status === "loading" || status === "idle") {
    return <LoadingBlock label={loadingLabel} />;
  }
  if (isEmpty?.(data)) {
    return <EmptyBlock title={emptyTitle} hint={emptyHint} />;
  }
  return <>{children(data)}</>;
}

export function SkeletonRows({ rows = 4 }: { rows?: number }) {
  return (
    <div className="space-y-2 p-4">
      {Array.from({ length: rows }).map((_, index) => (
        <div
          key={index}
          className="h-8 animate-pulse rounded-md bg-[var(--ecp-surface-2)]"
        />
      ))}
    </div>
  );
}

export function Pill({
  children,
  tone = "neutral",
  className,
}: {
  children: ReactNode;
  tone?: "neutral" | "good" | "warn" | "bad" | "info";
  className?: string;
}) {
  const tones: Record<string, string> = {
    neutral:
      "border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] text-[var(--ecp-text-muted)]",
    good: "border-[var(--ecp-success)]/40 bg-[var(--ecp-success-soft)] text-[var(--ecp-success)]",
    warn: "border-[var(--ecp-alert)]/40 bg-[var(--ecp-alert-soft)] text-[var(--ecp-alert)]",
    bad: "border-[var(--ecp-danger)]/40 bg-[var(--ecp-danger-soft)] text-[var(--ecp-danger)]",
    info: "border-[var(--ecp-sky)]/40 bg-[var(--ecp-sky-soft)] text-[var(--ecp-sky)]",
  };
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide",
        tones[tone],
        className
      )}
    >
      {children}
    </span>
  );
}