"use client";

import { type ReactNode } from "react";
import { cn } from "@/lib/utils";

export type MetricTone = "gov" | "sky" | "blue" | "alert" | "danger" | "neutral";

const TONE_STYLES: Record<MetricTone, { value: string; rail: string; glow: string }> = {
  gov: {
    value: "text-[var(--ecp-gov)]",
    rail: "from-[var(--ecp-gov)]",
    glow: "rgba(45, 212, 191, 0.22)",
  },
  sky: {
    value: "text-[var(--ecp-sky)]",
    rail: "from-[var(--ecp-sky)]",
    glow: "rgba(56, 189, 248, 0.2)",
  },
  blue: {
    value: "text-[var(--ecp-blue)]",
    rail: "from-[var(--ecp-blue)]",
    glow: "rgba(59, 130, 246, 0.2)",
  },
  alert: {
    value: "text-[var(--ecp-alert)]",
    rail: "from-[var(--ecp-alert)]",
    glow: "rgba(245, 158, 11, 0.22)",
  },
  danger: {
    value: "text-[var(--ecp-danger)]",
    rail: "from-[var(--ecp-danger)]",
    glow: "rgba(239, 68, 68, 0.22)",
  },
  neutral: {
    value: "text-[var(--ecp-text)]",
    rail: "from-[var(--ecp-text-dim)]",
    glow: "rgba(107, 120, 144, 0.2)",
  },
};

export function MetricCard({
  label,
  value,
  unit,
  hint,
  icon,
  tone = "gov",
  footNote,
  loading = false,
}: {
  label: string;
  value: ReactNode;
  unit?: string;
  hint?: ReactNode;
  icon?: ReactNode;
  tone?: MetricTone;
  footNote?: ReactNode;
  loading?: boolean;
}) {
  const styles = TONE_STYLES[tone];
  return (
    <div
      className="ecp-metric-card rounded-xl border border-[var(--ecp-border)] bg-[var(--ecp-surface)] px-4 py-3.5"
      style={{ "--card-glow": styles.glow } as React.CSSProperties}
    >
      <span
        className={cn(
          "absolute inset-x-0 bottom-0 h-[3px] bg-gradient-to-r to-transparent opacity-70",
          styles.rail
        )}
      />
      <div className="flex items-start justify-between gap-3">
        <p className="text-xs font-medium text-[var(--ecp-text-muted)]">{label}</p>
        {icon && <span className={cn("shrink-0", styles.value)}>{icon}</span>}
      </div>
      <div className="mt-2 flex items-baseline gap-1.5">
        <span
          className={cn(
            "text-[28px] font-bold leading-none tracking-tight",
            loading ? "animate-pulse text-[var(--ecp-text-dim)]" : styles.value
          )}
        >
          {loading ? "—" : value}
        </span>
        {unit && !loading && (
          <span className="text-sm font-medium text-[var(--ecp-text-muted)]">{unit}</span>
        )}
      </div>
      {hint && (
        <p className="mt-1.5 truncate text-[11px] text-[var(--ecp-text-dim)]">{hint}</p>
      )}
      {footNote && <div className="mt-2">{footNote}</div>}
    </div>
  );
}

export function MetricGrid({ children }: { children: ReactNode }) {
  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">{children}</div>
  );
}